"""高频成交量的峰、岭、谷信息（四）：加权价格分位点因子，分层回测表现不错！

自动生成自 ../sources/weijianrong/articles/2025-08-02_高频成交量的峰、岭、谷信息（四）：加权价格分位点因子，分层回测表现不错！.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/weijianrong/articles/images/2025-08-02_高频成交量的峰、岭、谷信息（四）：加权价格分位点因子，分层回测表现不错！/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: weijianrong
# 公众号  : 量化拯救散户
# 标题    : 高频成交量的峰、岭、谷信息（四）：加权价格分位点因子，分层回测表现不错！
# 日期    : 2025-08-02
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247489785&idx=1&sn=de66ba27a23e7657cafada9fc5d16c15
# 本地原文: ../sources/weijianrong/articles/2025-08-02_高频成交量的峰、岭、谷信息（四）：加权价格分位点因子，分层回测表现不错！.md
# 本地图片: ../sources/weijianrong/articles/images/2025-08-02_高频成交量的峰、岭、谷信息（四）：加权价格分位点因子，分层回测表现不错！/  (共 33 张)
# 段落识别: SKELETON_ONLY  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T03:24:28

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# 本文，笔者将继续高频成交量的峰、岭、谷信息这一专题，介绍一下第四个大类因子，加权价格分位点因子。
#
# 这个因子的计算可以分成两步。
#
# 第一步，计算一个价格区间，这个价格区间的由昨日收盘价、日内最低价和日内最高价这三者中间的最大值和最小值组成。
#
# 第二步，每日各个状态（峰、岭和谷）成交量加权价格相对于上述价格区间的分位点。然后，去过去20个交易日的均值就得到了加权价格分位点因子。
#
# 根据研报的描述，上述因子中，量峰和量谷的加权价格分位点是有效的因子，而量岭加权价格分位点这个因子则是无效的。关于这一结论的验证，暂且按下不表，先来看一看具体的实现代码，深刻理解下这个因子的计算过程。

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
# 量岭
#
# ## 收益分析
# 量谷
#
# ## 收益分析
# 总结：从IC上的表现来看，这个因子的表现似乎并没有研报中说的那么好。无论是量峰还是量谷计算的加权价格分位数因子，似乎都不太行。但是，从分层回测的结果来看，量峰和量岭的加权价格分位数因子的表现还是不错的，相交的情况并不多，而且单调性也不错。
#
# 不过，和上一个大类因子类似，如果用标准差来合成月频因子的话，效果应该会好点，至少在IC上的表现会好点。这次，笔者偷懒一下，就不展示完整的因子评价的结果了，就用语言简单和均值合成的因子进行对比。
#
# 量峰，这个IC绝对值都没有比均值合成的更高，那么分层回测的结果也就可想而知了。
#
# 量岭，绝对值更高，但是分层回测就乱成一团麻了，五组之间可以说是没有任何区分度。
#
# 量谷，IC绝对值略高一点，分层回测依旧表现不佳。
#
# 值得一提的是，上述用标准差合成的月度因子与用均值合成的月度因子相比，IC的正负关系正好相反。
#
# 最后，感谢大家这段时间的支持。各位大佬能否动动手指，点点赞，点点喜欢，也点一点分享和关注，谢谢大家了。
#

# ============================================================
# 本地图片清单（共 33 张）
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

# ============================================================
# 作者代码（按原文出现顺序，共 1 个代码块）
# ============================================================

# --- 代码块 1 ---
def process_single_day(self, idx):
    if idx < 20:
        return pd.DataFrame({})
    file_name = self.files[idx]
    date_str = file_name.split('.')[0]

    vol = []
    price_range = []
    for i in range(idx-20,idx+1):
        file_name = self.files[i]
        full_path = os.path.join(self.file_pth, file_name)
        if i == idx - 1:
            data = BaseDataLoader.load_data(full_path, fields=['volume', 'close'])
            price_range.append(data.to_dataframe('close').iloc[-1])
        elif i == idx:
            data = BaseDataLoader.load_data(full_path, fields=['volume', 'close', 'high', 'low'])
            price_range.append(data.to_dataframe('high').max())
            price_range.append(data.to_dataframe('low').min())
        else:
            data = BaseDataLoader.load_data(full_path, fields=['volume'])
        vol.append(data.to_dataframe('volume'))
    flag = self.cal_flag(vol)

    price_range = pd.concat(price_range, axis=1)
    price_range = price_range.reindex(flag.columns)
    low = price_range.min(axis=1)
    high = price_range.max(axis=1)

    vol = data.to_dataframe('volume')
    vol = vol.reindex(flag.columns, axis=1)
    close = data.to_dataframe('close')
    close = close.reindex(flag.columns, axis=1)

    res = []
    for i in range(3):
        tmp_flag = np.where(flag == i, 1, np.nan)
        weight = vol * tmp_flag
        tmp_price = (close * (weight.div(weight.sum(), axis=1))).sum()
        res.append((tmp_price - low) / (high -  low))
    res = pd.concat(res, axis=1)
    res = res.replace(0.0, np.nan)
    res.columns = ['peak', 'ridge', 'valley']
    res['datetime'] = pd.to_datetime(date_str) + timedelta(hours=15)
    res.index.name = 'code'
    return res.reset_index()

# (作者注) 第9-20行，和之前一样，还是读取数据，只不过为了节省内存，这里进行了一点点修改。当读取到前一个交易日的时候才获取收盘价，当读取到当前交易日的时候才读取最高价和最低价。
#
# (作者注) 第24-27行，获取价格区间。
#
# (作者注) 后续的步骤就和上一个大类因子计算时差不多了，现时计算每个状态的成交量加权价格，然后（这个价格-最低价）/（最高价-最低价）就得到了加权价格分位点因子了。对应代码第39行，第36-38行是计算加权价格。
#
# (作者注) 量峰

