# references — 参考书阅读笔记库

量化研究参考书的**结构化中文阅读笔记**。每本书一个子目录，含 `00-overview.md`（全书导读/入口）+ 逐章笔记。另有跨书《方法论总纲》与两份专题合成。

> 最后更新：2026-06-30

## 这是什么 / 怎么生成的
- 原书 PDF 在仓库根目录。**重心是方法论/思想，不是因子清单**（因子能自己想，书的价值在"怎么做、为什么"）。
- 两种读法：
  - **文本提取**（pdftotext）：ML in Asset Pricing（英文，公式略糊）。
  - **视觉精读**（按 PDF 物理页"看图"读，能捕公式+图表）：**因子投资 / Navigating the Factor Zoo / Market Microstructure**——细切每块十几页读透，图表逐一转述。中文书《因子投资》无文本层，只能视觉读。
- 局限：文本提取版公式/图表近似或缺失；视觉版看不清处标 `[图中存疑]`。精确公式回查根目录原 PDF。

## 四本书
| # | 书 | 作者 / 年 | 页 | 读法 | 目录 / 入口 |
|---|---|---|---:|---|---|
| 1 | Machine Learning in Asset Pricing | Stefan Nagel, Princeton UP, 2021 | 157 | 视觉精读 | [01_ML_in_Asset_Pricing](01_ML_in_Asset_Pricing/00-overview.md) |
| 2 | Navigating the Factor Zoo | Zhang, Lu & Shi(石川), Routledge, 2025 | 311 | 视觉精读 | [02_Navigating_the_Factor_Zoo](02_Navigating_the_Factor_Zoo/00-overview.md) |
| 3 | Market Microstructure in Practice (2nd) | Lehalle & Laruelle, World Sci., 2018 | 367 | 视觉精读 | [03_Market_Microstructure_in_Practice](03_Market_Microstructure_in_Practice/00-overview.md) |
| 4 | 因子投资：方法与实践 | 石川 / 刘洋溢 / 连祥斌 | 423 | 视觉精读 | [04_因子投资_方法与实践](04_因子投资_方法与实践/00-overview.md) |

> 第 2、4 本同源（石川），可互参：Factor Zoo 是英文学术综述，《因子投资》是最严谨的中文检验配方 + A股特殊性。

## 跨书 / 专题合成（先看这些最省时 · 对接三个决策点）
- **[_方法论总纲.md](_方法论总纲.md)** — 总览：把"读因子"变成"造因子·测因子·入库"，串起下面三个决策点。
- 决策点① scorecard 真假 → **[真假因子判据](02_Navigating_the_Factor_Zoo/_真假因子判据.md)**（多重检验 t>3/Bonferroni/FDR · 经济逻辑 · 风险vs错误定价vs数据窥探三检验 · 前向+反向OOS · 相关性 · 可投资性 → A/B/C）。
- 决策点② 回测避坑 → **[回测框架与检验方法](04_因子投资_方法与实践/_回测框架与检验方法.md)**（IC/分层/FM/GRS 检验 + √252重叠年化/单调性Spearman/合成稀释 三坑标准答案 + 稳健性 + PIT未来函数 + A股涨跌停/停牌/T+1/壳）。
- 决策点③ 成本与 L2 → **[成本模型与L2理论](03_Market_Microstructure_in_Practice/_成本模型与L2理论.md)**（成本函数模板 + 微观结构噪声为何是 L2 因子的理论根基）。

## 篇目（按书）

### 1. Machine Learning in Asset Pricing（视觉精读，11 块）
00-overview · ML01 引言 · ML02a/ML02b 监督学习 · ML03a–c 资产定价中的SL(信噪比/OOS R²/收缩=先验) · ML04a/ML04b 横截面ML(KNS·稀疏vs稠密,核心) · ML05a/ML05b 投资者信念(学习诱导伪可预测性) · ML06 研究议程

### 2. Navigating the Factor Zoo（视觉精读，22 块）
00-overview · _真假因子判据 · z01a/z01b 因子投资全景与共识因子 · z02 量化基本面 · z03a/z03b 统计矩 · z04a/z04b Market Beta(BAB/BAC) · z05a/z05b/z05c 技术分析(趋势·图形形态·指标) · z06a/z06b 微观结构与流动性 · z07 尾部风险 · z08a/z08b/z08c 行为金融 · z09 期权信息 · z10 不确定性 · z11 另类数据 · z12a/z12b 机器学习 · z13 Epilogue

### 3. Market Microstructure in Practice（视觉精读，23 块）
00-overview · _成本模型与L2理论 · m00a/m00b 导论 · m01a–m01f 第1章 碎片化(份额/SOR/tick/暗池) · m02a–m02e 第2章 流动性变量/HFT/闪崩 · m03a–m03d 第3章 冲击测量/订单簿动态/最优交易 · mA1–mA5 附录A(FEI/Kyle/Harris/最优调度/Hawkes·Signature·Epps) · mB 术语表

### 4. 因子投资：方法与实践（视觉精读，29 块）
00-overview · 01a/01b 基础(统一视角) · 02a–02e 方法论(排序单调性/回归FM/异象检验/正交化/GMM) · 03a–03d 主流因子(构造流程+成因+A股) · 04a/04b 多因子模型(A股定价) · 05a–05c 异象 · 06a–06e 研究现状(p-hacking/多重检验/行为/三类检验/样本外/ML) · 07a–07g 实践(收益·风险·组合优化·SmartBeta·择时·归因) · 08 后记+附录A

## 怎么用
- **定 scorecard / 筛 179 因子** → `_方法论总纲.md` + `02_*/_真假因子判据.md` + 因子投资 `06a/06c`。
- **回测框架避坑**（年化/单调性/正交合成/A股涨跌停停牌T+1/未来函数）→ `04_*/_回测框架与检验方法.md`（细节在因子投资 `02a/02c/02d/03a`）。
- **成本假设 / L2 因子理论** → `03_*/_成本模型与L2理论.md` + micro `m03b/m03c/mA5` + 因子投资 `07c`。
- **某因子族的构造与检验** → 对应章节笔记（统计矩/beta/流动性/行为/期权…）。
