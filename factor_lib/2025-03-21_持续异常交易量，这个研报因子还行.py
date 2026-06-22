"""持续异常交易量，这个研报因子还行

自动生成自 ../sources/general/articles/2025-03-21_持续异常交易量，这个研报因子还行.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-03-21_持续异常交易量，这个研报因子还行/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 持续异常交易量，这个研报因子还行
# 日期    : 2025-03-21
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247486493&idx=1&sn=584fd9415f446c7fb60e75296958460a
# 本地原文: ../sources/general/articles/2025-03-21_持续异常交易量，这个研报因子还行.md
# 本地图片: ../sources/general/articles/images/2025-03-21_持续异常交易量，这个研报因子还行/  (共 55 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文，笔者将带来招商证券在2023年的研报《“持续异常交易量”选股因子PATV》中提到的PATV因子。
#
# 这个因子首先要计算每分钟的异常交易量，就是用t分钟的交易量/过去一段时间交易量的均值。这里的过去一段时间，可以是过去一个交易日，但是笔者在使用的使用用的是过去20个交易日。
#
# 然后计算日内持续异常交易量，即每分钟异常交易量序列的均值除以标准差然后加上峰度。
#
# 这三个pandas都提供了对应的函数，均值是mean，标准差是std，峰度是kurt。

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
# ## 收益分析
# 5min
#
# ## 收益分析
# 10min
#
# ## 收益分析
# 30min
#
# ## 收益分析
# 60min
#
# ## 收益分析
# 总结：这个因子用1分钟的数据计算的IC绝对值还是不错的，频率越低效果越差，到60分钟的时候就完全不能用了。
#

# ============================================================
# 本地图片清单（共 55 张）
# ============================================================
# 001.png  <-  (文章开头)
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
# 012.png  <-  IC分析
# 013.png  <-  IC分析
# 014.png  <-  IC分析
# 015.png  <-  IC分析
# 016.png  <-  IC分析
# 017.png  <-  IC分析
# 018.png  <-  回归分析
# 019.png  <-  回归分析
# 020.png  <-  换手率分析
# 021.png  <-  换手率分析
# 022.png  <-  收益分析
# 023.png  <-  IC分析
# 024.png  <-  IC分析
# 025.png  <-  IC分析
# 026.png  <-  IC分析
# 027.png  <-  IC分析
# 028.png  <-  IC分析
# 029.png  <-  回归分析
# 030.png  <-  回归分析
# 031.png  <-  换手率分析
# 032.png  <-  换手率分析
# 033.png  <-  收益分析
# 034.png  <-  IC分析
# 035.png  <-  IC分析
# 036.png  <-  IC分析
# 037.png  <-  IC分析
# 038.png  <-  IC分析
# 039.png  <-  IC分析
# 040.png  <-  回归分析
# 041.png  <-  回归分析
# 042.png  <-  换手率分析
# 043.png  <-  换手率分析
# 044.png  <-  收益分析
# 045.png  <-  IC分析
# 046.png  <-  IC分析
# 047.png  <-  IC分析
# 048.png  <-  IC分析
# 049.png  <-  IC分析
# 050.png  <-  IC分析
# 051.png  <-  回归分析
# 052.png  <-  回归分析
# 053.png  <-  换手率分析
# 054.png  <-  换手率分析
# 055.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]
    if idx < 20:
        return pd.Series(name = pd.to_datetime(date_str) + timedelta(hours=15))

    data = BaseDataLoader.load_data(os.path.join(self.file_pth, file_name), fields=['volume'])
    mu = self.last_mean.iloc[idx-20]
    vol = data.to_dataframe('volume')
    vol = (vol.div(mu.reindex(data.codes, axis=1), axis=1)).rank(axis=1, pct=True)
    res = vol.mean(axis=0) / vol.std(axis=0) + vol.kurt(axis=0)
    res.name = pd.to_datetime(date_str) + timedelta(hours=15)
    return res

# (作者注) 这个代码没有什么难度。为了方便并行计算，笔者将过去20天每分钟成交量的均值保存了下来。如果是x分钟的数据的话，就将这个均值乘上x即可了。

# --- 代码块 2 ---
def __call__(self):
    # res = []
    if not os.path.exists('./last_mean.parquet') and self.freq == 1:
        for i in tqdm(range(len(self.files))):
            self.cal_mu(i)
        self.last_mean = pd.concat(self.last_mean, axis=1).T
        self.last_mean.to_parquet('./last_mean.parquet')
    else:
        self.last_mean = self.freq * pd.read_parquet('./last_mean.parquet')
    res = self.run()
    res = pd.concat(res, axis=1).T
    res.index.name = 'datetime'
    res = pd.melt(res.reset_index(), id_vars='datetime', var_name='code', value_name=self.name)

# (作者注) 好了，以上就是关于代码和因子计算的部分。挺简单的，但是因子的效果还是不错的。
#
# (作者注) 1min

