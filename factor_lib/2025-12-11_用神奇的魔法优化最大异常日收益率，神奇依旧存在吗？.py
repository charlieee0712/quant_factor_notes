"""用神奇的魔法优化最大异常日收益率，神奇依旧存在吗？

自动生成自 ../sources/general/articles/2025-12-11_用神奇的魔法优化最大异常日收益率，神奇依旧存在吗？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-12-11_用神奇的魔法优化最大异常日收益率，神奇依旧存在吗？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 用神奇的魔法优化最大异常日收益率，神奇依旧存在吗？
# 日期    : 2025-12-11
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247492651&idx=1&sn=4bd1f29073e4cd9c8708873feed48319
# 本地原文: ../sources/general/articles/2025-12-11_用神奇的魔法优化最大异常日收益率，神奇依旧存在吗？.md
# 本地图片: ../sources/general/articles/images/2025-12-11_用神奇的魔法优化最大异常日收益率，神奇依旧存在吗？/  (共 17 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **最大异常日收益率**
#
# 最大异常日收益率这个因子，笔者在2025年7月26日发布的这篇[最大异常日收益率，一个超级简单，却还算有效的因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489654&idx=1&sn=52d03fdfb5f895a7e657d8bf0ae358b5&scene=21#wechat_redirect)文章中介绍过。
#
# 当时的这个因子，IC还是挺高的，但是分层回测看起来差了那么一点点的。
#
# 最近，笔者在可转债上面又复现了一下这个因子的思想，[转债量化（四）：最大异常收益率，在可转债上也会表现出高IC吗？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247492518&idx=1&sn=5adc31d74856bb475e78ee020a91f063&scene=21#wechat_redirect)，结果不尽如人意。
#
# 但是，在复现完之后，笔者想到了一个神奇的魔法，就是用行业和市值对标的进行分组之后重新计算市场收益率。具体的思想在[基于日常收益的注意力溢出，一个IC和分层回测俱佳的因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490377&idx=1&sn=9278ded584d008824cb74e206f2a7cfd&scene=21#wechat_redirect)和[用行业和市值计算的注意力溢出，相比注意力的提升居然在这里！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490403&idx=1&sn=9d6ec36fa55f57c474f5f636c562b920&scene=21#wechat_redirect)这两篇文章中有介绍。
#
# 除了可以在计算市场收益的时候使用这种方法，还可以在计算完因子之后使用这种方法。于是，因子数量从1变成了4。
#
# 第一种，传统的最大异常日收益率，将其记为abnormal\_rtn。
#
# 第二种，用行业和市值分组后得到的市场收益率，计算的最大异常日收益率，将其记为group\_abnormal\_rtn。
#
# 第三种，用行业和市值处理abnormal\_rtn因子，用abnormal\_rtn\_attn来表示。
#
# 第四种，用行业和市值处理group\_abnormal\_rtn因子，用group\_abnormal\_rtn\_attn来表示。
#
# **计算思想和代码**
#
# 这样一来，因子的计算就比较复杂了，笔者将尝试一下，看看文字能否将这一系列因子描述清楚。这对于一个从小语文就不好的人来说，是一个不小的挑战。
#
# 不过，即使描述不清楚，也没有关系，因为后面我们有代码。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，获取因子值。如果是group\_abnormal\_rtn，这里的因子值就是最大异常日收益率。如果是第三种和第四种，那么对应的因子值便是abnormal\_rtn和group\_abnormal\_rtn。
#
# 第二步，将每日的因子值和每日的市值数据、行业数据拼接为一个dataframe。
#
# 第三步，按照行业groupby，然后对同行业按照市值分为大、中和小三类，每一类分别计算因子值的均值，然后用标的的因子值减去这个均值。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 从相关性来看，前四个因子属于一类，后两个因子属于另一类。
#
# 由于这系列因子在计算的时候，已经考虑过过去21个交易日的信息了，所以不需要额外的操作来合成“月度因子”了。
#
# 后两个因子的IC表现远不如前四个，分层回测也差了很多，所以就当它们是一次失败的尝试了。
#
# 前四个因子，从IC上来看，表现最好的是group\_abnormal\_rtn\_attn，这个因子在整个回测区间里每一年的IC绝对值都超过了0.08。
#
# 但是，笔者想展示的确是abnormal\_rtn\_attn，因为它的提升达到了笔者想要的效果。
#
# ## 收益分析
# 只看这个分层回测结果，肯定会有人说，它依旧不是很好。
#
# 但是，当你看了abnormal\_rtn的分层回测结果之后，你就会发现这个神奇的魔法真的有它的神奇之处。
#
# 这个图和之前的图不太一样，因为之前的因子计算和分层回测都没有考虑复权因子。
#
# 好了，本文到这里也就结束了。
#
# 最后，按照惯例，求一波点赞分享推荐和关注，谢谢各位大佬了。
#

# ============================================================
# 本地图片清单（共 17 张）
# ============================================================
# 001.png  <-  (文章开头)
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
# 017.png  <-  - *END* -

# ============================================================
# 作者代码（按原文出现顺序，共 4 个代码块）
# ============================================================

# --- 代码块 1 ---
def __call__(self):
    self.ind_data = BaseDataLoader.load_data('../../data/sw_industry.parquet', fields=['sw_l1_code']
                                        ).to_dataframe('sw_l1_code')
    start = self.ind_data.index.tolist()[0]
    codes = self.ind_data.columns.tolist()
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close', 'factor'],
                                    codes=codes, start=start, lag=4).to_dataframes()
    self.rtn = (data['close'] * data['factor']).pct_change().iloc[1:]
    self.market_cap = BaseDataLoader.load_data('../../data/capital.parquet', fields=['market_cap'], codes=codes,
                                          start=start).to_dataframe('market_cap')
    res = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_factors)(idx)
        for idx in range(len(self.ind_data))
    )
    res = pd.concat(res, axis=1).T
    res.index.name = 'datetime'
    res = res.rolling(21).max()
    res = pd.melt(res.reset_index(), id_vars='datetime', var_name='code', value_name='group_abnormal_rtn_attn')
    res.to_parquet('./group_abnormal_rtn.parquet')

# (作者注) 可以说，每一步对应一个函数。
#
# (作者注) 第一个函数，主要是获取数据，然后调用cal\_factors函数（低11-14行）完成每日因子的计算，最后将其拼接为一个dataframe。
#
# (作者注) 这里展示的是第二种因子的计算代码，如果是第三种或第四章的话，需要注释掉第17行，然后将6-8行替换为如下内容。

# --- 代码块 2 ---
data = BaseDataLoader.load_data('./all.parquet', fields=['group_abnormal_rtn'],
                                codes=codes, start=start).to_dataframes()
self.rtn = data['group_abnormal_rtn']

# (作者注) 接着，咱们来看看cal\_factors这个函数。

# --- 代码块 3 ---
def cal_factors(self, idx):
    day = self.ind_data.iloc[[idx]].index.tolist()[0]
    df = pd.concat([self.rtn.iloc[idx], self.ind_data.iloc[idx], self.market_cap.iloc[idx]], axis=1)
    df.columns = ['rtn', 'ind', 'cap']
    new_series = df.groupby('ind', as_index=False, group_keys=False).apply(self.__cal_factors__)
    new_series.name = day
    return new_series

# (作者注) 这个函数对同一个交易日的因子、行业和市值数据进行拼接，然后调用\_\_cal\_factors\_\_方法（第7行）计算因子。
#
# (作者注) 这一部分内容，对后三种因子的计算都适用。
#
# (作者注) @staticmethod

# --- 代码块 4 ---
def __cal_factors__(group):
    group.sort_values(by='cap', inplace=True)
    start = 0
    res = []
    for q in [0.3, 0.7, 1]:
        end = int(len(group) * q)
        tmp_group = group.iloc[start:end]
        res.append(np.abs(tmp_group['rtn'] - tmp_group['rtn'].mean()))
        start = end
    res = pd.concat(res)
    return res

# (作者注) 最后一个函数，就是最终因子值的计算了。
#
# (作者注) 这里第8行需要改动一下，如果是第三种或第四种因子，这里的绝对值需要去掉。
#
# (作者注) 当然，不去掉也是可以的，那就是另外的因子了，有点类似均值距离化的操作了。写到这里，笔者决定将这两个因子也纳入进来，一共是六个因子，它们就用abnormal\_rtn\_dis和group\_abnormal\_rtn\_dis来表示。

