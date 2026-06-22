"""高波期波动率均值，用GMM模型来分析波动率，效果竟然也不错！

自动生成自 ../sources/general/articles/2026-04-11_高波期波动率均值，用GMM模型来分析波动率，效果竟然也不错！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-04-11_高波期波动率均值，用GMM模型来分析波动率，效果竟然也不错！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 高波期波动率均值，用GMM模型来分析波动率，效果竟然也不错！
# 日期    : 2026-04-11
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247496049&idx=1&sn=3cd614dcef5662e4b074ebfc1d796cf6
# 本地原文: ../sources/general/articles/2026-04-11_高波期波动率均值，用GMM模型来分析波动率，效果竟然也不错！.md
# 本地图片: ../sources/general/articles/images/2026-04-11_高波期波动率均值，用GMM模型来分析波动率，效果竟然也不错！/  (共 15 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **高波期波动率均值**
#
# 在[波动率的分布，这个专题似乎没有研报聊过！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247495534&idx=1&sn=ab695b8e5fae5576ccd56fbe815607cb&scene=21#wechat_redirect)这篇文章中，笔者展开了对波动率分布的研究。
#
# 为什么会整这样一个专题研究呢？
#
# 因为，笔者在复现研报的时候发现，收益率分布中的alpha因子以及成交量分布中的alpha因子都有相关的研报，唯独波动率没有。所以，不自量力，想成为第一个吃螃蟹的人。
#
# 在波动率的分布中，笔者设计了一个叫做波动率极大值幅度的因子，这个因子用了方正证券曹春晓老师的更有波动率（[灾后重建是真的不行，不过更优波动率还是可以的](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247487891&idx=2&sn=a1c64d73624440e1772d61aac0450b55&scene=21#wechat_redirect)）的思想，然后结合了兴业证券郑兆磊老师的收益率极大值幅度（[收益率极大值幅度：一个我差点错过的超级多头因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247495105&idx=1&sn=cbd66f5bad81250e59992d6ed9cd3349&scene=21#wechat_redirect)）因子。
#
# 本文，笔者将介绍高波期波动率均值这个因子，仍旧参考了两位老师的研报。这里只要用到了GMM模型，在[跳价期波动，原理很复杂，但计算并不难，2023年IC绝对值超过0.1，2021年后半段的分层回测也不错](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247486703&idx=1&sn=243d4b885a2259f41204a0089045755f&scene=21#wechat_redirect)这篇文章中有过相关的介绍。
#
# **计算步骤和代码**
#
# 在用GMM模型来分析收益率的时候，郑老师将其分为了跳价期和震荡期，跳价期出现的概率低，而震荡期出现的概率高。
#
# 在分析波动率的时候，笔者将期分成了高波期和低波期。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，计算滚动5分钟的更优波动率。
#
# 第二步，对每个标的的波动率用两个高斯分布进行拟合，其中均值更大的高斯分布对应高波期，均值小的则对应低波期。
#
# 第三步，根据郑老师的思想，一共能得到10个因子。作为一个起名困难户，就不乱起名字了，大家根据代码来看吧。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 从相关性来看，有两个因子和其他8个因子之间的相关性并不是太高，它们是low\_vol\_mean2w和high\_vol\_mean2w。
#
# 在这10个因子当中，有些因子在IC上的表现非常不错（有四年的IC绝对值超过了0.1），比如：high\_vol\_mean、high\_vol\_std（2023年IC绝对值超过0.14）。但是，它们在分层回测上的表现就不怎样了，除了因子值最大的一组遥遥落后于其他四组之外，其余的净值曲线之间可以说是没有任何的区分度。
#
# 因此，这里笔者就只展示一下分层回测表现最好的high\_vol\_mean2w的因子评价结果了。注意，这里采用的是过去21个交易日的均值对其进行低频化的。
#
# ## IC分析
# 从IC上来看，high\_vol\_mean2w并不出彩，绝对值最高的一年也只是勉强超过了0.08。
#
# ## 收益分析
# 虽然，这个因子的IC绝对值并不是很高，但是分层回测还是能看的。至少，从2021年上半年开始，蓝线就拉开了与其他线的差距。
#
# 这么看来，波动率的分布这个专题还是有内容可挖的。不知道是否合各位大佬的胃口，如果您对其感兴趣的话，笔者需要您的点赞关注推荐和分享来支持支持，谢谢大家。
#

# ============================================================
# 本地图片清单（共 15 张）
# ============================================================
# 001.png  <-  计算代码
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

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    file_name = self.files[idx]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close', 'open', 'high', 'low', 'turnover', 'volume'])
    prefer_sigma_5 = []
    for i in range(5, len(data.data)+1):
        tmp_data = data.data[i-5:i, 0:4, :].reshape(-1, len(data.codes))
        tmp_sigma = np.nanstd(tmp_data, axis=0) / np.nanmean(tmp_data, axis=0)
        prefer_sigma_5.append(tmp_sigma)
    prefer_sigma_5 = pd.DataFrame(prefer_sigma_5, columns=data.codes)
    res = []
    for i in range(len(data.codes)):
        res.append(self.gmm_fit(prefer_sigma_5.iloc[:, i].values))
    res = np.array(res)
    factor_df = pd.DataFrame(index=data.codes, columns=['high_vol_weight', 'low_vol_weight', 'high_vol_mean', 'low_vol_mean', 'high_vol_std',
                                                        'low_vol_std'], data=res)
    factor_df['low_vol_mean2w'] = res[:, 3] / res[:, 1]
    factor_df['high_vol_mean2w'] = res[:, 2] / res[:, 0]
    factor_df['mean_diff'] = res[:, 2] - res[:, 3]
    factor_df['mean2w_diff'] = factor_df['mean_diff'] / (res[:, 0] - res[:, 1])
    factor_df['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    return factor_df

# (作者注) 第2-6行，读取数据。
#
# (作者注) 第7-12行，计算滚动5分钟的更优波动率。
#
# (作者注) 第13-16行，调用gmm\_fit方法用GMM模型对每个标的的更有波动率进行拟合。
#
# (作者注) 第17-22行，计算传说中的10个因子。

# --- 代码块 2 ---
@staticmethod
def gmm_fit(data):
    flag = ~np.isnan(data)
    arr = data[flag]
    gmm = GaussianMixture(n_components=2, covariance_type='full')
    gmm.fit(arr.reshape(-1, 1))
    keys = gmm.weights_
    mu = gmm.means_.reshape(-1)
    sigma = np.sqrt(gmm.covariances_).reshape(-1)
    if sigma[1] > sigma[0]:
        return np.concatenate((keys[::-1], mu[::-1], sigma[::-1]))
    return np.concatenate((keys, mu, sigma))

# (作者注) 这段代码就是调包，在调包之前先去掉数据中的nan值。
#
# (作者注) 第10行，保证返回的数据中，先返回高波期的，然后才是低波期的。

