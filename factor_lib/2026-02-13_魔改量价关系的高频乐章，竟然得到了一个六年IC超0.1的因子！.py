"""魔改量价关系的高频乐章，竟然得到了一个六年IC超0.1的因子！

自动生成自 ../sources/general/articles/2026-02-13_魔改量价关系的高频乐章，竟然得到了一个六年IC超0.1的因子！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-02-13_魔改量价关系的高频乐章，竟然得到了一个六年IC超0.1的因子！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 魔改量价关系的高频乐章，竟然得到了一个六年IC超0.1的因子！
# 日期    : 2026-02-13
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494798&idx=1&sn=83dc086434abfe9878072f763806ba1b
# 本地原文: ../sources/general/articles/2026-02-13_魔改量价关系的高频乐章，竟然得到了一个六年IC超0.1的因子！.md
# 本地图片: ../sources/general/articles/images/2026-02-13_魔改量价关系的高频乐章，竟然得到了一个六年IC超0.1的因子！/  (共 17 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **量价关系的高频乐章**
#
# 本文，笔者选择魔改的因子是《市场微观结构剖析系列6——量价关系的高频乐章》这篇研报中的一个因子。
#
# 这篇研报是朱定豪和严佳炜两位老师在2020年2月27日发布的。
#
# 这篇研报中一共介绍了四个因子，笔者曾经在[量价关系的高频乐章，连续五年IC绝对值超过0.1！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489336&idx=1&sn=2f35188bae2670bfbbb4e9062d3f48f6&scene=21#wechat_redirect)复现了其中的一个。这个因子的IC和分层回测的表现都是不错的。
#
# 值得一提的是，这篇文章的下方迎来了一位大佬的评价，他表示这个因子稍微改动一下就能实盘了。
#
# 遗憾的是，笔者当时没有看到这条评论。
#
# 幸运的是，鬼使神差地看到了这条评论。于是，笔者决定对他进行魔改。
#
# **计算思想和代码**
#
# 在之前的文章中笔者复现的是滞后一期对数收益率绝对值与成交额的相关性。
#
# 众所周知，成交额和成交量具有很高的相关性。用两者计算两个不同的因子之间的相关性可能会接近1。
#
# 根据笔者之前的多次尝试，两个相关性很高的因子相减是有可能出现一个效果更好的因子的。但是，本文笔者暂时不想尝试这种做法，因为最近关于这一类黑科技写太多了，感觉大家都要审美疲劳了。等到将来某个合适的时机，笔者再进行这样的尝试。
#
# **1**
#
# **计算思想**
#
# 本文，笔者用的是换手率替换掉了成交额。
#
# 同时，用[邪修！或许这才是换手率因子的正确打开方式，分层回测效果显著提升！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494731&idx=1&sn=d9124d8e466624575fe06d0fa0c510ad&scene=21#wechat_redirect)这篇文章中的方式处理了一下换手率。
#
# 然后，再按照同标的过去21个交易日同分钟的数据进行z-score标准化。
#
# 最后，计算滞后一期对数收益率绝对值和它的相关性。
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
# 这两个因子的相关性还是挺高的，超过了0.7。
#
# 从IC分析和分层回测的结果来看，这两个因子差距不是太大，看起来tr\_new这个因子的IC略高一点点，而分层回测则是两者各有优势。
#
# 所以，接下来展示的因子评价结果还是以tr\_new为主，tr仅展示一下分层回测结果供各位大佬对比。
#
# ## IC分析
# 这个IC的表现真的很不错了，有六年超过了0.1，其中还有1年到达了0.12。即使是最低的一年，也接近0.08了。
#
# 如果是tr因子，其2023年的IC绝对值离0.12还有一点微小的距离。
#
# ## 收益分析
# 虽然这个因子在IC上的表现很出色，但是其分层回测的表现可以说是差了那么一点点，黄线的年化收益超过了蓝线。
#
# tr因子其在分层回测上的优势是，黄线和蓝线的差距不是那么大， 但是它的单调性也不是很好，其红线的年化收益率看起来超过了绿线。
#
# 今天是大A在蛇年的最后一个交易日了，祝大家在马年涨不停。
#
# 不出意外的话，春节期间，笔者也会继续更新的，希望各位大佬能够多多点赞分享推荐和关注支持支持。
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
# 017.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    cur = pd.to_datetime(date_str) + timedelta(hours=15)
    if cur <= pd.to_datetime('2010-01-01') or cur >= pd.to_datetime('2026-01-01'):
        return pd.DataFrame(columns=['tr', 'tr_new'])
    # 加载当日分钟数据
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close'], codes=self.codes).to_dataframes()
    ret = np.abs(np.log(1 + data['close'].pct_change().shift(1)))
    tr_new, tr = [], []
    for i in range(idx - 20, idx + 1):
        file_name = self.files[i]
        full_path = os.path.join(self.file_pth, file_name)
        vol = BaseDataLoader.load_data(full_path, fields=['volume'], codes=self.codes).to_dataframe('volume')
        cap = self.market_cap['circulating_cap'].iloc[i - 243]
        cap = cap.values.reshape(1, -1)
        self.tr = vol / cap
        self.neutralize(idx)
        tr_new.append(self.res)
        tr.append(self.tr)
    tr = pd.concat(tr)
    tr['minute'] = tr.index.hour * 60 + tr.index.minute
    tr = tr.groupby('minute', as_index=False, group_keys=False).apply(self.z_score)
    tr_new = pd.concat(tr_new)
    tr_new['minute'] = tr_new.index.hour * 60 + tr.index.minute
    tr_new = tr_new.groupby('minute', as_index=False, group_keys=False).apply(self.z_score)
    res = pd.concat([ret.corrwith(tr), ret.corrwith(tr_new)])
    res.columns = ['tr', 'tr_new']
    res['datetime'] = cur
    return res

# (作者注) 第一段代码，主要起到一个读取数据的作用。
#
# (作者注) 这当中新的内容应该是第19行，调用了neutralize这个方法对换手率进行行业市值中性化。

# --- 代码块 2 ---
def neutralize(self, idx):
    self.res = []
    df = pd.concat([self.ind_data.iloc[idx - 1458], self.market_cap['market_cap'].iloc[idx - 243]], axis=1)
    df.columns = ['ind', 'cap']
    df.groupby('ind', as_index=False, group_keys=False).apply(self.__neutralize__)
    self.res = pd.concat(self.res, axis=1)

# (作者注) 这里需要注意的是，第3行。
#
# (作者注) 因为行业数据是从2010年1月1日开始的，市值数据从2025年1月1日开始，而分钟行情数据是从2004年1月1日开始的，所以它们之间有个gap。

# --- 代码块 3 ---
def __neutralize__(self, group):
    group.sort_values(by='cap', inplace=True)
    start = 0
    for q in [0.3, 0.7, 1]:
        end = int(len(group) * q)
        tmp_group = group.iloc[start:end]
        codes = tmp_group.index.tolist()
        self.res.append(self.tr[codes] - self.tr[codes].mean(axis=1).values.reshape(-1, 1))
        start = end

# (作者注) 这里的话，就是按照行业市值对标的分类，然后批量对每个交易日所有分钟数据进行中性化。

