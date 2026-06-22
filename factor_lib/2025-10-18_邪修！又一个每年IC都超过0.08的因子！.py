"""邪修！又一个每年IC都超过0.08的因子！

自动生成自 ../sources/general/articles/2025-10-18_邪修！又一个每年IC都超过0.08的因子！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-10-18_邪修！又一个每年IC都超过0.08的因子！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 邪修！又一个每年IC都超过0.08的因子！
# 日期    : 2025-10-18
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490823&idx=1&sn=c05fc7c23f5f6dc4a01deca726eb8d56
# 本地原文: ../sources/general/articles/2025-10-18_邪修！又一个每年IC都超过0.08的因子！.md
# 本地图片: ../sources/general/articles/images/2025-10-18_邪修！又一个每年IC都超过0.08的因子！/  (共 14 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文，笔者将继续邪修。邪修的方式也很简单，就是将两篇研报中的因子进行了简单的结合。
#
# 第一篇研报是曹春晓老师早期的研报，介绍了一个叫做时间网络相对中心度的因子，笔者在[时间网络相对中心度，一个简单却还算有效的因子](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489222&idx=1&sn=0d6134ce3c876599fb4634dcee95f9c4&scene=21#wechat_redirect)这篇文章中复现了这个因子。
#
# 由于这个因子的计算用到了zscore标准化后的收益率，只不过这个收益率是在整个截面上做的。笔者参考了中信证券2024年研报《投资者有限关注及注意力捕捉与溢出》中的处理方式，将标的按照行业和市值进行分类，然后在每一个类中计算zscore标准化后的收益率。具体操作方式可以参考[基于日常收益的注意力溢出，一个IC和分层回测俱佳的因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490377&idx=1&sn=9278ded584d008824cb74e206f2a7cfd&scene=21#wechat_redirect)这篇文章。
#
# **因子计算步骤和代码**
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，对截面上所有标的按照行业分类，这里的行业笔者使用的是申万一级行业。
#
# 第二步，对每个行业内的标的，按照市值分为大（最大的30%）、中（中间的40%）和小（最小的30%）三类。
#
# 第三步，对每个标的在其所在的行业和市值类别中，对收益率进行zscore标准化。
#
# 第四步，计算标准化后的收益率的平方，并取过去21个交易日的均值。
#
# 第五步，取第四步得到的因子值的倒数。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 接下来，就到了激动人心的因子评价时刻了。
#
# 由于这个因子在计算过程中已经用到了过去21个交易日的信息了，所以不需要再计算一次21个交易日的均值或者标准差来合成月度因子了。
#
# 从因子评价结果来看，经过这一系列复杂的操作之后，这个因子的IC值有所提升，分层回测的结果也更好了。
#
# 需要注意的是，这次的整个因子评价是考虑了复权系数的。
#
# ## 收益分析
# 如果不乘上复权因子的话，那么这个因子的分层回测曲线是下面这样的。
#

# ============================================================
# 本地图片清单（共 14 张）
# ============================================================
# 001.png  <-  代码
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
# 014.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def __call__(self):
    self.ind_data = BaseDataLoader.load_data('../../data/sw_industry.parquet', fields=['sw_l1_code']
                                            ).to_dataframe('sw_l1_code')
    start = self.ind_data.index.tolist()[0]
    codes = self.ind_data.columns.tolist()
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close'],
                                    codes=codes, start=start, lag=31).to_dataframe('close')
    self.ret = data.pct_change()
    self.market_cap = BaseDataLoader.load_data('../../data/capital.parquet', fields=['market_cap'], codes=codes,
                                               start=start).to_dataframe('market_cap')
    self.ret = self.ret.reindex(self.ind_data.index.tolist())
    res = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_factors)(idx)
        for idx in range(len(self.ret))
    )
    res = pd.concat(res, axis=1).T
    res = np.square(res)
    res = 1 / res.rolling(21).mean()
    dfs = {'tcc': res}
    df = dfs_to_df(dfs)
    df.to_parquet('./new_tcc.parquet')

# (作者注) 第一段代码，主要是读取数据，然后调用cal\_factors方法来实现第一步到第三步的计算。
#
# (作者注) 第2行代码，读取行业数据。因为笔者的行业数据是从2010年开始的，所以先读取行业数据，然后第3-4行获取行业数据的开始时间和标的信息。这样，后续读取行情和市值数据的时候可以传入start和codes两个参数。
#
# (作者注) 第6-10行，读取市值数据和行情数据，并计算了收益率。
#
# (作者注) 第12行，因为笔者的行情数据更新快于行业数据，所以行情数据多了几天，这里用reindex实现了时间的对齐。
#
# (作者注) 第12-15行，并行调用cal\_factors方法实现前三步的计算。
#
# (作者注) 第17-18行，对应计算步骤的第四步和第五步。
#
# (作者注) 剩下的代码就是保存数据了。

# --- 代码块 2 ---
def cal_factors(self, idx):
    day = self.ind_data.iloc[[idx]].index.tolist()[0]
    df = pd.concat([self.ret.iloc[idx], self.ind_data.iloc[idx], self.market_cap.iloc[idx]], axis=1)
    df.columns = ['ret', 'ind', 'cap']
    new_series = df.groupby('ind', as_index=False, group_keys=False).apply(self.__cal_factors__)
    new_series.name = day
    return new_series

# (作者注) 第2行代码，获取当前交易日的信息，用来记录因子的计算时间。
#
# (作者注) 第3行代码，将收益率、行业和市值数据拼接为一个dataframe。
#
# (作者注) 第4行，重新命名dataframe的列。
#
# (作者注) 第5行，按照行业groupby之后，调用\_\_cal\_factors\_\_计算因子。

# --- 代码块 3 ---
@staticmethod
def __cal_factors__(group):
    group.sort_values(by='cap', inplace=True)
    start = 0
    res = []
    for q in [0.3, 0.7, 1]:
        end = int(len(group) * q)
        tmp_group = group.iloc[start:end]
        res.append((tmp_group['ret'] - tmp_group['ret'].mean()) / tmp_group['ret'].std())
        start = end
    res = pd.concat(res)
    return res

# (作者注) 第3行，对按照行业聚合后的数据的市值进行排序。
#
# (作者注) 第4-10行，按照市值分为小中大三类分别计算zscore之后的收益率。

