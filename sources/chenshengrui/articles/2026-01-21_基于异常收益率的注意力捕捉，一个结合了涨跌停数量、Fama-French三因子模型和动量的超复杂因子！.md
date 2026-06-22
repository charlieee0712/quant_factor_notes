---
account: 量化拯救散户
author: 量化拯救散户
date: '2026-01-21'
fetched_at: '2026-06-22T02:20:12'
title: 基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！
url: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247494289&idx=1&sn=ac78d20e2d7ae806dd70c3ecea64ed73
---

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/MA6hRUd7yGuqOzPBGDicxBaEq6CBu248CbE9yLOd34j3qF0V5qiaOCaqCoHibUAib7iaovFwSBRgialhceATP6SraaHQ/640?wx_fmt=gif&from=appmsg)

**基于异常收益率的注意力捕捉**

本文，笔者将介绍一个超级复杂的因子，这个因子来自中信建投陈升锐老师的研报《投资者有限关注及注意力捕捉与溢出》。

这篇研报中有多个因子，在此之前笔者对两个实现起来相对容易的因子进行了复现，在[基于日常收益的注意力溢出，一个IC和分层回测俱佳的因子！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490377&idx=1&sn=9278ded584d008824cb74e206f2a7cfd&scene=21#wechat_redirect)和[基于日常换手率的注意力溢出，效果会让人大吃一惊！](https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247490446&idx=1&sn=2ef37c5222769e2a70abd4888cdca079&scene=21#wechat_redirect)这两篇文章中。

本文复现的因子叫做基于异常收益率的注意力捕捉，是一个超级复杂的因子，它考虑了涨跌停标的占比、Fama-French三因子模型和动量。

关于这个因子的逻辑，2025年的《因子日历》中是这样描述的，不同股票对同一市场关注度事件的反映程度往往是不同的，可借助个股收益对市场关注度事件的敏感程度来衡量股票对该事件的注意力捕捉效应；捕捉能力越强（敏感程度越高），表明个股更能吸引市场注意，从而导致买盘压力增大，股价高估；上述因子以异常收益占比作为市场关注度事件，极端日收益率是衡量关注度的一个重要指标。出现较高或较低收益都代表关注度高。

**计算步骤和代码**

从计算步骤来看，这个因子就是一个时序回归。

但是，不得不说，它真的很复杂。

**1**

**计算步骤**

以标的的日收益率为被解释变量，以涨跌停占比（可以是全市场的，也可以是标的所属行业的）、市场收益率、SMB因子收益率、HML因子收益率和UMD因子收益率。

其中，SMB因子收益率和HML因子收益率的计算方式和Fama-French三因子模型一致；而UMD因子收益率则是用过去12个月到过去1个月的收益率排序，然后用前30%标的组合的收益率减去后30%的。

**2**

**代码**

```python
def __call__(self):
    self.ind_data = BaseDataLoader.load_data('../../data/sw_industry.parquet', fields=['sw_l1_code']
                                        ).to_dataframe('sw_l1_code')
    start = self.ind_data.index.tolist()[0]
    codes = self.ind_data.columns.tolist()
    self.data = BaseDataLoader.load_data('../../data/stock_bar_1day.parquet', fields=['close', 'limit_up',
                                                                                  'limit_down', 'factor'],
                                    codes=codes, start=start, lag=400).to_dataframes()
    market_limit_num = (self.data['close'] == self.data['limit_up']) + (self.data['close'] == self.data['limit_down'])
    self.market_limit_num = market_limit_num.iloc[267:].mean(axis=1)
    price = self.data['close'] * self.data['facotr']
    self.umd = (price.shift(252) / price.shift(21) - 1).iloc[267:]
    self.rtn = (price.pct_change()).iloc[267:]
    self.market_cap = BaseDataLoader.load_data('../../data/capital.parquet',
                                               fields=['market_cap', 'pb_ratio'], codes=codes,
                                               start=start).to_dataframes()
    premium = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_premium)(idx)
        for idx in range(len(self.rtn))
    )
    premium = pd.concat(premium)
    premium.index.name = 'code'
    premium.reset_index(inplace=True)
    self.codes = self.rtn.columns.tolist()
    self.premium = BaseDataLoader.from_dataframe(premium, codes=self.codes).to_dataframes()
    res = Parallel(n_jobs=16, verbose=10)(
        delayed(self.cal_beta)(idx)
        for idx in range(21, len(self.rtn) + 1)
    )
    res = pd.concat(res)
    res.reset_index(inplace=True)
    res.to_parquet('./factor.parquet')
```

第2-5行，读取行业数据，并确定开始时间和标的数量。这样，后面读取行情和估值数据就能直接对齐了。

第6-8行，读取行情数据，这次除了读取收盘价和复权因子，还读取了涨停价和跌停价。

第9-10行，计算全市场涨跌停标的的占比。

第11-13行，计算日频收益率和动量因子（UMD）。

第14-16行，读取了pb和市值数据用来计算Fama-French三因子模型中的市场收益率、SMB因子收益率和HML因子收益率。

第17-20行，调用cal\_premium方法计算因子溢价（因子收益率）。

第21-25行，用BaseDataLoader类将因子溢价的dataframe转换为多个数据透视表。

第26-29行，调用cal\_beta计算最后的因子。

```python
def cal_premium(self, idx):
    day = self.ind_data.iloc[[idx]].index.tolist()[0]
    df = pd.concat([self.data['close'].iloc[idx], self.data['limit_up'].iloc[idx],
                    self.data['limit_down'].iloc[idx], self.ind_data.iloc[idx]], axis=1)
    df.columns = ['close', 'limit_up', 'limit_down', 'ind']
    ind_limit_num = df.groupby('ind', as_index=False, group_keys=False).apply(self.cal_limit_num)
    umd_data = pd.concat([self.rtn.iloc[idx], self.umd.iloc[idx],
                          self.market_cap['market_cap'].iloc[idx]], axis=1)
    umd_data.columns = ['rtn', 'umd', 'market_cap']
    umd_premium, mkt_rtn = self.cal_umd_premium(umd_data)
    fama_data = pd.concat([self.rtn.iloc[idx], 1 / self.market_cap['pb_ratio'].iloc[idx],
                          self.market_cap['market_cap'].iloc[idx]], axis=1)
    fama_data.columns = ['rtn', 'bp', 'market_cap']
    smb, hml = self.cal_fama(fama_data)
    tot_data = ind_limit_num.to_frame()
    tot_data.insert(0, 'mkt_limit_num', self.market_limit_num.iloc[idx])
    tot_data.insert(2, 'mkt_rtn', mkt_rtn)
    tot_data.insert(3, 'umd', umd_premium)
    tot_data.insert(4, 'smb', smb)
    tot_data.insert(5, 'hml', hml)
    tot_data['datetime'] = day
    return tot_data
```

第2行，确定当前计算的时间戳。

第3-6行，拼接数据计算行业中涨跌停标的的比例。

第6-10行，计算UMD因子的因子溢价和市场收益率。

第11-14行，计算SMB和HML因子的因子溢价。

第15行，将series转换为dataframe。

第16-21行，插入计算的结果。

```python
@staticmethod
def cal_limit_num(group):
    group = group.dropna()
    res = (group.iloc[:, 0] == group.iloc[:, 1]) + (group.iloc[:, 0] == group.iloc[:, 2])
    group['ind_limit_num'] = np.sum(res) / len(group)
    return group['ind_limit_num']
```

这个方法计算行业涨跌停占比，比较简单。

```python
def cal_umd_premium(self, data):
    data = data.dropna()
    data.sort_values(by='umd', inplace=True)
    l = int(len(data) * 0.3)
    umd_low = self.__cal_rtn__(data.iloc[:l, :])
    umd_high = self.__cal_rtn__(data.iloc[-l:, :])
    mkt_rtn = self.__cal_rtn__(data)
    return umd_high - umd_low, mkt_rtn
```

这个方法计算UMD因子的因子溢价。

第2行，去掉nan值。

第3行，按照umd因子排序。

第4行，计算30%的标的数量。

第5-7行，计算UMD因子溢价和市场收益率。

```python
def cal_fama(self, data):
    data = data.dropna()
    data = data.sort_values(by='market_cap')
    l1 = len(data) // 2
    s = data.iloc[:l1, :].sort_values(by='bp')
    b = data.iloc[l1:, :].sort_values(by='bp')
    start = 0
    s_premium, b_premium = [], []
    for q in [0.3, 0.7, 1]:
        end = int(l1 * q)
        s_premium.append(self.__cal_rtn__(s.iloc[start:end]))
        b_premium.append(self.__cal_rtn__(b.iloc[start:end]))
        start = end
    smb = np.mean(s_premium) - np.mean(b_premium)
    hml = (s_premium[-1] + b_premium[-1]) * 0.5 - (s_premium[0] + b_premium[0]) * 0.5
    return smb, hml
```

SMB和HML因子溢价的计算和UMD的其实是类似的，唯一需要理解的就是Fama-French的原理。当然，笔者的实现和最初的Fama-French不同，笔者是按照全市场每日的pb和市值来计算，Fama-French是按照一个固定的时间（一年一次）重新计算分组然后，并且标的池可以是沪深300。

```python
@staticmethod
def __cal_rtn__(data):
    data['market_cap'] = data['market_cap'] / data['market_cap'].sum()
    return (data['rtn'] * data['market_cap']).sum()
```

这个方法是为了避免重复代码写的，也很简单。

```python
def cal_beta(self, idx):
    y = self.rtn.iloc[idx-21:idx, :]
    day = y.index.tolist()[-1]
    res = []
    for code in self.codes:
        tmp = pd.concat([y.loc[:, code], self.premium['mkt_limit_num'].loc[:, code],
                         self.premium['ind_limit_num'].loc[:, code], self.premium['umd'].loc[:, code],
                         self.premium['smb'].loc[:, code], self.premium['hml'].loc[:, code],
                         self.premium['mkt_rtn'].loc[:, code]], axis=1).dropna()
        res.append(self.__cal_beta__(tmp))
    res = pd.DataFrame(res, columns=['mkt', 'ind'], index=self.codes)
    res['datetime'] = day
    return res
@staticmethod
def __cal_beta__(data):
    y = data.iloc[:, 0].values
    if len(y) < 5:
        return [np.nan] * 2
    beta = []
    for i in range(1,3):
        x = data.iloc[:, [i, 2, 3, 4, 5, 6]].values
        x = np.c_[np.ones((len(data), 1)), x]
        beta_full = np.linalg.pinv(x.T @ x) @ x.T @ y
        beta.append(abs(beta_full[1]))
    return beta
```

最后就是时序回归部分了，这部分最近介绍了很多次了，也不赘述了。

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/001.png)

**因子评价**

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/002.png)

从相关性来看，用全市场涨跌停标的占比和行业内涨跌停占比计算的因子相关性不高。

从IC上来看，两个因子是差不多的，分层回测区别较大，但是都不好。所以，这里就简单展示一下ind因子的评价结果了。

**01**

**IC分析**

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/003.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/004.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/005.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/006.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/007.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/008.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/008.png)

**02**

**回归分析**

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/009.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/010.png)

**03**

**换手率分析**

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/011.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/012.png)

**04**

**收益分析**

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/013.png)

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/014.png)

这个因子没啥好总结的了，毕竟它的复杂程度就能阻止大部分人使用它了。

不过，从学习的角度来看，复现一下这个因子对个人能力的提升还是有一些的，如果对量化感兴趣又不知道怎么上手的话，可以尝试以下从复现这种复杂的因子开始。

最后，希望各位大佬能够点赞分享推荐和关注，支持一下笔者。

![](images/2026-01-21_基于异常收益率的注意力捕捉，一个结合了涨跌停数量、Fama-French三因子模型和动量的超复杂因子！/001.png)

**- *END* -**

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/MA6hRUd7yGuqOzPBGDicxBaEq6CBu248CbE9yLOd34j3qF0V5qiaOCaqCoHibUAib7iaovFwSBRgialhceATP6SraaHQ/640?wx_fmt=gif&from=appmsg)