"""邪修！聪明钱因子3.0版本，IC和分层回测全方面的提升！

自动生成自 ../sources/general/articles/2025-10-29_邪修！聪明钱因子3.0版本，IC和分层回测全方面的提升！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-10-29_邪修！聪明钱因子3.0版本，IC和分层回测全方面的提升！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 邪修！聪明钱因子3.0版本，IC和分层回测全方面的提升！
# 日期    : 2025-10-29
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247491161&idx=1&sn=cf4df4ff883d989bb9c24ae64abaf53d
# 本地原文: ../sources/general/articles/2025-10-29_邪修！聪明钱因子3.0版本，IC和分层回测全方面的提升！.md
# 本地图片: ../sources/general/articles/images/2025-10-29_邪修！聪明钱因子3.0版本，IC和分层回测全方面的提升！/  (共 15 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 在很久很久之前，笔者围绕着聪明钱因子进行了一系列的研究。
#
# [聪明钱因子，IC虽然不高，但分层回测还不错！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247487419&idx=1&sn=65f73c2e96f4c451ec69de89d0753217&scene=21#wechat_redirect)和[聪明钱因子模型的2.0版本，思路打开，因子变多也变好！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247488086&idx=1&sn=021f3488e65c5e7a08d899cf9bea86b9&scene=21#wechat_redirect)这两篇文章是复现了魏建榕老师的研报，然后在这个基础上笔者进行了第一次的邪修，有了[根据“待著而救”因子改进“聪明钱”因子，会取得更好的效果吗？](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247487588&idx=1&sn=5cb6ed71b0fd2daf57619331a46b785b&scene=21#wechat_redirect)这篇文章。
#
# 本文，将是笔者第二次对聪明钱的因子进行改进。
#
# **计算步骤和代码**
#
# 本文用放量时刻的vwap价格与不放量时刻的vwap价格的比值作为聪明钱因子的3.0版本。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，计算每分钟的成交量数据与过去21个交易日同分钟的成交量数据相比，是否大于均值+1倍标准差。如果满足这一条件，则认为这一分钟属于放量时刻。
#
# 第二步，计算放量时刻的vwap价格（放量时刻的成交额之和/放量时刻的成交量之和）与不放量时刻的vwap价格。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 由于在之前的因子评价中，笔者是使用的是过去21个交易日的均值除以过去21个交易日的标准差来合成月度因子的。
#
# 因为，这种方式得到的因子分层回测的单调性比较好，所以这里展示的也是用这种方式合成的。
#
# ## IC分析
# 虽然，IC超过0.08的年份数量一样，但是整体来说，这个因子的IC值略微高一点点。前三年的超过了0.09，2023年的超过了0.12，这都是比之前高的。
#
# ## 收益分析
# 此外，从分层回测来看，这个3.0版本的因子表现也是更好的。
#
# 笔者对于这一次邪修的因子还是比较满意的。
#
# 也希望各位读者多多支持，你们的每一次关注、点赞、分享、收藏和喜欢都是笔者继续更新的动力。
#

# ============================================================
# 本地图片清单（共 15 张）
# ============================================================
# 001.png  <-  (文章开头)
# 002.png  <-  代码
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
# 015.png  <-  - *END* -

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    if idx < 20:
        return pd.DataFrame({})
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    vol = []
    fields = ['volume']
    for i in range(idx-20,idx+1):
        file_name = self.files[i]
        full_path = os.path.join(self.file_pth, file_name)
        if i == idx:
            fields.append('turnover')
        data = BaseDataLoader.load_data(full_path, fields=fields)
        vol.append(data.to_dataframe('volume'))
    flag = self.z_score(vol)
    codes = flag.columns.tolist()
    cur_vol = vol[-1].reindex(columns=codes)
    amt = data.to_dataframe('turnover').reindex(columns=codes)
    vwap_large_vol = (amt * np.where(flag, 1, np.nan)).sum() / (cur_vol * np.where(flag, 1, np.nan)).sum()
    vwap_small_vol = (amt * np.where(flag, np.nan, 1)).sum() / (cur_vol * np.where(flag, np.nan, 1)).sum()
    res = vwap_large_vol / vwap_small_vol
    res.name = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 第14行之前的代码是用来读取数据的，需要注意的是，成交量数据每天读取并保存在vol这个list中；成交额因子只需要读取最后一个交易日的。
#
# (作者注) 第15行，调用z\_score方法来计算哪些分钟属于放量时刻。
#
# (作者注) 第16-18行，对其flag、cur\_vol和amt这三个dataframe的columns。
#
# (作者注) 第19行，计算放量时刻的vwap价格。
#
# (作者注) 第20行，计算不放量时刻的vwap价格。
#
# (作者注) 第21行，计算聪明钱因子。

# --- 代码块 2 ---
def z_score(self, data):
    data = pd.concat(data)
    data['minute'] = data.index.hour * 60 + data.index.minute
    data = data.groupby('minute', as_index=False, group_keys=False).apply(self._z_score_)
    return data

# (作者注) 第2行，将过去21个交易日的成交量数据拼接为一个datafame。
#
# (作者注) 第3行，将时间转换为对应的分钟。
#
# (作者注) 第4行，对相同分钟groupby，然后调用\_z\_score\_方法得到最后一个交易日该分钟是否放量的flag。

# --- 代码块 3 ---
@staticmethod
def _z_score_(group, mode):
    thd = group.mean(axis=0) + group.std(axis=0)
    group = group > thd
    group = group.iloc[[-1]]
    return group.drop(columns=['minute'])

# (作者注) 最后一部分代码就是简单的计算了。

