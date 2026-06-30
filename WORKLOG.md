# WORKLOG — quant_factor_notes

本地多来源因子笔记库的进度时间线（倒序，最新在上）。
配套文档：项目现状见 [PROJECT_STATUS.md](PROJECT_STATUS.md)，用法/目录/工作流见 [README.md](README.md)。

## 2026-06-30 — references 扩到 4 本 + 全书视觉精读 + 方法论合成
- **新增第4本《因子投资：方法与实践》(石川/刘洋溢/连祥斌, 423页)**：中文书无文本层(Calibre 转制)、pdftotext 抽不出中文→改 **Read 工具视觉看图读**(渲染页图像)。全书 29 块视觉精读 → `04_因子投资_方法与实践/`(+00-overview)。
- **Factor Zoo + Microstructure + MLAP 全部升级为全书视觉精读**(替换第一遍 pdftotext 浅版)：按物理页细切(zoo offset +15 / 22 块 z*；micro offset +27 / 23 块 m*；MLAP 11 块 ML*，公式视觉读更准——纠正了文本版把 γ/g 误读成 λ/β)，方法论优先、逐图转述(第一遍丢的 K线形态/订单簿/冲击曲线图补回)；第一遍浅版章节文件已删。
- **方法论合成 4 份(用户重点：方法论 > 清单，对接三个决策点)**：`_方法论总纲.md`(总览) + ①`02_*/_真假因子判据.md`(scorecard A/B/C：多重检验 t>3/Bonferroni/FDR · 经济逻辑 · 风险vs错误定价vs数据窥探三检验 · 前向+反向OOS · 相关性 · 可投资性) + ②`04_*/_回测框架与检验方法.md`(回测避坑：检验统计法 + √252/单调性/合成稀释三坑标准答案 + 稳健性 + PIT/未来函数 + A股涨跌停停牌T+1壳) + ③`03_*/_成本模型与L2理论.md`(成本函数 TC=Σc|Δω|+Σd(Δω)² + 微观结构噪声=L2 因子理论根基)。
- 三个反复踩的坑均落到书里标准答案：√252 重叠收益年化→Newey-West HAC(滞后 J=⌊4(T/100)^(2/9)⌋)+错开子策略；单调性→Spearman 秩相关 ρ_s(非看两端)；合成稀释尾部→先正交后合成护尾部。
- 方法：大书重活全在一次性子 agent(视觉读)，主上下文只收一行确认；计划/规范存 scratchpad(deep_read_plan/eng_spec/yinzi_spec)防压缩丢；每块即时落盘可断点续。**局限**：视觉版看不清标 [图中存疑]，精确公式回查根目录 PDF。

## 2026-06-30 — 新增 references/ 参考书阅读笔记库（3 本英文书 / 30 篇笔记，后被上一条扩充）
- 把根目录 3 本英文参考书抽成结构化中文阅读笔记，新建 `references/`（外部参考书，方法论/因子百科；与自产 `factor_lib/` 分开，不计入因子库统计）：
  - **Machine Learning in Asset Pricing**（Nagel, Princeton 2021；157页/6章；高维 ML 资产定价、收缩、稀疏 vs 稠密 SDF、OOS 评估）
  - **Navigating the Factor Zoo**（Zhang/Lu/Shi, Routledge 2025；311页/12章+尾声；第三作者 Chuan Shi=石川，与《因子投资》同源；**最贴本项目**）
  - **Market Microstructure in Practice** 2nd ed.（Lehalle & Laruelle, World Scientific 2018；367页；碎片化/HFT/流动性/最优执行）
- 产物 30 篇 .md：27 篇逐章笔记 + 3 篇全书 `00-overview.md` + `references/README.md` 索引。每篇含「与因子研究的关联 / 与本项目的连接」，已对 `factor_index.md`/`factor_lib/`/`DATA_SOURCES.md`。
  - Book2 overview 含「因子主清单」≈56 行/≈120 具名因子，按族标注 本地已有/部分/可补/A股受限，并列可新增清单（RSJ/半beta/共偏度、Kyle/PIN-VPIN、CGO/ST/PEAD、个股跳跃、概念注意力/Lazy Prices 等）。
- 方法（抗闪退）：PDF 整页直读会撑爆上下文→闪退；改 `pdftotext` 抽纯文本→按章切块→逐章子 agent 读文本并落盘，主上下文不堆原文、每章即时持久化可断点续。**局限**：公式/图/表近似或缺失，存疑处已标注，精确内容回查根目录原 PDF。

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
