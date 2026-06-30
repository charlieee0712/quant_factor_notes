# WORKLOG — quant_factor_notes

本地多来源因子笔记库的进度时间线（倒序，最新在上）。
配套文档：项目现状见 [PROJECT_STATUS.md](PROJECT_STATUS.md)，用法/目录/工作流见 [README.md](README.md)。

## 2026-06-30 — DATA_SOURCES 加 §5 同花顺 iFinD 产品目录
- 转写公司图灵盘字典 `同花顺特色&基础高频数据.xlsx`（9 sheet；本机无 Python，用解 zip 读 `sharedStrings.xml`+`sheet*.xml`）成 §5.1–5.5：
  - 5.1 基础高频（高频数据库 ≈200 表 + 沪深 Level2 实时）、5.2 特色因子库（日频 938 / 日内 809 / 实时新闻 2552 行成品因子）、5.3 特色数据（↔ 已落 47 的 §2/§3 同表，补官方起始日）、5.4 基础数据库（≈1138 低频表）、5.5 访问方式&待办。
  - 同步：§1 东财覆盖更新（领导补近三月 ~2026-06，待 ssh 47 核）；§4 加「通联 L2 ↔ 同花顺高频」两套厂商辨识，勿混用。
- **数据本体不在本机**：成品因子/订阅数据落公司服务器（最可能 47 `royalFlush/` 或 `alterIfind/`），待 ssh 47 落地确认路径/覆盖。

## 2026-06-24 — 新增另类数据源说明 DATA_SOURCES.md（实地摸底 3 源）
- 摸底公司另类数据湖（47 `/mnt/sda2/HuaTZ/AlterDatabase/`）3 源并成文 §1–§4：
  - 东财 alterDC（活跃度/人气/情绪，10 pickle / 8.8 GB，静态快照）、同花顺 concept_data（iFinD 概念指数清洗数据，64 GB，2012→2026）、同花顺 AlterDataIfind（MySQL 原始库 `192.168.2.47:3306`，32 表）。
- PROJECT_STATUS 加「另类数据源」段引用；写概念/活跃度/情绪类因子前先查 DATA_SOURCES.md。

## 2026-06-22 — 扩充为多来源，库 109 → 179 篇 / 6 来源
- **查重**：5 位首席合集 URL 与 general 已爬 109 篇按 `mid+idx` 全局查重 → 跨合集 0 重复、与 general 0 重复，70 篇全是新文（同公众号不同作者系列）。
- **爬取**：在线 `fetch.py --source <name>` 分来源抓取 5 首席合集共 70 篇：
  - 曹春晓 10 / 覃川桃 8 / 魏建榕 14 / 陈升锐 16 / 郑兆磊 22，全成功 0 失败。
  - 过程换了 3 个出口 IP（验证码按 IP 累计请求量触-发，详见运维教训）。
- **重构**：单来源 → 多来源结构。`articles/`→`sources/general/articles/`、`html_dump/`→`sources/general/html/` 等；`factor_lib/` 留根、跨来源统一不分目录；脚本全部加 `--source`；CSV 加 `source` 列、每个 `.py` 头加 `# 来源标识`。重构前整库备份于 `C:\Users\cnc\quant_factor_notes_backup_20260622\`。
- **入库**（一次性）：download_images（5 源共 1683 张图，0 失败）→ build_factor_lib（逐源，70 个 .py 并入统一 factor_lib/）→ build_index（179 篇/6 来源）→ classify（CSV 179 行）。factor_lib.zip 重打包到 179。
- **结果**：179 篇 / 6 来源；factor_lib / factor_index.md / factor_classification.csv 三者均 179、对齐。

## 2026-06 — general 增量到 109 篇
- 5-13 之后新增 10 篇，general 由 99 → 109 篇。
- 确认两个陷阱：① 增量跑 download_images 必须 `--skip-backup`（否则用已本地化版覆盖原始 URL 备份）；② 抓取 URL 必须带 `chksm`（缺 chksm 会跳验证码、易误判 IP 反爬）。

## 2026-06 初 — general 全量建库（99 篇）
- 完成公众号"量化拯救散户" 99 篇全量抓取 + 图片本地化 + 结构化 factor_lib（严格摘录原文：来源 + 段落 + 图片清单 + 作者代码，不加 AI 推断）。
- 建立脚本链：fetch / parse_local_html / download_images / build_factor_lib / build_index / classify_factors。

## 待办
- **回测/实现**：因子的工程实现 + 回测在 47 的 `factor_library` 项目做；本地只产因子笔记。
