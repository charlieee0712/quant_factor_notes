"""自身显著性和自身显著性反转因子，原来写因子可以如此简单！

自动生成自 ../sources/zhengzhaolei/articles/2025-05-05_自身显著性和自身显著性反转因子，原来写因子可以如此简单！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/zhengzhaolei/articles/images/2025-05-05_自身显著性和自身显著性反转因子，原来写因子可以如此简单！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: zhengzhaolei
# 公众号  : 量化拯救散户
# 标题    : 自身显著性和自身显著性反转因子，原来写因子可以如此简单！
# 日期    : 2025-05-05
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247488322&idx=1&sn=352e6af32fe6066a2fca819ad52dc2e7
# 本地原文: ../sources/zhengzhaolei/articles/2025-05-05_自身显著性和自身显著性反转因子，原来写因子可以如此简单！.md
# 本地图片: ../sources/zhengzhaolei/articles/images/2025-05-05_自身显著性和自身显著性反转因子，原来写因子可以如此简单！/  (共 55 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:29

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 在介绍了日内时间分域和日内价格分域之后，研报中还有一个分域显著性的因子。
#
# 在研报中，提出了三种不同的分域显著性，分别是价格分域，成交量分域和时间分域。
#
# 前两个，研报中是这么说的，由于个股日内的分钟级别数据存在较大的随机性，因此我们采用切片方式来提高分域的鲁棒性。我们分域的核心处理方式为：采用不重叠方法分域，再构建域内特征数据。具体来说，我们首先按照不重叠原则，将需要被分域的时间序列数据进行特征序列刻画。进一步，我们对特征序列进行等频分域。最后，我们计算每个分域内的量价特征。
#
# 笔者暂时没有理解这段话的意思，所以这两个分域暂时是复现不了了。
#
# 第三个，时间分域就简单了，半小时一切片即可。
#
# 对于时间分域，又有两类因子，一类是自身显著性，另一类是自身显著性反转。
#
# 自身显著性=max((abs(因子值)-abs(因子值的均值))/(abs(因子值)+abs(因子值的均值)))。
#
# 自身显著性反转就是自身显著性乘上其对应分域区间的收益率。
#
# 同时，对于每一类，研报当中又给出了两个选择。也就是计算自身显著性时候的因子值，同样有多种选择。研报给出的是收益率和成交量，笔者自己又加了个波动率。这样一来，就时间分域，按照这个思路就能产生六个因子了。

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
# 成交量自身显著性
#
# ## 收益分析
# 收益率自身显著性
#
# 一个可能不是那么好的因子，至少笔者测出来不太行，无论是标准差合成还是均值合成，其结果都很一般。
#
# 波动自身显著性反转
#
# ## 收益分析
# 成交量自身显著性反转
#
# ## 收益分析
# 收益率自身显著性反转
#
# ## 收益分析
# 总结：前两个因子都是用均值合成效果更好，后面的因子和收益率扯上了关系之后，就变成了标准差合成效果更好了。所以上面的因子评价结果，除了前两个，后面的都是标准差合成的结果。
#
# 从分层回测结果可以看出，后面的自身显著性反转因子就比较一般了，
#

# ============================================================
# 本地图片清单（共 55 张）
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
# 作者代码（按原文出现顺序，共 3 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]

    # 加载当日分钟数据
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close', 'open', 'volume'])
    dfs = data.to_dataframes()

    ret = dfs['close'] / dfs['open'] - 1
    sigma = ret.rolling(30).std()
    vol = dfs['volume'].rolling(30).sum()
    vol = vol.div(dfs['volume'].sum(axis=0), axis=1)

    idx = list(range(29, 240, 30))
    sigma = self.cal_factors(sigma, idx)
    vol = self.cal_factors(vol, idx)

    ret_30 = dfs['close'] / dfs['open'].shift(29) - 1
    intraDSStd_byT = sigma.max(axis=0)
    intraDSVol_byT = vol.max(axis=0)
    new_ret_30 = self.cal_factors(ret_30, idx)
    intraDSRtn_byT = new_ret_30.max(axis=0)

    intraDSS2td_byT = intraDSStd_byT * self.get_max_rtn(sigma, ret_30.iloc[idx])
    intraDS2Vol_byT = intraDSVol_byT * self.get_max_rtn(vol, ret_30.iloc[idx])
    intraDS2Rtn_byT = intraDSRtn_byT * self.get_max_rtn(new_ret_30, ret_30.iloc[idx])

    res = pd.concat([intraDSStd_byT, intraDSVol_byT, intraDSRtn_byT,
                     intraDSS2td_byT, intraDS2Vol_byT, intraDS2Rtn_byT], axis=1)
    res.columns = ['intraDSStd_byT', 'intraDSVol_byT', 'intraDSRtn_byT',
                   'intraDSS2td_byT', 'intraDS2Vol_byT', 'intraDS2Rtn_byT']
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    res.index.name = 'code'
    return res.reset_index()

# (作者注) 这里的代码也变长了很多，同时还调用了两个其他的方法。
#
# (作者注) 第8行之前，都是加载数据的。
#
# (作者注) 第10-11行，计算每30分钟的波动性。
#
# (作者注) 第12-13行，计算每30分钟的成交量占比。
#
# (作者注) 第15行，按照每半小时对数据切片。
#
# (作者注) 第16-17行，调用cal\_factors方法计算波动和成交量对应的(abs(因子值)-abs(因子值的均值))/(abs(因子值)+abs(因子值的均值))。这里没有直接求max，因为后面计算分域显著性反转的时候还需要最大值的索引。
#
# (作者注) 第19行，计算每30分钟的收益率。
#
# (作者注) 第20、21和23行，计算波动、成交量和收益率的自身分域显著性因子。
#
# (作者注) 第25-27行，调用get\_max\_rtn方法，计算自身分域显著性反转因子。

# --- 代码块 2 ---
@staticmethod
def cal_factors(data, idx):
    data = data.iloc[idx]
    res = np.abs(data.sub(data.mean(axis=0), axis=1))
    res = res / data.abs().add(data.abs().mean(axis=0), axis=1)
    return res

# (作者注) cal\_factors方法就是按照公式实现。
#
# (作者注) 第3行，是每半小时去一次数据。

# --- 代码块 3 ---
@staticmethod
def get_max_rtn(data, rtn):
    idx = data.dropna(how='all', axis=1).idxmax(axis=0)
    return pd.Series({col: rtn.loc[row, col] for col, row in idx.items()})

# (作者注) get\_mat\_rtn就是取(abs(因子值)-abs(因子值的均值))/(abs(因子值)+abs(因子值的均值))这个值最大的区间所对应的收益率。
#
# (作者注) 这里需要注意第三行，需要将全为nan的列去掉，不然会出现NaT（not a time）导致第四行代码报错。
#
# (作者注) 波动自身显著性

