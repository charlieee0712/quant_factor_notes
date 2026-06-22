#!/usr/bin/env python3
"""Parse locally-saved WeChat article HTML (e.g. from the SingleFile browser
extension) into markdown using the same logic fetch.py applies to live HTTP
responses. Output is written to articles/ with the same front-matter shape.

Usage:
    C:\\Users\\cnc\\anaconda3\\envs\\wechat_fetch\\python.exe scripts\\parse_local_html.py
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Make `from wechat_common import ...` work whether run as script or imported as package member.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from bs4 import BeautifulSoup, Comment

from wechat_common import (
    DEFAULT_SOURCE,
    articles_dir,
    existing_urls,
    html_dir,
    normalize_url,
    parse_soup,
    save_article,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# matches a WeChat article URL anywhere in a string (used inside HTML comments)
_WECHAT_URL_RE = re.compile(r'https?://mp\.weixin\.qq\.com/s\?[^\s"\'<>]+')


def extract_url(soup) -> tuple[str | None, str]:
    """Find the original article URL. Returns (url, source) where source is one of:
    'canonical', 'og:url', 'comment', 'not_found'.
    """
    link = soup.find("link", rel="canonical")
    if link and link.get("href") and "mp.weixin.qq.com" in link["href"]:
        return link["href"], "canonical"

    meta = soup.find("meta", attrs={"property": "og:url"})
    if meta and meta.get("content") and "mp.weixin.qq.com" in meta["content"]:
        return meta["content"], "og:url"

    # SingleFile injects a banner comment near the top, e.g.
    #   <!--
    #    Page saved with SingleFile
    #    url: https://mp.weixin.qq.com/s?__biz=...&mid=...&idx=...&sn=...
    #    saved date: ...
    #   -->
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        m = _WECHAT_URL_RE.search(str(c))
        if m:
            return m.group(0), "comment"

    return None, "not_found"


def log_failure(failed_file: Path, filename: str, kind: str, err: Exception) -> None:
    line = (
        f"{datetime.now().isoformat(timespec='seconds')}\t"
        f"{kind}\t{type(err).__name__}\t{filename}\t{str(err)[:200]}\n"
    )
    failed_file.parent.mkdir(parents=True, exist_ok=True)
    with failed_file.open("a", encoding="utf-8") as f:
        f.write(line)


def run_dry_run(fp: Path) -> None:
    """Parse one file and print diagnostics; do NOT write to articles/."""
    print(f"DRY RUN: {fp.name}")
    print(f"文件大小: {fp.stat().st_size:,} bytes")
    print()

    html = fp.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "lxml")

    raw_url, source = extract_url(soup)
    print(f"=== URL 提取 ===")
    print(f"来源 (fallback): {source}")
    print(f"原始 URL: {raw_url}")
    if raw_url:
        print(f"规范化 URL: {normalize_url(raw_url)}")
    print()

    meta = parse_soup(soup)
    print(f"=== 元信息 ===")
    print(f"title:   {meta['title']}")
    print(f"account: {meta['account']}")
    print(f"author:  {meta['author']}")
    print(f"date:    {meta['date']}")
    print()

    body_md = meta["body"]
    n_data_uri = body_md.count("data:image")
    n_mmbiz = body_md.count("mmbiz.qpic.cn")

    print(f"=== body_md ===")
    print(f"总长度: {len(body_md):,} 字符")
    print(f"data: URI 数量: {n_data_uri}  (期望 0)")
    print(f"mmbiz 原始 URL 数量: {n_mmbiz}  (期望 = 图片数)")
    print()
    print(f"前 300 字符:")
    print("-" * 60)
    print(body_md[:300])
    print("-" * 60)
    print(f"后 200 字符:")
    print("-" * 60)
    print(body_md[-200:])
    print("-" * 60)
    print("(未写盘)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Parse local SingleFile-saved WeChat HTML.")
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="来源标识，对应 sources/<source>/ (默认 general)")
    ap.add_argument(
        "--dry-run-first",
        action="store_true",
        help="只解析 sources/<source>/html/ 中第一个文件并打印诊断信息，不写盘",
    )
    args = ap.parse_args()

    html_dump_dir = html_dir(args.source)
    adir = articles_dir(args.source)
    failed_file = html_dump_dir.parent / "html_parse_failed.txt"
    print(f"来源: {args.source}  →  html={html_dump_dir}")

    if not html_dump_dir.exists():
        sys.exit(f"找不到 {html_dump_dir}")

    files = sorted(html_dump_dir.glob("*.html"))
    if not files:
        sys.exit(f"{html_dump_dir} 下没有 .html 文件")

    if args.dry_run_first:
        run_dry_run(files[0])
        return

    adir.mkdir(parents=True, exist_ok=True)
    done = existing_urls(adir)

    total = len(files)
    n_new = n_skip = n_fail = 0

    for i, fp in enumerate(files, 1):
        print(f"[{i}/{total}] 解析中: {fp.name}")
        try:
            html = fp.read_text(encoding="utf-8", errors="replace")
            soup = BeautifulSoup(html, "lxml")

            raw_url, _source = extract_url(soup)
            if raw_url:
                canon = normalize_url(raw_url)
                if canon in done:
                    print("  → 跳过 (已存在)")
                    n_skip += 1
                    continue
            else:
                canon = ""
                print("  ⚠ 未提取到原始 URL，url 字段将为空（dedup 无法生效）")

            meta = parse_soup(soup)
            path = save_article(meta, canon, adir)
            print(f"  ✓ 新增: {meta['title']}  → {path.name}")
            n_new += 1
            if canon:
                done.add(canon)

        except ValueError as e:
            log_failure(failed_file, fp.name, "找不到正文", e)
            print(f"  ✗ 失败 (找不到正文): {e}")
            n_fail += 1
        except Exception as e:
            log_failure(failed_file, fp.name, "解析错误", e)
            print(f"  ✗ 失败 ({type(e).__name__}): {e}")
            n_fail += 1

    print()
    print(f"扫描总数: {total}")
    print(f"新增: {n_new}")
    print(f"跳过 (dedup): {n_skip}")
    print(f"失败: {n_fail}")
    final = sum(1 for _ in adir.glob("*.md"))
    print(f"{adir} 当前共: {final} 篇")


if __name__ == "__main__":
    main()
