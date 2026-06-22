"""价差偏离度因子，难道是我的打开方式不对？

自动生成自 ../sources/general/articles/2025-07-07_价差偏离度因子，难道是我的打开方式不对？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-07-07_价差偏离度因子，难道是我的打开方式不对？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 价差偏离度因子，难道是我的打开方式不对？
# 日期    : 2025-07-07
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489425&idx=1&sn=de75464064fde198e3dc01e4028c69f8
# 本地原文: ../sources/general/articles/2025-07-07_价差偏离度因子，难道是我的打开方式不对？.md
# 本地图片: ../sources/general/articles/images/2025-07-07_价差偏离度因子，难道是我的打开方式不对？/  (共 22 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文，笔者要复现的因子叫做“价差偏离度因子”。这个因子，来自东方证券朱剑涛老师2016年5月12日在研报《因子选股系列研究之七：投机、交易行为与股票收益（下）》中提到的因子。
#
# 这个因子的计算分成三部。
#
# 第一步，每月月底在全市场搜索与股票 i 距离最近（相似度最高）的 N 只股票等权构该股票的特征组合，特征组合的净值价格我们称之为参考价格；
#
# 第二步，计算股票 i 的价格和参考价格的对数价差，即ln（股票价格）-ln（参考价格）；
#
# 第三步，对第二步的结果，在时序上进行z-score标准化，标准化的窗口长度为60。
#
# 至于股票间距离的计算，研报中是用1-两股票过去250个交易日涨跌幅的 pearson 相关系数。笔者在实现的时候进行了一点点简单的修改，笔者直接选择了相似度最高的10支票，和距离最近的10支是一个意思。

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
# 然后，笔者又按照之前的惯用手段，用标准差和均值这两种方式合成了以下。
#
# 在合成的过程中，笔者发现，均值的表现好于标准差。因此，接下来就只展示一下均值合成的结果了。
#
# 至于标准差合成的结果，2013年、2015年、2020年和2022年这四年的IC绝对值接近0。同时，只有2014年、2019年和2023年这三年的IC绝对值超过了0.02，其中2019年IC的方向还与其他年份不同。
#
# ## 收益分析
# 总结：这个因子如果按照研报的方式来合成最终的因子，那么它在2018年之后的表现从IC上来看是远不如2018年之前的。如果是用均值合成的话，那么2013年和2019年这两年的IC和其他年份完全相反。
#
# 值得一提的是，因子这篇研报是2016年5月12日发表的。因此，它在发表的时候回测的区间是2005年开始到2015年的。所以，在研报中的表现还是不错的。另外，笔者在复现的时候没有去掉st的股票，可能也会有一定的影响。
#
# 因此，这个因子的表现不行，可能就是笔者的打开方式不对吧。
#

# ============================================================
# 本地图片清单（共 22 张）
# ============================================================
# 001.png  <-  IC分析
# 002.png  <-  IC分析
# 003.png  <-  IC分析
# 004.png  <-  IC分析
# 005.png  <-  IC分析
# 006.png  <-  IC分析
# 007.png  <-  回归分析
# 008.png  <-  回归分析
# 009.png  <-  换手率分析
# 010.png  <-  换手率分析
# 011.png  <-  收益分析
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

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def __call__(self):
    self.data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close']
                                         ).to_dataframe('close')
    self.ret = self.data.pct_change()

    res = Parallel(n_jobs=16, verbose=10, backend=self.parallel)(
        delayed(self.process_single_day)(idx)
        for idx in range(252, len(self.data))
    )

    res = pd.concat(res, axis=1).T
    res.index.name = 'datetime'
    res.reset_index(inplace=True)
    res = pd.melt(res, id_vars='datetime', var_name='code', value_name='spread_bias')
    res.to_parquet('./spread_bias.parquet')

def process_single_day(self, idx):
    ret = self.ret.iloc[idx - 252:idx].dropna(how='all', axis=1)
    price = self.data.iloc[idx-1].dropna()
    ret = ret.reindex(price.index, axis=1)

    ret = ret.corr()
    ret.reset_index(inplace=True, drop=True)
    mask_matrix = np.eye(len(ret), dtype=bool)
    ret = ret.mask(mask_matrix)
    flag = ret > ret.quantile(1-10/len(ret))

    ref_price = price.values.reshape(-1, 1) * np.where(flag, 1, np.nan)
    ref_price = np.nanmean(ref_price, axis=0)
    price = np.log(price) - np.log(ref_price)
    return price

# (作者注) 这段代码中有两个方法。
#
# (作者注) 第一个，\_\_call\_\_用来读取数据，然后调用process\_single\_day方法来计算因子，并将计算的因子保存为一个parquet文件。
#
# (作者注) 第二个，process\_single\_day方法，是用来计算因子的。
#
# (作者注) 第18-20行，获取数据，这里笔者还是使用的252。
#
# (作者注) 第22行，计算相关性。
#
# (作者注) 第24-25行，将对角线上的值置为nan，即忽略自相关性。
#
# (作者注) 第26行，通过quantile来获取相关性最大的10个标的。
#
# (作者注) 第28-29行，计算股票的价格和参考价格的对数价差。
#
# (作者注) 在因子评价的时候，笔者先按照研报中第三步的方法，合成了一个因子，然后进行评价。
#
# (作者注) 合成的代码如下：

# --- 代码块 2 ---
def cal_ts_zscore(data):
    data = data.sub(data.mean(axis=0), axis=1).div(data.std(axis=0), axis=1)
    return data.iloc[[-1]]
    

if __name__ == '__main__':
    res = BaseDataLoader.load_data('./spread_bias.parquet').to_dataframe('spread_bias')
    data = Parallel(n_jobs=16, verbose=10)(
        delayed(cal_ts_zscore)(res.iloc[idx-63:idx])
        for idx in range(63, len(res))
    )
    data = pd.concat(data)

