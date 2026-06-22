"""筹码分布因子，IC不高，但是分层结果相当出色！

自动生成自 ../sources/chenshengrui/articles/2026-05-19_筹码分布因子，IC不高，但是分层结果相当出色！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/chenshengrui/articles/images/2026-05-19_筹码分布因子，IC不高，但是分层结果相当出色！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: chenshengrui
# 公众号  : 量化拯救散户
# 标题    : 筹码分布因子，IC不高，但是分层结果相当出色！
# 日期    : 2026-05-19
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247496768&idx=1&sn=8f1818c558b626bd6d89ffacb6b8d73f
# 本地原文: ../sources/chenshengrui/articles/2026-05-19_筹码分布因子，IC不高，但是分层结果相当出色！.md
# 本地图片: ../sources/chenshengrui/articles/images/2026-05-19_筹码分布因子，IC不高，但是分层结果相当出色！/  (共 18 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:28

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **筹码分布因子**
#
# 本文，笔者将复现中信建投陈升锐和姚紫薇两位老师在2025年8月25日发布的研报《筹码分布因子系统构建》。
#
# 这篇研报中的因子一共有四个主题，分别是筹码分布、筹码集中度、筹码换手和筹码盈利。
#
# 本文，先来看看筹码分布下的因子，一共有七个，分别是标准差、偏度、峰度、变异系数、相对价位、成本带宽和成本重心。但是，这篇文章笔者将先介绍前面四个。
#
# 原因也很简单，因为后面三个在计算的时候算错了。
#
# **计算步骤和代码**
#
# 这个因子的计算关键就在于筹码分布。
#
# 笔者在写代码的时候，没有想到什么好的加速方法，所以这个因子从2017年11月开始到2026年3月底这段时间的计算就耗费了8个多小时。
#
# **1**
#
# **筹码分布的计算**
#
# 这里就直接截图了，因为笔者太懒了。
#
# 需要注意的是，第一天计算的时候，没有t-1日的筹码分布时该怎么办？
#
# 笔者能想到的是两种。
#
# 第一种，直接用当日的成交量。
#
# 第二种，假设前一日的筹码分布全是0。
#
# 在实现的时候，笔者选择了第二种方式，但是直观上感觉第一种方式应该是更好的。但是，由于笔者的回测是从2018年开始的，所以这个影响并不是太大。
#
# **2**
#
# **因子计算公式**
#
# 这里看起来是有8个因子，但是第一个筹码加权平均成本是用来计算后面的因子的，它自己并不是一个因子。
#
# 因为，用它做因子的话，茅台的因子值始终是最大的那一组的，这显然是不合理的。
#
# 至于后面三个为什么没在这篇文章中介绍，是因为笔者在计算的时候把chip\_higest理解为筹码最多的价格，实际上是有筹码的价格中的最大值。
#
# **3**
#
# **代码**

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
# ## 因子评价
# 在这次介绍的四个因子中，研报的数据显示偏度因子的表现是最好的。同时，笔者测试的结果和研报一致，所以这里就仅展示偏度因子的因子评价结果了。
#
# 至于偏度因子，如果用均值进行低频化的话，其IC表现比较一般，但是分层回测的结果看起来不错；而用标准差低频化的因子则在IC上表现更好。
#
# 纠结再三，笔者还是选择展示用均值低频化的因子评价结果。
#
# ## IC分析
# 这个IC表现确实不行，如果用标准差低频化的话，其IC累加能达到-6。
#
# ## 收益分析
# 这个分层回测看起来还行。在整个回测区间里，其年化收益率的单调性是完美的，因子值越小的组年化收益率越高。
#
# 至于用标准差低频化后的分层回测结果，其因子值最大的一组遥遥落后其他四组，而其他四组可以说是你中有我我中有你，无法区分。
#
# ## 总结
# 关于筹码分布偏度因子的介绍到这里就结束了。
#
# 相对价位、成本带宽和成本重心这三个因子如果表现还不错的话，笔者会再开一篇文章介绍一下它们的因子评价结果。
#
# 如果您感兴趣的话，麻烦动动金手点赞关注推荐和分享支持一下笔者。
#
# 从研报的结果来看，成本带宽这个因子的IC应该是这7个因子里面最高的，所以还是值得期待的。
#

# ============================================================
# 本地图片清单（共 18 张）
# ============================================================
# 001.png  <-  筹码分布的计算
# 002.png  <-  因子计算公式
# 003.png  <-  因子计算公式
# 004.png  <-  代码
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
# 017.png  <-  总结

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def __init__(self, file_pth, name, need_last_close, gap=100, parallel="threading"):
    super().__init__(file_pth, name, need_last_close, gap, parallel)
    self.last_chip = {}
    self.turnover_ratio = BaseDataLoader.load_data('../../data/stock/capital.parquet',
                                                   fields=['turnover_ratio']).to_dataframe()
    self.factor = BaseDataLoader.load_data('../../data/stock/stock_bar_1day.parquet',
                                                   fields=['factor']).to_dataframe()

# (作者注) 首先，读取换手率和复权因子的数据。在笔者的数据中，是后复权因子。同时，还用一个字典last\_chip来保存上一时刻各个标的的筹码分布。
#
# (作者注) 后复权，就是保持开始的时候的价格不变，改变后面的价格。
#
# (作者注) 前复权，则是保持当前价格不变，改变之前的价格。
#
# (作者注) 理解了这个原理，就很容易将后复权转换为前复权了。后面的代码将会对此详细说明。

# --- 代码块 2 ---
def process_single_day(self, idx):
    if idx < 243 or idx >= 5098:
        return
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['volume', 'close'])
    codes = data.codes
    tr = (self.turnover_ratio.iloc[idx-243]).reindex(codes)
    factor = (self.factor.iloc[idx-243]).reindex(codes)
    data = data.to_dataframes()
    res = Parallel(n_jobs=-1, verbose=10, backend="threading")(
        delayed(self.cal_factors)(codes[i],data['close'].iloc[:, i], data['volume'].iloc[:, i],
                                  factor.iloc[i], tr.iloc[i] / 100)
        for i in range(len(codes))
    )
    res = pd.DataFrame(res, index=codes, columns=['mean', 'std', 'skew', 'kurt', 'cv', 'ckdp', 'cbw', 'ckdw'])
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    res.reset_index(inplace=True)
    self.save(res)

# (作者注) 这段代码主要是读取数据，然后调用cal\_factors方法，为每个标的计算因子。感觉并不需要太多的介绍了。

# --- 代码块 3 ---
def cal_factors(self, code, close, volume, factor, tr):
    data = pd.concat([close, volume], axis=1)
    data.columns = ['close', 'volume']
    data = data.groupby('close', as_index=False, group_keys=False).sum()
    last_data = self.last_chip.get(code, None)
    if last_data is None:
        data.iloc[:, -1] *= tr
    else:
        last_data['close'] /= factor
        data = data.merge(last_data, how='outer', on=['close'])
        data = data.fillna(0)
        data['volume'] = data.iloc[:, -1] * (1 - tr) + data.iloc[:, -2] * tr
        data = data[['close', 'volume']]
    chip_high = data['close'].iloc[data['volume'].argmax()]
    chip_low = data['close'].iloc[data['volume'].argmin()]
    diff = chip_high - chip_low
    close = close.iloc[-1]
    def weighted_central_moment(x, w, k, mean):
        """计算k阶加权中心矩"""
        return np.average((x - mean) ** k, weights=w)
    weight = data['volume'] / data['volume'].sum()
    mean = np.average(data['close'], weights=weight)
    std = np.sqrt(weighted_central_moment(data['close'], weight, 2, mean))
    x = (data['close'] - mean) / std
    skew = weighted_central_moment(x, weight, 3, 0)
    kurt = weighted_central_moment(x, weight, 4, 0)
    data.iloc[:, 0] *= factor
    self.last_chip[code] = data.copy()
    return (mean, std, skew, kurt, std / mean, (close - mean) / diff, chip_high / chip_low - 1,
            (mean - chip_low) / diff)

# (作者注) 这部分代码可以分为两块。
#
# (作者注) 第一块，前13行，计算筹码分布。
#
# (作者注) 第2-3行，数据拼接，并重命名列。
#
# (作者注) 第4行，将收盘价相同的成交量求和。
#
# (作者注) 第5行，获取上一个交易日的筹码。
#
# (作者注) 第6-7行，没有上一个交易日的筹码数据时的计算。
#
# (作者注) 第8-13行，有上一个交易日的筹码数据时的计算。这里需要注意的是第9行，通过除以当前时刻的后复权因子，将价格转换成了前复权的价格。（所以也就第27-28行，对价格乘以当前的复权因子，再次变成后复权的价格）
#
# (作者注) 第二块，14行之后，计算因子值。
#
# (作者注) 14-16行，其实是错了的，应该直接获取最低价和最高价就行了。笔者想复杂了。
#
# (作者注) 第18-20行，是一个用来计算加权偏度、峰度和标准差的函数。
#
# (作者注) 第21行，计算权重。
#
# (作者注) 第22行，计算加权均价。
#
# (作者注) 第23行，计算标准差。
#
# (作者注) 第24-26行，计算峰度和偏度。

