#!/usr/bin/env python3
"""Fetch WeChat (mp.weixin.qq.com) articles into local markdown files.

Run with the project's conda env interpreter:

    C:\\Users\\cnc\\anaconda3\\envs\\wechat_fetch\\python.exe scripts\\fetch.py --limit 3

Or after `conda activate wechat_fetch`:

    python scripts\\fetch.py --limit 3

Shared parsing logic lives in wechat_common.py; this module only owns the
HTTP layer, anti-scrape detection, and the CLI / main loop.
"""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

# Make `from wechat_common import ...` work whether this file is run as a script
# (`python scripts/fetch.py`) or imported as a package member (`import scripts.fetch`).
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import requests

from wechat_common import (
    DEFAULT_SOURCE,
    CaptchaError,
    articles_dir,
    existing_urls,
    normalize_url,
    parse_article,
    save_article,
    source_root,
)

# Windows 控制台默认 GBK，打不出 ✓ ✗ → 等符号
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "MicroMessenger/8.0.40(0x18002834) NetType/WIFI Language/zh_CN"
)

HEADERS = {
    "User-Agent": MOBILE_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


_CAPTCHA_KEYWORDS = (
    "环境异常",
    "访问过于频繁",
    "completing the verification",
    "安全验证",
)


def detect_captcha(response) -> str | None:
    """Return a reason string if the response looks like a verification page, else None."""
    if "wappoc_appmsgcaptcha" in response.url:
        return f"redirected to captcha page: {response.url[:120]}"
    text = response.text
    if len(text) < 5000:
        return f"response too small ({len(text)} bytes) — likely intercept page"
    for kw in _CAPTCHA_KEYWORDS:
        if kw in text:
            return f"keyword detected: {kw!r}"
    return None


def load_urls(urls_file, limit):
    """Return original URLs (chksm intact, needed for fetch), deduped on canonical form."""
    if not urls_file.exists():
        sys.exit(f"找不到 {urls_file}")
    urls, seen = [], set()
    for line in urls_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        canon = normalize_url(line)
        if canon in seen:
            continue
        seen.add(canon)
        urls.append(line)
    return urls[:limit] if limit else urls


def fetch_one(url: str, retry: int) -> str:
    last = None
    for attempt in range(retry + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            r.encoding = r.apparent_encoding or "utf-8"
            reason = detect_captcha(r)
            if reason:
                raise CaptchaError(reason)
            return r.text
        except CaptchaError:
            raise  # propagate immediately, retry won't help
        except Exception as e:
            last = e
            if attempt < retry:
                time.sleep(2 * (attempt + 1))
    raise last


def log_failure(failed_file: Path, url: str, err: Exception, kind: str) -> None:
    line = (
        f"{datetime.now().isoformat(timespec='seconds')}\t"
        f"{kind}\t{type(err).__name__}\t{url}\t{str(err)[:200]}\n"
    )
    failed_file.parent.mkdir(parents=True, exist_ok=True)
    with failed_file.open("a", encoding="utf-8") as f:
        f.write(line)


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch WeChat articles to markdown.")
    ap.add_argument("--source", default=DEFAULT_SOURCE,
                    help="来源标识，对应 sources/<source>/ (默认 general)")
    ap.add_argument("--limit", type=int, default=None, help="只抓前 N 条")
    ap.add_argument("--retry", type=int, default=2, help="单条失败重试次数")
    ap.add_argument("--sleep", type=int, default=8, help="每篇之间间隔秒数")
    args = ap.parse_args()

    adir = articles_dir(args.source)
    urls_file = source_root(args.source) / "urls.txt"
    failed_file = source_root(args.source) / "failed.txt"
    print(f"来源: {args.source}  →  {adir}")

    adir.mkdir(parents=True, exist_ok=True)
    urls = load_urls(urls_file, args.limit)
    done = existing_urls(adir)
    total = len(urls)

    for i, url in enumerate(urls, 1):
        canon = normalize_url(url)
        print(f"[{i}/{total}] 抓取中... {canon[:70]}")
        if canon in done:
            print("  → 跳过 (已存在)")
            continue
        try:
            html = fetch_one(url, args.retry)  # original URL (chksm needed)
            meta = parse_article(html)
            path = save_article(meta, canon, adir)   # canonical URL into front matter
            print(f"  ✓ 成功: {meta['title']}  → {path.name}")
        except CaptchaError as e:
            log_failure(failed_file, canon, e, kind="captcha")
            print(f"  ✗ 反爬触发: {e}")
            print()
            print("⚠ 反爬触发，已停止整个批次。建议：")
            print("  1) 换梯子节点（换出口 IP）")
            print("  2) 等 30 分钟后再试")
            print(f"  3) 增大 --sleep（当前 {args.sleep}s，可试 12-20s）")
            sys.exit(2)
        except ValueError as e:
            log_failure(failed_file, canon, e, kind="找不到正文")
            print(f"  ✗ 解析失败: {e}")
        except Exception as e:
            log_failure(failed_file, canon, e, kind="网络错误")
            print(f"  ✗ 失败: {type(e).__name__}: {e}")
        if i < total:
            time.sleep(args.sleep)


if __name__ == "__main__":
    main()
