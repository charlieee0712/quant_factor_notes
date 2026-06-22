#!/usr/bin/env python3
"""Download remote WeChat images into articles/images/ and rewrite .md links.

Run with the project's conda env interpreter:

    C:\\Users\\cnc\\anaconda3\\envs\\wechat_fetch\\python.exe scripts\\download_images.py --limit 3

Backs up articles/*.md to articles_backup/ before modifying anything (unless
--skip-backup). GIFs (mmbiz_gif / wx_fmt=gif) are left untouched. Failed
downloads also leave the original URL in place so the .md stays renderable.
"""

import argparse
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import requests

from wechat_common import DEFAULT_SOURCE, articles_dir, source_root
from fetch import MOBILE_UA

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


HEADERS = {
    "User-Agent": MOBILE_UA,
    # Anti-hotlink: mmbiz.qpic.cn checks Referer for non-mp.weixin origins.
    "Referer": "https://mp.weixin.qq.com/",
}

# Markdown image syntax: ![alt](url). URL has no whitespace and no ')'.
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")

# Skip decorative animations entirely.
GIF_MARKERS = ("mmbiz_gif", "wx_fmt=gif")


def is_gif(url: str) -> bool:
    return any(m in url for m in GIF_MARKERS)


def is_remote(url: str) -> bool:
    # Re-running on already-rewritten .md must not try to "download" local paths.
    return url.startswith("http://") or url.startswith("https://")


def guess_extension(url: str, content_type: str | None) -> str:
    """Pick a file extension. Prefer wx_fmt query, then Content-Type, else .png."""
    fmt = (parse_qs(urlparse(url).query).get("wx_fmt") or [""])[0].lower()
    if fmt in {"png", "jpg", "jpeg", "webp", "bmp"}:
        return ".jpg" if fmt == "jpeg" else f".{fmt}"
    if content_type:
        ct = content_type.lower()
        if "png" in ct:
            return ".png"
        if "jpeg" in ct or "jpg" in ct:
            return ".jpg"
        if "webp" in ct:
            return ".webp"
    return ".png"


def download_image(url: str, dest_no_ext: Path, retries: int = 1, timeout: int = 15) -> Path:
    """Download a single image. Returns the final path (with extension)."""
    last = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            ext = guess_extension(url, r.headers.get("Content-Type"))
            dest = dest_no_ext.with_suffix(ext)
            dest.write_bytes(r.content)
            return dest
        except Exception as e:
            last = e
            if attempt < retries:
                time.sleep(3)
    raise last


def log_image_failure(failed_file: Path, md_name: str, idx: int, url: str, err: Exception) -> None:
    line = (
        f"{datetime.now().isoformat(timespec='seconds')}\t"
        f"{md_name}\t{idx:03d}\t{url}\t{type(err).__name__}: {str(err)[:200]}\n"
    )
    failed_file.parent.mkdir(parents=True, exist_ok=True)
    with failed_file.open("a", encoding="utf-8") as f:
        f.write(line)


def backup_articles(adir: Path, backup_dir: Path) -> None:
    """Copy all .md from `adir` into `backup_dir`. Refuses to overwrite an existing backup."""
    if backup_dir.exists() and any(backup_dir.iterdir()):
        sys.exit(
            f"articles_backup/ 已存在且非空：{backup_dir}\n"
            f"  → 删除该目录后重跑，或使用 --skip-backup（已备份过的情况）"
        )
    backup_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for md in sorted(adir.glob("*.md")):
        shutil.copy2(md, backup_dir / md.name)
        n += 1
    print(f"  备份完成 → {backup_dir}  ({n} 篇)")


def process_one(md_path: Path, images_dir: Path, failed_file: Path) -> dict:
    """Process a single .md. Returns stats dict for the article."""
    # Use bytes IO so source line endings (LF/CRLF) survive the round trip
    # untouched — write_text on Windows would otherwise translate \n → \r\n.
    text = md_path.read_bytes().decode("utf-8")
    matches = list(IMG_RE.finditer(text))

    stats = {"total": 0, "downloaded": 0, "skipped_gif": 0, "failed": 0}
    if not matches:
        return stats

    # Build first-seen ordered map of non-GIF remote URLs → 1-based index.
    seen: dict[str, int] = {}
    next_idx = 1
    for m in matches:
        url = m.group(2)
        if not is_remote(url):
            continue  # already rewritten to local path on a previous run
        if is_gif(url):
            stats["skipped_gif"] += 1
            continue
        if url not in seen:
            seen[url] = next_idx
            next_idx += 1

    stats["total"] = len(seen)
    if not seen:
        return stats

    img_dir = images_dir / md_path.stem
    img_dir.mkdir(parents=True, exist_ok=True)

    url_to_local: dict[str, str] = {}
    for url, idx in seen.items():
        dest_no_ext = img_dir / f"{idx:03d}"
        try:
            final = download_image(url, dest_no_ext)
            url_to_local[url] = f"images/{md_path.stem}/{final.name}"
            stats["downloaded"] += 1
        except Exception as e:
            print(f"    x [{idx:03d}] {type(e).__name__}: {str(e)[:80]}")
            log_image_failure(failed_file, md_path.name, idx, url, e)
            stats["failed"] += 1
        time.sleep(0.3)

    if url_to_local:
        def repl(m):
            alt, url = m.group(1), m.group(2)
            if url in url_to_local:
                return f"![{alt}]({url_to_local[url]})"
            return m.group(0)
        md_path.write_bytes(IMG_RE.sub(repl, text).encode("utf-8"))

    return stats


def dir_size_bytes(p: Path) -> int:
    if not p.exists():
        return 0
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def fmt_size(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Download images for all articles and rewrite .md links."
    )
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="来源标识，对应 sources/<source>/ (默认 general)")
    ap.add_argument("--limit", type=int, default=None,
                    help="只处理前 N 篇（按文件名排序）")
    ap.add_argument("--skip-backup", action="store_true",
                    help="跳过 articles/ 备份（已经备份过的情况）")
    args = ap.parse_args()

    adir = articles_dir(args.source)
    images_dir = adir / "images"
    backup_dir = source_root(args.source) / "articles_backup"
    failed_file = source_root(args.source) / "image_failed.txt"
    print(f"来源: {args.source}  →  {adir}")

    md_files = sorted(adir.glob("*.md"))
    if args.limit:
        md_files = md_files[: args.limit]

    if not md_files:
        sys.exit(f"{adir} 下没有 .md 文件")

    if args.skip_backup:
        print("跳过备份 (--skip-backup)")
    else:
        print(f"备份 {adir.name}/*.md → {backup_dir}")
        backup_articles(adir, backup_dir)

    images_dir.mkdir(parents=True, exist_ok=True)

    totals = {"total": 0, "downloaded": 0, "skipped_gif": 0, "failed": 0}
    t0 = time.time()

    for i, md in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] {md.name}")
        s = process_one(md, images_dir, failed_file)
        for k in totals:
            totals[k] += s[k]
        print(f"  -> 总 {s['total']}  下载 {s['downloaded']}  "
              f"GIF跳过 {s['skipped_gif']}  失败 {s['failed']}")
        if i < len(md_files):
            time.sleep(1)

    elapsed = time.time() - t0

    print()
    print("=" * 60)
    print(f"处理篇数            : {len(md_files)}")
    print(f"图片 URL 数 (非 GIF): {totals['total']}")
    print(f"成功下载            : {totals['downloaded']}")
    print(f"GIF 跳过            : {totals['skipped_gif']}")
    print(f"下载失败            : {totals['failed']}")
    print(f"耗时                : {elapsed:.1f}s")
    print(f"images/ 总大小      : {fmt_size(dir_size_bytes(images_dir))}")
    if totals["failed"]:
        print(f"失败记录            : {failed_file}")


if __name__ == "__main__":
    main()
