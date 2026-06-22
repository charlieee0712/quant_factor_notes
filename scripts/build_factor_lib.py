#!/usr/bin/env python3
"""Generate unified factor_lib/*.py 'code-form notebook' from a source's articles/*.md.

Input is one 来源 at a time (--source, default general → sources/general/articles/),
but output always lands in the single root-level factor_lib/ shared across all
sources. Each file records its 来源 via a '# 来源标识:' line so factors can be
filtered by source later even though they live in one unified directory.

Each generated file mirrors one article: provenance metadata, verbatim section
摘录, image manifest, then the original Python code blocks. Headings are
detected in two formats — bold-wrapped (**XXX**) used by newer articles, and
short plain-text standalone lines (e.g. 'IC分析') used by older ones.

Strictly extractive: # comments are verbatim from the original. No 推断,
no summarization, no AI commentary. Sections the author never wrote get
'(原文中无此段落)' so the missing-ness is visible.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import frontmatter

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from wechat_common import DEFAULT_SOURCE, PROJECT_ROOT, articles_dir

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


FACTOR_LIB_DIR = PROJECT_ROOT / "factor_lib"

# Plain-text section names seen in older articles (no **bold** wrapper).
KNOWN_PLAIN_HEADINGS = {
    "IC分析", "回归分析", "换手率分析", "收益分析",
    "分层回测", "分层回测分析", "总结",
    "因子评价", "因子表现", "表现分析",
    "代码", "计算步骤", "因子逻辑",
}
# Frequency markers used as section dividers in 1/5/10/30/60-minute articles.
FREQ_MARKER_RE = re.compile(r"^(\d+)分钟K线$")

CALC_NAMES = {"计算步骤", "计算步骤和代码分析", "因子计算", "因子计算步骤"}
LOGIC_NAMES = {"因子逻辑", "因子说明", "因子描述", "因子介绍", "因子计算逻辑"}
BACKTEST_NAMES = {
    "因子评价", "因子表现", "表现分析",
    "IC分析", "回归分析", "换手率分析", "收益分析",
    "分层回测", "分层回测分析", "总结",
}

IMG_RE = re.compile(r"!\[[^\]]*\]\(images/[^/]+/([^)]+)\)")
ANY_IMG_LINE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")  # local OR external — for prose stripping
CODE_OPEN_RE = re.compile(r"^```python\s*$")
CODE_CLOSE_RE = re.compile(r"^```\s*$")


def bucket_of(text: str):
    if text in CALC_NAMES:
        return "calc"
    if text in LOGIC_NAMES:
        return "logic"
    if text in BACKTEST_NAMES:
        return "backtest"
    return None


def detect_heading(line: str):
    """Return the cleaned heading text if this line looks like one, else None."""
    s = line.strip()
    if not s:
        return None
    if s.startswith("**") and s.endswith("**") and len(s) >= 4:
        inner = s[2:-2].strip()
        return inner if inner else None
    if s in KNOWN_PLAIN_HEADINGS or FREQ_MARKER_RE.match(s):
        return s
    return None


def parse_body(body: str):
    """Return (lines, in_code, code_blocks, headings, images, leading_end)."""
    lines = body.split("\n")
    n = len(lines)

    code_blocks = []           # (start_line, end_line, code_text)
    in_code = [False] * n
    i = 0
    while i < n:
        if CODE_OPEN_RE.match(lines[i]):
            j = i + 1
            while j < n and not CODE_CLOSE_RE.match(lines[j]):
                j += 1
            code_blocks.append((i, j, "\n".join(lines[i + 1:j])))
            for k in range(i, min(j + 1, n)):
                in_code[k] = True
            i = j + 1
        else:
            i += 1

    headings = []  # (line_idx, raw_text, bucket_or_None)
    for li, line in enumerate(lines):
        if in_code[li]:
            continue
        text = detect_heading(line)
        if text is not None:
            headings.append((li, text, bucket_of(text)))

    images = []  # (filename, nearest-preceding-heading-text)
    for li, line in enumerate(lines):
        if in_code[li]:
            continue
        for m in IMG_RE.finditer(line):
            section = "(文章开头)"
            for h_li, h_text, _ in headings:
                if h_li < li:
                    section = h_text
                else:
                    break
            images.append((m.group(1), section))

    # 导读 ends at first BUCKETED heading or first code block, whichever earlier.
    # Title-repeat banners (**title**) without a bucket don't cut it short.
    first_bucket = next((li for li, _, b in headings if b is not None), n)
    first_code = code_blocks[0][0] if code_blocks else n
    leading_end = min(first_bucket, first_code)

    return lines, in_code, code_blocks, headings, images, leading_end


def clean_prose(lines, in_code, start, end) -> str:
    """Slice lines[start:end], drop code-block lines + image lines, trim blanks."""
    out = []
    for k in range(start, end):
        if k < 0 or k >= len(lines):
            continue
        if in_code[k]:
            continue
        l = lines[k]
        if ANY_IMG_LINE_RE.search(l):
            continue
        out.append(l)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    collapsed, prev_blank = [], False
    for l in out:
        if not l.strip():
            if not prev_blank:
                collapsed.append("")
            prev_blank = True
        else:
            collapsed.append(l)
            prev_blank = False
    return "\n".join(collapsed)


def commented(text: str) -> str:
    if not text.strip():
        return "# (无内容)"
    out = []
    for l in text.split("\n"):
        out.append(f"# {l}" if l else "#")
    return "\n".join(out)


def coverage_label(headings) -> str:
    has = {b for _, _, b in headings if b}
    if {"calc", "logic", "backtest"} <= has:
        return "FULL"
    if "backtest" in has and ("calc" in has or "logic" in has):
        return "PARTIAL"
    if "backtest" in has:
        return "SKELETON_ONLY"
    if has:
        return "PARTIAL"
    return "NONE"


def build_one(md_path: Path, out_dir: Path, source: str) -> tuple[Path, str, int, int]:
    raw = md_path.read_bytes().decode("utf-8")
    post = frontmatter.loads(raw)
    meta = post.metadata
    body = post.content

    lines, in_code, code_blocks, headings, images, leading_end = parse_body(body)
    slug = md_path.stem
    # Relative path from the unified factor_lib/ back to this source's articles.
    rel = f"../sources/{source}/articles"

    # 导读
    leading_text = clean_prose(lines, in_code, 0, leading_end)

    # Section buckets. Also track headings-seen-per-bucket so we can distinguish
    # 'section never existed' from 'section existed but had no text (images only)'.
    buckets = {"calc": [], "logic": [], "backtest": []}
    headings_seen = {"calc": [], "logic": [], "backtest": []}
    for i, (li, text, bucket) in enumerate(headings):
        if bucket is None:
            continue
        headings_seen[bucket].append(text)
        next_li = headings[i + 1][0] if i + 1 < len(headings) else len(lines)
        content = clean_prose(lines, in_code, li + 1, next_li)
        if bucket == "backtest":
            # Skip empty backtest sub-sections to avoid noise (their images are
            # still listed in 本地图片清单 with the right section attribution).
            if content.strip():
                buckets["backtest"].append(f"## {text}\n{content}")
        else:
            buckets[bucket].append(content if content.strip() else f"## {text}\n(无独立文本)")

    cov = coverage_label(headings)
    title = meta.get("title", slug)

    parts = []
    parts.append(
        f'"""{title}\n\n'
        f"自动生成自 {rel}/{slug}.md。\n"
        f"所有 # 注释内容均直接摘录自原文，未经改写或归纳。\n"
        f"图片位于 {rel}/images/{slug}/\n"
        f'"""\n'
    )

    def hdr(title):
        return [
            "# ============================================================",
            f"# {title}",
            "# ============================================================",
        ]

    parts += hdr("来源")
    parts.append(f"# 来源标识: {source}")
    parts.append(f"# 公众号  : {meta.get('account', '?')}")
    parts.append(f"# 标题    : {title}")
    parts.append(f"# 日期    : {meta.get('date', '?')}")
    parts.append(f"# 原文 URL: {meta.get('url', '?')}")
    parts.append(f"# 本地原文: {rel}/{slug}.md")
    parts.append(f"# 本地图片: {rel}/images/{slug}/  (共 {len(images)} 张)")
    parts.append(f"# 段落识别: {cov}  "
                 f"(FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)")
    parts.append(f"# 生成时间: {datetime.now().isoformat(timespec='seconds')}")
    parts.append("")

    parts += hdr("导读（原文头部，至首个内容段标题或首个代码块前）")
    parts.append(commented(leading_text))
    parts.append("")

    def render_bucket(bucket_name):
        if buckets[bucket_name]:
            for block in buckets[bucket_name]:
                parts.append(commented(block))
                parts.append("#")
        elif headings_seen[bucket_name]:
            names = " / ".join(dict.fromkeys(headings_seen[bucket_name]))  # dedup, preserve order
            parts.append(f"# (原文有相关段标题 [{names}]，但均为图片，无独立文本；图片见下方清单)")
        else:
            parts.append("# (原文中无此段落)")

    parts += hdr("作者原文 — 计算步骤")
    render_bucket("calc")
    parts.append("")

    parts += hdr("作者原文 — 因子逻辑")
    render_bucket("logic")
    parts.append("")

    parts += hdr("作者原文 — 回测表现说明")
    render_bucket("backtest")
    parts.append("")

    parts += hdr(f"本地图片清单（共 {len(images)} 张）")
    if images:
        for filename, section in images:
            parts.append(f"# {filename}  <-  {section}")
    else:
        parts.append("# (无图片)")
    parts.append("")

    parts += hdr(f"作者代码（按原文出现顺序，共 {len(code_blocks)} 个代码块）")
    parts.append("")
    if not code_blocks:
        parts.append("# (原文未给出 python 代码)")
        parts.append("")
    for i, (cs, ce, code) in enumerate(code_blocks, 1):
        parts.append(f"# --- 代码块 {i} ---")
        parts.append(code)
        parts.append("")
        # Prose immediately after this code block, until next code block or next heading.
        next_code_start = code_blocks[i][0] if i < len(code_blocks) else len(lines)
        next_heading_li = next((hli for hli, _, _ in headings if hli > ce), len(lines))
        prose_end = min(next_code_start, next_heading_li)
        prose = clean_prose(lines, in_code, ce + 1, prose_end)
        if prose.strip():
            for pl in prose.split("\n"):
                if pl.strip():
                    parts.append(f"# (作者注) {pl}")
                else:
                    parts.append("#")
            parts.append("")

    text = "\n".join(parts) + "\n"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.py"
    out_path.write_bytes(text.encode("utf-8"))
    return out_path, cov, len(images), len(code_blocks)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate unified factor_lib/*.py from a source's articles/*.md"
    )
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="来源标识，对应 sources/<source>/ (默认 general)")
    ap.add_argument("--limit", type=int, default=None,
                    help="处理前 N 篇（按文件名排序）")
    ap.add_argument("--files", nargs="*", default=None,
                    help="显式指定 .md 文件名（sources/<source>/articles/ 下，不含路径）")
    args = ap.parse_args()

    adir = articles_dir(args.source)

    if args.files:
        md_files = [adir / f for f in args.files]
        for m in md_files:
            if not m.exists():
                sys.exit(f"找不到 {m}")
    else:
        md_files = sorted(adir.glob("*.md"))
        if args.limit:
            md_files = md_files[: args.limit]

    if not md_files:
        sys.exit(f"{adir} 下没有可处理的 .md 文件")

    print(f"来源: {args.source}  ←  {adir}")
    print(f"输出目录(统一): {FACTOR_LIB_DIR}")
    print()
    cov_counts = {"FULL": 0, "PARTIAL": 0, "SKELETON_ONLY": 0, "NONE": 0}
    for i, md in enumerate(md_files, 1):
        out_path, cov, n_img, n_code = build_one(md, FACTOR_LIB_DIR, args.source)
        cov_counts[cov] += 1
        print(f"[{i}/{len(md_files)}] {md.name}")
        print(f"  -> {out_path.name}")
        print(f"     段落: {cov}  图: {n_img}  代码块: {n_code}")

    print()
    print("=" * 60)
    print(f"处理篇数      : {len(md_files)}")
    print(f"段落识别分布  : "
          f"FULL={cov_counts['FULL']}  "
          f"PARTIAL={cov_counts['PARTIAL']}  "
          f"SKELETON_ONLY={cov_counts['SKELETON_ONLY']}  "
          f"NONE={cov_counts['NONE']}")


if __name__ == "__main__":
    main()
