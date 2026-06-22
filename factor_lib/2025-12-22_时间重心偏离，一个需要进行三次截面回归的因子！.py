"""时间重心偏离，一个需要进行三次截面回归的因子！

自动生成自 ../sources/weijianrong/articles/2025-12-22_时间重心偏离，一个需要进行三次截面回归的因子！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/weijianrong/articles/images/2025-12-22_时间重心偏离，一个需要进行三次截面回归的因子！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: weijianrong
# 公众号  : 量化拯救散户
# 标题    : 时间重心偏离，一个需要进行三次截面回归的因子！
# 日期    : 2025-12-22
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247493107&idx=1&sn=3a20f683473ea9915b7b008eaa3697b6
# 本地原文: ../sources/weijianrong/articles/2025-12-22_时间重心偏离，一个需要进行三次截面回归的因子！.md
# 本地图片: ../sources/weijianrong/articles/images/2025-12-22_时间重心偏离，一个需要进行三次截面回归的因子！/  (共 14 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:28

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **时间重心偏离**
#
# 在[时间和，一个分层回测表现有点离谱的多头因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247493059&idx=1&sn=8371648040cfc68b3c850c8bad6bc488&scene=21#wechat_redirect)这篇文章中笔者复现了研报《市场微观结构研究系列（19）：日内分钟收益率的时序特征-逻辑讨论与因子增强》中的四个因子。
#
# 本文，笔者将继续复现这篇研报中的第五个因子，叫做时间重心偏离。
#
# 在构建这个因子之前，魏建榕老师对这个因子进行分析，然后得出了这样的结论：
#
# > 我们在分析时间指标与收益率结构的关系时发现日内涨跌幅，尤其是盘尾阶段的涨跌幅对于“时间差 Alpha”有较强的解释能力，而盘初阶段的涨跌幅会带来负向干扰。此外，诸如极端涨跌幅样本的平均涨幅和平均跌幅越高，同样也会降低因子的有效性。简单归纳一下影响因素，主要有两个方面：
# >
# > （1）收益率结构：时段 1 和时段 2 的收益率、隔夜收益率；
# >
# > （2）极端收益率的反转效应：平均涨幅、平均跌幅
#
# **计算步骤和代码**
#
# 这个因子的计算需要进行三次截面回归，咱们先通过计算步骤来大致了解一下它的一个计算过程，再用大佬来深入了解一下。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，计算平均涨幅、平均跌幅、隔夜收益、第一个30分钟的收益率和第二个30分钟的收益率。
#
# 第二步，以涨幅时间重心为y，平均涨幅、隔夜收益、第一个30分钟的收益率和第二个30分钟的收益率为x，进行线性回归并计算残差。
#
# 第三步，以跌幅时间重心为y，平均跌幅、隔夜收益、第一个30分钟的收益率和第二个30分钟的收益率为x，进行线性回归并计算残差。
#
# 第四步，以跌幅时间重心的残差为y，涨幅时间重心的残差为x，进行线性回归并计算残差。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 从相关性来看，这个因子和跌幅时间重心和时间和这两个因子的相关性超过了0.7。
#
# 对于这个因子，如果用标准差合成的话，其IC绝对值偏低，分层回测的表现也不是太好。因此，下面展示的是用均值合成的因子。
#
# ## 收益分析
# 这个分层回测的话，在2022年之前可以说是区分度不高。但是，到了2022年之后，各组之前的区分度还是不错的。
#
# 值得一提的是，这个因子多头组最后的净值接近了1.8，和之前表现离谱的时间和因子的差距大概10%。
#
# 至此，这篇研报中的所有因子，笔者都介绍过一遍了。
#
# 又到了求赞求关注求分享求推荐的时间了，希望各位大佬能动动金手支持一下，谢谢大家。
#

# ============================================================
# 本地图片清单（共 14 张）
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
# 001.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 4 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close', 'open']).to_dataframes()
    rtn = (data['close'] / data['open'] - 1)
    up_flag = rtn > 0
    down_flag = rtn < 0
    ru = (rtn * np.where(up_flag, 1, np.nan)).mean()
    rd = (rtn * np.where(down_flag, 1, np.nan)).mean()
    r1 = data['close'].iloc[29] / data['open'].iloc[0] - 1
    r2 = data['close'].iloc[59] / data['open'].iloc[30] - 1
    res = pd.concat([ru, rd, r1, r2], axis=1)
    res.columns = ['ru', 'rd', 'r1', 'r2']
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 这段代码对应计算步骤中的第一步，主要计算了平均涨幅、平均跌幅、第一个30分钟的收益率和第二个30分钟的收益率。
#
# (作者注) 感觉没什么需要特别说明的了。

# --- 代码块 2 ---
def __call__(self):
    res = self.run()
    res = pd.concat(res)
    res.index.name = 'code'
    res.reset_index(inplace=True)
    data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['open', 'close'])
    self.rtn_overnight = data.to_dataframe('open') / data.to_dataframe('close').shift(1) - 1
    start = self.rtn_overnight.index.tolist()[0]
    self.factor = BaseDataLoader.load_data('./gravity_center1.parquet', fields=['gu', 'gd'], start=start
                                           ).to_dataframes()
    res = res[res['datetime'] >= start]
    self.res = BaseDataLoader.from_dataframe(res).to_dataframes()
    res = []
    for i in tqdm(range(len(self.rtn_overnight))):
        res.append(self.cal_factors(i))
    res = pd.concat(res, axis=1).T
    res.index.name = 'datetime'
    res = pd.melt(res.reset_index(), id_vars='datetime', var_name='code', value_name='tcd')
    res.to_parquet('./tcd.parquet')

# (作者注) 这段代码主要是读取涨跌幅时间重心这两个因子，然后计算隔夜收益率，最后调用cal\_factors来计算时间重心偏离（TCD）因子。
#
# (作者注) 第2-5行，是调用process\_single\_day来计算一些需要用到分钟级数据的因子。
#
# (作者注) 第6-7行，计算隔夜收益。
#
# (作者注) 第8行，获取隔夜收益率的起始时间。
#
# (作者注) 第9-10行，读取涨跌幅时间重心因子。
#
# (作者注) 第11-12行，将res这个dataframe转换为BaseDataLoader的数据结构。

# --- 代码块 3 ---
def cal_factors(self, idx):
    rtn_overnight = self.rtn_overnight.iloc[idx]
    day = rtn_overnight.name
    gu = self.factor['gu'].iloc[idx]
    gd = self.factor['gd'].iloc[idx]
    ru = self.res['ru'].iloc[idx]
    rd = self.res['rd'].iloc[idx]
    r1 = self.res['r1'].iloc[idx]
    r2 = self.res['r2'].iloc[idx]
    data = pd.concat([ru, rd, r1, r2, rtn_overnight, gu, gd], axis=1)
    data.columns = ['ru', 'rd', 'r1', 'r2', 'rtn_overnight', 'gu', 'gd']
    data = data.dropna()
    if len(data) <= 10:
        return pd.Series(index=data.index.tolist(), name=day)
    error_u = self.cal_residual(data[['ru', 'r1', 'r2', 'rtn_overnight', 'gu']].values)
    error_d = self.cal_residual(data[['rd', 'r1', 'r2', 'rtn_overnight', 'gd']].values)
    res = self.cal_residual(np.array([error_u, error_d]).T)
    res = pd.Series(res, index=data.index.tolist(), name=day)
    return res

# (作者注) 第2-12行，获取截面上的各因子值，然后去掉有nan的情况。
#
# (作者注) 第13-14行，如果截面上所有因子不为nan的标的不超过10个，就返回一个空的dataframe。
#
# (作者注) 第15行，计算涨幅时间重心的残差。
#
# (作者注) 第16行，计算跌幅时间重心的残差。
#
# (作者注) 第17行，计算残差的残差。

# --- 代码块 4 ---
def cal_residual(self, x):
    y = x[:, -1].reshape(-1, 1)
    x = x[:, :-1]
    lr = LinearRegression()
    lr.fit(x, y)
    resi = y - lr.predict(x)
    return resi.reshape(-1)

# (作者注) 最后一段代码，就是进行线性回归然后计算残差了。
#
# (作者注) 这里需要注意的是，输入 的数据是一个ndarry，最后一列的数据是y，其他列的数据是x。

