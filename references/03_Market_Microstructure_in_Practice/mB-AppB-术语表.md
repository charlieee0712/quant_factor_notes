# Market Microstructure in Practice · 附录B 术语表 (Glossary) [PDF p.350–356]

> C.-A. Lehalle & S. Laruelle, *Market Microstructure in Practice* (2nd ed.), World Scientific, 2018 · 视觉精读(PDF 物理页 p.350–356 = 原书 pp.323–329；p.357 为空白分隔页) · 生成 2026-06-30

## 本块讲什么

全书术语表，**按主题(theme)分组**而非按字母排序，作者意在让读者顺读一遍即可建立全书主干概念的整体图景；也可反查索引直接跳到术语。本笔记把它整理为**中文速查表**：每条给出「英文术语 / 中文译名 / 一句话定义」，分组沿用原书四大主题。纯客观术语翻译与定义转述，不展开方法论（方法论见各章 m01–m03 / 附录 mA 笔记）。

---

## 1. 价格形成过程 (Price Formation Process)

> 主题界定：价格形成过程涵盖交易期间一切导致市场价格持续演化的事件——例如新订单的插入、订单的撤销、对手方订单的撮合。

| 英文术语 | 中文译名 | 一句话定义 |
|---|---|---|
| Walrasian Equilibrium | 瓦尔拉斯均衡 | 消费者与生产者之间使供给与需求完全匹配的均衡。 |
| Fair Price / latent price | 公允价 / 潜在价 | 一个理论价格，表示若全部供给与需求能瞬时、无摩擦地相互对碰时价格应处的位置。 |
| Fixing (auction) | 集合竞价 | 含两阶段的竞价：盘前(pre-fixing)阶段参与者可挂单/改单但订单互不成交；随后的 fixing 本身计算一个市场出清价(market clearing price)，目标是逼近瓦尔拉斯均衡。 |
| Continuous auction | 连续竞价 | 任一订单一旦进入交易设施的撮合引擎，即与其他订单实时撮合。 |
| Market Transparency | 市场透明度 | 盘前透明度=向参与者披露订单簿状态(可仅为最优买卖价、完整报价含价与量、或更深档位)；盘后透明度=披露撮合引擎已成交的价格与数量。 |
| Market Order | 市价单 | 在任意价格上消耗流动性，因而必定消耗流动性(definitely consume liquidity)。 |
| Limit Order | 限价单 | 带有不可逾越的限价；通常由打算充当流动性提供者(liquidity provider)的参与者使用。 |
| marketable (limit) price | 可成交限价 | 为限制订单价格冲击而设置的、能立即成交的限价(限价单的一种用法)。 |
| Iceberg Order | 冰山单 | 披露数量(disclosed quantity)小于其真实规模的订单；盘前信息中只显示母单的一部分，可见部分被吃掉后再披露下一部分，直至全部成交。 |
| Request for Quote (RFQ) | 询价 | 在某些市场(如固定收益)，交易者与做市商(dealer)不在多边设施里匿名混合订单，而是交易者向做市商索取双向(买与卖)第一档的价与量"报价"，再决定是否与该做市商成交。 |

---

## 2. 监管 (Regulation)

> 主题界定：监管通过组织市场设计来确保价格形成过程的效率。

| 英文术语 | 中文译名 | 一句话定义 |
|---|---|---|
| Reg NMS | 全国市场体系规则 | 美国 SEC 于 2005 年颁布的 Regulation National Market System，旨在鼓励各市场之间、各订单之间的竞争；包含穿价规则、接入规则(market data 接入)、次美分规则(最小报价增量)与市场数据规则。 |
| Consolidated Tape | 合并行情带 | 为在美国交易所挂牌的证券提供最新成交与交易数据的电子服务，合并所有市场行情并驱动穿价规则的执行。 |
| Trade-Through Rule | 穿价规则 | 当某股票在多个市场交易时，若另一市场有更优价格，则本市场不得成交，须强制把订单重新路由(rerouting)到其他市场。 |
| MiFID | 金融工具市场指令 | Markets in Financial Instruments Directive，2007 年 11 月起施行，属欧盟委员会推动欧洲金融市场竞争的举措；2011 年修订并经欧洲议会表决，ESMA 于 2016 年 1 月发布技术标准(原计划 2018 年 1 月 1 日生效)。 |
| LIS (Large in Scale) | 大宗规模 | 当订单规模≥MiFID 实施细则附件II表2规定的最小订单规模时,即被视为相对常规市场规模"大宗";满足 LIS 的暗池不受 MiFID II 成交量上限(caps)约束。 |
| ESMA | 欧洲证券和市场管理局 | The European Securities and Markets Authority，由欧盟委员会推举取代 CESR 并增加职责；负责维护金融体系的完整与稳定、市场与金融产品的透明度、投资者保护，并防止监管套利、保障公平竞争环境。 |
| CESR | 欧洲证券监管者委员会 | The Committee of European Securities Regulators，职责为改善各国证券监管者间的协调、作为协助欧盟委员会的咨询机构,并确保成员国对欧共体立法更一致、更及时地日常落实。 |
| SEC | 美国证券交易委员会 | Securities and Exchange Commission，使命是保护投资者、维护公平有序高效的市场,并促进资本形成。 |

---

## 3. 交易场所 (Trading Venues)

> 主题界定：MiFID 取消了本国交易所集中交易规则，承认三类交易目的地——受监管市场(Regulated Markets, RMs)、多边交易设施(MTFs)、系统内部撮合商(Systematic Internalizers, SIs)；其余一切为场外(OTC)。

| 英文术语 | 中文译名 | 一句话定义 |
|---|---|---|
| Primary Market | 一级市场 / 新发行市场 | 证券首次发行之处;书中以 Euronext Paris、伦敦证券交易所(LSE)、Xetra 为一级市场之例。 |
| MTF (Multilateral Trading Facility) | 多边交易设施 | 由投资公司或市场运营商运营的多边系统，把多个第三方的买卖意愿按合约方式撮合在一起;书中研究的有 Chi-X、Turquoise、BATS。 |
| ECN (Electronic Communication Network) | 电子通信网络 | 一类便利在证券交易所之外交易金融产品的计算机系统;为 MTF 在美国的对应物。 |
| ATS (Alternative Trading Venue) | 另类交易场所 | 美国常用缩写,指非交易所的交易设施;**勿与 Average Trade Size(平均成交规模)混淆**。 |
| Lit pool | 明池 | 订单簿可见(visible order book)的交易目的地。 |
| Dark pool | 暗池 | 不披露其订单簿的交易目的地。 |
| SOR (Smart Order Router) | 智能订单路由 | 按已披露的执行策略把订单路由到一组给定交易目的地的装置;必要时可把一个订单拆成更小的子单,喷洒(spray)到所有可用目的地。 |
| BCN (Broker Crossing Network) | 经纪商交叉网络 | 一种另类交易系统,在不先把订单路由到交易所或其他显示市场的情况下电子化撮合买卖单;订单或匿名置于黑箱、或向交叉网络其他参与者标示;优势是能在不冲击公开报价的前提下完成大宗(block)成交。 |
| Matching Engine | 撮合引擎 | 持有某交易目的地上每只挂牌股票全部待成交订单、并撮合订单以算出可能成交的软件装置;一旦撮合完成,已成交交易的信息便流出引擎。 |
| Co-hosting / Co-location | 主机托管 / 同址托管 | 市场运营商提供的服务,使参与者的计算机或交易软件与交易设施的撮合引擎处于同一地点。 |
| Latency | 延迟 | 一条消息从参与者传到交易设施撮合引擎所耗的时间;交易场所通常按尽可能贴近引擎(即同址参与者)来度量,故参与者须在此基础上再加网络延迟与自身交易系统的内部延迟,才得到其实际承受的完整延迟。 |

---

## 4. 执行成本与市场深度度量 (Execution Costs and Market Depth Measurements)

> 主题界定：执行成本是费用(fees)、买卖价差(bid–ask spread)、价格冲击(price impact)、市场冲击(market impact)、机会风险(opportunity risk)与市场风险(market risk)的混合。

| 英文术语 | 中文译名 | 一句话定义 |
|---|---|---|
| Market Risk | 市场风险 | 对价格变动不确定性的度量。 |
| Price Impact | 价格冲击 | 一个订单的成交量对市场价格的冲击。 |
| Market Impact | 市场冲击 | 一笔大单(可能被拆成更小的消耗/提供流动性的子单)的成交量所带来的冲击;含两部分——先是暂时冲击(temporary impact)随后衰减(decay),余下的价格移动即为永久冲击(permanent component)。 |
| Tick Size | 最小报价单位 | 两个不同价格之间所允许的最小差额;由各交易目的地的交易规则界定。 |
| Decimalization | 小数化 | 美国股票市场 2001 年发生的最小报价单位小数化——tick 被设为一美分(one penny)而非此前更大的取值;其他地区缩小 tick 的过程也常被称为"小数化阶段(decimalization phase)",即便并未把 tick 设为一美分。 |
| LOB (Limit Order Book) | 限价订单簿 | 由交易目的地维护的未成交限价单的记录。 |
| BBO (Best Bid and Offer) | 最优买卖报价 | 市场某时点可得的最高买价或最低卖价。 |
| Touch | (同侧)最优价 | 对买单是最优买价、对卖单是最优卖价(即与订单同方向的最优价)。 |
| Best Opposite | 对侧最优价 | 对买单是最优卖价、对卖单是最优买价(即可立即对碰的对手侧最优价)。 |
| Bid–Ask Spread | 买卖价差 | 最优买价与最优卖价之间的距离,可用货币或基点(bp)表示。 |
| mid price | 中间价 | 买卖价差的中点。 |
| VWAS (Volume-Weighted Average Spread) | 成交量加权平均价差 | 每笔成交时买卖价差的中点,按该笔成交量加权(原文定义如此)。 |
| Market Depth | 市场深度 | 使市场价格移动给定增量所需的订单规模;市场越深,改变价格所需的订单越大;与流动性(liquidity)概念密切相关。 |
| Average daily number of trades | 日均成交笔数 | 该值越高,股票交易越活跃;对股票流动性有正向贡献。 |
| ATS (Average Trade Size) | 平均成交规模 | 以欧元计的平均成交规模,可视为该场所订单的"自然规模(natural size)";**勿与 Alternative Trading System 混淆**。 |
| % Time at E/N-BBO | 处于 E/N-BBO 时间占比 | 一天中该场所所提供价差等于欧洲或全国最优买卖价(EBBO 对应欧洲、NBBO 对应美国)的时间比例。 |
| Adverse Selection | 逆向选择 | 买卖双方信息不对称的市场过程(类比保险业中越想投保者越可能有健康问题);例如暗池中,若你的订单被完全成交,说明对手方流动性比你更大、很可能引发市场冲击把价格推向不利于你的方向——订单被成交本身就是"其实你不该让它成交"(本应等价格被推动后再去对碰)的信号。 |
| Opportunity Costs | 机会成本 | 逆向选择成本的对偶:已成交时若几分钟后价格更有利,则承担逆向选择成本;选择不交易时若几分钟后价格更不利,则承担机会成本。 |
| bp (Basis Point) | 基点 | 百分之一的百分之一,即 1/100/100(万分之一)。 |

---

## 术语与存疑

- **ATS 一词两义**：原书明确警示同一缩写在不同语境含义不同——交易场所主题下指 Alternative Trading Venue(另类交易场所),度量主题下指 Average Trade Size(平均成交规模),互勿混淆。
- **VWAS 定义**：原书字面写作"每笔成交时买卖价差的中点(middle of the bid–ask spread),按成交量加权",名称却为"平均价差(Average Spread)";此处忠实转述原文,未作改写。
- 全部条目均为原书附录B 直译/转述,未掺入外部定义;书内对应章节深入处见 m01–m03 与 mA 系列笔记。
