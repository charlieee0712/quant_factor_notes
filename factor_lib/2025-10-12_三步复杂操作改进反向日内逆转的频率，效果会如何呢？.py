"""三步复杂操作改进反向日内逆转的频率，效果会如何呢？

自动生成自 ../sources/general/articles/2025-10-12_三步复杂操作改进反向日内逆转的频率，效果会如何呢？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-10-12_三步复杂操作改进反向日内逆转的频率，效果会如何呢？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 三步复杂操作改进反向日内逆转的频率，效果会如何呢？
# 日期    : 2025-10-12
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490582&idx=1&sn=9d775630d6ef9f9b493237a93d7ae79e
# 本地原文: ../sources/general/articles/2025-10-12_三步复杂操作改进反向日内逆转的频率，效果会如何呢？.md
# 本地图片: ../sources/general/articles/images/2025-10-12_三步复杂操作改进反向日内逆转的频率，效果会如何呢？/  (共 12 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **点击蓝字 关注我们**
#
# 本文复现的因子来自于一篇研报，但是不知道是因子本身不行，还是笔者复现的时候出现了误差，导致这个因子的效果非常差，甚至可以说是非常一般。
#
# 在这篇研报中，一共提出了三种改进的方式。
#
# 第一种，修改隔夜收益的计算方式。老外的论文中，隔夜收益是用今日开盘价/昨日收盘价-1得到的，日内收益率是用今日收盘价/今日开盘价-1计算的。在这篇研报中，用每日10点的价格来替换了今日开盘价。
#
# 第二种，计算满足第一种改进方式下的日内成交量占比（每日10点之后的成交量之和除以当日的总成交量）和隔夜日内力量差（隔夜收益率-日内收益率）的相关性。
#
# 第三种，进一步修改第一种改进方式中的条件，改为隔夜收益率大于0且隔夜日内力量差大于0。
#
# 从研报的结果来看，第三种方式改进之后的结果是最好的。所以，笔者也只展现一下第三种改进方式得到的结果。
#
# 代码

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 总结
# 这个因子改进之后的效果真的是不尽如人意。它和笔者昨天在分钟级别的数据上改进的因子相比，真的差了太多了。但是，和原始因子相比的话，它又稍微好了那么一点点。
#
# 当然，也有可能是笔者的水平有限，没有复现到这个因子的精髓。
#
# 虽然，这个因子的效果并不是太好，但是它给我们提供了一种全新的思路，用每日10点的价格来代替开盘价来计算因子，值得学习。
#
# 感谢大家的支持，希望大家多多点赞关注分享和喜欢。笔者也会继续扩展自己的能力，为大家提供更多的优质文章。
#

# ============================================================
# 本地图片清单（共 12 张）
# ============================================================
# 001.jpg  <-  点击蓝字 关注我们
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

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close', 'volume'])
    close = data.to_dataframe('close').iloc[0]
    vol = data.to_dataframe('volume')
    vol = vol.iloc[1:].sum() / vol.sum()
    res = pd.concat([close, vol], axis=1)
    res.columns = ['close', 'ivr']
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 这个因子的计算需要用到日频数据和分钟级别的数据，所以代码分为两段。
#
# (作者注) 第一段代码是处理分钟级别数据的，这里用的是30分钟的k线数据。
#
# (作者注) 第6行代码，取10点中的收盘价数据。
#
# (作者注) 第7-8行，计算日内成交量占比。

# --- 代码块 2 ---
def __call__(self):
    res = self.run()
    res = pd.concat(res)
    res.index.name = 'code'
    res.reset_index(inplace=True)

    res = BaseDataLoader.from_dataframe(res)
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close']).to_dataframe('close')
    data = data.reindex(res.trade_days)
    res = res.to_dataframes()
    gap = res['close'] / data.shift(1) - 1
    rtn = data / data.shift(1) - 1

    oid = (gap - rtn)
    flag = np.where((gap > 0) * (oid > 0), 1, np.nan)
    oid = oid * flag
    ivr = res['ivr'].reindex(columns=oid.columns.tolist()) * flag

    factor = Parallel(n_jobs=16, verbose=10, backend="loky")(
        delayed(ts_corr)(ivr.iloc[idx-21:idx], oid.iloc[idx-21:idx])
        for idx in range(21, len(oid))
    )
    factor = pd.concat(factor, axis=1).T
    factor.index.name = 'datetime'
    factor = pd.melt(factor.reset_index(), id_vars='datetime', var_name='code', value_name='reverse_prob')
    factor.to_parquet('./reverse_prob.parquet')

# (作者注) 第二段代码，前5行是调用第一段代码，获取日内成交量占比和每日10点的收盘价。
#
# (作者注) 第7行，调用BaseDataLoader类的from\_dataframe方法将dataframe转换为BaseDataLoader数据类。关于这个类的具体内容，大家可以查看[基础数据类BaseDataLoader](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247484608&idx=1&sn=0084065053710f0791b0c1741712b6ad&scene=21#wechat_redirect)这篇文章。
#
# (作者注) 第8行，读取日频的收盘价数据。
#
# (作者注) 第9行，将两个数据的时间进行对齐。
#
# (作者注) 第11行，计算隔夜收益。
#
# (作者注) 第12行，计算日内收益。
#
# (作者注) 第14行，计算隔夜日内力量差。
#
# (作者注) 第15行，计算满足条件的交易日。
#
# (作者注) 第19-22行，计算隔夜日内力量差和日内成交量占比的相关性。

