"""邪修成功！我计算了五种波动率，然后用k-means将其聚类后，得到波谷分钟数因子！

自动生成自 ../sources/general/articles/2026-04-16_邪修成功！我计算了五种波动率，然后用k-means将其聚类后，得到波谷分钟数因子！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-04-16_邪修成功！我计算了五种波动率，然后用k-means将其聚类后，得到波谷分钟数因子！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 邪修成功！我计算了五种波动率，然后用k-means将其聚类后，得到波谷分钟数因子！
# 日期    : 2026-04-16
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247496194&idx=1&sn=0d718abb4aa0818591a87b1bd9e4d9e8
# 本地原文: ../sources/general/articles/2026-04-16_邪修成功！我计算了五种波动率，然后用k-means将其聚类后，得到波谷分钟数因子！.md
# 本地图片: ../sources/general/articles/images/2026-04-16_邪修成功！我计算了五种波动率，然后用k-means将其聚类后，得到波谷分钟数因子！/  (共 14 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **波谷分钟数**
#
# 一日不邪修，浑身痒痒！
#
# 在复现了两篇研报之后，笔者又开始邪修了。
#
# 这次的邪修主要是参考了开源证券魏建榕老师在《市场微观结构研究系列（27）：高频成交量的峰、岭、谷信息》这篇研报中的思想。这篇研报，笔者用了四篇文章来复现其中的因子（[高频成交量的峰、岭、谷信息（一）：2025年7月20日应该还热乎的研报，IC和分层回测都还不错](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489605&idx=1&sn=e301d0cbc940fa40ed8d0731a5796eb5&scene=21#wechat_redirect)），但还没复现完。
#
# 本文，在这篇研报的思想上，笔者将成交量换成了波动率，想看看波动率的峰、岭、谷信息当中有没有能看一看的alpha因子。
#
# **计算步骤和代码**
#
# 虽然，这次的邪修参考了魏建榕老师的思想，但不是简单地将成交量换成波动率来计算的。
#
# 而是，对每日分钟数据计算滚动5分钟的波动率（一共5种），然后对波动率序列用k-means算法进行聚类，来划分波动率高点和低点。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，计算标的滚动五分钟的波动率，分别是，更优波动率、标准差，还有[学术论文中的五大波动率因子，一篇文章给你讲完！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247491633&idx=1&sn=475c413d080e670285d2ae920595f7be&scene=21#wechat_redirect)这篇文章中介绍的sigma\_p、sigma\_gk和sigma\_rs（没有考虑另外两个是因为它们计算出来会有很多nan）。这样，每天，每个标的的数据维度为235\*5。
#
# 第二步，对每个标的的235条数据进行聚为两类。
#
# 第三步，计算两个聚类中心的差值，如果大于0的概率超过0.5，那就认为第1类是高波动率，第0类则是低波动率。
#
# 第三步，单独出现的高波动率记为峰、连续出现的高波动率记为岭、其余为谷，并统计每个状态出现的次数。
#
# 第四步，用过去21个交易日的均值对其进行低频化处理。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 按照惯例，这里需要进行一通相关性分析的。但是，感觉没必要了。因为，波峰因子大部分标的都是0，这就导致了波谷和波岭因子的相关性接近-1。
#
# 同时，笔者在测试中发现，波峰分钟数因子并不好，而波岭分钟数和波谷分钟数相关性很高，所以这里仅展示波谷分钟数因子的评价结果。
#
# ## IC分析
# 这个IC的表现和一些好的因子相比确实不怎么样，但是和量峰、量岭和量谷分钟数这三个因子相比的话，就还算可以的，至少和它们三中最好的那一个是差不多的。
#
# ## 收益分析
# 这个分层回测也并不是很好，只能说看起来比量岭、量峰和量谷分钟数这三个因子舒服一点。
#
# 值得一提的是，在魏老师的研报中，分钟数本来就不是表现最好的因子。所以，接下来，笔者会用波动率的峰、岭、谷思想来魔改一下魏老师研报中表现最好的因子。
#
# 如果各位大佬对这个系列感兴趣的话，能不能动动金手指帮笔者点赞关注推荐和分享一下呢？
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
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    cur = pd.to_datetime(date_str) + timedelta(hours=15)
    file_name = self.files[idx]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close', 'open', 'high', 'low'])
    prefer_sigma_5 = []
    for i in range(5, len(data.data) + 1):
        tmp_data = data.data[i-5:i, :, :].reshape(-1, len(data.codes))
        tmp_sigma = np.nanstd(tmp_data, axis=0) / np.nanmean(tmp_data, axis=0)
        prefer_sigma_5.append(tmp_sigma)
    prefer_sigma_5 = pd.DataFrame(prefer_sigma_5, columns=data.codes)
    prefer_sigma_5.index = data.trade_days[4:]
    data = data.to_dataframes()
    sigma = data['close'].pct_change().rolling(5).std()
    hl_ratio = data['high'] / data['low']
    co_ratio = data['close'] / data['open']
    hc_ratio = data['high'] / data['close']
    ho_ratio = data['high'] / data['open']
    lc_ratio = data['low'] / data['close']
    lo_ratio = data['low'] / data['open']
    sigma_p = np.sqrt((np.square(np.log(hl_ratio))).rolling(5).sum() / (20 * np.log(2)))
    sigma_gk = np.sqrt((0.5 * np.square(np.log(hl_ratio)) -
                        (2 * np.log(2) - 1) * np.square(np.log(co_ratio))).rolling(5).mean())
    sigma_rs = (np.log(hc_ratio) * np.log(ho_ratio) +
                np.log(lc_ratio) * np.log(lo_ratio)).rolling(5).mean()
    sigma_rs = np.sqrt(sigma_rs)
    res = []
    for i in range(sigma_rs.shape[1]):
        tmp = pd.concat([prefer_sigma_5.iloc[:, i], sigma.iloc[:, i], sigma_p.iloc[:, i], sigma_gk.iloc[:, i],
                         sigma_rs.iloc[:, i]], axis=1)
        res.append(self.run_kmeans(tmp.iloc[5:]))
    res = pd.concat(res, axis=1)
    res = res.astype(bool)
    flag = res.shift(fill_value=False) | res.shift(-1, fill_value=False)
    flag = np.where(res, np.where(flag, 2, 1), 0)
    res = pd.DataFrame(index=res.columns, columns=['valley', 'peak', 'ridge'])
    res['valley'] = np.sum(flag == 0, axis=0)
    res['peak'] = np.sum(flag == 1, axis=0)
    res['ridge'] = np.sum(flag == 2, axis=0)
    res['datetime'] = cur
    return res

# (作者注) 前7行，读取数据。
#
# (作者注) 第8-14行，计算更优波动率，这个概念是方正证券的曹春晓老师提出的。
#
# (作者注) 第15-16行，计算分钟收益率的5标准差。
#
# (作者注) 第17-28行，计算sigma\_p、sigma\_gk和sigma\_rs，完全是按照公式来的，没什么需要特别说明的。
#
# (作者注) 第30-34行，调用run\_kmeans方法，对每个标的的波动率进行聚类。
#
# (作者注) 第35-37行，划分峰岭谷。
#
# (作者注) 最后，计算各个状态出现的次数。

# --- 代码块 2 ---
@staticmethod
def run_kmeans(data):
    val = data.values
    model = KMeans(n_clusters=2)
    model.fit(val)
    center = np.mean(np.diff(model.cluster_centers_, axis=0) > 0)
    label = model.labels_
    if center < 0.5:
        label = 1 - label
    data.iloc[:, 0] = label
    return data.iloc[:, 0:1]

# (作者注) run\_kmeans方法主要就是调包。
#
# (作者注) 这里需要的就是第6-9行，根据聚类中心的情况来修改label。

