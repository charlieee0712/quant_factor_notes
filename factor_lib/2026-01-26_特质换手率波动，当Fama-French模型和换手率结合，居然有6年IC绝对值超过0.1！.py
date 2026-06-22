"""特质换手率波动，当Fama-French模型和换手率结合，居然有6年IC绝对值超过0.1！

自动生成自 ../sources/general/articles/2026-01-26_特质换手率波动，当Fama-French模型和换手率结合，居然有6年IC绝对值超过0.1！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-01-26_特质换手率波动，当Fama-French模型和换手率结合，居然有6年IC绝对值超过0.1！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 特质换手率波动，当Fama-French模型和换手率结合，居然有6年IC绝对值超过0.1！
# 日期    : 2026-01-26
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494417&idx=1&sn=1f4e922ded0caf0123a0ca22530013d5
# 本地原文: ../sources/general/articles/2026-01-26_特质换手率波动，当Fama-French模型和换手率结合，居然有6年IC绝对值超过0.1！.md
# 本地图片: ../sources/general/articles/images/2026-01-26_特质换手率波动，当Fama-French模型和换手率结合，居然有6年IC绝对值超过0.1！/  (共 14 张)
# 段落识别: FULL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **特质换手率波动**
#
# 对于特质波动率，大家应该很熟悉了，就是用一个多因子模型对收益率进行回归然后取残差的波动率。这里的多因子模型通常是用两种，CAMP模型或者Fama-French三因子模型，但是实际上任何多因子模型都可以。
#
# 在上周，笔者复现了一个复杂的因子，它也和Fama-French三因子模型有那么一点点关系。具体参考[基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494289&idx=1&sn=ac78d20e2d7ae806dd70c3ecea64ed73&scene=21#wechat_redirect)。不得不说，这个因子很复杂，但是效果比较一般。
#
# 本文，笔者在中银证券2024年发布的研报《价值组合因子》中，发现了一个和Fama-French三因子模型有一点关系的因子，它叫做特质换手波动率。这个因子瞬间吸引了笔者的兴趣，于是便有了此文。
#
# **计算步骤和代码**
#
# 这个因子虽然说和Fama-French三因子模型有一点关系，但是关系不是那么大， 或者说作者的改动很大。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 计算步骤很简单，就是一个时序回归。
#
# 回归的时候以标的t日换手率为被解释变量，t-1日的市场换手率，SMB换手率，HML换手率和MOM换手率为解释变量。
#
# 这里，笔者认为被解释变量和解释变量都可以直接使用t日的。如果因子解释变量使用t-1日的效果远好于t日的话，大概率意味着这个因子是过拟合的。
#
# 市场换手率：全市场换手率的均值。
#
# SMB换手率：对市值排序，用后1/3标的换手率均值-前1/3标的换手率均值。（注意，这里不是30%，实际上应该也是差不多的，如果因子对这一点点参数也敏感的话，大概率也是过拟合的）。
#
# HML换手率：对pb排序（这里也和Fama-French不一样，Fama-French用的是bp），用前1/3的换手率均值-后1/3的换手率均值。
#
# MOM换手率：对过去21个交易日的收益率进行排序，用前1/3的换手率均值-后1/3的换手率均值。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# 在2025年的《因子日历》中，是这样描述的。
#
# 借鉴特质波动率的构建理念，特质换手率波动剥离了市场主流风格（风险因子）对换手率的影响，可以更好的测算市场对错误定价的修正效率。
#

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 这个因子在计算的时候已经考虑了过去21个交易日的数据了，所以它实际上已经可以被认为是一个月度因子了，无需再用过去21个交易日的标准差或者均值来合成了。
#
# ## IC分析
# 这个因子在IC上的表现可以说是非常不错了，疑似有六年的IC绝对值超过了0.1（2020年的IC绝对值感觉超一点点超过0.1）。
#
# ## 收益分析
# 分层回测的结果显示这是一个空头因子，因子值最大的一组收益率远远低于其他四组。
#
# 这个因子有一点惊喜，但也有缺陷，不过它背后的思想应该比因子本身具有更大的价值。作者在写研报的时候为什么要简化Fama-French模型呢？是因为原模型效果不行呢？还是其他的原因呢？
#
# 在复现这个因子之前，笔者想的是如果没有什么价值的话，那这个因子就到这里结束了，如果有价值的话，那么笔者将深入研究一下。目前看来，这个思想是值得深入挖掘的。
#
# 如果您对本文的内容感兴趣，能否点赞关注分享推荐支持一下呢？
#

# ============================================================
# 本地图片清单（共 14 张）
# ============================================================
# 001.png  <-  因子逻辑
# 002.png  <-  IC分析
# 003.png  <-  IC分析
# 004.png  <-  IC分析
# 005.png  <-  IC分析
# 006.png  <-  IC分析
# 007.png  <-  IC分析
# 008.png  <-  回归分析
# 009.png  <-  回归分析
# 010.png  <-  换手率分析
# 011.png  <-  换手率分析
# 012.png  <-  收益分析
# 013.png  <-  收益分析
# 001.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 4 个代码块）
# ============================================================

# --- 代码块 1 ---
def __call__(self):
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close', 'factor'])
    self.codes = data.codes
    data = data.to_dataframes()
    price = data['close'] * data['factor']
    self.mom= price.pct_change(21).iloc[21:]
    self.market_cap = BaseDataLoader.load_data('../../data/capital.parquet',
                                               fields=['market_cap', 'pb_ratio', 'turnover_ratio'],
                                               codes=self.codes, start=self.umd.index.tolist()[0]
                                               ).to_dataframes()
    premium = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_premium)(idx)
        for idx in range(len(self.umd))
    )
    self.premium = pd.concat(premium, axis=1).T
    res = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_resi)(idx)
        for idx in range(3000, len(self.premium) + 1)
    )
    res = pd.concat(res)
    res.reset_index(inplace=True)
    res.to_parquet('./tr_resi_sigma.parquet')

# (作者注) 第一段代码，主要是读取数据，然后调用两个不同的方法分别计算回归过程中的解释变量（cal\_premium）和计算残差波动（cal\_resi）。

# --- 代码块 2 ---
def cal_premium(self, idx):
    day = self.mom.iloc[[idx]].index.tolist()[0]
    df = pd.concat([self.market_cap['turnover_ratio'].iloc[idx], self.mom.iloc[idx],
                    self.market_cap['pb_ratio'].iloc[idx], self.market_cap['market_cap'].iloc[idx]], axis=1)
    df.columns = ['tr', 'umd', 'pb', 'cap']
    data = df.dropna()
    l = len(data) // 3
    res = []
    for key in ['mom', 'pb', 'cap']:
        data.sort_values(by=key, inplace=True)
        tr_30 = data.iloc[:l, 0].mean()
        tr_70 = data.iloc[-l:, 0].mean()
        if key == 'cap':
            res.append(tr_70 - tr_30)
        else:
            res.append(tr_30 - tr_70)
    res.append(df['tr'].mean())
    res = pd.Series(res, index=['tmom', 'thml', 'tsmb', 'mkt'])
    res.name = day
    return res

# (作者注) 第2-6行，拼接数据，并去掉nan值。
#
# (作者注) 第7-16行，计算MOM、SMB和HML三个因子的换手率。
#
# (作者注) 第17行，计算市场换手率。

# --- 代码块 3 ---
def cal_resi(self, idx):
    y = self.market_cap['turnover_ratio'].iloc[idx-21:idx, :]
    x = self.premium.iloc[idx-21:idx, :]
    data = y.join(x)
    day = y.index.tolist()[-1]
    res = []
    for code in self.codes:
        cols = [code] + ['tmom', 'thml', 'tsmb', 'mkt']
        tmp = y[cols].dropna()
        res.append(self.__cal_beta__(tmp))
    res = pd.DataFrame(res, columns=['resi_sigma'], index=self.codes)
    res['datetime'] = day
    return res
@staticmethod
def __cal_resi__(data):
    y = data.iloc[:, 0].values
    if len(y) < 5:
        return np.nan
    x = data.iloc[:, 1:].values
    x = np.c_[np.ones((len(data), 1)), x]
    beta_full = np.linalg.pinv(x.T @ x) @ x.T @ y
    resi = y - beta_full @ x.T
    return np.nanstd(resi)

# (作者注) 这段代码就是将解释变量和被解释变量拼接在一起，然后去掉nan值进行时序回归，并计算残差的波动率。
#
# (作者注) 这段代码是可以优化的，因为所有标的的解释变量都是一样的。因此，对于过去21个交易日的换手率没有nan值的标的可以进行批量计算。
#
# (作者注) 批量计算的代码如下：

# --- 代码块 4 ---
@staticmethod
def __cal_beta__(data):
    y = data.iloc[:, :-4].values
    if len(y) < 5:
        return np.nan
    x = data.iloc[:, -4:].values
    x = np.c_[np.ones((len(data), 1)), x]
    beta_full = np.linalg.pinv(x.T @ x) @ x.T @ y
    resi = y - x @ beta_full
    return np.nanstd(resi, axis=0)

