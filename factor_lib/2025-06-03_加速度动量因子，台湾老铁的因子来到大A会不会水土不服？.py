"""加速度动量因子，台湾老铁的因子来到大A会不会水土不服？

自动生成自 ../sources/general/articles/2025-06-03_加速度动量因子，台湾老铁的因子来到大A会不会水土不服？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2025-06-03_加速度动量因子，台湾老铁的因子来到大A会不会水土不服？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 加速度动量因子，台湾老铁的因子来到大A会不会水土不服？
# 日期    : 2025-06-03
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489180&idx=1&sn=08cabda24fe84e4c4475802ab53f9491
# 本地原文: ../sources/general/articles/2025-06-03_加速度动量因子，台湾老铁的因子来到大A会不会水土不服？.md
# 本地图片: ../sources/general/articles/images/2025-06-03_加速度动量因子，台湾老铁的因子来到大A会不会水土不服？/  (共 12 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文，笔者将复现加速度动量因子。
#
# 这个因子不是来自券商的研报，而是来自两位台湾学者在2013年发表的论文《Investor Attention, Visual Price Pattern, and Momentum Investing》。
#
# 这个因子叫做加速度动量，其计算过程需要用到日频数据，并且需要进行线性回归。
#
# 线性回归的被解释变量，也就是y，用的是价格，这里笔者用收盘价。
#
# 线性回归的解释变量，也就是x，用的是时间等差序列（1，2，3，……，21）和时间等差序列的平方。
#
# 时间平方的回归系数被称作加速度动量，时间的回归系数被称为价格涨跌强弱。
#
# 关于这个因子，有这样的一段解释。
#
# 加速度动量衡量了股票历史价格上涨或下跌的速度（对历史价格的visual pattern的刻画）；当股票呈现“价格处于上涨（下跌）趋势且价格走势加速上涨（下跌）”模式时，更能吸引投资者注意力并引起过度反应，进而获得比传统动量更高的收益。

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
# 本地图片清单（共 12 张）
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

# ============================================================
# 作者代码（按原文出现顺序，共 1 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    tmp_y = self.data.iloc[idx - 21:idx].dropna(how='all', axis=1)
    Y_full = tmp_y.dropna(axis=1)
    idx_full, Y_full = Y_full.columns, Y_full.values

    tmp_y['t'] = np.arange(1, 22, 1)
    tmp_y['t_square'] = np.square(tmp_y['t'])
    X_full = np.c_[np.ones((21, 1)), tmp_y[['t', 't_square']].values]
    beta_full = np.linalg.pinv(X_full.T @ X_full) @ X_full.T @ Y_full
    r2 = compute_r_squared(X_full @ beta_full, Y_full)
    factor_full = pd.DataFrame(data=beta_full.T, index=idx_full, columns=['alpha', 'beta', 'gama'])
    factor_full['r2'] = r2

    factor_lack = {}
    for c in set(tmp_y.columns) - set(idx_full) - {'t', 't_square'}:
        lack_tmp_y = tmp_y.loc[:, [c, 't', 't_square']].copy()
        lack_tmp_y = lack_tmp_y.dropna()
        lack_tmp_x = lack_tmp_y[['t', 't_square']]
        if len(lack_tmp_y) < 10:
            factor_lack[c] = [np.nan] * 4
            continue
        X_lack = np.c_[np.ones(len(lack_tmp_y)), lack_tmp_x.values]
        Y_lack = lack_tmp_y.drop(columns=['t', 't_square']).values
        beta_lack = np.linalg.pinv(X_lack.T @ X_lack) @ X_lack.T @ Y_lack
        r2 = compute_r_squared(X_lack @ beta_lack, Y_lack)
        factor_lack[c] = np.hstack((beta_lack.reshape(-1), r2))
    if factor_lack:
        factor_lack = pd.DataFrame(factor_lack).T
        factor_lack.columns = ['alpha', 'beta', 'gama', 'r2']
        factor_full = pd.concat([factor_full, factor_lack])
    factor_full['datetime'] = tmp_y.index[-1]
    factor_full.index.name = 'code'
    return factor_full.reset_index()

# (作者注) 关于这段回归的代码，在最早的Barra系列中就有过说明。后来，在介绍价格时滞因子的时候，又进行了说明。这一段代码，是在价格时滞因子的基础上进行的改进。
#
# (作者注) 主要分为两部分，第一部分是前12行，对没有缺失值的标的用最小二乘的公式批量进行回归。除动量加速度和价格涨跌强弱这两个因子外，笔者还将alpha和r方都作为因子一并计算了。
#
# (作者注) 从14-26行，就是对有缺失值的标的一个一个进行最小二乘计算因子。
#
# (作者注) 从相关性来看，价格涨跌强弱（beta）和加速度动量（gama）这两个因子的相关性很高。
#
# (作者注) 从因子评价的效果来看，这四个因子都很差。看来，台湾同胞的研究并不适合大A市场。
#
# (作者注) 所以，在接下来的结果展示中，笔者也就展示一下加速度动量的因子评价结果，这样也和本文的标题所对应。

