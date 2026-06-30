# Navigating the Factor Zoo · 第4章 Market Beta（下）：Beta 相关因子 BAB / BAC [PDF p.99–108]

> Michael Zhang, Tao Lu & Chuan Shi, *Navigating the Factor Zoo: The Science of Quantitative Investing*, Routledge, 2025 · 视觉精读(PDF 物理页 p.99–108 = 书页 84–93) · 生成 2026-06-30

## 本块讲什么

本块收尾 §4.5 的 beta 分解（隔夜 beta），主体是 **§4.6 基于 beta 构造的因子**，核心两个：

- **BAB（Betting-Against-Beta，赌 beta 反向）** —— Frazzini & Pedersen (2014)，最受关注也最受争议；
- **BAC（Betting-Against-Correlation，赌相关性反向）** —— Asness, Frazzini & Gormsen (2020)，把 beta 拆成"相关性 × 相对波动"两块，只赌相关性那一块。

外加 **§4.6.2 对 BAB 的系统性批评**（Novy-Marx & Velikov 2022，"Betting Against Betting Against Beta"），以及 **§4.7 全章结论**。全块没有数据图/收益曲线，唯一插图是 Cliff Asness/AQR 的人物方框（见末节转述）。重心在**低 beta 异象的机理与两派之争**（杠杆约束 vs 彩票偏好），不是因子清单。

---

## 方法论 / 机理要点（重点·展开）

### 0. beta 分解的收尾：隔夜 beta（§4.5.3）

承上文跳跃 beta（discontinuous/jump beta，把个股跳跃与市场跳跃对比以刻画"突变带来的系统性风险"），本块补上 **隔夜 beta（overnight beta）**：刻画从前一交易日**收盘到次日开盘**的价格变化对市场的敏感度。隔夜段被视为"不连续"且往往幅度可观，因为它吸收了**闭市期间**积累的全部信息与事件。估计方法与跳跃 beta 类似，但把样本聚焦在隔夜收益上，单列为一类风险。要点在于：隔夜收益的动态与盘中不同，受**盘后新闻、全球市场联动**等驱动，可能在开盘时引发显著的价格重定价——所以把"盘中连续 / 盘中跳跃 / 隔夜"三段 beta 分开估计是有信息增量的。

### 1. 低 beta 异象：实证起点与 Black CAPM

CAPM 的核心断言：beta 高 → 应被更高预期收益补偿。但实证恰恰相反——**低 beta 证券反而有更高的风险调整后收益**，证据可追溯到 1970 年代。

- **Black, Jensen & Scholes (1972)** 用真实数据发现，**证券市场线（SML）远比 CAPM 预测的平坦**。做法：按市场 beta 把股票分成十组（deciles），逐组做时序回归。结论：**alpha 在统计上显著非零，且与 beta 负相关**——高 beta 组 alpha 为负、低 beta 组 alpha 为正。据此他们给 CAPM 增加一个**零 beta 因子（zero-beta factor）**，得到两因子模型，即 **Black CAPM**。这是"SML 太平"这一实证事实的第一次正式建模。

### 2. BAB 的机理：杠杆约束假说（leverage constraints）

Black CAPM 之后 40 年，**Frazzini & Pedersen (2014)** 提出 BAB 因子，并给"alpha 与 beta 负相关"一个**结构性解释——杠杆约束**：

- **核心故事**：很多投资者受杠杆约束（不能借钱，或借钱太贵/条款不允许加杠杆）。他们想要高收益，但无法"持有最高夏普比组合再加杠杆"，于是退而**超配高 beta 股票**来推高组合收益。这种集体行为**抬高高 beta 股价、压低其未来收益**，从而压平甚至反转 SML，造成高 beta **被高估**、低 beta **被低估**。不受约束的聪明钱（hedge funds、LBO、Berkshire Hathaway 之类有廉价杠杆来源者）反向操作——持有低 beta 再加杠杆——赚取这块溢价。
- **精确表述**：模型推出 **α = Ψ(1 − β)**。Ψ ≥ 0 是市场层面的**融资约束紧度**（约束的拉格朗日乘子式度量）。β < 1 时 alpha 为正，β > 1 时 alpha 为负；Ψ 越大（约束越紧），高低 beta 之间的 alpha 利差越大。这就把"alpha 随 beta 递减"从经验观察升级为可检验的结构关系。
- **投资者异质性**：约束更强的投资者（共同基金、个人投资者）偏好高 beta；约束更弱的（对冲基金、LBO、Berkshire）偏好低 beta。BAB 本质是去赚约束方与非约束方之间的定价错位。
- **TED spread 作为 Ψ 的代理**：TED = 三月期美债（T-Bills，视为无风险）利率与三月期 LIBOR（银行间拆借，含信用风险）之差，衡量融资/信用松紧。**TED 走阔 = 银行间信用风险上升 = 信用收紧、企业融资更难；TED 收窄 = 信用风险下降、融资宽松。** 在 BAB 语境下：**TED 走阔（感知风险更高、信用更紧）→ 预测未来 BAB 收益更高**——因为融资紧时高 beta 资产因高风险高资金成本而表现更差，BAB（多低 beta、空高 beta）反而占优；TED 收窄时高 beta 不被惩罚，BAB 收益偏低。
  - ⚠️ **书中前后矛盾[存疑]**：p.85 第一段写成"wider TED spreads, indicating *easier* financing, are associated with *lower* future BAB returns"，但同页中后段又写"wider TED spread = tighter credit = *higher* future BAB returns"。两处方向相反。按经济学与 Frazzini-Pedersen 原意，**后一种（走阔=收紧=未来 BAB 收益更高）才正确**，第一段疑为笔误。

### 3. BAB 的构造（重点公式：rank 加权 + beta 归一化）

设 \(\hat\beta_{it}\) 为股票 i 在 t 时的估计 beta。构造步骤：

1. **按 beta 升序排名**，得排名向量 \(z_i = \text{rank}(\hat\beta_{it})\)（n×1），令 \(\bar z\) 为横截面平均排名。
2. **以中位数为界分两组**：beta 低于中位数 → 低 beta 组；高于中位数 → 高 beta 组。
3. **组内按"排名偏离"加权**（不是市值加权，也不是等权——名义上想给极端 beta 更大权重）：
   \[
   w_H = k(z - \bar z)^+,\qquad w_L = k(z - \bar z)^-\quad(4.34)
   \]
   k 为归一化常数，\(x^+,x^-\) 取向量正/负元素。低 beta 股在低 beta 组里权重更大，高 beta 股在高 beta 组里权重更大；且 \(\mathbf 1'w_H=\mathbf 1'w_L=1\)。
4. **两腿各自缩放到组合 beta = 1**，再做**自融资、beta 中性**组合：做多低 beta 组、做空高 beta 组。超额收益：
   \[
   r^{BAB}_{t+1}=\frac{1}{\beta^L_t}\big(r^L_{t+1}-r_f\big)-\frac{1}{\beta^H_t}\big(r^H_{t+1}-r_f\big)\quad(4.35)
   \]
   其中 \(r^L=r'w_L,\ r^H=r'w_H\)，\(\beta^L=\beta'w_L,\ \beta^H=\beta'w_H\)。

> **机理关键（务必理解 4.35 的两个 1/β）**：低 beta 腿 \(\beta^L<1\) 故 \(1/\beta^L>1\) → **给多头加杠杆**把它拉到 beta=1；高 beta 腿 \(\beta^H>1\) 故 \(1/\beta^H<1\) → **给空头去杠杆**把它拉到 beta=1。两腿 beta 都=1，净 beta=0 → 市场中性。这正是"betting against beta"能在**剥离市场暴露**的同时、纯净捕捉低-高 beta 的 alpha 利差的机制。实证上多个市场都支持 FP，BAB 已成为防御型策略的标志、广受机构追捧。

**BAB 是市场层面（market-wide）的度量**，刻画"低 beta 相对高 beta 的风险溢价"，**不是可直接排序选股的公司层面特征**（这与 Fama-French 那种直接按公司特征排序的因子在构造上根本不同——也正是它被批评的焦点）。要拿 BAB 选股，需**两遍法**：先把个股超额收益对 BAB 因子做时序回归，得到每只股票对 BAB 的**暴露（loading）**，再用暴露选股。

### 4. 对 BAB 的批评（§4.6.2，Novy-Marx & Velikov 2022，"BABAB"）

该文从三方面挑战 BAB：

**批评①+②：排名加权 ≈ 等权 → 微盘股+风格因子搭便车。**
- 用排名做权重，效果**几乎等于等权（equal weighting）**，从而**大幅抬高小盘/微盘股的作用**，与 FP "给极端 beta 更大权重"的初衷相悖。
- 而且 FP 那套"给低 beta 多头加杠杆、给高 beta 空头去杠杆"以达到 beta 中性的做法，**同样近似等权**。
- 两者叠加 → BAB 实际上**过度超配超小盘公司**，并对 **size、profitability、investment** 三个风格因子有**高暴露**。由于这三个因子在美股本就有效，BAB 的优异表现**很大程度是搭了它们的便车**，而非纯粹来自 beta。

**批评③：估 beta 时波动率与相关性用了不同窗口 → beta 估计有偏，"无意中"自证其说。**
- 回到 OLS：被解释变量 y（个股）、解释变量 x（市场），
  \[
  \beta=\frac{\operatorname{cov}(y,x)}{\operatorname{var}(x)}\quad(4.36),\qquad
  \rho_{xy}=\frac{\operatorname{cov}(x,y)}{\sigma_x\sigma_y}\quad(4.37)
  \]
  代入得 **beta = 相关性 × 相对波动**：
  \[
  \beta=\rho_{xy}\frac{\sigma_y}{\sigma_x}\quad(4.38)
  \]
- FP 的做法：**相关性用 5 年窗、波动率用 1 年窗**。代数整理（4.39）：
  \[
  \beta_i^{FP}\equiv\rho_i^{(5)}\frac{\sigma_i^{(1)}}{\sigma_m^{(1)}}
  =\underbrace{\Big(\rho_i^{(5)}\tfrac{\sigma_i^{(5)}}{\sigma_m^{(5)}}\Big)}_{=\,\beta_i^{(5)}\ \text{传统5年beta}}
  \times\frac{\sigma_i^{(1)}/\sigma_i^{(5)}}{\sigma_m^{(1)}/\sigma_m^{(5)}}
  \]
  即 **FP-beta = 传统 5 年 beta × 一个调整系数**，系数 = （个股 1年/5年 波动比）÷（市场 1年/5年 波动比）。
- Novy-Marx & Velikov 实证：当**市场本身高波动**时，个股波动比对市场波动比的弹性 < 1 → 调整系数 < 1 → **FP-beta 偏低于真 beta**；市场低波动时弹性 > 1 → **FP-beta 偏高**。后果：把 \(\beta^{FP}\) 用到全体资产上，**全市场加总 beta 不等于 1**（随时间漂移、均值略高于 1），说明 \(\beta^{FP}\) **不是一个合理的 beta 估计量**——它内嵌了一个与**市场波动率挂钩的时变偏差**，这个偏差**无意中让策略具备了择时性**，从而"自证"了 BAB 的理论。**纠正这一窗口错配偏差后，BAB 的理论支撑被削弱（书中措辞：nullifies the theory）。**

### 5. BAC：把 beta 拆开，只赌相关性（§4.6.3，Asness, Frazzini & Gormsen 2020）

**动机**：由 (4.38)，beta 由两块构成——**与市场的相关性 ρ** 和 **相对波动率 σ_i/σ_m**。BAB 是同时赌这两块；AFG 提出框架**把两块分离**，构造只聚焦**相关性**那一块的 **BAC 因子**。

**构造（与 BAB 类似，但要控制波动率 → 相依双重排序 dependent double sort）**，每个 t：
1. **先按波动率升序分 5 组（quintiles）**；组内**再按与市场的相关性排名**分成低相关/高相关两个组合。低相关股在"低相关组合"里权重大：
   \[
   w_L^q=k^q(z^q-\bar z^q)^-\quad(4.40),\qquad k^q=\frac{2}{\mathbf 1'_{n_q}\,|z^q-\bar z^q|}
   \]
   \(z^q\) 是第 q 个波动率分组内的相关性排名向量，\(\bar z^q\) 为组内平均排名，\(\mathbf 1'w_L^q=1\)。
2. 高相关股在"高相关组合"里权重大：
   \[
   w_H^q=k^q(z^q-\bar z^q)^+\quad(4.41),\qquad \mathbf 1'w_H^q=1
   \]
   每个波动率分组内的 BAC 超额收益（同样两腿各除以自身 beta 做 beta 中性）：
   \[
   r^{BAC(q)}_{t+1}=\frac{1}{\beta^{L,q}_t}\big(r^{L,q}_{t+1}-r_f\big)-\frac{1}{\beta^{H,q}_t}\big(r^{H,q}_{t+1}-r_f\big)\quad(4.42)
   \]
3. **5 个波动率分组等权平均**得 BAC 因子：
   \[
   r^{BAC}_{t+1}=\frac15\sum_{q=1}^{5}r^{BAC(q)}_{t+1}\quad(4.43)
   \]

> 构造上 BAC **仍是 beta 中性**，但**不是 correlation 中性**（它就是要净暴露在相关性维度上）。和 BAB 一样，BAC 是**市场层面度量**，选股需先回归取暴露再选。

**为什么 BAC 是裁决两派之争的关键实验设计**：低 beta 异象有两种竞争解释——
- **杠杆约束假说（FP）**：异象源于 beta/融资约束。相关性是 beta 中真正与"系统性风险/与市场协动"相关的那部分，故约束溢价应体现在**相关性**这一块。
- **彩票偏好假说（lottery demand，Bali et al. 2017，见 §3.4）**：异象源于散户追逐"彩票型"股票（高特质波动、高 MAX），而**彩票属性绑定的是波动率，不是相关性**。

BAC 在构造上**已控制波动率、与彩票需求基本无关**。于是形成干净的判别：**BAC 若赚到显著收益 → 支持杠杆约束（相关性/beta 通道在剥离波动率后依然有效）；BAC 若失效 → 支持彩票偏好。**

**实证结论（AFG 2020）**：
- BAC **取得显著且稳健的超额收益** → 偏向支持杠杆约束。
- **保证金贷款余额（margin loan）检验**：BAB 与 BAC 在**前期保证金贷款较低（杠杆约束更紧）**时表现都显著更好 → **强支持杠杆约束假说**。
- **赌博偏好检验**：用**赌场分红/GDP 的季度变化**代理博彩偏好，发现它对 **MAX 效应有显著影响，但对 BAB 无显著影响** → 彩票故事能解释 MAX，却解释不了 BAB。
- 总判断：**杠杆约束是 BAB 的可信解释；彩票偏好则不确定（inconclusive）。**

### 6. 全章结论与未来方向（§4.7）

- beta（系统性风险）是理解市场动态的核心；其**时变不稳定性**使估计远不止"对历史做回归"那么简单。**beta 异象**（高 beta 未必高收益）已被学界充分记录。
- 条件 beta 的估计谱系（呼应"上"半章）：从**滚动窗口+预设滞后**这种基础法，到**工具变量法（IV）**、**GARCH 框架下的动态条件 beta（DCB）**；并把股票对市场的敏感度拆成**盘中连续 / 盘中跳跃 / 隔夜**三段。
- 因子应用上 BAB、BAC 最重要；但鉴于其构造方法与机理仍有争议，作者**主张理性、辩证地对待**——它们在美股及全球股市确有显著超额收益，但**不可视为理所当然**，应保持开放心态、独立验证。
- **未来方向**：① 沿 IV 思路寻找更多有稳健经济学依据的外生工具来估 beta；② 用**贝叶斯方法（Bayesian regression）**建模条件 beta；③ 把 beta 视为需用市场数据校准的**随机过程（stochastic process）**。

---

## 关键公式 · 图表 · 定义（图表要转述其内容）

| 编号 | 公式 / 含义 |
|---|---|
| (4.34) | BAB 权重：\(w_H=k(z-\bar z)^+,\ w_L=k(z-\bar z)^-\)，按 beta 排名偏离中位数加权，组内权重和=1 |
| (4.35) | BAB 收益：两腿各除自身 beta（低 beta 加杠杆、高 beta 去杠杆）→ 自融资、净 beta=0 |
| (4.36)–(4.38) | OLS beta \(=\operatorname{cov}/\operatorname{var}=\rho_{xy}\,\sigma_y/\sigma_x\)：**beta = 相关性 × 相对波动**（BAC 拆分的代数基础） |
| (4.39) | \(\beta^{FP}=\beta^{(5)}\times\dfrac{\sigma_i^{(1)}/\sigma_i^{(5)}}{\sigma_m^{(1)}/\sigma_m^{(5)}}\)：FP 用 5 年相关性+1 年波动，等价于"传统 5 年 beta × 与市场波动挂钩的时变调整系数"→ 偏差来源 |
| (4.40)–(4.41) | BAC 组内权重：先按波动率分 5 组，组内按相关性排名加权，\(k^q=2/(\mathbf 1'|z^q-\bar z^q|)\) |
| (4.42)–(4.43) | BAC 组内收益（beta 中性两腿）→ 5 组等权平均 = BAC 因子 |
| α = Ψ(1−β) | FP 杠杆约束模型核心：alpha 随 beta 递减，斜率由融资紧度 Ψ 决定 |

**唯一插图（人物方框转述）**：p.89 一个 "Cliff Asness and AQR" 文字方框。要点：Asness 是 **AQR Capital Management** 联合创始人（以系统化/量化投资著称）；芝加哥大学金融学博士，**师从 Eugene Fama**，博士论文奠定其因子投资研究；学术上实证检验各类因子（含动量、价值）的存在性与持续性，实务上把量化研究落地为面向养老金/保险/捐赠基金的因子策略产品（共同基金、对冲基金等），是把因子投资**系统化、规模化**落地的先驱之一。无任何数据图/收益曲线。

---

## 与因子研究 & 回测的关联（构造/检验/成本/L2/A股）

- **构造-估计耦合**：BAB/BAC 的全部性质都依赖 beta 估计质量，直接接回"上"半章的条件 beta 方法。**务必窗口一致**：估 beta 时波动率与相关性用同一窗口，或直接 OLS 估 beta——不要像 FP 那样混用 1 年波动+5 年相关，否则按 (4.39) 会引入与市场波动挂钩的时变偏差，污染因子。
- **两遍法选股**：BAB、BAC 都是**市场层面因子**，不能像市值/估值那样直接排序选股；需先把个股收益对因子做时序回归取 loading，再用 loading 选股。回测里要把这步显式建模，注意 loading 估计的滚动样本与前视偏差。
- **微盘+风格搭便车（Novy-Marx 批评落地）**：排名加权≈等权会过度超配微盘，并被动加载 size/profitability/investment。回测 BAB/BAC 时**必须**：①做市值加权或微盘剔除的稳健性检验；②对 FF 风格因子做归因回归，看 alpha 在控制这些因子后是否还在。**A 股微盘有壳价值+极端特质收益，此问题可能更严重。**
- **杠杆/做空可行性（A 股关键约束）**：BAB 的精髓是给低 beta 腿加杠杆、给高 beta 腿做空。A 股**融资融券标的有限、融券难且贵、T+1**，纯净的 beta 中性多空难实现；现实多退化为**多头低 beta 倾斜**（low-vol/low-beta 增强），其经济含义与可归因性会变。
- **本土可做的机理检验**：A 股有**两融余额（margin loan）**数据，可复刻 AFG 的"前期保证金低→约束紧→BAB/BAC 更强"检验；彩票通道可用 MAX、特质波动、换手等代理。L2/高频数据可用于把 beta 拆成盘中连续/跳跃/隔夜后再造 BAB 变体。
- **成本提示**：BAB/BAC 高换手（按排名时变加权、定期重缩放到 beta=1）+ 做空成本，扣费后超额会明显缩水；微盘腿冲击成本大。回测必须含融券费、冲击成本与容量约束。

---

## 术语与存疑

- **术语**：BAB=Betting-Against-Beta；BAC=Betting-Against-Correlation；BABAB=Betting Against Betting Against Beta（Novy-Marx & Velikov 2022 的批评论文）；SML=Security Market Line；TED spread=Treasury-Eurodollar 利差；MAX=月内最大日收益（彩票代理）；dependent double sort=相依双重排序；beta-neutral=beta 中性；self-financing=自融资。
- **关键人物/文献**：Black-Jensen-Scholes (1972, Black CAPM)；Frazzini-Pedersen (2014, BAB)；Asness-Frazzini-Gormsen (2020, BAC)；Bali et al. (2017, 彩票需求)；Blitz-Falkenstein-van Vliet (2014) / Blitz-van Vliet (2007, 杠杆约束/低波异象)；Novy-Marx & Velikov (2022, 批评)。
- **[存疑①·书中前后矛盾]** p.85 第一段 "wider TED = easier financing = lower future BAB returns" 与同页后文 "wider TED = tighter credit = higher future BAB returns" 方向相反。按经济学与 FP 原意取**后者**（走阔=收紧→未来 BAB 更高），第一段疑为笔误。
- **[存疑②·符号]** (4.39) 中"弹性 elasticity"一词书中用得较口语化，指个股 \(\sigma^{(1)}/\sigma^{(5)}\) 对市场 \(\sigma_m^{(1)}/\sigma_m^{(5)}\) 的响应灵敏度；本笔记照其文字转述其方向（市场高波动时<1、低波动时>1），未见其给出弹性的严格定义。
- **[范围说明]** 本块无收益曲线/分布等数据图，仅 Asness 人物方框，已转述。
