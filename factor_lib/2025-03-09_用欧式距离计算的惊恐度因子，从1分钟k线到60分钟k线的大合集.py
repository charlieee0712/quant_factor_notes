"""用欧式距离计算的惊恐度因子，从1分钟k线到60分钟k线的大合集

自动生成自 ../sources/general/articles/2025-03-09_用欧式距离计算的惊恐度因子，从1分钟k线到60分钟k线的大合集.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-03-09_用欧式距离计算的惊恐度因子，从1分钟k线到60分钟k线的大合集/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 用欧式距离计算的惊恐度因子，从1分钟k线到60分钟k线的大合集
# 日期    : 2025-03-09
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247485610&idx=1&sn=b03824f3c7f1b3b31d31762d3b3a6b9e
# 本地原文: ../sources/general/articles/2025-03-09_用欧式距离计算的惊恐度因子，从1分钟k线到60分钟k线的大合集.md
# 本地图片: ../sources/general/articles/images/2025-03-09_用欧式距离计算的惊恐度因子，从1分钟k线到60分钟k线的大合集/  (共 56 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文，我们将介绍一个因子。这个因子的思想是从研报来的，但是被笔者改进了。
#
# 新的因子，没有使用市场收益，而是直接计算标的与其余标的之间的欧式距离，并取等权平均。
#
# 原来的研报的名字忘记了，后续找到了的话补充在评论里面吧。
#
# 从结果来看，瞎改没有任何好处，这因子简直不能看。但是之前，笔者用日频的收益率进行改造，看起来是比原始因子有提升的。
#
# 不过，如果等权的话，净值曲线可能会好看的。但是，某券商大佬曾经给笔者提过建议，等权的净值曲线好大概率是因为小票导致的，波动率肯定也大很多，所以不能完全说明是你的因子好。
#
# 好了，废话说了很多了，接下来看一看代码。

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
# (原文有相关段标题 [IC分析 / 回归分析 / 换手率分析 / 收益分析]，但均为图片，无独立文本；图片见下方清单)

# ============================================================
# 本地图片清单（共 56 张）
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
# 012.png  <-  收益分析
# 013.png  <-  IC分析
# 014.png  <-  IC分析
# 015.png  <-  IC分析
# 016.png  <-  IC分析
# 017.png  <-  IC分析
# 018.png  <-  IC分析
# 019.png  <-  回归分析
# 020.png  <-  回归分析
# 021.png  <-  换手率分析
# 022.png  <-  换手率分析
# 023.png  <-  收益分析
# 024.png  <-  IC分析
# 025.png  <-  IC分析
# 026.png  <-  IC分析
# 027.png  <-  IC分析
# 028.png  <-  IC分析
# 029.png  <-  IC分析
# 030.png  <-  回归分析
# 031.png  <-  回归分析
# 032.png  <-  换手率分析
# 033.png  <-  换手率分析
# 034.png  <-  收益分析
# 035.png  <-  IC分析
# 036.png  <-  IC分析
# 037.png  <-  IC分析
# 038.png  <-  IC分析
# 039.png  <-  IC分析
# 040.png  <-  IC分析
# 041.png  <-  回归分析
# 042.png  <-  回归分析
# 043.png  <-  换手率分析
# 044.png  <-  换手率分析
# 045.png  <-  收益分析
# 046.png  <-  IC分析
# 047.png  <-  IC分析
# 048.png  <-  IC分析
# 049.png  <-  IC分析
# 050.png  <-  IC分析
# 051.png  <-  IC分析
# 052.png  <-  回归分析
# 053.png  <-  回归分析
# 054.png  <-  换手率分析
# 055.png  <-  换手率分析
# 056.png  <-  收益分析

# ============================================================
# 作者代码（按原文出现顺序，共 6 个代码块）
# ============================================================

# --- 代码块 1 ---
def calculate_single_column(df, j):
    """计算单列与其他列的恐惧距离"""
    col_vector = df.values[:, j:j + 1]  # 保持二维结构
    distances = np.sqrt(np.square(col_vector - df.values))
    valid_distances = np.delete(np.nanmean(distances, axis=0), j)
    return np.nanmean(valid_distances)

# (作者注) 这个函数，就是用笔者改进的方法来计算惊恐度的，计算j列收益率与其他列收益率的欧氏距离的均值。

# --- 代码块 2 ---
class FearXMin:
    def __init__(self, file_pth):
        pass

    def _load_last_day_close(self):
        """加载每日最后一分钟收盘价"""
        pass

    def run(self):
        """主执行函数"""
        pass

    def process_single_day(self, idx):
        """处理单日数据"""
        pass

# (作者注) 同时，我们定义了一个类，专门计算x分钟的惊恐度。
#
# (作者注) 在这个类中，有四个函数，分别是初始化函数\_\_init\_\_，加载每日最后x分钟收盘价的函数\_load\_ladt\_day\_close（因为笔者的数据是每日的数据一个parquet的，所以为了计算每日第一个x分钟的收益率需要用到上一日最后x分钟的收盘价），主执行函数run和处理单日数据的函数process\_signle\_day。

# --- 代码块 3 ---
def __init__(self, file_pth):
    self.file_pth = file_pth
    self.files = sorted([f for f in os.listdir(file_pth) if f.endswith('.parquet')])
    self.last_close = self._load_last_day_close()

# (作者注) \_\_init\_\_函数，读取文件列表，并调用\_load\_last\_day\_close函数。

# --- 代码块 4 ---
def _load_last_day_close(self):
    """加载每日最后一分钟收盘价"""
    results = []
    for f in tqdm(self.files, desc='Loading last close'):
        # 使用DuckDB快速查询最后一条记录
        last_time = f.split('.')[0] + ' 15:00:00'

        query = f"""
        SELECT datetime, code, close
        FROM '{os.path.join(self.file_pth, f)}' 
        WHERE datetime = '{str(last_time)}'
        """
        df = duckdb.query(query).fetchdf()
        results.append(
            df.pivot(index='datetime', columns='code', values='close')
        )
    results = pd.concat(results)
    results.index = results.index.astype(str)
    return results

# (作者注) 该函数循环读取每一个文件，并将每个文件的最后一条收盘价数据合并成dataframe。
#
# (作者注) 第8-12行，获取最后一个时间戳所有标的收盘价的sql。
#
# (作者注) 第13行，将其变成dataframe。
#
# (作者注) 第14-16行，将其变成行是时间，列是对应标的dataframe。

# --- 代码块 5 ---
def run(self):
    """主执行函数"""
    # 外层并行
    results = Parallel(n_jobs=8, verbose=10)(
        delayed(self.process_single_day)(idx)
        for idx in range(len(self.files))
    )

    # 整理结果
    result_df = pd.concat(results, axis=1).T
    result_df.index.name = 'datetime'
    result_df.reset_index(inplace=True)
    result_df = pd.melt(result_df, id_vars='datetime', var_name='code', value_name='fear_60min')
    result_df.to_parquet('fear_xmin.parquet')

# (作者注) 第4-7行，用joblib包的并行计算加速。
#
# (作者注) 第10-14行，整理结果并保存。

# --- 代码块 6 ---
def process_single_day(self, idx):
    """处理单日数据"""
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]

    # 加载当日分钟数据
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['close'])

    if idx == 0:
        last_df = pd.DataFrame()
    else:
        last_df = self.last_close.iloc[[idx-1]]

    # 合并最后收盘价
    combined_df = pd.concat([
        last_df,
        data.to_dataframe('close')
    ])
    combined_df.index = combined_df.index.astype(str)
    combined_df.sort_index(inplace=True)
    # 计算收益率（避免除零错误）
    returns = combined_df.pct_change().iloc[1:]

    # 内层并行：计算所有股票的距离指标
    n_stocks = len(data.codes)
    fear_values = Parallel(n_jobs=-1, prefer='threads')(
        delayed(calculate_single_column)(returns, j)
        for j in range(n_stocks)
    )

    return pd.Series(fear_values, index=data.codes, name=pd.to_datetime(date_str) + timedelta(hours=15))

# (作者注) 第3-8行，加载idx对应交易日的数据。
#
# (作者注) 第10-13行，获取该交易日前一个交易日收盘价数据。
#
# (作者注) 第16-21行，将起一个交易日的收盘价数据与当日的数据合并，并按照时间戳排序。
#
# (作者注) 第23行，计算收益率。
#
# (作者注) 第26-30行，用joblib包并行调用calculate\_single\_column函数计算惊恐度。
#
# (作者注) 需要注意的是，计算出来每天都有一个惊恐度，在分析的时候我们选取了最近21个交易日的做平均。同时，nanmean会出现所有值都是nan，但是均值为0的情况，所以简单的将所有结果为0的都换成nan。理论上，也不存在某一标的收益率不为nan，但是惊恐度为0的情况。因为这意味着其他所有标的和他的收益率序列都是一样的。

