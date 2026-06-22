"""高频类反转因子，和之前分域思想很像！

自动生成自 ../sources/qinchuantao/articles/2025-05-07_高频类反转因子，和之前分域思想很像！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/qinchuantao/articles/images/2025-05-07_高频类反转因子，和之前分域思想很像！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: qinchuantao
# 公众号  : 量化拯救散户
# 标题    : 高频类反转因子，和之前分域思想很像！
# 日期    : 2025-05-07
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247488423&idx=1&sn=b4fa8f9ca4210de0b41eeac360c78883
# 本地原文: ../sources/qinchuantao/articles/2025-05-07_高频类反转因子，和之前分域思想很像！.md
# 本地图片: ../sources/qinchuantao/articles/images/2025-05-07_高频类反转因子，和之前分域思想很像！/  (共 79 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:27

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文复现的是2019年7月21日由长江证券的覃川桃老师发布的研报《基础因子研究（八）：高频因子（三），高频因子研究框架》。
#
# 在这篇研报中，介绍了两类因子。
#
# 第一类，流动性溢价因子，这个因子的计算需要《高频因子（一）：流动性溢价因子》中的相关内容，笔者暂时还没有找到这篇研报，所以暂时不实现这一类因子了。
#
# 第二类，高频类反转因子。
#
# 这一类又分成了四类，分别是基础类、全局类、分割类和开盘类。
#
# 基础类有一个因子，就叫做基础反转因子，其计算为日对数收益率等权和。
#
# 全局类有两个因子，一个是高频反转因子，计算为k线对数收益率成交量加权和；另一个是结构化反转因子，在上一篇文章中有介绍，即反转区间反转因子-动量区间反转因子。
#
# 分割类也有两个因子，一个是动量区间反转因子，另一个则是反转区间反转因子。这两个区间通过成交量的大小来划分，K线成交量小于10%分位数的为动量区间，大于的为反转区间。对于动量区间的对数收益率用成交量的倒数加权求和，对反转区间的对数收益率用的则是成交量加权求和。
#
# 开盘类同样也有两个因子，第一个是开盘反转因子，即高频k线每日开盘对数收益率等权（成交量）求和；第二个是去开盘反转因子，顾名思义就是去掉开盘数据后的对数收益率等权（成交量）求和。
#
# 笔者在复现的时候，对开盘类因子两种不同的加权方式都进行了实现，而对基础类因子则没有复现，下面是因子计算的代码。

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
# 结构化反转因子
#
# ## 收益分析
# 高频反转因子
#
# ## 收益分析
# 去开盘反转因子（等权）
#
# ## 收益分析
# 去开盘反转因子（成交量加权）
#
# ## 收益分析
# 开盘反转因子（等权）
#
# ## 收益分析
# 开盘反转因子（成交量加权）
#
# ## 收益分析
# 总结：开盘反转因子无论用什么方式加权都不太行，去开盘反转因子的话用成交量加权好于等权。其他的几个因子就差不多了。
#

# ============================================================
# 本地图片清单（共 79 张）
# ============================================================
# 001.png  <-  (文章开头)
# 002.png  <-  (文章开头)
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
# 014.png  <-  IC分析
# 015.png  <-  IC分析
# 016.png  <-  IC分析
# 017.png  <-  IC分析
# 018.png  <-  IC分析
# 019.png  <-  IC分析
# 020.png  <-  回归分析
# 021.png  <-  回归分析
# 022.png  <-  换手率分析
# 023.png  <-  换手率分析
# 024.png  <-  收益分析
# 025.png  <-  IC分析
# 026.png  <-  IC分析
# 027.png  <-  IC分析
# 028.png  <-  IC分析
# 029.png  <-  IC分析
# 030.png  <-  IC分析
# 031.png  <-  回归分析
# 032.png  <-  回归分析
# 033.png  <-  换手率分析
# 034.png  <-  换手率分析
# 035.png  <-  收益分析
# 036.png  <-  IC分析
# 037.png  <-  IC分析
# 038.png  <-  IC分析
# 039.png  <-  IC分析
# 040.png  <-  IC分析
# 041.png  <-  IC分析
# 042.png  <-  回归分析
# 043.png  <-  回归分析
# 044.png  <-  换手率分析
# 045.png  <-  换手率分析
# 046.png  <-  收益分析
# 047.png  <-  IC分析
# 048.png  <-  IC分析
# 049.png  <-  IC分析
# 050.png  <-  IC分析
# 051.png  <-  IC分析
# 052.png  <-  IC分析
# 053.png  <-  回归分析
# 054.png  <-  回归分析
# 055.png  <-  换手率分析
# 056.png  <-  换手率分析
# 057.png  <-  收益分析
# 058.png  <-  IC分析
# 059.png  <-  IC分析
# 060.png  <-  IC分析
# 061.png  <-  IC分析
# 062.png  <-  IC分析
# 063.png  <-  IC分析
# 064.png  <-  回归分析
# 065.png  <-  回归分析
# 066.png  <-  换手率分析
# 067.png  <-  换手率分析
# 068.png  <-  收益分析
# 069.png  <-  IC分析
# 070.png  <-  IC分析
# 071.png  <-  IC分析
# 072.png  <-  IC分析
# 073.png  <-  IC分析
# 074.png  <-  IC分析
# 075.png  <-  回归分析
# 076.png  <-  回归分析
# 077.png  <-  换手率分析
# 078.png  <-  换手率分析
# 079.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    # 加载当日分钟数据
    if idx < 20:
        return pd.DataFrame(columns=['code', 'datetime', 'rev_rev', 'rev_mom', 'rev_struct',
                                     'rev_hf', 'rev_no_open', 'rev_no_open_vol', 'rev_open', 'rev_open_vol'])
    ret = []
    vol = []
    for i in range(idx-20, idx+1):
        file_name = self.files[i]
        full_path = os.path.join(self.file_pth, file_name)
        data = BaseDataLoader.load_data(full_path, fields=['volume', 'close', 'open'])
        ret.append(np.log(data.to_dataframe('close') / data.to_dataframe('open')))
        vol.append(data.to_dataframe('volume'))
    date_str = file_name.split('.')[0]

    ret = pd.concat(ret)
    vol = pd.concat(vol)
    thd = vol.quantile(0.1)
    flag = vol > thd
    rev_flag = np.where(flag, 1, np.nan)
    mom_flag = np.where(flag, np.nan, 1)

    rev_weights = vol * rev_flag
    rev_weights = rev_weights.div(rev_weights.sum(axis=0), axis=1)
    rev_rev = (rev_weights * ret).sum(axis=0)
    
    mom_weights = 1 / (vol * mom_flag)
    mom_weights = mom_weights.replace(np.inf, np.nan).replace(-np.inf, np.nan)
    mom_weights = mom_weights.div(mom_weights.sum(axis=0), axis=1)
    rev_mom = (mom_weights * ret).sum(axis=0)

    rev_struct = rev_rev - rev_mom

    weights = vol.div(vol.sum(axis=0), axis=1)
    rev_hf = (ret * weights).sum(axis=0)

    ret['flag'] = self.get_flag(ret)
    vol['flag'] = self.get_flag(vol)

    weights_no_open = vol[vol['flag']]
    weights_no_open = weights_no_open.div(weights_no_open.sum(axis=0), axis=1)
    rev_no_open = ret[ret['flag']].sum(axis=0)
    rev_no_open_vol = (ret[ret['flag']] * weights_no_open).sum(axis=0)

    weights_open = vol[~vol['flag']]
    weights_open = weights_open.div(weights_open.sum(axis=0), axis=1)
    rev_open = ret[~ret['flag']].sum(axis=0)
    rev_open_vol = (ret[~ret['flag']] * weights_open).sum(axis=0)

    res = pd.concat([rev_rev, rev_mom, rev_struct, rev_hf, rev_no_open.drop(columns=['flag']),
                     rev_no_open_vol.drop(columns=['flag']), rev_open.drop(columns=['flag']),
                     rev_open_vol.drop(columns=['flag'])], axis=1)
    res.columns = ['rev_rev', 'rev_mom', 'rev_struct', 'rev_hf',
                   'rev_no_open', 'rev_no_open_vol', 'rev_open', 'rev_open_vol']
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    res.index.name = 'code'
    return res.reset_index()

# (作者注) 这次，笔者采取了21个交易日的数据一起计算，同时为了避免内存溢出，选择了5分钟的数据来进行复现。研报中用到的数据是10分钟、5分钟和2分钟，除了5分钟，其他两种K线都不太常见。同时，在上一篇文章复现的结构化反转因子来看，5分钟数据的表现会好于1分钟的数据。综合这两点，这里采取了5分钟的数据来复现这一系列因子。
#
# (作者注) 第6-17行，读取过去21个交易日的数据，并拼接为1个dataframe。
#
# (作者注) 第18-21行，划分动量区间和反转区间。
#
# (作者注) 第23-25行，计算反转区间反转因子。
#
# (作者注) 第27-30行，计算动量区间反转因子。
#
# (作者注) 第32行，计算结构化反转因子。
#
# (作者注) 第34-35行，计算高频反转因子。
#
# (作者注) 第37-38行，获取开盘数据的flag。这里，笔者将第一条k线作为开盘数据。
#
# (作者注) 第40-43行，计算去开盘反转因子。
#
# (作者注) 第45-48行，计算开盘反转因子。

# --- 代码块 2 ---
@staticmethod
def get_flag(df):
    df['flag'] = df.index.day
    df['flag'] = df['flag'] == df['flag'].shift(1)
    return df['flag']

# (作者注) get\_flag方法根据日期来获取是否为每日第一根k线。
#
# (作者注) 在因子评价的过程中，笔者发现动量区间反转因子的效果不行，所以就不展示了。至于其他因子，他们的效果都不如每日计算一个因子，然后对过去21个交易日去标准差的做法。但是，这里还是展示以下直接用过去21个交易日的分钟k线数据一起计算的因子。
#
# (作者注) 反转区间反转因子

