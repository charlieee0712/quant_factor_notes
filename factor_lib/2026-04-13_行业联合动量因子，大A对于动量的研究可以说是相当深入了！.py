"""行业联合动量因子，大A对于动量的研究可以说是相当深入了！

自动生成自 ../sources/general/articles/2026-04-13_行业联合动量因子，大A对于动量的研究可以说是相当深入了！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-04-13_行业联合动量因子，大A对于动量的研究可以说是相当深入了！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 行业联合动量因子，大A对于动量的研究可以说是相当深入了！
# 日期    : 2026-04-13
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247496118&idx=1&sn=2ddda432aa017bc60be3da0204cdbbe4
# 本地原文: ../sources/general/articles/2026-04-13_行业联合动量因子，大A对于动量的研究可以说是相当深入了！.md
# 本地图片: ../sources/general/articles/images/2026-04-13_行业联合动量因子，大A对于动量的研究可以说是相当深入了！/  (共 22 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **行业联合动量**
#
# 本文，笔者将复现国信证券张欣慰和刘璐两位老师在2024年1月9日发布的研报《金融工程专题研究：个股与行业的共振——联合动量因子》。
#
# 这篇研报和传统动量（反转）因子最大的区别在于，它考虑了行业的信息。用研报中的原文来说，那就是：
#
# > 在构建动量因子时，以往的研究主要注重挖掘个股本身的趋势和形态，即个股的“小势”，缺乏对个股背后行业、板块以及市场趋势的关注，个股背后的“大势”也同样重要，不同的行业、市场驱动力可能对应着后续完全不同的走势。
#
# 所以，这篇研报，是从行业角度来计算动量因子的。
#
# 值得一提的是，Barra CNE6模型中也有行业动量，但是这个因子考虑行业信息的方式很特别。
#
# **计算步骤和代码**
#
# 关于行业联动动量，研报中一共提出了五个因子，分别是ICM、VICM、ICR、VICR和CMC。
#
# 笔者将通过文字和代码两种方式，来给各位大佬介绍一下这五个因子。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，对标的过去21个交易的收益率排序，取最大的5个交易日，对应ICM因子；若取最小的15个交易日则对应ICR因子。因为，
#
# 第二步，对这取出来的这些交易日的行业收益率进行加权求和就得到了最终的因子，权重为：
#
# 注意：这个权重没有归一化。
#
# 如果，在第一步排序的时候，使用的是成交量和收益率的乘积，那么就得到了VICM和VICR这两个因子。至于，CMC因子，则是VICM-VICR得到的。不过，笔者在代码中修改了一下，VCMC是VICM-VICR，CMC是ICM-ICR。
#
# 关于行业收益率，研报中使用的是中信一级行业指数，而笔者使用的是申万一级行业所有标的的收益率按市值加权。等权笔者也尝试了一下，效果不行。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# ICM、ICR、VICM、VICR这四个因子之间的相关性还是比较低的。
#
# 对于这些因子，笔者想说，乘上了volume之后的三个因子都不太行。不乘volume的因子，ICM确实表现出了动量的特性，IC为正；而ICR确实表现出了反转的特性，IC为负。
#
# 从IC绝对值的角度来看，ICM这个因子的表现要好那么一点点，所以因子评价将以它为主。
#
# 因为，这个因子本身就是用低频数据计算的，所以不需要再进行一次低频化了。
#
# ## IC分析
# 这个IC的表现说实话，其实也挺一般的，最高的一年也才勉强超过了0.07。
#
# ## 收益分析
# 这个分层回测的结果应该算是比较差了。
#
# 接下来，看看ICR这个因子的分层回测结果。
#
# 为什么笔者复现的结果比较一般呢？可能有以下两个原因。
#
# 第一，笔者是对全市场所有标的进行测试的，没有去掉st。
#
# 第二，行业收益率的计算，特别是当行业中有标的停牌的时候，笔者的处理和直接使用行业指数肯定是存在差距的。
#
# 即使是两者相减，效果也不是很好。
#
# 同时，考虑到两个因子值的数量级存在差异，笔者用截面排名相减，结果也比较一般，但是比直接相减强了那么一点。
#
# 好了，又到了求赞求关注求推荐求分享的时刻了，希望各位大佬能多多支持，您每动一次金手，对笔者来说都是莫大的鼓励。
#

# ============================================================
# 本地图片清单（共 22 张）
# ============================================================
# 001.png  <-  计算步骤
# 002.png  <-  代码
# 003.png  <-  因子评价
# 004.png  <-  IC分析
# 005.png  <-  IC分析
# 006.png  <-  IC分析
# 007.png  <-  IC分析
# 008.png  <-  IC分析
# 009.png  <-  IC分析
# 010.png  <-  回归分析
# 011.png  <-  回归分析
# 012.png  <-  换手率分析
# 013.png  <-  换手率分析
# 014.png  <-  收益分析
# 015.png  <-  收益分析
# 016.png  <-  收益分析
# 017.png  <-  收益分析
# 018.png  <-  收益分析
# 019.png  <-  收益分析
# 020.png  <-  收益分析
# 021.png  <-  收益分析
# 022.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 6 个代码块）
# ============================================================

# --- 代码块 1 ---
def __init__(self):
    self.ind_data = self.market_cap = self.rtn = self.vol = None
    self.sector_rtn = None
    self.w_5 = np.array([0.5, 0.59, 0.7, 0.84, 1])
    self.w_15 = np.array([2 ** (-(i-1)/14) for i in range(1, 16)])

# (作者注) 第一段代码，初始化一些属性。其中，最主要的是两个权重，一个是5天的权重，另一个则是15天的权重。
#
# (作者注) 可以看到，这两个权重的顺序是相反的。这样处理的话，在后续计算因子的时候，只需要升序排列一次即可。

# --- 代码块 2 ---
def __call__(self):
    self.ind_data = BaseDataLoader.load_data('../../data/stock/sw_industry.parquet', fields=['sw_l1_code']
                                             ).to_dataframe('sw_l1_code')
    start = self.ind_data.index.tolist()[0]
    codes = self.ind_data.columns.tolist()
    data = BaseDataLoader.load_data('../../data/stock/stock_bar_1day.parquet', fields=['close', 'volume', 'factor'],
                                    codes=codes, start=start, lag=4).to_dataframes()
    self.rtn = (data['close'] * data['factor']).pct_change().iloc[1:]
    self.vol = data['volume'].iloc[1:]
    self.rtn = self.rtn * np.where(self.vol != 0, 1.0, np.nan)
    self.market_cap = BaseDataLoader.load_data('../../data/stock/capital.parquet', fields=['market_cap'], codes=codes,
                                               start=start).to_dataframe('market_cap')
    res = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_factors)(idx)
        for idx in range(20, len(self.ind_data)+1)
    )
    res = pd.concat(res)
    res.index.name = 'code'
    res.reset_index(inplace=True)
    res.to_parquet('./ind_mom.parquet')

# (作者注) 第二段代码，主要是读取数据，然后调用cal\_factors方法计算因子。这段代码复用了[基于日常收益的注意力溢出，一个IC和分层回测俱佳的因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490377&idx=1&sn=9278ded584d008824cb74e206f2a7cfd&scene=21#wechat_redirect)这篇文章中的代码。

# --- 代码块 3 ---
def cal_factors(self, idx):
    day = self.ind_data.iloc[[idx-1]].index.tolist()[0]
    ind_data = self.ind_data.iloc[idx-1:idx].T
    ind_data.columns = ['ind']
    res = ind_data.groupby('ind', as_index=False, group_keys=False).apply(self.cal_factors_by_ind, idx)
    res['datetime'] = day
    res['vcmc'] = res['vicm'] - res['vicr']
    res['cmc'] = res['icm'] - res['icr']
    return res

# (作者注) 第三段代码，对行业进行聚合，然后调用cal\_factors\_by\_ind来计算因子。

# --- 代码块 4 ---
def cal_factors_by_ind(self, group, idx):
    codes = group.index.tolist()
    rtn = self.rtn.iloc[idx-20:idx][codes]
    weights = self.market_cap.iloc[idx-20:idx][codes]
    weights = weights / weights.sum(axis=1).values.reshape(-1, 1)
    self.sector_rtn = (rtn * weights).sum(axis=1)
    vol = self.rtn.iloc[idx-20:idx][codes]
    res = []
    for i in range(len(codes)):
        res_rtn = self.cal_factors_by_code(rtn.iloc[:, i])
        res_vol_rtn = self.cal_factors_by_code(rtn.iloc[:, i] * vol.iloc[:, i])
        res .append(res_rtn + res_vol_rtn)
    res = pd.DataFrame(res, index=codes, columns=['icm', 'icr', 'vicm', 'vicr'])
    return res

# (作者注) 第2行，获取当前行业的所有标的代码。
#
# (作者注) 第3行，读取这些标的过去20个交易日的收益率数据。
#
# (作者注) 第4-5行，计算每个标的按市值加权的权重。
#
# (作者注) 第6行，计算行业收益率。
#
# (作者注) 第7行，获取这些标的过去20个交易日的成交量数据。
#
# (作者注) 第8-14行，调用cal\_factors\_by\_code计算每个标的的因子。

# --- 代码块 5 ---
def cal_factors_by_code(self, data):
    data = data.sort_values()
    return [self.__cal_factors__(data.iloc[-5:]), self.__cal_factors__(data.iloc[:15], reverse=True)]

# (作者注) 第2行，对标的日收益率从小到大进行排序。
#
# (作者注) 第3行，调用\_\_cal\_factors\_\_分别计算ICM（VICM）和ICR（VICR）。

# --- 代码块 6 ---
def __cal_factors__(self, data, reverse=False):
    idx = data.index.tolist()
    sector_rtn = self.sector_rtn.loc[idx]
    if reverse:
        z = sector_rtn * self.w_15
    else:
        z = sector_rtn * self.w_5
    return np.sum(z)

# (作者注) 第2行，获取交易日索引信息。
#
# (作者注) 第3行，获取对应交易日的行业收益率数据。
#
# (作者注) 第4-5行，计算ICR或VICR因子，此时sector\_rtn中的第一个值对应的是最小值，所以权重为1。
#
# (作者注) 第5-7行，计算ICM或VICM因子，此时sector\_rtn中最后一个值对应的是最大值，其权重也为1。

