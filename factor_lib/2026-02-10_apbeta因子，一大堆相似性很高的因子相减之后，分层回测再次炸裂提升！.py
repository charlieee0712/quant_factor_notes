"""apbeta因子，一大堆相似性很高的因子相减之后，分层回测再次炸裂提升！

自动生成自 ../sources/zhengzhaolei/articles/2026-02-10_apbeta因子，一大堆相似性很高的因子相减之后，分层回测再次炸裂提升！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/zhengzhaolei/articles/images/2026-02-10_apbeta因子，一大堆相似性很高的因子相减之后，分层回测再次炸裂提升！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: zhengzhaolei
# 公众号  : 量化拯救散户
# 标题    : apbeta因子，一大堆相似性很高的因子相减之后，分层回测再次炸裂提升！
# 日期    : 2026-02-10
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494698&idx=1&sn=02e1ef048d67bedb1b67ab0b6f63054e
# 本地原文: ../sources/zhengzhaolei/articles/2026-02-10_apbeta因子，一大堆相似性很高的因子相减之后，分层回测再次炸裂提升！.md
# 本地图片: ../sources/zhengzhaolei/articles/images/2026-02-10_apbeta因子，一大堆相似性很高的因子相减之后，分层回测再次炸裂提升！/  (共 18 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:29

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **apbeta**
#
# 这个因子和非流动性有那么一点点的关系，但是感觉关系也不是很大。
#
# 这个因子来自兴业证券的郑兆磊老师在2025年11月18日发布的研报《高频系列十一——流动性因子全解析：选股、择时与多策略》。
#
# 这个研报中一共有三类因子，第一类因子在[这次的非流动性因子，真的不知道该起什么名字了！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494524&idx=1&sn=896925d110852e7be503bdf484ba3393&scene=21#wechat_redirect)中有过介绍。
#
# 本文介绍的是这篇研报中的第二类因子，apbeta因子。
#
# **计算公式和代码**
#
# 这类因子，有四个，而且计算公式不是简单的几句话就能描述清楚的。所以，笔者只能截图了。
#
# **1**
#
# **计算公式**
#
# 研报中，仅对apbeta4因子进行研究。
#
# 但是，笔者在测试的时候发现，apbeta1和apbeta3这两个因子用过去21天的标准差合成的时候表现最好。
#
# 所以，笔者将只复现这两个因子。
#
# 同时，由于成交额、成交量和换手率都可以用来计算非流动性，那么一共是6个因子。
#
# **2**
#
# **计算代码**

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
# 这六个因子的相关性很有规律，3个ap\_beta1之间的相关性为1，2个ap\_beta3之间的相关性为1，ap\_beta1和ap\_beta3之间的相关性为0.5。
#
# 笔者在测试的时候发现这些因子当中ap\_beta3\_money用过去21个交易日的标准差合成之后的效果是最好的。但是，它不是本文的重点。因为，有一个因子虽然IC不如它，但是分层回测要比它好。
#
# 那就是，用过去21个交易日的均值合成的ap\_beta1\_money-ap\_beta1\_tr。
#
# ## IC分析
# 这个因子的IC表现很一般。
#
# ap\_beta3\_money这个因子有六年的IC绝对值超过了0.06，其中一年超过了0.08！
#
# ## 回归分析
# 这个因子表现出了不错的分层回测单调性。接下来，将展示一下ap\_beta3\_money的分层回测结果。
#
# 这个因子是因子值中间组的表现是最好的。
#
# 需要注意的是，做差的两个因子可能存在着过拟合的情况。因为用ap\_beta3\_money-ap\_beta3\_tr的表现没有这么好，用ap\_beta1\_money-ap\_beta1\_vol的表现也没有这么好。
#
# 或许，ap\_beta2和ap\_beta4用同样的方法构造能得到更好的结果，这里就留给大家自己尝试了。
#
# 要验证这个因子是不是过拟合，就需要看看它在样本外的表现了。比如：在2025年的表现，甚至是2026年的表现。
#
# 好了，又到了求赞求关注求分享求推荐的时间了，希望各位大佬能多多支持！
#

# ============================================================
# 本地图片清单（共 18 张）
# ============================================================
# 001.png  <-  计算公式
# 002.png  <-  计算代码
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
# 014.png  <-  回归分析
# 015.png  <-  回归分析
# 016.png  <-  回归分析
# 017.png  <-  回归分析
# 018.png  <-  回归分析

# ============================================================
# 作者代码（按原文出现顺序，共 1 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    if idx < 243 or pd.to_datetime(date_str) >= pd.to_datetime('2026-01-01'):
        return pd.DataFrame({})
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['volume', 'close', 'open', 'turnover'])
    rtn = data.to_dataframe('close') / data.to_dataframe('open') - 1
    vol = data.to_dataframe('volume')
    money = data.to_dataframe('turnover')
    data.to_dataframe('volume')
    tmp_cap = self.cap.iloc[idx - 243].reindex(data.codes)
    tr = vol / tmp_cap.values.reshape(1, -1)
    vol = (np.log(rtn.abs() / vol)).diff()
    money = (np.log(rtn.abs() / money)).diff()
    tr = (np.log(rtn.abs() / tr)).diff()
    res = []
    for data in [vol, money, tr]:
        tmp = data.replace(np.inf, np.nan)
        tmp = tmp.replace(-np.inf, np.nan)
        mkt_vol = tmp.mean(axis=1)
        mkt_rtn = rtn.mean(axis=1)
        denominator = (np.square(mkt_rtn - mkt_vol - (mkt_rtn.mean() - mkt_vol.mean()))).sum()
        ap_beta1 = (rtn - rtn.mean().values.reshape(1, -1)) * ((mkt_rtn - mkt_rtn.mean()).values.reshape(-1, 1))
        ap_beta1 = ap_beta1.sum()/ denominator
        # ap_beta2 = (tmp - tmp.mean().values.reshape(1, -1)) * ((mkt_rtn - mkt_rtn.mean()).values.reshape(-1, 1))
        # ap_beta2 = ap_beta2.sum() / denominator
        ap_beta3 = (rtn - rtn.mean().values.reshape(1, -1)) * ((mkt_vol- mkt_vol.mean()).values.reshape(-1, 1))
        ap_beta3 = ap_beta3.sum()/ denominator
        res.append(ap_beta1)
        res.append(ap_beta3)
        #
        # ap_beta4 = (tmp - tmp.mean().values.reshape(1, -1)) * ((mkt_vol- mkt_vol.mean()).values.reshape(-1, 1))
        # ap_beta4 = ap_beta4.sum() / denominator
    res = pd.concat(res, axis=1)
    res.columns = ['ap_beta1_vol', 'ap_beta3_vol', 'ap_beta1_money', 'ap_beta3_money', 'ap_beta1_tr', 'ap_beta3_tr']
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 这个代码没有什么难度，都是按照公式来计算各个因子。
#
# (作者注) 因此，这里就不赘述了，如果您对代码有疑问的话，可以评论区留言，笔者会对其进行解答的。

