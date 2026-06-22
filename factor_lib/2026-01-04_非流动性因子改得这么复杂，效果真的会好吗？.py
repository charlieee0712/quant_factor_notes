"""非流动性因子改得这么复杂，效果真的会好吗？

自动生成自 ../sources/chenshengrui/articles/2026-01-04_非流动性因子改得这么复杂，效果真的会好吗？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/chenshengrui/articles/images/2026-01-04_非流动性因子改得这么复杂，效果真的会好吗？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: chenshengrui
# 公众号  : 量化拯救散户
# 标题    : 非流动性因子改得这么复杂，效果真的会好吗？
# 日期    : 2026-01-04
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247493633&idx=1&sn=f31ada053ccebe1002826a8dc1945180
# 本地原文: ../sources/chenshengrui/articles/2026-01-04_非流动性因子改得这么复杂，效果真的会好吗？.md
# 本地图片: ../sources/chenshengrui/articles/images/2026-01-04_非流动性因子改得这么复杂，效果真的会好吗？/  (共 15 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:28

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **改进非流动性因子**
#
# 关于非流动性这个因子，笔者已经写过4篇文章了，分别是[用换手率来计算非流动性，来自绿皮书作者的另一本书，在大A会有怎样的表现呢？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247492599&idx=1&sn=03048ff9440bd39dd689ca9dff8b945f&scene=21#wechat_redirect)、[让DeepSeek改造Amihud非流动性因子，结果它还真行！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247487689&idx=1&sn=18a36fb1eb25886dd42dd379e17c9fbd&scene=21#wechat_redirect)、[基于K线最短路径构造的非流动性因子，分层回测的效果有点惊艳！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247487661&idx=1&sn=c25570f33538ba91e76745ca7f904174&scene=21#wechat_redirect)和[轨迹的非流动性，来自长江证券的首席覃川桃！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247487397&idx=1&sn=7aa8ff7a8c9a60ba9d6b11695a10f36d&scene=21#wechat_redirect)。
#
# 其实，除了这四篇外，笔者在古早的时候还复现过正收益非流动性、负收益非流动性和流动性冲击这样的一些因子。
#
# 本以为，这个因子应该已经被研究“烂”了。
#
# 结果，笔者最近又找到了一些和非流动性有关的研报，有的是2025年11月18日发布的，有的则是2022年10月左右发布的。
#
# 本文，笔者复现的是后者，由中信建投的陈升锐老师在2022年10月发布的研报《高频因子选股系列五：流动性因子系统解读与再增强》。
#
# 需要注意的是，这篇研报中提到了四个因子，分别是预期换手率因子、改进非流动性因子、增强非流动性因子和高频类流动性因子。
#
# 由于内容较多，很难在一篇文章中讲完，所以笔者本文先复现一下改进非流动性因子。
#
# **计算公式和代码**
#
# 这个因子的计算公式的推导过程有点复杂，笔者觉得自己也很难讲解清楚，所以各位大佬有兴趣的话可以找找原文看一看。
#
# 在这里，我们将直接使用最后推导出来的公式。
#
# **1**
#
# **计算公式**
#
# 改进非流动性=非流动性-b\*CV。
#
# 其中，b是收益率的绝对值对成交量回归的斜率，CV是成交量的变异系数。
#
# 根据之前的文章，[用换手率来计算非流动性，来自绿皮书作者的另一本书，在大A会有怎样的表现呢？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247492599&idx=1&sn=03048ff9440bd39dd689ca9dff8b945f&scene=21#wechat_redirect)，成交量可以替换为成交额或者换手率，因此有三个因子可以计算。
#
# 同时，斜率和变异系数都是需要一个时间窗口的，这里按照笔者的习惯都取21个交易日。
#
# 笔者还有一个奇怪的想法，用非流动过去21个交易日的均值-b\*CV，但是这个效果看起来也并没有什么太大的改善。
#
# **2**
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
# 从相关性来看，用换手率计算的因子与其他两个因子的相关性不高。
#
# 但是，在因子评价的时候，笔者发现，用成交额计算的因子分层回测是唯一一个能看的，所以下面展示的是成交额计算的因子分层回测结果。
#
# 同时，传统的非流动性因子，需要取过去21个交易日的均值，这里笔者也会再去一次过去21个交易日的均值。
#
# ## IC分析
# IC确实不是很高，但是2018年的IR居然有2.0。
#
# ## 收益分析
# 说实话，这个改进，除了提升了因子的复杂度之外，其他方面可以说是没有任何的提升。
#
# 传统的非流动性因子可能几分钟就计算完了，这个因子的计算需要大概50分钟。
#
# 好了，又到了文章的最后了，希望各位大佬能动动金手，帮笔者点点关注分享推荐和赞，谢谢大家。
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
# 010.png  <-  回归分析
# 011.png  <-  换手率分析
# 012.png  <-  换手率分析
# 013.png  <-  收益分析
# 001.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def __call__(self):
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close', 'volume', 'turnover'])
    self.codes = data.codes
    cap = BaseDataLoader.load_data('../../data/capital.parquet', fields=['market_cap', 'turnover_ratio'],
                                   codes=self.codes)
    rtn = np.abs(data.to_dataframe('close').pct_change())
    vol = data.to_dataframe('volume')
    money = data.to_dataframe('turnover')
    tr = cap.to_dataframe('turnover_ratio')
    illiquidity_vol = rtn / vol
    illiquidity_money = rtn / money
    illiquidity_tr = rtn / tr
    b_list = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_beta)(rtn.iloc[i - 21:i, :], vol.iloc[i - 21:i, :],
                               money.iloc[i-21:i, :], tr.iloc[i-21:i, :])
        for i in range(22, len(rtn) + 1)
    )
    b_list = np.array(b_list)
    days = rtn.index.tolist()[21:]
    b_dict = {
        'illiquidity_vol': pd.DataFrame(b_list[:, :, 0], columns=self.codes, index=days),
        'illiquidity_money': pd.DataFrame(b_list[:, :, 1], columns=self.codes, index=days),
        'illiquidity_tr': pd.DataFrame(b_list[:, :, 2], columns=self.codes, index=days)}
    dfs = {'illiquidity_vol': illiquidity_vol, 'illiquidity_tr': illiquidity_tr,
           'illiquidity_money': illiquidity_money}
    cv_dict = {
        'illiquidity_vol': vol.rolling(21).std() / vol.rolling(21).mean(),
        'illiquidity_money': money.rolling(21).std() / money.rolling(21).mean(),
        'illiquidity_tr': tr.rolling(21).std() / tr.rolling(21).mean()
    }
    for key in dfs:
        dfs[key] = dfs[key] - b_dict[key] * cv_dict[key]
    df = dfs_to_df(dfs)
    df.to_parquet('./illiquidity_new.parquet')

# (作者注) 这段代码前12行，就是经典的非流动性因子计算。
#
# (作者注) 第13-23行，计算斜率b。
#
# (作者注) 第26-30行，计算变异系数。
#
# (作者注) 第31-32行，计算改进的非流动性因子。

# --- 代码块 2 ---
def cal_beta(self, y, x1, x2, x3):
    res = []
    for code in self.codes:
        data = pd.concat([y.loc[:, code], x1.loc[:, code], x2.loc[:, code], x3.loc[:, code]], axis=1)
        res.append(self.__cal_beta__(data.dropna()))
    return res

# (作者注) 第二段代码，按照标的循环调用\_\_cal\_beta\_\_方法，计算每个标的每20个交易日的3个斜率。

# --- 代码块 3 ---
@staticmethod
def __cal_beta__(data):
    y = np.abs(data.iloc[:, 0].values)
    if len(y) < 5:
        return [np.nan] * 3
    beta = []
    for i in range(1, 4):
        x = np.c_[np.ones((len(data), 1)), data.iloc[:, i].values]
        beta_full = np.linalg.pinv(x.T @ x) @ x.T @ y
        beta.append(beta_full[-1])
    return beta

# (作者注) 第三段代码，进行三次线性回归得到三个斜率。
#
# (作者注) 因为，这里每个标的的y和x都是不一样的，所以即使是时序回归也要分标的进行。同时，需要计算的斜率是三个，如果一起计算会考虑到各自的影响，所以还是得分开计算。
#
# (作者注) 第3-5行，处理数据较少的情况，直接返回nan。
#
# (作者注) 第6-10行，通过线性回归得到斜率，i=1，2，3分别对应成交量、成交额和换手率。

