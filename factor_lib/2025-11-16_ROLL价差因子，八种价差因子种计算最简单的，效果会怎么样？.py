"""ROLL价差因子，八种价差因子种计算最简单的，效果会怎么样？

自动生成自 ../sources/chenshengrui/articles/2025-11-16_ROLL价差因子，八种价差因子种计算最简单的，效果会怎么样？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/chenshengrui/articles/images/2025-11-16_ROLL价差因子，八种价差因子种计算最简单的，效果会怎么样？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: chenshengrui
# 公众号  : 量化拯救散户
# 标题    : ROLL价差因子，八种价差因子种计算最简单的，效果会怎么样？
# 日期    : 2025-11-16
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247491751&idx=1&sn=97d36d3674a00bae3b501117a561ff78
# 本地原文: ../sources/chenshengrui/articles/2025-11-16_ROLL价差因子，八种价差因子种计算最简单的，效果会怎么样？.md
# 本地图片: ../sources/chenshengrui/articles/images/2025-11-16_ROLL价差因子，八种价差因子种计算最简单的，效果会怎么样？/  (共 17 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:28

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **ROLL价差因子**
#
# 这一部分，陈升锐老师提出了4种不同的构造方式，一共能计算8个流动性因子，然后这8个流动性因子除以成交额又得到了八个流动性增强因子，一共16个因子。
#
# 但是，这一次的4种构造方式都很复杂，所以笔者只能一个一个地介绍了。
#
# 本文要复现的构造方式，叫做ROLL价差。
#
# **计算公式和代码**
#
# ROLL价差因子的推导过程在研报中有，所以笔者就不赘述了，这里仅仅展示一下最终的计算公式。
#
# **1**
#
# **计算公式**
#
# 上面是研报中的原文，笔者偷懒，直接贴图了。
#
# 看到这里，笔者忽然觉得[学术论文中的五大波动率因子，一篇文章给你讲完！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247491633&idx=1&sn=475c413d080e670285d2ae920595f7be&scene=21#wechat_redirect)这篇文章中的波动率因子复现错了，研报的意思应该是在分钟数据中复现的。
#
# 所以，这一次，笔者干脆在分钟数据和日频数据上都复现一下这个因子，然后对比看看。
#
# **2**
#
# **分钟数据代码**

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
# 从相关性来看，分钟数据计算的roll因子和日频数据计算的roll\_daily因子之间的相关性接近于0。
#
# 至于roll\_i这个增强因子，它和成交额的倒数（money）相关性为0.78，证实了笔者之前的猜想。
#
# 由于roll因子是基于分钟级别数据计算的，所以21日调仓的话可以有两种合成方式（其实不止，这个以后再说吧），取过去21个交易日的均值或者标准差。这两种方式，笔者都尝试过了，均值合成的表现不如标准差合成的。
#
# 标准差合成的，IC虽然比日频的高一点点，但是分层回测似乎就没那么好了。所以，下面的结果展示的是日频数据计算的因子。
#
# ## IC分析
# 日频数据计算的因子，IC绝对值超过0.05的有五年。
#
# 标准差合成的分钟数据因子只有四年IC绝对值超过了0.05（由于有三年超过0.08，有一年超过0.12，所以IC累加更好），甚至还有一年只有0.02。
#
# 至于均值合成的因子，甚至有一年的IC与其他年份相反。
#
# ## 收益分析
# 如果是标准差合成的分钟因子，那么红色的线将是最终净值最高的。它的结果就是下面的这张图。
#
# 最后，感谢各位大佬的支持，也希望大家能够继续支持，帮忙点点赞、分享分享，收藏收藏，甚至可以推荐推荐。当然，没有关注的大佬可以点点关注。
#

# ============================================================
# 本地图片清单（共 17 张）
# ============================================================
# 001.jpg  <-  ROLL价差因子
# 002.png  <-  计算公式
# 003.png  <-  日频数据代码
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
# 003.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close'])
    delta_close = (np.log(data.to_dataframe('close'))).diff()
    delta_close_shift = delta_close.shift()
    res = []
    for i in range(len(delta_close.columns)):
        res.append(max(-4 * delta_close.iloc[:, i].cov(delta_close_shift.iloc[:, i]), 0))
    res = pd.Series(data=np.sqrt(res), index=delta_close.columns.tolist(),
                    name=pd.to_datetime(date_str) + timedelta(hours=15))
    return res

# (作者注) 第2-5行，都是准备工作。
#
# (作者注) 第6行，计算对数收盘价的差分。
#
# (作者注) 第7行，错位。
#
# (作者注) 第8-10行，计算ROLL价差因子。

# --- 代码块 2 ---
def __call__(self):
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close']
                                         )
    self.delta_close = (np.log(data.to_dataframe('close'))).diff()
    self.delta_close_shift = self.delta_close.shift()
    res = Parallel(n_jobs=16, verbose=10, backend=self.parallel)(
        delayed(self.process_single_day)(idx)
        for idx in range(21, len(self.delta_close) + 1))
    res = pd.concat(res, axis=1).T
    res.index = data.trade_days[20:]
    res.index.name = 'datetime'
    res.reset_index(inplace=True)
    res = pd.melt(res, id_vars='datetime', var_name='code', value_name='roll')
    res.to_parquet('./roll.parquet')

def process_single_day(self, idx):
    delta_close = self.delta_close.iloc[idx - 21:idx].dropna(how='all', axis=1)
    delta_close_shift = self.delta_close_shift.reindex(columns=delta_close.columns)
    res = []
    for i in range(len(delta_close.columns)):
        res.append(max(-4 * delta_close.iloc[:, i].cov(delta_close_shift.iloc[:, i]), 0))
    res = pd.Series(data=np.sqrt(res), index=delta_close.columns.tolist())
    return res

# (作者注) 日频数据的核心和分钟数据是一致的，所以就只贴出代码了，细节的说明就免了。

