---
account: 量化拯救散户
author: 量化拯救散户
date: '2026-05-09'
fetched_at: '2026-05-26T07:36:39'
title: Betting Against Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？
url: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247496611&idx=1&sn=7d269a8739548bc69ba9e98e0907acd2
---

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/cvcTnuxE6ibaGd3B74hnwxbiawIoFc8o684suA4kZWdkX0xxuxVicacbibWMriaHQdIEWYZyJiaia82pSFrQ7GDekn2DrNmhUHuCw9OfP4SPFjRbJU/640?wx_fmt=gif&from=appmsg)

**Betting Against Beta**

这个因子是笔者在研究基金收益来源分析的时候发现的。

在五一假期之前，笔者发了篇文章来分析一个热门基金的收益来源，当时用的是Barra CNE6模型。结果，评论区有位大佬说这样做是不对的。

看到这位大佬的评论之后，笔者去请教了一些人，然后虚心并验证了一下，好像确实不对（为什么不对，就等到下一次对基金收益来源进行拆解的时候再说吧）。

就在笔者思考应该如何正确地对基金收益进行拆解的时候，《巴菲特的Alpha》这篇论文出现了（在孟岩老师的《投资第一课》中看到的，知道孟岩老师是2022年的时候，那时候笔者下载了一个叫做有知有行的App，用半年多时间在上面看了600篇文章）。

于是，果断下载下来学习，在学习的过程中发现需要用到两个全新的因子，一个就是本文要介绍的BAB，另一个则是QMJ。如果一切顺利，QMJ将在下周和大家见面。

**计算步骤和代码**

在论文中，这个因子的计算主要是用日频数据的。同时，它还提到了对于没有日频数据，只有月频数据的标的，也是可以用月频数据计算的，只不过计算时的一些参数不同。

因此，笔者认为这个因子也是可以用分钟级别的数据来计算的。但是，因为论文主推的是日频数据，所以这里仅以日频数据为例进行复现。

**1**

**计算步骤**

以标的收益率为被解释变量，滞后K期市场收益率为解释变量，进行时序回归，然后取时序回归的K个Beta的均值作为因子。

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/001.png)

为了减少异常值的影响，作者引用了一个放缩的操作。

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/002.png)

这里，带TS的Beta就是上面用时序回归估计出来的，而带XS的Beta则是截面均值。

但是作者又简化了处理。

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/003.png)

这个收缩的操作不会影响标的的因子排序，但是在构建零Beta的投资组合计算因子收益率的时候，它会影响到每个标的的权重，最后影响因子收益率。

至此，因子的计算介绍完了。

最后，还有参数需要说明，时序回归的窗口长度，以及之后K期到底是几期。

对于日频数据来说，时间窗口为1年，至少要有200个样本点。其最大滞后数为5，也就是一共会有6个Beta。

对于月频数据来说，时间窗口为3年，至少要有36个样本点。其最大滞后数为1。

**2**

**代码**

```python
def __call__(self):
    data = BaseDataLoader.load_data('../../data/stock/stock_bar_1day.parquet', fields=['close', 'factor']).to_dataframes()
    rtn = (data['close'] * data['factor']).pct_change()
    mkt_rtn = BaseDataLoader.load_data('../../data/index/index_bar_1day.parquet', fields=['close', 'factor'],
                                       codes=['000985.SH']).to_dataframes()
    mkt_rtn = (mkt_rtn['close'] * mkt_rtn['factor']).pct_change()
    for lag in range(1, 6):
        mkt_rtn[f'lag{lag}'] = mkt_rtn['000985.SH'].shift(lag)
    self.data = mkt_rtn.dropna().join(rtn)
    res = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_factors)(idx)
        for idx in range(252, len(self.data) + 1)
    )
    res = pd.DataFrame(res, index=self.data.index.tolist()[251:], columns=self.data.columns.tolist()[6:])
    res.index.name = 'datetime'
    res = 0.5 * res + 0.5
    res = pd.melt(res.reset_index(), id_vars='datetime', var_name='code', value_name='bab')
    res.to_parquet('./bab.parquet')
```

第一段代码主要就是读取数据，然后调用cal\_factors方法计算每日的因子值。

这里，笔者的市场收益使用的是中证全指。

第7-8行，计算的是滞后0-5期的市场收益率。

第9行，将市场收益率和标的收益率拼接在一起，这样的话索引0到5（包括5）就是解释变量。

```python
def cal_factors(self, idx):
    data = self.data.iloc[idx-252:idx]
    res = []
    for i in range(6, data.shape[1]):
        res.append(self.__cal_factors__(data.iloc[:, [0, 1, 2, 3, 4, 5, i]]))
    return res
def __cal_factors__(self, data):
    data = data.dropna()
    if len(data) < 200:
        return np.nan
    x = data.iloc[:, :-1].values
    y = data.iloc[:, -1:].values
    lr = LinearRegression()
    lr.fit(x, y)
    return np.mean(lr.coef_)
```

这两个方法就是取数然后线性回归了，没有什么需要特别说明的了。

**3**

**计算因子收益率**

因为，《巴菲特的Alpha》的作者是用这个因子的因子收益率对巴菲特的超额收益进行时序回归来分析巴菲特的投资组合的因子暴露的。

所以，还需要计算一次因子收益率。

在《Betting Against Beta》这篇文章中，它的因子收益率的计算和所有常见的因子都不一样！具体如下：

第一步，根据其估计贝塔值按升序排列，排名后的股票被分配到两个投资组合之一：低贝塔组合和高贝塔组合。

第二步，标的按其排名贝塔进行加权，组合在每个日历月重新平衡。

第三步，在组合形成时，两个组合都被重新调整，使其贝塔值均为1。

这里，笔者在计算的时候选择偷懒，改成每日调仓，因此只要计算每日每个标的的权重，然后乘以它们各自的收益率求和就行了。

```python
data = BaseDataLoader.load_data('./bab.parquet').to_dataframe('bab')
weight = data.rank(pct=True, ascending=False)
weight = weight - weight.mean(axis=1).values.reshape(-1, 1)
weight = weight / (weight.abs()).sum(axis=1).values.reshape(-1, 1)
weight_plus_decay = (data * np.where(weight > 0, weight, np.nan)).sum(axis=1).values.reshape(-1, 1)
weight_minus_decay = (data * np.where(weight < 0, weight, np.nan)).abs().sum(axis=1).values.reshape(-1, 1)
weight[weight > 0] = weight[weight > 0] / weight_plus_decay
weight[weight < 0] = weight[weight < 0] / weight_minus_decay
```

第1行，读取因子值。

第2-4行，计算每个标的的权重。

第5-6行，分别计算多头组和空头组的beta之和。

第7-8行，调整权重，使整个多空组合的beta暴露等于0。

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/004.png)

**因子评价**

虽然，研究这篇论文最初的目的是用来对基金收益率进行拆解的，但是，笔者也想看看这样计算出来的Beta因子到底有没有选股能力。

所以，还是弄了一个因子评价。

需要注意的是，这个因子再计算一下过去21个交易日的标准差之后的表现会更好。

**01**

**IC分析**

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/005.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/006.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/007.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/008.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/009.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/010.png)

这个因子的IC绝对值不算高，但是胜在稳定。

**02**

**回归分析**

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/011.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/012.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/013.png)

**03**

**换手率分析**

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/014.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/015.png)

**04**

**收益分析**

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/016.png)

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/017.png)

至于分层回测嘛，那就是普普通通，不算好但也谈不上差。

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/018.png)

**总结**

介绍这个因子的主要目的还是为了后面对基金收益率进行拆解的，顺便看了看用它来选股的效果。

在这种没有任何期待的情况下，它能有这样的表现真是有点出乎意料了。

如果各位大佬对笔者的创作内容感兴趣的话，能不能点赞推荐关注和分享支持一波呢？这真的很重要！

![](images/2026-05-09_Betting_Against_Beta，一个能解释巴菲特公开投资组合收益来源的因子，在大A会有怎么样的表现？/004.png)

**- *END* -**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/cvcTnuxE6ibbpmEBoe3YzJvUAcLzSt4xmBFSmwiaLQFBrDPY2Ug8CicxB3zDicibhJZDCiav2oyRKAsiadNotjtI9vCb3WSuGlqO8XY3SUNk4MGVDE/640?wx_fmt=gif&from=appmsg)