"""转移熵系列因子，不会写代码，那就调包吧！

自动生成自 ../sources/zhengzhaolei/articles/2025-05-12_转移熵系列因子，不会写代码，那就调包吧！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/zhengzhaolei/articles/images/2025-05-12_转移熵系列因子，不会写代码，那就调包吧！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: zhengzhaolei
# 公众号  : 量化拯救散户
# 标题    : 转移熵系列因子，不会写代码，那就调包吧！
# 日期    : 2025-05-12
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247488696&idx=1&sn=9fe11ed13fab4330e534347e3d76c42a
# 本地原文: ../sources/zhengzhaolei/articles/2025-05-12_转移熵系列因子，不会写代码，那就调包吧！.md
# 本地图片: ../sources/zhengzhaolei/articles/images/2025-05-12_转移熵系列因子，不会写代码，那就调包吧！/  (共 23 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:29

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 这个因子，本应该在交易时间下的基础系列因子之前介绍的。
#
# 但是，笔者在写文章的时候，发现可能有点错误，于是就推迟到了今天。
#
# 可是，问题还是存在的。研报中提到了一个“转移熵”的概率，然后笔者研究了半天最后还是选择了直接调用第三方包来计算。
#
# 需要注意的是，x到y的转移熵，和y到x的转移熵是不一样的，转移熵月度说明x到y的因果关系越显著。因此，只有收益率和成交量占比这两个字段就能得到两个不同的转移熵，研报中将其用te\_v2r和te\_r2v来表示。
#
# 但是，这两个因子在笔者复现的时候效果并不好。然后，笔者加了两个te\_m2r和te\_r2m，m代表成交额占比。
#
# 这两个因子的效果和用成交量占比应该是一样的，或者说是差不多的，效果肯定也不会太好。

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
# (原文有相关段标题 [回归分析]，但均为图片，无独立文本；图片见下方清单)

# ============================================================
# 本地图片清单（共 23 张）
# ============================================================
# 001.png  <-  (文章开头)
# 002.png  <-  (文章开头)
# 003.png  <-  (文章开头)
# 004.png  <-  (文章开头)
# 005.png  <-  (文章开头)
# 006.png  <-  (文章开头)
# 007.png  <-  (文章开头)
# 008.png  <-  (文章开头)
# 009.png  <-  (文章开头)
# 010.png  <-  (文章开头)
# 011.png  <-  (文章开头)
# 012.png  <-  (文章开头)
# 013.png  <-  (文章开头)
# 014.png  <-  (文章开头)
# 015.png  <-  (文章开头)
# 016.png  <-  (文章开头)
# 017.png  <-  (文章开头)
# 018.png  <-  (文章开头)
# 019.png  <-  回归分析
# 020.png  <-  回归分析
# 021.png  <-  回归分析
# 022.png  <-  回归分析
# 023.png  <-  回归分析

# ============================================================
# 作者代码（按原文出现顺序，共 16 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    # 加载当日分钟数据
    file_name = self.files[idx]
    full_path = os.path.join(self.file_pth, file_name)
    data = BaseDataLoader.load_data(full_path, fields=['volume', 'close', 'open', 'high', 'low', 'turnover'])
    date_str = file_name.split('.')[0]

    vol = data.to_dataframe('volume').iloc[10:-10]
    vol = vol.div(vol.sum(axis=0), axis=1)
    money = data.to_dataframe('turnover').iloc[10:-10]
    money = money.div(money.sum(axis=0), axis=1)
    ret = (data.to_dataframe('close') / data.to_dataframe('open')).iloc[10:-10] - 1

    res = []
    for idx in range(len(ret.columns)):
        res.append(self.cal_factors(ret.iloc[:, idx].values, money.iloc[:, idx].values, vol.iloc[:, idx].values))
    res = pd.DataFrame(data=res, columns=['te_r2m', 'te_m2r', 'te_r2v', 'te_v2r'], index=ret.columns.tolist())
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    res.index.name = 'code'
    return res.reset_index()

# (作者注) 第3-6行，读取数据。
#
# (作者注) 第8-12行，数据预处理，计算成交量占比、成交额占比和收益率。
#
# (作者注) 第14-16行，调用函数，一个标的一个标的的计算转移熵。

# --- 代码块 2 ---
@staticmethod
def cal_factors(x, y1, y2):
    flag1 = ~np.isnan(x) & ~np.isnan(y1)
    if not np.any(flag1):
        return [np.nan] * 4
    flag2 = ~np.isnan(x) & ~np.isnan(y2)
    x = np.digitize(x, np.linspace(np.nanmin(x), np.nanmax(x), 10))
    y1 = np.digitize(y1, np.linspace(np.nanmin(y1), np.nanmax(y1), 10))
    y2 = np.digitize(y2, np.linspace(np.nanmin(y2), np.nanmax(y2), 10))
    te_r2m, te_m2r, te_r2v, te_v2r = 0, 0, 0, 0
    for i in range(1, 4, 1):
        te_r2m += pyinform.transfer_entropy(x[flag1], y1[flag1], k=i)
        te_m2r += pyinform.transfer_entropy(y1[flag1], x[flag1], k=i)
        te_r2v += pyinform.transfer_entropy(x[flag2], y2[flag2], k=i)
        te_v2r += pyinform.transfer_entropy(y2[flag2], x[flag2], k=i)
    return [te_r2m / 3, te_m2r / 3, te_r2v / 3, te_v2r / 3]

# (作者注) 第4-5行，防止成交量全为nan的情况，这种情况直接返回nan。
#
# (作者注) 第3行和第6行，去掉数据中的nan。
#
# (作者注) 第7-9行，将数据分为10桶，计算熵。
#
# (作者注) 第11-15行，根据研报的思维采用多期滞后的方式计算转移熵。这里笔者用三阶滞后尝试了一下。
#
# (作者注) 在计算完之后，又根据之前差分的思想，凭空捏造了四个因子。

# --- 代码块 3 ---
te_rm_diff = te_r2m - te_m2r。

# --- 代码块 4 ---
te_rv_diff = te_r2v - te_v2r。

# --- 代码块 5 ---
diff1 = te_r2m - te_r2v。

# --- 代码块 6 ---
diff2 = te_m2r - te_v2r。

# --- 代码块 7 ---
diff1

# --- 代码块 8 ---
IC分析

# --- 代码块 9 ---
回归分析

# --- 代码块 10 ---
换手率分析

# --- 代码块 11 ---
收益分析

# --- 代码块 12 ---
diff2

# --- 代码块 13 ---
IC分析

# --- 代码块 14 ---
换手率分析

# --- 代码块 15 ---
收益分析

# --- 代码块 16 ---
总结：这一系列因子，最后勉强能看的也就diff1和diff2这两个了，这两个因子都是通过标准差合成的。

