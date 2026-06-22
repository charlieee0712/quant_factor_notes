#!/usr/bin/env python3
"""Generate factor_index.md — a single unified index of all articles, all sources.

By default scans every sources/<source>/articles/ and merges them into one
date-sorted table (序号 spans all sources = the '统一编号'). Pass --source to
index just one source. Links point at sources/<source>/articles/<slug>.md.

Columns: 序号 (newest=highest), 日期, 标题 (link), 关键词, 代码行数, 图片数, 来源.
Keyword extraction matches a curated whitelist against the article title; add
more terms to KEYWORDS as the library grows.

Run AFTER build_factor_lib.py has populated factor_lib/ — the 代码行数 column
counts non-blank, non-comment lines in factor_lib/{slug}.py's code section.
"""

import argparse
import re
import sys
from pathlib import Path

import frontmatter

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from wechat_common import PROJECT_ROOT, SOURCES_DIR, articles_dir

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


FACTOR_LIB_DIR = PROJECT_ROOT / "factor_lib"
INDEX_FILE = PROJECT_ROOT / "factor_index.md"

# Order matters slightly: longer / more specific terms first so they win
# the 'first N' cap before generic ones.
KEYWORDS = [
    # method tags
    "邪修", "研报", "改进", "改写", "复杂",
    # factor concepts
    "欧式距离", "理想振幅", "振幅", "成交量", "交易量", "波动率", "换手率",
    "反转", "动量", "残差", "收益率", "非流动性", "流动性",
    "自相关", "相关性", "差分", "加速度", "资金流入", "资金流",
    "K-means", "高斯混合", "跳价期", "跳价", "震荡期", "震荡",
    "黄金分割", "趋势", "MAX", "Beta", "偏度", "峰度",
    "CVaR", "VCVaR", "尾部", "二八定律", "聪明钱",
    "事件驱动", "异常", "价格时滞", "持续异常", "锚定", "买卖压力",
    "可预测性", "R方",
    # frequency / data
    "1分钟", "5分钟", "15分钟", "30分钟", "60分钟", "日频", "日内",
]

# Match the "作者代码" banner created by build_factor_lib.py.
CODE_SECTION_RE = re.compile(r"^# 作者代码.*$", re.MULTILINE)
IMG_LINE_RE = re.compile(r"!\[[^\]]*\]\(images/[^)]+\)")


def extract_keywords(title: str, body: str = "", max_n: int = 5) -> list[str]:
    hay = title + "\n" + body[:500]
    out, seen = [], set()
    for kw in KEYWORDS:
        if kw in hay and kw not in seen:
            out.append(kw)
            seen.add(kw)
            if len(out) >= max_n:
                break
    return out


def count_code_lines(py_path: Path) -> int:
    """Count non-blank, non-comment lines in the '作者代码' section."""
    if not py_path.exists():
        return 0
    text = py_path.read_bytes().decode("utf-8")
    m = CODE_SECTION_RE.search(text)
    if not m:
        return 0
    tail = text[m.end():]
    n = 0
    for l in tail.split("\n"):
        ls = l.strip()
        if not ls or ls.startswith("#"):
            continue
        n += 1
    return n


def count_images(md_text: str) -> int:
    return len(IMG_LINE_RE.findall(md_text))


def iter_source_articles(only_source=None):
    """Yield (source, md_path) for every sources/<source>/articles/*.md.
    only_source restricts to a single source; otherwise all sources are merged."""
    if not SOURCES_DIR.exists():
        return
    sources = [only_source] if only_source else sorted(
        p.name for p in SOURCES_DIR.iterdir() if p.is_dir()
    )
    for src in sources:
        adir = articles_dir(src)
        if not adir.exists():
            continue
        for md in sorted(adir.glob("*.md")):
            yield src, md


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate unified factor_index.md across all sources (or one --source)."
    )
    ap.add_argument("--source", default=None,
                    help="只索引该来源；缺省汇总 sources/ 下全部来源（统一编号）")
    args = ap.parse_args()

    rows = []
    seen_slugs = {}
    for src, md in iter_source_articles(args.source):
        post = frontmatter.loads(md.read_bytes().decode("utf-8"))
        meta = post.metadata
        slug = md.stem
        if slug in seen_slugs:
            print(f"⚠ 跨来源重名 slug: {slug}  ({seen_slugs[slug]} vs {src}) "
                  f"— 二者共享 factor_lib/{slug}.py，会相互覆盖")
        seen_slugs[slug] = src
        rows.append({
            "source": src,
            "date": str(meta.get("date", "?")),
            "title": meta.get("title", slug),
            "slug": slug,
            "keywords": extract_keywords(meta.get("title", slug), post.content),
            "n_code": count_code_lines(FACTOR_LIB_DIR / f"{slug}.py"),
            "n_img": count_images(post.content),
        })

    if not rows:
        sys.exit("没有 .md 文件")

    rows.sort(key=lambda r: r["date"], reverse=True)
    n = len(rows)
    n_src = len({r["source"] for r in rows})

    out = [
        "# 因子库索引",
        "",
        f"共 {n} 篇，来自 {n_src} 个来源。按日期倒序（序号越大越新）。",
        "链接指向原 markdown；代码行数来自 `factor_lib/{slug}.py` 的"
        " '作者代码' 段（非空且非注释行）。",
        "",
        "| 序号 | 日期 | 标题 | 关键词 | 代码行数 | 图片数 | 来源 |",
        "|---:|:---|:---|:---|---:|---:|:---|",
    ]
    for i, r in enumerate(rows):
        idx = n - i
        kw = " / ".join(r["keywords"]) if r["keywords"] else "—"
        title_link = f"[{r['title']}](sources/{r['source']}/articles/{r['slug']}.md)"
        out.append(
            f"| {idx} | {r['date']} | {title_link} | {kw} | "
            f"{r['n_code']} | {r['n_img']} | {r['source']} |"
        )

    INDEX_FILE.write_bytes(("\n".join(out) + "\n").encode("utf-8"))
    print(f"已生成 {INDEX_FILE}  ({n} 篇, {n_src} 个来源, {args.source or '全部'})")


if __name__ == "__main__":
    main()
