# Market Microstructure in Practice · 第1章 §1.3 最优 tick size（上）[PDF p.101–115]

> C.-A. Lehalle & S. Laruelle, *Market Microstructure in Practice* (2nd ed.), World Scientific, 2018 · 视觉精读(PDF 物理页 p.101–115，对应书内页 p.74–88) · 生成 2026-06-30

---

## 本块讲什么

本块进入第1章 §1.3「Still Looking for the Optimal Tick Size（仍在寻找最优 tick size）」，覆盖两小节：

- **§1.3.1 Why does tick size matter?（tick size 为何重要）**——定义 tick size、两种 tick 制度（统一制 vs. 动态/分档制）、tick 对价格离散性与波动率度量的污染，并抛出贯穿全节的**三个核心问题**。
- **§1.3.2 How tick size affects market quality（tick size 如何影响市场质量）**——用一组"市场质量代理变量（proxies）"系统论证：缩小 tick **只有在 tick 是约束（binding）时**才压低 spread；同时缩 tick 会让盘口变薄、挂单变小、成交变小、撤改单/成交比上升。配 6 张实证图（Fig. 1.19–1.24，DAX/S&P500/FTSE100）。

核心立场（作者反复强调）：**单个代理变量都不等于"市场质量"本身**；缩 tick 是有阈值的、对不同股票效果相反的、并且常被交易场所当作抢市场份额的杠杆而非改善质量的手段。本块在讨论"queue jumping（插队）"机理处于书内页 p.88 中途截断，留待"下"篇续。

---

## 方法论 / 机理要点（重点·展开）

### 1. tick size 的定义与两种制度（识别问题的根源）
- **定义**：tick size 是合法限价单必须落在的**价格网格**步长——任何报价必须是 tick 的整数倍；因此它也是**两个限价之间的最小价格增量**，是 bid–ask spread 的天然下界。
- **两种制度（这是后续一切"识别策略"的前提）**：
  - **统一制（"one size fits all"）**：不分股价/流动性，全市场同一 tick（美国对 >US$1 的股票用统一 $0.01）。
  - **动态/分档制（tick size regime / dynamic tick size）**：tick 依股价区间与报价分组而定（除美国、澳大利亚、印度外，全球多数市场如此）。理论意图是**按流动性给股票分组**给不同 tick。
- **机理后果**：tick 决定成交价的**离散程度**。建模时要么简化为常数价格增量，要么必须引入"底层连续价格 + 离散化"的复杂模型。

### 2. tick 对波动率度量的"污染"（一个易被忽视的坑）
- 设想一只**大 tick（相对 spread 而言）**资产：spread 长期黏在 1 个 tick，bid/ask 在一段时间内恒定。此时若**只用成交价**估波动率，所得"波动率"其实只是 tick size 的函数——它度量的是"下一笔成交价的不确定性"，与小 tick 资产上同名的波动率**含义不同**。
- 文献佐证：[Wyart et al., 2008] 发现"spread 与波动率的关系"在小 tick 资产成立、在大 tick 资产**不成立**。[Dayri and Rosenbaum, 2012] 用 **uncertainty zone model（不确定区模型）** 显式建模离散化，试图还原"若 tick 不是 spread 地板时本应观测到的、与波动率相关的 implicit/underlying spread（隐含/底层 spread）"。[Harris, 1994] 是另一个还原底层 spread 的模型（书中放在 Appendix A.6，称 **Harris Model: Underlying Continuous spread Discretized by Tick**）。
- **方法论启示**：在大 tick / A股这种 tick 常被打满的标的上，直接用成交价算的 realized vol、价差类指标都可能被 tick 机械地"撑住"，需用离散化模型去还原"底层"量。

### 3. 贯穿全节的三个核心问题，以及它们为何纠缠在一起
作者明确列出真正要回答的三问（而上面那些代理变量都只是"成分"、都没有公认的定义与综合方法）：
1. **tick size 如何影响市场质量？**
2. **交易场所如何用 tick size 去抢市场份额（market share）？**
3. **tick size 如何改变各类参与者的盈利能力（profitability）？**

为何纠缠：研究"某市场因改 tick 而流动性下降"（问题1）若其实流动性只是**转移到了另一交易池**（问题2），则问题1的结论失真；而若抢到份额的市场主要被某类（需要高级技术的）参与者使用，则问题3浮现——这类参与者所付成本/所赚租金，相对他们对价格形成（price formation）的贡献是否过高？

### 4. "代理变量 ≠ 市场质量"——本节最重要的方法论警告
作者把市场质量的常用度量逐一点名：quoted/effective spread、price impact、market impact、quoted size、orderbook depth、trade size、resiliency（韧性）、order exposure（挂单暴露）、quoted adverse selection、考虑成交等待时间的限价单盈利性、被插队/front running 的难易、机构投资者总交易成本……

两条"代理变量不可信"的根本理由：
- **混杂**：真实交易中所有效应交织，单独看某个代理变量的变化无法给出全局结论；
- **内生适应**：给定投资者的交易成本取决于其投资与执行策略，市场设计一变，策略就会**主动适配**——而适配所需的技术/研究投入（往往不小）根本无法度量。

并指出研究欧洲当前市场用 orderbook 的两难：只看一个市场的 orderbook 无意义；但把所有交易场所 orderbook 简单加总也不对——存在 **mirroring orders（镜像单）**（在别处成交时会被撤），还有交易场所间的同步问题（[van Kervel, 2012]）。

### 5. 度量"tick 对 spread 的约束程度"的两个简单指标
- **Binding probability（绑定概率）**：bid–ask spread 恰等于 1 个 tick 的"成交笔数/成交金额/报价持续时长"占比。取值 0–1，越大说明 tick 约束越强。
- **Spread Leeway（spread 余量）**：以 tick 为单位表示的 spread 再减 1。越大说明该股越不受 tick 约束。（书中作图时直接用"以 tick 表示的 spread"即 **spread in ticks**。）
- 用途：简单可算、能有效筛出"哪些股票会因缩 tick 而 spread 真正下降"。

### 6. 缩 tick 压低 spread 的机理与"阈值效应"（§1.3.2 主线）
- **机理**：tick 是 spread 的硬下界 → tick 越是把 spread 约束住（binding 越强），把 tick 调小、spread 的预期下降幅度越大。Harris 模型正是用来**量化**"缩小最小报价单位能带来多大 spread 下降"。
- **谁受益**：高换手、低价股（spread 几乎总等于 1 tick）缩 tick 后 spread 明显下降；而 >$150 的高价股 spread 本就不受 tick 约束，缩 tick 无效。
- **阈值/反转效应（关键）**：实证（[Jones and Lipson, 2001]、[Chakravarty et al., 2005]、[Wu et al., 2011] 用美国 1992→2001 缩 tick；[Aitken and Comerton-Forde, 2005] 用澳洲）一致表明**存在一个 tick 阈值，低于它再缩 tick 反而会让 spread 变大**——对低流动性高价股甚至"最好情况是无效、坏情况是 spread 上升、所有流动性代理都变差"。[Ahn et al., 1996] 用 1992 年 AMEX 把 $1–$5 股票从 1/8 改 1/16 的事件检验 Harris 模型：**方向对，但幅度被高估**。
- **代价**：即便缩 tick 有效压低了 spread（小额市价单的 liquidity premium 下降），代价是 **quoted size 下降**——于是引出下一个问题：给定成交量，调大 tick 是否反而降低 taker 成本？

### 7. "更小更快的流动性 = 更不稳定？"——盘口变薄的机理
- **机械原因**：小 tick 把限价单摊到更多价位 → 每个价位的挂单量更少。
- **行为原因（更关键）**：小 tick 下只需极小的价格改善就能取得**时间优先权（queue jumping，插队）**，因此无需再"排在队尾等队列耗尽"——随时能以微小增量刷到最优价之前。结果：最优档的挂单量在小 tick 下**大幅缩小**。
- **挂单暴露（order exposure）的经济激励**：除了"价位更多"的机械稀释，更有**故意隐藏单子全量**的动机——[Bacidore et al., 2003]、[Goldstein and Kavajecz, 2000] 发现小 tick 下不仅每个价位单子更少，**单笔挂单本身也更小**：因为别人用微小价格改善就能抢到你前面，于是参与者宁可少露量以**避免被 front run**。
- **连锁后果**：挂单变小 → 成交量 = min(provider 单, consumer 单)，故**成交规模变小**（成交笔数应增多但总成交量几乎不变）；同时**撤改单/成交比（order-to-trade ratio）上升**——流动性不仅更薄，还更频繁地在价位间跳动，单条报价的"价值"下降（既更小、寿命又更短）。
- 结论性比喻：可挂单的价位越多，每个价位上的流动性就越少（不奇怪）；但"健康、有深度的 orderbook"终究是可欲的——这正是 spread 单指标无法捕捉的。

### 8. 累计深度（cumulative depth）与"重建 orderbook"测成本的方法
- 想同时纳入 spread 与挂单量、衡量**给定成交量的执行成本**，可在有**逐单（order-by-order）数据库**时**重建限价 orderbook**，算出任意规模市价单的即时流动性消耗成本（即 effective spread / price impact），并比较事件前后、判断哪个 orderbook 更稳健。
- **优点**：能纳入 hidden liquidity（隐藏流动性）。
- **缺陷**：① 结论**条件于 taker 行为**——若 taker 因缩 tick 而把单子拆小，则前后不可比；② 多数研究用美国 decimalization 事件，而美国当时已高度碎片化，单一 orderbook 的变化未必代表参与者真实面对的情况（可去 ECN 成交）。
- **实证与"深度悖论"**：[Bacidore et al., 2003]（NYSE 逐单库）发现 decimalization（1/16→cent）后**任意规模市价单的期望成本都下降**、orderbook（在成交时点上、条件于成交单规模）更深；但他们看**任意时点的累计深度**时发现：**距 BBO 15 美分以内更稳健、更深档却变差**。看似矛盾实则不然——样本里成本 >15 美分的市价单几乎不存在，故"最深档缺失的流动性"在成交数据里看不见（这也顺带反映 orderbook 的 **resiliency 韧性**——成交"足迹"被消耗后补回队列的能力）。
- **方法论批评（很重要）**：他们的深度度量用的是**绝对成本**而非**相对于成交标的价值**的成本——意味着"为买 1000 美元的东西多付 1 美元"和"为买 10 美元的东西多付 1 美元"被等同看待，不合理。

### 9. 跨研究的稳健结论：不分股票一刀切缩 tick 会损害流动性
- [Goldstein and Kavajecz, 2000]（NYSE 单据 + 加入 specialist 报价 + 看 effective spread 纳入隐藏流动性；成本用 **basis points** 计以便跨高低价股可比；并按高/低价、高/低成交量**分样本**——这是更干净的设计）发现：decimalization 后**公开 orderbook 变浅**；高换手股的"虚拟大单"成本上升、低换手股任意规模成本上升；但加入 specialist 流动性后小单成本对各类股票都改善（至少 quoted spread 改善），**大单成本对所有类别仍更贵**；effective spread 看：小单对所有股票成本下降、高价高换手股的大单无改善、低换手股的大单显著改善。
- 总结论：**不顾股票特性一刀切缩 tick，会通过抬升成本而损害流动性**；并佐证"挂单暴露被抑制"。
- [Harris, 1996]（多伦多交易所 + 巴黎 Bourse，后者无 tick 变化但 spread-in-tick 异质足以识别）与 [Bourghelle and Declerck, 2004]（巴黎 Bourse 有股票 tick 升、有股票 tick 降）都证实：**tick 越小，限价挂单暴露越被抑制，参与者更多用隐藏流动性以防被 front run**。
- [Aitken and Comerton-Forde, 2005]（澳洲 1995 缩 tick）证实"需要小 tick 的股票流动性更便宜、本就小相对 tick 且低换手的股票更贵"；但他们称"对挂单暴露无影响"——作者批评这只是因为其**显著性检验不显著就拒绝解读**，而从业者视角看变化幅度其实重要（除一个样本外都呈现"部分隐藏单占比上升"，只是统计不显著；而那个例外样本是缩 tick 后相对 tick 仍高达股价 1% 的极大相对 tick 组）。
- **总方法论提醒**：order exposure 受多种力作用，**度量方式不同结论可能截然不同**。

### 10. 相对 tick 大 → 暗池/插队更盛（连接到"交易场所竞争"的伏笔）
- 美国 off-lit（暗池）交易在**相对 tick 最大的股票**上更多——因为暗池可在比 tick 更细的网格上成交，从而用极小价格改善 queue jump。
- 大 tick 股策略更盛的两重原因：① 大 tick 股因 tick 约束而 spread 大，能用微小让价 undercut 限价单的人即可"做市"赚取大 spread 租金；② 美国几乎所有场所采 **maker-taker fee（挂单返佣、吃单收费）**，费用按"美元/股"而非按成交价值计——故相对成交价值看，**低价股付给流动性提供方的返佣更大**，构成在低价股提供流动性、用 ECN 以微小价格改善赢得竞争的额外激励。
- 末尾引出"queue jumping 被视为小 tick 下挂单受抑的根因"：插队若非为建仓，可被视为一种 front running（被插队者从耐心变急躁、跨 spread 反向砸向刚抢走机会的那个 provider）——此处文本在书内页 p.88 截断，留待"下"。

---

## 关键公式 · 图表 · 定义（图表逐一转述）

### 定义/指标
- **tick size**：限价单价格网格步长 = 合法报价的最小整数倍单位 = 相邻限价的最小增量 = spread 的硬下界。
- **relative tick size（相对 tick）**：≈ 绝对 tick / 股价（或 / mid-price）。在 log–log 图上，固定绝对 tick 时它是一条斜率 −1 的直线段。
- **Binding probability**：spread = 1 tick 的占比（笔数/金额/时长口径），∈[0,1]，越大约束越强。
- **Spread Leeway** = (spread 以 tick 计) − 1，越大越不受约束。
- **spread in ticks**：VWAS（成交量加权平均 spread）÷ tick——FTSE 系列图的横轴/分组依据，本质是"相对 tick 的反向代理"（spread-in-ticks 越大 ⇒ 相对 tick 越小、tick 越不绑定）。
- **order-to-trade ratio**：前五档之一发生更新的次数 ÷ 成交笔数（用成交笔数归一化以免被最活跃股主导；比值越大说明单条 orderbook 更新的信息含量越低）。

### Fig. 1.19 — DAX/XETRA，相对 spread vs 股价（log–log，2012-07）
横轴=股价（log，约 2→90+），纵轴=spread（basis points，log，约 2→9+）。**绿色十字** = 单股单日 VWAS(bp) vs VWAP；**实线** = 相对 tick size，呈**锯齿（sawtooth）**：每个价格档内随股价升高相对 tick 下降（向下斜段），跨档时绝对 tick 跳升、相对 tick 随之**向上跳**——这是欧洲**分档 tick 制度**的指纹。十字基本都落在锯齿线**上方**：只有当相对 tick 成为 spread 的有效下界时，spread 才会贴到这条线。传达：欧洲相对 tick 随价格非单调（锯齿）变化；spread 与价格本无关系（spread 已相对化），唯有 tick 当地板时才出现"贴线"约束。

### Fig. 1.20 — S&P500/美国，相对 spread vs 股价（log–log，2012-07）
横轴=股价（log，约 7→403），纵轴=spread（bp，log，约 1→55）。**绿色十字** = 单股单日 VWAS(bp)；**实线** = 相对 tick size，是**一条单一向下直线**（美国统一 $0.01 tick ⇒ 相对 tick = 0.01/股价，在 log–log 上为直线）。低价股：十字**紧贴这条线**（spread=1 tick，完全被约束）；高价股（>$150）：十字**远在线上方且发散**（不受约束，spread 反映波动率而非 tick）。与 Fig.1.19 对照：美国"one size fits all"是直线、欧洲分档是锯齿。传达：同一 tick 政策下，便宜股 tick 绑定、贵股不绑定——这种**横截面异质性**让研究者**无需 tick 变更事件**，只要找"特征相似但 spread-in-tick 不同"的两只股票即可识别 tick 对某流动性指标的影响（本书下一节用它讲交易场所竞争）。

### Fig. 1.21 — FTSE100，最优档挂单量 vs spread-in-ticks（2012-04）
横轴=spread in tick 的十分位（约 1→7+），纵轴=最优档挂单量（pence，×10⁶，0→18）。每个十分位一个**箱线图**+离群绿十字+连线（绿方块=均值/中位趋势）。趋势**单调下降**：spread=1 tick 时挂单量最高（中位 ~8×10⁶），到 7 ticks 降至 ~1×10⁶。传达：相对 tick 越小（spread-in-ticks 越大），**最优档可成交量越少**——更小的 quoted spread 其实只对应更少的可成交量，"跨过 spread 去成交超额量"的成本未必更低，故 **spread 单指标不足以评判市场质量**。

### Fig. 1.22 — FTSE100，最优档单笔挂单均值 vs spread-in-ticks（2012-04）
横轴=十分位（约 1→13），纵轴=最优档每笔挂单的均值（pence，×10⁵，约 1→14）。箱线图**下降**，首尾分位**近 3 倍**落差（首位 ~8×10⁵ → 尾位 ~3.5×10⁵）。传达：不仅价位上"总量"少，**单笔挂单本身也变小**——印证小 tick 下"少露量防插队/防 front run"的挂单暴露抑制机理。

### Fig. 1.23 — FTSE100，平均成交规模 vs spread-in-ticks（2012-04）
横轴=十分位（约 1→17），纵轴=平均成交规模（pence，×10⁵，约 1→12）。**下降**：首位 ~6×10⁵ → 尾位 ~3×10⁵。传达：成交规模 = min(provider 单, consumer 单)，挂单变小 ⇒ **成交变小**（总成交量基本不变，但应有更多笔成交）。

### Fig. 1.24 — FTSE100，order-to-trade ratio vs spread-in-ticks（2012-04）
横轴=十分位（约 1→13），纵轴=前五档之一每笔成交对应的更新次数（约 5→50）。趋势**上升**：首位 ~17 → 尾位 ~26，**首尾约 +50%**。传达：相对 tick 越小，流动性不仅更薄，还**更频繁地在价位间跳动**——单条报价价值下降（既更小、寿命又更短）。

### 模型指针
- **Harris Model（Underlying Continuous spread Discretized by Tick）**：把可观测离散 spread 视为"底层连续 spread 被 tick 离散化"的结果，用以量化缩 tick 的 spread 下降幅度。详见书末 **Appendix A.6**（本块仅指针）。

---

## 与因子研究 & 回测的关联（构造/检验/成本/L2/A股）

- **A股是典型"大 tick / tick 常绑定"市场**：低价股 spread 长期=1 tick。直接用成交价算的波动率、价差类微结构因子会被 tick **机械撑住**，含义被污染——做这类因子前应先估 **binding probability / spread-in-ticks**，对"tick 绑定"与"非绑定"样本分层，或借 uncertainty zone / Harris 思路还原底层 spread/波动率再入因子。
- **横截面识别范式可直接借用**：Fig.1.20 的思路——用 **spread-in-ticks** 作为"相对 tick 约束强度"的连续代理，做**横截面分层/回归**，无需依赖一次性 tick 改制事件。可用于检验"相对 tick 约束"是否解释流动性/反转/做市收益类因子的横截面差异。
- **成本建模**：本块的硬结论——缩 tick 压低 quoted spread 但**盘口变薄、单笔挂单变小、order-to-trade 比上升**。回测的冲击成本/滑点模型**不能只看 quoted spread**，必须叠加"给定成交量需吃穿多少档"的**累计深度（cumulative depth / effective spread）**；尤其大单成本在小 tick 下可能不降反升。
- **L2/逐单数据的用法**：用逐单库**重建限价 orderbook**、算任意规模市价单的即时消耗成本（effective spread / price impact），并比较事件前后——是衡量"哪本 orderbook 更稳健"的标准做法；注意其结论**条件于 taker 行为**（taker 拆单会破坏前后可比性），且需关注 **resiliency（韧性，补单能力）**。
- **挂单暴露/隐藏单因子**：小 tick → 更多 hidden liquidity、更小可见挂单。构造"挂单暴露/隐藏比例"类因子时，要意识到它对 tick 绑定程度高度敏感；并警惕 **mirroring orders（镜像单）** 污染跨场所深度聚合。
- **成本要相对化**：作者批评"绝对成本"度量——所有成本/深度类因子与回测口径都应**相对于成交价值（bp 计）**，而非绝对货币额或股数，以便跨高低价股可比。
- **maker-taker 与低价股**：按"美元/股"计的返佣使低价股做市相对收益更高——做市/提供流动性类策略的收益因子需把**费率结构 × 价位**一并纳入。

---

## 术语与存疑

- **tick size / tick**：最小报价单位（价格网格步长）。**relative tick**：相对 tick ≈ 绝对 tick/股价。
- **tick size regime / dynamic tick size**：动态/分档 tick 制度（按价格区间与报价分组设 tick）。
- **binding probability**：绑定概率（spread=1 tick 的占比）。**spread leeway**：spread 余量 = (spread/tick) − 1。**spread in ticks**：以 tick 计的 spread（VWAS/tick）。
- **VWAS**：Volume Weighted Average Spread（成交量加权平均 spread）；**VWAP**：成交量加权平均价。
- **decimalization**：美国 1990s 把最小报价从 1/8（后 1/16）美元改为 1 美分的"十进制化"改革。
- **queue jumping**：插队（以微小价格改善抢时间优先权）；**front running**：抢跑/抢先交易。
- **order exposure**：挂单暴露（愿意公开显示的挂单量）；**hidden liquidity**：隐藏流动性。
- **resiliency**：韧性（orderbook 被消耗后补回队列的能力）。**cumulative depth**：累计深度。
- **effective spread / price impact**：有效价差/价格冲击（任意规模市价单的即时流动性消耗成本）。
- **maker-taker fee**：挂单返佣、吃单收费的费率模式。**ECN**：电子通讯网络（一类电子交易场所）。**BBO**：Best Bid and Offer（最优买卖报价）。**mirroring orders**：镜像单（在他处成交时会被撤）。
- **uncertainty zone model**：不确定区模型（[Dayri and Rosenbaum, 2012] 还原 implicit spread）；**Harris Model**：底层连续 spread 被 tick 离散化的模型（Appendix A.6）。
- 引用的实证：[Wyart et al., 2008]、[Harris, 1994/1996]、[Angel, 1997]、[Ahn et al., 1996]、[Jones and Lipson, 2001]、[Chakravarty et al., 2005]、[Wu et al., 2011]、[Aitken and Comerton-Forde, 2005]、[Bacidore et al., 2003]、[Goldstein and Kavajecz, 2000]、[Bourghelle and Declerck, 2004]、[van Kervel, 2012]。

存疑：
- 各 FTSE 图纵轴量纲（×10⁶/×10⁵ pence）与横轴十分位上界（7/13/17 等）系从图轴刻度目测读取，**具体数值为近似**，趋势方向确凿。[图中存疑：精确刻度]
- 本块文本在书内页 p.88 讨论"queue jumping 是否构成 front running"处**中途截断**，相关完整论证续见"下"篇（§1.3 后半）。
