"""我还是对它念念不忘！用换手率和振幅的相关性来识别算法交易，IC大幅提升！

自动生成自 ../sources/general/articles/2026-01-25_我还是对它念念不忘！用换手率和振幅的相关性来识别算法交易，IC大幅提升！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-01-25_我还是对它念念不忘！用换手率和振幅的相关性来识别算法交易，IC大幅提升！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 我还是对它念念不忘！用换手率和振幅的相关性来识别算法交易，IC大幅提升！
# 日期    : 2026-01-25
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494382&idx=1&sn=3ed01020d8920d716d332d76bd3f92e6
# 本地原文: ../sources/general/articles/2026-01-25_我还是对它念念不忘！用换手率和振幅的相关性来识别算法交易，IC大幅提升！.md
# 本地图片: ../sources/general/articles/images/2026-01-25_我还是对它念念不忘！用换手率和振幅的相关性来识别算法交易，IC大幅提升！/  (共 17 张)
# 段落识别: PARTIAL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **换手率和振幅的相关性**
#
# 不知从何时开始，笔者满脑子都是用因子来识别VWAP或TWAP这一类算法交易的参与度。之前，尝试过几次，比如[邪修！自创因子识别算法交易，好像有那味了！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494144&idx=1&sn=faa9a98d68a0ba2a03e0d354c47c1c66&scene=21#wechat_redirect)，又比如[一个瞎编的因子，我想从知情交易者的角度来强行解释一下他](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489844&idx=1&sn=29b3f77499fa435fb0d8c7ae85b3c5de&scene=21#wechat_redirect)。
#
# 但是，都太能令人满意。
#
# 不过，走火入魔的人是很难走出来的。于是，笔者继续研究，甚至到了对这个想法念念不忘的程度，可以说是这世界点点滴滴全部都是它。
#
# 在这样的一个背景下，笔者用换手率和振幅的相关性来构建了这样的一个因子，相关性低证明存在VWAP或者TWAP交易的概率越大，未来收益会上涨。
#
# **计算步骤和代码**
#
# 换手率和振幅的相关性，看起来挺简单的。不过，笔者利用这个思想构建了四个因子。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 第一步，计算振幅和换手率。这里需要注意的是，为了让每分钟都有振幅的数据，笔者采取的是（最高价-最低价）/开盘价的形式来计算振幅的。
#
# 第二步，计算相关性，这里一共有四个相关性。第一个，就是原始因子的相关性；第二个，对振幅和换手率按照过去21个交易日同分钟进行zscore标准化后计算相关性；第三个，对振幅和换手率进行截面zscore标准化后计算相关性；第四个，对振幅和换手率进行时序zscore标准化后计算相关性。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# (原文中无此段落)

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 从相关性来看，这四个因子之间的相关性是很高的，最低也有0.71。
#
# 按照世坤兼职顾问的标准，相关性超过0.7的话，需要夏普提升10%，不然就是要“扣钱”的因子。
#
# 因此，在因子评价的时候笔者选择了最简单的corr因子。同时，这个因子用过去21个交易日的均值合成的表现好于标准差的。
#
# ## IC分析
# 从IC来看，这个因子的IC绝对值有五年超过了0.06，这是远超之前因子的表现的。
#
# 由于ts\_zscore\_corr因子和它的相关性是1，所以它们是一样的。
#
# 至于zscore\_corr因子，其IC绝对值有两年超过了0.08，但是最高的一年没有超过0.1。
#
# 最差的就是same\_min\_corr这个因子了，它只有两年的IC绝对值超过了0.06。
#
# ## 收益分析
# 这个因子虽然在IC上有所提升了，但是分层回测的表现依旧是不尽如人意的。从某种意义上来说，它甚至不如zscore\_corr这个因子。
#
# 好了，这篇文章结束了。但是，这个因子依旧有缺陷，笔者肯定还会继续研究的，只不过这一次不知道需要思考多少时间，进行多少次尝试，才能获得一个超越这个因子的新因子。
#
# 希望大家能够喜欢，也希望大家能多多点赞分享推荐和关注支持一下笔者，你们的每一次支持将给笔者带来无穷的动力。
#

# ============================================================
# 本地图片清单（共 17 张）
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
# 001.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 1 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    # 加载当日分钟数据
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    cur = pd.to_datetime(date_str) + timedelta(hours=15)
    if idx < 243 or cur >= pd.to_datetime('2026-01-01'):
        return pd.DataFrame(columns=['same_min_corr', 'corr', 'ts_zscore_corr', 'zscore_corr', 'datetime'])
    tr, amp = [], []
    for i in range(idx - 20, idx + 1):
        file_name = self.files[i]
        full_path = os.path.join(self.file_pth, file_name)
        data = BaseDataLoader.load_data(full_path, fields=['volume', 'high', 'low', 'open'])
        cap = self.cap.iloc[i - 243].reindex(data.codes)
        cap = cap.values.reshape(1, -1)
        tr.append(data.to_dataframe('volume') / cap)
        tmp_amp = (data.to_dataframe('high') - data.to_dataframe('low')) / data.to_dataframe('open')
        amp.append(tmp_amp)
    tr_zscore_same_min = self.cal_zscore(tr)
    amp_zscore_same_min = self.cal_zscore(amp)
    cur_tr = tr[-1]
    cur_amp = amp[-1]
    cur_tr_ts_zscore = (cur_tr - cur_tr.mean().values.reshape(1, -1)) / cur_tr.std().values.reshape(1, -1)
    cur_tr_zscore = (cur_tr - cur_tr.mean(axis=1).values.reshape(-1, 1)) / cur_tr.std(axis=1).values.reshape(-1, 1)
    cur_amp_ts_zscore = (cur_amp - cur_amp.mean().values.reshape(1, -1)) / cur_amp.std().values.reshape(1, -1)
    cur_amp_zscore = (cur_amp - cur_amp.mean(axis=1).values.reshape(-1, 1)) / cur_amp.std(axis=1).values.reshape(-1, 1)
    res = pd.concat([amp_zscore_same_min.corrwith(tr_zscore_same_min),
                     cur_tr.corrwith(cur_amp),
                     cur_amp_ts_zscore.corrwith(cur_tr_ts_zscore),
                     cur_amp_zscore.corrwith(cur_tr_zscore)], axis=1)
    res.columns = ['same_min_corr', 'corr', 'ts_zscore_corr', 'zscore_corr']
    res['datetime'] = cur
    return res
def cal_zscore(self, data):
    data = pd.concat(data)
    data['minute'] = data.index.hour * 60 + data.index.minute
    data = data.groupby('minute', as_index=False, group_keys=False).apply(self.__cal_zscore__)
    return data
@staticmethod
def __cal_zscore__(group):
    group = group.drop(columns=['minute'])
    mu = group.mean().values.reshape(1, -1)
    sigma = group.std().values.reshape(1, -1)
    group = (group - mu) / sigma
    return group.iloc[[-1]]

# (作者注) 这段代码一共包含了三个方法，后两个方法在之前的多个因子当中（比如成交量的峰、岭、谷信息的系列文章中有过相关的介绍）。
#
# (作者注) 至于第一个方法，那就是读取数据，然后进行相关性计算了。
#
# (作者注) 第18-19行，调用后两个方法进行同分钟数据的zscore标准化。
#
# (作者注) 第22-25行，ts\_zscore代表时序zscore标准化，zscore代表截面zscore标准化。
#
# (作者注) 其他的也就没什么需要特别介绍的了。

