# PROJECT_STATUS — quant_factor_notes

> 项目现状速览。进度时间线见 [WORKLOG.md](WORKLOG.md)，用法/目录/工作流见 [README.md](README.md)。
> 最后更新：2026-06-22

## 定位
多来源**因子笔记库**：抓取微信公众号的量价因子文章 → 结构化成 `factor_lib/*.py`（严格摘录原文：来源元数据 + 段落摘录 + 图片清单 + 作者代码，**不加 AI 推断**）。本地只负责"产因子笔记"，**不做回测**。

## 现状
- **179 篇 / 6 来源**（general 109 + 5 首席 70），全部已抓取 + 图片本地化 + 入库。
- `factor_lib/`、`factor_index.md`、`factor_classification.csv` 三者均 **179**、对齐。

## 来源清单
| 来源 (source) | 公众号 / 作者 | 篇数 |
|---|---|---:|
| general | 量化拯救散户（账号自身因子流） | 109 |
| caochunxiao | 曹春晓 | 10 |
| qinchuantao | 覃川桃 | 8 |
| weijianrong | 魏建榕 | 14 |
| chenshengrui | 陈升锐 | 16 |
| zhengzhaolei | 郑兆磊 | 22 |
| **合计** | | **179** |

## 目录结构（要点）
- `sources/<来源>/` — 按来源隔离：`urls.txt` + `articles/`(+`images/`) + `articles_backup/`；`general` 另含早期 SingleFile 的 `html/` 与日志，在线抓取的首席源无。
- `factor_lib/` — **跨来源统一**，不分来源子目录、统一编号；每个 `.py` 头含 `# 来源标识`。
- `factor_index.md` / `factor_classification.csv` — 跨来源汇总（CSV 含 `source` 列）。
- `scripts/` — 共享脚本，全部支持 `--source`（默认 general）。

## 数据规模
- factor_lib：**179** 个 `.py`
- 图片：约 **3772** 张（~431 MB）
- 段落识别：FULL 5 / PARTIAL 63 / SKELETON_ONLY 109 / NONE 2
- has_code：yes 162 / none 15 / partial 2

## 与 47 `factor_library` 的关系
- **本地 quant_factor_notes**：爬虫 + 产出因子笔记（`factor_lib/*.py`，摘录原文与作者代码）。
- **47 的 `factor_library`**（`/mnt/sda2/lichenchen/factor_library/`）：通用回测库，做因子的工程实现 + 回测 + 交付。
- 流向：本地因子笔记 → 47 落地实现 / 回测。两者分开维护、各有自己的 PROJECT_STATUS。

## 运维教训
- WeChat 文章端验证码 `wappoc_appmsgcaptcha` 按**出口 IP 累计请求量**触发（约 10–23 篇/IP，与 `--sleep` 关系不大）；撞墙后换梯子节点、`fetch.py` 幂等续抓（dedup 自动跳过已抓）。本次抓 70 篇换了 3 个 IP。
- 抓取 URL **必须带 `chksm`**（缺 chksm 跳验证码，易误判 IP 反爬）。
- 图片 CDN `mmbiz.qpic.cn` 不限流（本次 1683 张图 0 失败）。
- 大批量抓取若不想反复换 IP，优先 SingleFile 兜底（存 HTML → `parse_local_html.py`）。

## 待办
- 因子的回测 / 工程实现：在 47 的 `factor_library` 做。

## 备份 / 版本
- 重构前整库备份：`C:\Users\cnc\quant_factor_notes_backup_20260622\`（确认无误后可删）。
- 已纳入 git，分支 `main`，远程 `origin` = `github.com/charlieee0712/quant_factor_notes`（**Private**）；`.gitignore` 排除图片/HTML/备份/zip/日志/大体积文件，版本化脚本 + 文档 + `.md` 文章 + `factor_lib/*.py` + `urls.txt` + 汇总产物。
