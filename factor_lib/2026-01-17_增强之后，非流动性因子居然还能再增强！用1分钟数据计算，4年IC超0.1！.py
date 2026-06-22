"""增强之后，非流动性因子居然还能再增强！用1分钟数据计算，4年IC超0.1！

自动生成自 ../sources/chenshengrui/articles/2026-01-17_增强之后，非流动性因子居然还能再增强！用1分钟数据计算，4年IC超0.1！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/chenshengrui/articles/images/2026-01-17_增强之后，非流动性因子居然还能再增强！用1分钟数据计算，4年IC超0.1！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: chenshengrui
# 公众号  : 量化拯救散户
# 标题    : 增强之后，非流动性因子居然还能再增强！用1分钟数据计算，4年IC超0.1！
# 日期    : 2026-01-17
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494174&idx=1&sn=8c15c74c35656d0d100429bc3fbcdbe4
# 本地原文: ../sources/chenshengrui/articles/2026-01-17_增强之后，非流动性因子居然还能再增强！用1分钟数据计算，4年IC超0.1！.md
# 本地图片: ../sources/chenshengrui/articles/images/2026-01-17_增强之后，非流动性因子居然还能再增强！用1分钟数据计算，4年IC超0.1！/  (共 15 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:28

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **非流动性**
#
# 这周，笔者已经介绍过一个非流动性因子了，在[增强非流动性因子，竟然真的增强了？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494084&idx=1&sn=0cc067d4512e9cfd147029674c682c37&scene=21#wechat_redirect)这篇文章中有过介绍。
#
# 本文，笔者将介绍同一篇研报中的最后一个非流动性因子，研报中将其称为高频非流动性因子，使用的是30分钟的数据来计算的。不过，笔者在复现的时候，发现这个因子用1分钟的数据计算的话，IC会更高（耗时会更长）。
#
# **计算步骤和代码**
#
# 这个因子在计算上和增强非流动性因子很像，都是要进行时序回归。只不过，增强非流动性因子多了一个解释变量，t-1时刻的收益。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 以收益率为被解释变量，收益率的符号函数乘以成交量（成交额、换手率）为被解释变量，进行时序回归，取回归的斜率作为最后的因子。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 和之前的因子一样，成交额和成交量计算的因子的相关性高于0.6，用换手率计算的因子和两者相关性都很低。
#
# 同时，由于这个因子的计算直接使用了过去21个交易日的数据，所以不再用均值或者标准差来合成月度因子了。
#
# 为了能和之前的文章进行对比，笔者将展示用换手率计算的因子的因子评价结果。
#
# ## IC分析
# 从IC上来看，有四年的IC超过了0.1，六年IC超过0.08，确实比增强非流动性因子强了不少。
#
# ## 收益分析
# 虽然，因子的IC看起来有一定的提升，但是分层回测和增强非流动性因子相比就没什么区别了，至少用肉眼很难看出来区别。
#
# 所以，这里也就只展示一下用换手率计算的因子，其他的没必要了。
#
# 至此，这篇研报中三个基于非流动性思想计算的因子就介绍完了。但是，这篇研报还没有结束，它还有一个和换手率相关的因子。如果各位大佬对这篇研报剩下的内容感性的话，可以动动金手指，点赞分享推荐和关注都点一点，支持一下笔者。你们的每一次支持，都是笔者持续更新最大的动力，谢谢各位大佬。
#

# ============================================================
# 本地图片清单（共 15 张）
# ============================================================
# 001.png  <-  代码
# 002.png  <-  因子评价
# 003.png  <-  IC分析
# 004.png  <-  IC分析
# 005.png  <-  IC分析
# 006.png  <-  IC分析
# 007.png  <-  IC分析
# 008.png  <-  IC分析
# 009.png  <-  回归分析
# 010.png  <-  回归分析
# 011.png  <-  换手率分析
# 012.png  <-  换手率分析
# 013.png  <-  收益分析
# 014.png  <-  收益分析
# 001.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def __init__(self, file_pth, name, need_last_close, gap=100, parallel="threading"):
    super().__init__(file_pth, name, need_last_close, gap, parallel)
    factor = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['factor'])
    self.factor = factor.to_dataframe('factor')
    cap = BaseDataLoader.load_data('../../data/capital.parquet', fields=['circulating_cap'])
    self.cap = cap.to_dataframe('circulating_cap')

# (作者注) 在初始化阶段，读取了复权因子和流通股本的数据，用来计算复权价格和换手率。

# --- 代码块 2 ---
def process_single_day(self, idx):
    if idx < 243:
        return pd.DataFrame({})
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    vol, money, rtn, tr = [], [], [], []
    for i in range(idx - 20, idx + 1):
        file_name = self.files[i]
        full_path = os.path.join(self.file_pth, file_name)
        data = BaseDataLoader.load_data(full_path, fields=['volume', 'close', 'open', 'turnover'])
        vol.append(data.to_dataframe('volume'))
        money.append(data.to_dataframe('turnover'))
        tmp_cap = self.cap.iloc[idx - 243].reindex(data.codes)
        tr.append(vol[-1] / tmp_cap.values.reshape(1, -1))
        tmp_factor = self.factor.iloc[idx - 243].reindex(data.codes)
        tmp_close = data.to_dataframe('close') * tmp_factor.values.reshape(1, -1)
        rtn.append(tmp_close)
    rtn = pd.concat(rtn).pct_change()
    vol = pd.concat(vol)
    money = pd.concat(money)
    tr = pd.concat(tr)
    res = []
    for i in range(rtn.shape[1]):
        res.append(self.cal_beta(rtn.iloc[:, i], vol.iloc[:, i], money.iloc[:, i], tr.iloc[:, i]))
    res = pd.DataFrame(data=res, index=rtn.columns, columns=['vol', 'money', 'tr'])
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 由于笔者的日频数据从2005年开始，分钟数据从2004年开始，这两者之间有个gap，这个gap刚好243天，所以当日期索引小于243的时候，返回空的dataframe。
#
# (作者注) 第6-17行，读取过去21个交易日的数据。其中，13-14行计算换手率，这里用iloc是因为速度更快，但是需要人工确认数据对齐。15-17行，计算复权后的收益率。
#
# (作者注) 第23-24行，对每个标的进行时序回归。

# --- 代码块 3 ---
def cal_beta(self, y, x1, x2, x3):
    data = pd.concat([y, x1, x2, x3], axis=1).dropna()
    y = data.iloc[:, 0].values
    if len(y) < 5:
        return [np.nan] * 3
    beta = []
    for i in range(1, 4):
        x = (data.iloc[:, i] * np.sign(data.iloc[:, 0])).values.reshape(-1, 1)
        x = np.c_[np.ones((len(data), 1)), x]
        beta_full = np.linalg.pinv(x.T @ x) @ x.T @ y
        beta.append(beta_full[1])
    return beta

# (作者注) 这段代码大家应该很熟悉了，笔者就不赘述了。

