"""显著信息特质波动率，花里胡哨的操作带来的提升肉眼不可见，最后还得靠黑科技！

自动生成自 ../sources/general/articles/2026-06-10_显著信息特质波动率，花里胡哨的操作带来的提升肉眼不可见，最后还得靠黑科技！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-06-10_显著信息特质波动率，花里胡哨的操作带来的提升肉眼不可见，最后还得靠黑科技！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 显著信息特质波动率，花里胡哨的操作带来的提升肉眼不可见，最后还得靠黑科技！
# 日期    : 2026-06-10
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247497238&idx=1&sn=8aaf1b13d6d434828e8aa75dcb57d132
# 本地原文: ../sources/general/articles/2026-06-10_显著信息特质波动率，花里胡哨的操作带来的提升肉眼不可见，最后还得靠黑科技！.md
# 本地图片: ../sources/general/articles/images/2026-06-10_显著信息特质波动率，花里胡哨的操作带来的提升肉眼不可见，最后还得靠黑科技！/  (共 31 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **显著信息特质波动率**
#
# 刚介绍完特质家族中的新兄弟特质盈利能力因子（[特质盈利能力因子，特质家族中又多了个兄弟，它能撼动老大的地位吗？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247497198&idx=1&sn=635fc19b604f0e0d2e52736269a21519&scene=21#wechat_redirect)），笔者又发现了新的研究，它叫作显著信息特质波动率。不过，它应该不能算是特质家族的新兄弟了，说难听点，算是对特质波动率进行基因改造了。
#
# 这个因子仍旧来自东北证券王琦老师的研报，发布于2025年9月5日的《因子选股系列之十二——特质波动率因子重构》。
#
# **计算方法和代码**
#
# 特质波动率其实就是残差收益率的标准差，那么显著信息特质波动率就是在信息显著的时候残差收益率的标准差。
#
# 当然，也不一定非要计算标准差，也可以是残差收益率平方后的均值然后开方。
#
# 这并不是计算这个因子的关键，这个因子的计算关键是如何判断信息是否显著。
#
# **1**
#
# **计算方法**
#
# 研报中一共选择了四个变量来判断信息是否显著，它们分别是大单净流入、换手率、日内振幅和日内波动率。
#
# 在过去60天中，这四个变量最大的20天，就是信息显著时刻，也就是计算这20天的残差收益率的波动。
#
# 由于笔者没有大单净流入的数据，所以这个就不复现了。
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
# 在测试的时候，笔者发现用残差收益率平方后的均值再开方计算的波动率在IC上的表现会好一点点。所以，笔者使用的是这种方法来计算波动率的。
#
# 从相关性来看，这重构之后的因子和重构之前的相关性可是非常之高了，即使是最低的也达到了0.98。
#
# 所以，笔者选择了resi\_sigma\_tr进行因子评价结果的展示。
#
# ## IC分析
# 这个因子的IC表现确实很好，但是没有什么太大的作用。
#
# 因为，波动率因子的IC表现也很好。
#
# ## 收益分析
# 这个分层回测的表现就有点拉胯了。
#
# 为什么会出现IC表现很好，分层拉胯呢？因为，笔者的分层回测是采取市值加权的方式。IC计算的时候又不会考虑市值，所以会出现这样的现象。
#
# 如果换成等权的话，会得到下面这样的结果。
#
# 这个分层回测的结果是不是就挺好了。
#
# 这对于所有IC表现好，但是分层回测表现差的因子使用，其效果都是很不错的。
#
# 如果市值加权的分层回测表现不行，但是等权的分层回测表现很好，这通常意味着这个因子属于小票暴露。
#
# ## IC分析
# IC有所下降，这也是意料之中的。
#
# ## 收益分析
# 这个分层回测是用市值加权的。
#
# 看起来是不是比上面用市值加权的舒服多了。
#
# 那如果特质波动率在计算一次标准差呢？笔者替各位大佬试过了，比上面的结果还要差！
#
# ## 总结
# 这个改造的想法看起来是不错的，但是笔者在复现的过程中没有看到这个改造带来的显著提升。
#
# 为了一点肉眼不可见的提升，加入一些花里胡哨的操作可能会带来过拟合的风险，总感觉不值得。
#
# 好了，整个特质家族的介绍应该暂时告一段路了，感谢大家的支持，也希望各位大佬能继续通过点赞推荐关注和分享的方式来支持笔者。
#

# ============================================================
# 本地图片清单（共 31 张）
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
# 015.png  <-  收益分析
# 016.png  <-  收益分析
# 017.png  <-  收益分析
# 018.png  <-  IC分析
# 019.png  <-  IC分析
# 020.png  <-  IC分析
# 021.png  <-  IC分析
# 022.png  <-  IC分析
# 023.png  <-  IC分析
# 024.png  <-  回归分析
# 025.png  <-  回归分析
# 026.png  <-  换手率分析
# 027.png  <-  换手率分析
# 028.png  <-  收益分析
# 029.png  <-  收益分析
# 017.png  <-  收益分析
# 017.png  <-  总结

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
    def __init__(self, file_pth, name, need_last_close, gap=100, parallel="threading"):
        super().__init__(file_pth, name, need_last_close, gap, parallel)
        self.turnover_ratio = BaseDataLoader.load_data('../../data/stock/capital.parquet', start='2013-01-01',
                                                       fields=['turnover_ratio']).to_dataframe()
        self.pv = BaseDataLoader.load_data('../../data/stock/stock_bar_1day.parquet', start='2012-12-31',
                                                       fields=['close', 'high', 'low', 'factor']).to_dataframes()
    def __call__(self):
        self.premium = pd.read_parquet('../../fund_return_analysis/premium.parquet',
                                  columns=['datetime', 'mkt_rtn', 'smb', 'hml'])
        self.premium.set_index('datetime', inplace=True)
        for key in ['close', 'high', 'low']:
            self.pv[key] *= self.pv['factor']
        self.rtn = self.pv['close'].pct_change().iloc[1:]
        self.amp = ((self.pv['high'] - self.pv['low']) / self.pv['close'].shift(1)).iloc[1:]
        sigma = self.run()
        sigma = pd.concat(sigma, axis=1).T
        self.sigma = sigma[sigma.index >= pd.to_datetime('2013-01-01')]
        trade_days = self.rtn.index.tolist()
        res = Parallel(n_jobs=16, verbose=10)(
            delayed(self.cal_resi_rtn)(idx, trade_days[idx])
            for idx in range(60, len(self.premium) + 1)
        )
        res = pd.concat(res)
        res.index.name = 'code'
        res.reset_index(inplace=True)
        res.to_parquet('./resi_sigma1.parquet')

# (作者注) 前12行，读取一些数据，包括换手率、日频的高低收三个价格和复权因子。
#
# (作者注) 第13行，计算日频收益率。
#
# (作者注) 第14行，计算振幅。
#
# (作者注) 第15-17行，读取分钟数据计算日内波动率。
#
# (作者注) 第18-26行，调用cal\_resi\_rtn计算因子。

# --- 代码块 2 ---
def __cal_resi_rtn__(self, data, amp, tr, sigma):
    data = data.dropna()
    if len(data) < 10:
        return [np.nan] * 4
    x = data.iloc[:, 1:]
    y = data.iloc[:, 0]
    lr = LinearRegression()
    lr.fit(x, y)
    resi = y - lr.predict(x)
    resi_sigma = np.sqrt(np.mean(np.square(resi)))
    resi_sigma_tr = self.cal_resi_by_large_20(resi, tr)
    resi_sigma_amp = self.cal_resi_by_large_20(resi, amp)
    resi_sigma_sigma = self.cal_resi_by_large_20(resi, sigma)
    return [resi_sigma, resi_sigma_tr, resi_sigma_amp, resi_sigma_sigma]
@staticmethod
def cal_resi_by_large_20(resi, sort_data):
    resi = pd.concat([resi, sort_data], axis=1)
    resi.columns = ['resi', 'sort_data']
    resi.sort_values('sort_data', inplace=True)
    return np.sqrt(np.mean(np.square(resi.iloc[-20:, 0])))
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['open', 'close']).to_dataframes()
    rtn = data['close'] / data['open'] - 1
    res = rtn.std()
    res.name = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 剩下的代码就是调包然后计算残差了，感觉没有什么需要特别说明的了。

