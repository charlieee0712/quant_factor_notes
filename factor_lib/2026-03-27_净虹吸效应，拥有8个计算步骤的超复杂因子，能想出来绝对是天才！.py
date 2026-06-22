"""净虹吸效应，拥有8个计算步骤的超复杂因子，能想出来绝对是天才！

自动生成自 ../sources/general/articles/2026-03-27_净虹吸效应，拥有8个计算步骤的超复杂因子，能想出来绝对是天才！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-03-27_净虹吸效应，拥有8个计算步骤的超复杂因子，能想出来绝对是天才！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 净虹吸效应，拥有8个计算步骤的超复杂因子，能想出来绝对是天才！
# 日期    : 2026-03-27
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247495737&idx=1&sn=0661c0105e13450dc604544b9c410cc1
# 本地原文: ../sources/general/articles/2026-03-27_净虹吸效应，拥有8个计算步骤的超复杂因子，能想出来绝对是天才！.md
# 本地图片: ../sources/general/articles/images/2026-03-27_净虹吸效应，拥有8个计算步骤的超复杂因子，能想出来绝对是天才！/  (共 21 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **净虹吸效应**
#
# 本文，笔者将继续复现民生证券叶尔乐老师在2025年1月21日发布的研报《量化专题报告：资金流潮汐与“引力场”因子构建》中的第二个因子，虹吸效应。
#
# 第一个因子，主买成交特异性，笔者在[主买成交特异性，用分钟数据强行构造主买数据，能行吗？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247495622&idx=1&sn=53bc4a83c3269657abcfcff21f50a56f&scene=21#wechat_redirect)这篇文章中复现了。
#
# 该因子的核心逻辑是，出现与市场卖盘不同步的主卖成交量，未来股价更有可能反转。同时，研报中还分析了在两种情况下主卖情绪较大的股票未来可能上涨。
#
# 第一，主力资金恐慌性震仓，导致大量噪音交易者抛售手中筹码，股票处于超卖状态，待主力资金低价吸收筹码后，股票价格进入上涨趋势。
#
# 第二，突然出现热点，追热点的人卖出部分持仓然后买入热点标的，当热点退去，他们很有可能买回之前的标的。
#
# **计算步骤和代码**
#
# 关于这个因子的计算步骤，研报中给出了一张图片来进行说明。
#
# 但是，只看图片的话应该不太好理解，还是得结合步骤来看。毕竟，这个因子的的计算有八步！
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，计算成交量放大倍数（个股第 t 分钟成交量 / 个股第 t-1 分钟成交量），记作AM。
#
# 第二步，计算收益率修正的成交量放大倍数，记作RAM。这一步的设计利用了威科夫交易法中的“努力（成交量）与结果（收益率）”原则。
#
# 若个股当前分钟收益率 > 所有个股成交总额(TA)加权的当前分钟平均收益率，则取AM；否则为 0。
#
# 第三步，计算市场炒作热度，就是个股成交总额(TA)加权的平均RAM。
#
# 第四步，计算热度时间，即去掉第一分钟和最后三分钟后取市场炒作热度最大的23分钟。
#
# 第五步，计算虹吸效应。即，热度时间中，“个股每分钟主卖成交额占比（即个股每分钟主卖成交额 / 市场当日主卖成交额之和，注意不是市场每分钟主卖成交额）”和“市场每分钟主卖成交额占比”的相关系数。
#
# 第六步，计算虹吸回流综合效应。简单来说，就是将最后5分钟定义为回流时刻，将其当作一根k线来计算个股每分钟主卖成交额占比和市场每分钟主卖成交额占比。最后，和前面的23个数据一起，一共24条数据（即热度时刻+回流时刻一共24条k线）按照第五步的方法计算相关性。
#
# 第七步，以虹吸回流综合效应为被解释变量，虹吸效应为解释变量进行截面回归并取残差。
#
# 第八步，取残差过去21个交易日的均值。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 从相关性来看，净虹吸效应和虹吸回流综合效应的相关性较高，为0.94，两者的分层回测表现应该不会出现太大的差异了。
#
# 净虹吸效应因子无论是用均值来进行低频化，还是用标准差来进行低频化，其在IC上的表现是差不多的，两者仅在分层回测的时候有微小的差别。
#
# 所以，笔者前面仅展示均值低频化的因子评价结果，只在收益分析的时候提一嘴标准差低频化的因子。
#
# 值得一提的是，用主买来计算这个因子，也就是将第2段代码第9行的（1-prob）改成prob，IC和分层回测都会好那么一点点。因此，这个因子的收益分析笔者也将展示一下。
#
# 至于虹吸效应因子，这个因子在IC和分层回测上的表现都不行，所以就不提了。
#
# ## IC分析
# 这个因子IC绝对值最高的一年都没有超过0.05。
#
# ## 收益分析
# 这个因子的分层回测结果展现出了两头好中间差的趋势。
#
# 用标准差低频化之后，分层回测的单调性看起来好了一点点。至少，因子值最小的一组收益率最高，因子值最大的一组收益率最小了。不过，这个因子的方向似乎和研报中的相反了，可能还是因为主卖成交额的计算方式导致的吧。
#
# 最后，再来看看用主买成交额计算的因子的分层回测结果。
#
# 这个因子用均值或标准差低频化之后的结果不太一样，这里展示的是用均值低频化的因子。
#
# 好了，这个超级复杂的因子介绍到这里就结束了。从笔者的复现情况来看，这个因子的表现很平庸。当然，这可能是主买主卖的计算方式导致的。
#
# 虽然，这个因子的表现很平庸，但是笔者在理解这个因子复杂的计算步骤的时候还是浪费了很多脑细胞的，所以希望各位大佬看完之后能够点赞关注推荐和分享支持一波。
#

# ============================================================
# 本地图片清单（共 21 张）
# ============================================================
# 001.png  <-  计算步骤和代码
# 002.jpg  <-  代码
# 003.png  <-  代码
# 004.png  <-  因子评价
# 005.png  <-  IC分析
# 006.png  <-  IC分析
# 007.png  <-  IC分析
# 008.png  <-  IC分析
# 009.png  <-  IC分析
# 010.png  <-  IC分析
# 011.png  <-  回归分析
# 012.png  <-  回归分析
# 013.png  <-  换手率分析
# 014.png  <-  换手率分析
# 015.png  <-  收益分析
# 016.png  <-  收益分析
# 017.png  <-  收益分析
# 018.png  <-  收益分析
# 019.png  <-  收益分析
# 020.png  <-  收益分析
# 021.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    # 加载当日分钟数据
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    cur_time = pd.to_datetime(date_str) + timedelta(hours=15)
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close', 'volume', 'turnover', 'high', 'low']).to_dataframes()
    rtn = data['close'].pct_change()
    am = data['volume'].pct_change() + 1
    ta = data['turnover'] / data['turnover'].sum(axis=1).values.reshape(-1, 1)
    mkt_rtn = (rtn * ta).sum(axis=1)
    flag = rtn > mkt_rtn.values.reshape(-1, 1)
    ram = am * flag
    ram = ram.replace(np.inf, np.nan)
    mkt_ram = (ram * ta).sum(axis=1)
    mkt_ram.reset_index(inplace=True, drop=True)
    self.warm_time = mkt_ram.iloc[1:-3].sort_values(ascending=False).iloc[:23].index.tolist()
    act_buy_ratio, mkt_act_buy_ratio, tot_act_buy = self.cal_act_ratio(data)
    siphon = act_buy_ratio.corrwith(mkt_act_buy_ratio)
    data_5min = BaseDataLoader.load_data(os.path.join('../../data/stock/stock_bar_5min', file_name),
                                    fields=['close', 'volume', 'turnover', 'high', 'low'],
                                    start=cur_time-timedelta(minutes=5)).to_dataframes()
    act_buy, mkt_act_buy = self.cal_act_ratio(data_5min, 5)
    act_buy_ratio = pd.concat([act_buy_ratio, act_buy / tot_act_buy])
    mkt_act_buy_ratio = pd.concat([mkt_act_buy_ratio, mkt_act_buy / tot_act_buy])
    reflux = act_buy_ratio.corrwith(mkt_act_buy_ratio)
    res = pd.concat([siphon, reflux], axis=1)
    res.columns = ['siphon', 'reflux']
    net_siphon = self.cal_resi(res)
    res = res.join(net_siphon)
    res['datetime'] = cur_time
    return res

# (作者注) 前7行，读取数据。
#
# (作者注) 第8行，计算分钟收益率。
#
# (作者注) 第9行，对应第一步，计算成交量放大倍数。
#
# (作者注) 第10行，计算成交额加权的权重。
#
# (作者注) 第11行，计算市场收益率。
#
# (作者注) 第12-14行，计算收益率修正的成交额放大倍数。
#
# (作者注) 第15行，计算市场炒作热度。
#
# (作者注) 第16-17行，计算热度时间。
#
# (作者注) 第18行，计算个股每分钟主卖成交额占比和市场每分钟主卖成交额占比。
#
# (作者注) 第19行，计算虹吸效应因子。
#
# (作者注) 第20-26行，计算虹吸回流综合效应因子。其中，第20-25行，是计算回流时刻的个股每分钟主卖成交额占比和市场每分钟主卖成交额占比。
#
# (作者注) 第29行，计算净虹吸效应因子。

# --- 代码块 2 ---
def cal_act_ratio(self, data, mode=1):
    prob = (data['close'] - data['low']) / (data['high'] - data['low'])
    prob = prob.replace(np.inf, np.nan)
    prob = prob.replace(-np.inf, np.nan)
    prob = prob.clip(lower=0, upper=1)
    flag = data['close'].pct_change() > 0
    prob[pd.isna(prob) & flag] = 1
    prob[pd.isna(prob) & ~flag] = 0
    act_buy = data['turnover'] * (1 - prob)
    mkt_act_buy = act_buy.sum(axis=1)
    if mode == 1:
        tot_act_buy = mkt_act_buy.sum()
        act_buy_ratio = act_buy / tot_act_buy
        mkt_act_buy_ratio = mkt_act_buy / tot_act_buy
        return act_buy_ratio.iloc[self.warm_time], mkt_act_buy_ratio.iloc[self.warm_time], tot_act_buy
    return act_buy.iloc[-1:], mkt_act_buy.iloc[-1:]

# (作者注) 这一次，笔者在计算主卖概率的时候，相对于[主买成交特异性，用分钟数据强行构造主买数据，能行吗？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247495622&idx=1&sn=53bc4a83c3269657abcfcff21f50a56f&scene=21#wechat_redirect)进行了优化。整个思路是一致的，只不过对收盘价最高价和最低价相等的情况进行了特殊处理。
#
# (作者注) 第3-5行，是为了防止收盘价高于最高价或者低于最低价的情况。
#
# (作者注) 因为笔者发现有一条数据是这样的。第3-4行，就是为了防止这种类似无穷大的情况。
#
# (作者注) 对于这种情况，最高价=最低价的情况，用分钟收益率来辅助判断，分钟收益率大于0，全为主买，否则全为主卖。代码6-8行，实现的就是这个功能。
#
# (作者注) 第9行，计算每个标的每分钟的主卖成交额。
#
# (作者注) 第10行，计算市场每分钟主卖成交额。
#
# (作者注) 第11-16行，就是针对1分钟k线和5分钟k线的不同处理了。

# --- 代码块 3 ---
@staticmethod
def cal_resi(data):
    data = data.dropna()
    lr = LinearRegression()
    lr.fit(data.iloc[:, :1], data.iloc[:, 1:])
    resi = data.iloc[:, 1:] - lr.predict(data.iloc[:, :1])
    resi.columns = ['net_siphon']
    return resi

# (作者注) 回归这个没有什么需要特殊说明的了，就贴一个代码了。

