"""Shared WeChat-article parsing logic.

Used by both fetch.py (live HTTP) and parse_local_html.py (saved SingleFile HTML).
The public surface is:

  Constants : PROJECT_ROOT, SOURCES_DIR, DEFAULT_SOURCE
  Path helpers : source_root, articles_dir, html_dir
  Exception : CaptchaError
  Functions : normalize_url, slugify, parse_date,
              normalize_code_snippets, parse_soup, parse_article,
              existing_urls, save_article
  Class     : WeChatConverter

Multi-source layout (one subdir per 来源 under sources/):
  sources/<source>/articles/         markdown notes (+ images/ subdir)
  sources/<source>/html/             SingleFile HTML dumps
The unified factor_lib/ at the project root is NOT per-source — every
source's factors land there together (see build_factor_lib.py).
"""

import re
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse, urlunparse

import frontmatter
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "sources"
DEFAULT_SOURCE = "general"


def source_root(source: str) -> Path:
    """Per-source root, e.g. sources/general/."""
    return SOURCES_DIR / source


def articles_dir(source: str) -> Path:
    """Per-source markdown dir, e.g. sources/general/articles/."""
    return source_root(source) / "articles"


def html_dir(source: str) -> Path:
    """Per-source SingleFile HTML dump dir, e.g. sources/general/html/."""
    return source_root(source) / "html"


class CaptchaError(Exception):
    """WeChat returned a verification / rate-limit page instead of the article.
    Should NOT be retried — same IP will keep hitting the same wall."""


# WeChat URLs carry tracking junk (chksm, scene, srcid, mpshare, #rd …);
# only these four identify an article uniquely.
_KEEP_KEYS = ("__biz", "mid", "idx", "sn")


def normalize_url(url: str) -> str:
    """Strip tracking params and fragment; force https; canonical key order.
    Build the query manually so __biz's base64 '==' padding stays literal
    (urlencode would percent-encode it as %3D%3D, which WeChat rejects).
    """
    p = urlparse(url.strip())
    q = parse_qs(p.query, keep_blank_values=False)
    kept = [(k, q[k][0]) for k in _KEEP_KEYS if k in q]
    query = "&".join(f"{k}={v}" for k, v in kept)
    return urlunparse(("https", "mp.weixin.qq.com", "/s", "", query, ""))


def slugify(text: str, max_len: int = 60) -> str:
    """Filesystem-safe slug that keeps Chinese characters."""
    text = re.sub(r'[\\/:*?"<>|\r\n\t]+', "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text[:max_len] if text else "untitled"


def parse_date(soup) -> str:
    meta = soup.find("meta", {"property": "article:published_time"})
    if meta and meta.get("content"):
        return meta["content"][:10]

    em = soup.find(id="publish_time")
    if em:
        m = re.search(r"(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})", em.get_text())
        if m:
            y, mo, d = m.groups()
            return f"{y}-{int(mo):02d}-{int(d):02d}"

    for script in soup.find_all("script"):
        s = script.string or ""
        m = re.search(r'var\s+ct\s*=\s*["\'](\d{9,})["\']', s)
        if m:
            return datetime.fromtimestamp(int(m.group(1))).strftime("%Y-%m-%d")
        m2 = re.search(r'publish_time\s*=\s*["\'](\d{4}-\d{2}-\d{2})', s)
        if m2:
            return m2.group(1)

    return datetime.now().strftime("%Y-%m-%d")


def normalize_code_snippets(soup, body_tag) -> None:
    """WeChat puts each code line in its own <code> element with <br> between them.
    Merge them into a single <pre><code>line1\\nline2\\n...</code></pre> so markdownify
    emits a real fenced code block instead of squashing everything onto one line.
    """
    for section in body_tag.select('section[class*="code-snippet"]'):
        codes = section.find_all("code")
        if not codes:
            continue
        text = "\n".join(c.get_text() for c in codes)

        lang = ""
        for cls in section.get("class", []):
            m = re.match(r"code-snippet__(\w+)$", cls)
            if m and m.group(1) not in {"fix", "line-index"}:
                lang = m.group(1)
                break

        new_pre = soup.new_tag("pre")
        new_code = soup.new_tag("code")
        if lang:
            new_code["class"] = [f"language-{lang}"]
        new_code.string = text
        new_pre.append(new_code)
        section.replace_with(new_pre)


def _code_language_callback(el):
    """Force all fenced code blocks to be tagged 'python'.

    WeChat's editor tags code by visual style class (commonly code-snippet__js),
    not by actual language — this account writes Python, so override unconditionally.
    """
    return "python"


class WeChatConverter(MarkdownConverter):
    """Markdown converter tuned for WeChat content."""

    # signature differs across markdownify versions (convert_as_inline vs parent_tags),
    # so accept **kwargs to stay forward/backward compatible
    def convert_img(self, el, text, **kwargs):
        src = el.get("src") or el.get("data-src") or ""
        alt = (el.get("alt") or "").strip()
        return f"![{alt}]({src})" if src else "[图片]"

    def convert_figure(self, el, text, **kwargs):
        return text or "[图片]"


def parse_soup(soup) -> dict:
    """Extract title/account/author/date/body-markdown from an already-parsed soup.
    Used directly by parse_local_html.py (which also needs to extract the URL from
    the same soup). For raw-HTML callers, use parse_article() below.
    """
    title_tag = soup.find(id="activity-name") or soup.find("h1", class_="rich_media_title")
    title = title_tag.get_text(strip=True) if title_tag else "未命名"

    account_tag = soup.find(id="js_name") or soup.find(class_="profile_nickname")
    account = account_tag.get_text(strip=True) if account_tag else ""

    author_tag = soup.find(id="js_author_name") or soup.find(class_="rich_media_meta_text")
    author = author_tag.get_text(strip=True) if author_tag else ""

    date = parse_date(soup)

    body_tag = soup.find(id="js_content") or soup.find(class_="rich_media_content")
    if body_tag is None:
        raise ValueError("找不到正文容器 (js_content / rich_media_content)")

    # Restore a usable URL into src when it's missing (WeChat lazy-load) OR
    # when SingleFile has inlined the image as a base64 data: URI (huge bloat).
    # data-src preserves the original mmbiz.qpic.cn URL in both cases.
    for img in body_tag.find_all("img"):
        src = img.get("src", "")
        if (not src or src.startswith("data:")) and img.get("data-src"):
            img["src"] = img["data-src"]

    normalize_code_snippets(soup, body_tag)

    body_md = WeChatConverter(
        heading_style="ATX",
        bullets="-",
        strip=["script", "style"],
        code_language_callback=_code_language_callback,
    ).convert_soup(body_tag).strip()
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)

    return {
        "title": title,
        "account": account,
        "author": author,
        "date": date,
        "body": body_md,
    }


def parse_article(html: str) -> dict:
    """Convenience wrapper for callers that have raw HTML, not a soup."""
    return parse_soup(BeautifulSoup(html, "lxml"))


def existing_urls(adir: Path):
    """Set of normalized URLs already saved in `adir` (read from each markdown's front matter)."""
    seen = set()
    if not adir.exists():
        return seen
    for md in adir.glob("*.md"):
        try:
            post = frontmatter.load(md)
            u = post.metadata.get("url")
            if u:
                seen.add(normalize_url(u))
        except Exception:
            continue
    return seen


def save_article(meta: dict, url: str, adir: Path) -> Path:
    adir.mkdir(parents=True, exist_ok=True)
    slug = slugify(meta["title"])
    path = adir / f"{meta['date']}_{slug}.md"
    i = 2
    while path.exists():
        path = adir / f"{meta['date']}_{slug}_{i}.md"
        i += 1

    post = frontmatter.Post(
        meta["body"],
        url=url,
        title=meta["title"],
        account=meta["account"],
        author=meta["author"],
        date=meta["date"],
        fetched_at=datetime.now().isoformat(timespec="seconds"),
    )
    path.write_bytes(frontmatter.dumps(post).encode("utf-8"))
    return path
