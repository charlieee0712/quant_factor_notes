"""成交量在价格上的分布，会比其在收益率上的分布因子表现更好吗？

自动生成自 ../sources/general/articles/2026-06-08_成交量在价格上的分布，会比其在收益率上的分布因子表现更好吗？.md。
所有 # 注释内容均直接摘录自原文，未经改写或归纳。
图片位于 ../sources/general/articles/images/2026-06-08_成交量在价格上的分布，会比其在收益率上的分布因子表现更好吗？/
"""

# ============================================================
# 来源
# ============================================================
# 来源标识: general
# 公众号  : 量化拯救散户
# 标题    : 成交量在价格上的分布，会比其在收益率上的分布因子表现更好吗？
# 日期    : 2026-06-08
# 原文 URL: https://mp.weixin.qq.com/s?__biz=MzkwNjYzMTEyMg==&mid=2247497167&idx=1&sn=c6b45d36e4dda278266ffec7d402ab9c
# 本地原文: ../sources/general/articles/2026-06-08_成交量在价格上的分布，会比其在收益率上的分布因子表现更好吗？.md
# 本地图片: ../sources/general/articles/images/2026-06-08_成交量在价格上的分布，会比其在收益率上的分布因子表现更好吗？/  (共 15 张)
# 段落识别: FULL  (FULL=三段齐备 / PARTIAL=部分 / SKELETON_ONLY=仅回测段 / NONE=无段标题)
# 生成时间: 2026-06-22T00:56:51

# ============================================================
# 导读（原文头部，至首个内容段标题或首个代码块前）
# ============================================================
# **成交量在价格上的分布**
#
# 本文，笔者将和各位大佬继续探讨一下东北证券王琦老师在2023年11月30日发布的研报《因子选股系列之六：日内成交量分布因子及Logsig-Alpha因子生成》。
#
# 在上周一的时候，笔者复现了这篇研报中的第三类因子，日内成交量在收益率上的分布相关的因子。这一主题一共四个因子，其中价格显著上行价稳量比稳定因子的表现还算不错。
#
# 按照一个月前的作风，笔者肯定会贴出介绍这个因子的文章链接，但是这样做导致了笔者被限流了，所以现在不敢了，只能麻烦各位大佬通过关键字搜索了。
#
# 同时，笔者现在也更需要各位大佬的支持，所以恳请各位大佬动动金手，多多点赞推荐关注和分享支持支持笔者。
#
# **计算步骤和代码**
#
# 这个主题下，一共两个因子。
#
# 这两个因子唯一的联系就是，都需要对日内价格进行分组。
#
# 具体为，对于每个标的按照日内价格分位数分成10组，计算每组的成交量之和，然后在此基础上计算因子。
#
# **1**

# ============================================================
# 作者原文 — 计算步骤
# ============================================================
# 成交量在价格上的分布偏移因子（v\_p\_skewness）：
#
# 第一步，每组成交量除以当日总成交得到每组成交量占比。
#
# 第二步，计算Pearson中值偏度，即3\*(均值-中值)/标准差。
#
# 成交量在价格上的分布反转因子（v\_p\_reversal）：
#
# 第一步，每组成交量与前后两组相加（如果是第一组则乘2与后一组相加，如果是最后一组则乘2与前一组相加），然后获取其成交量之和最大的序号，记为POC。
#
# 第二步，获取收盘价对应的序号，记为C。
#
# 第三步，根据日内收益率计算因子。
#
# 如果日内收益率大于0，(POC-C+1)\*日内收益，否则(C-poc+1)\*日内收益。
#

# ============================================================
# 作者原文 — 因子逻辑
# ============================================================
# 价格区间成交量的高低表示该价格附近多空博弈的激烈程度以及该价格范围是否被广泛认可。较高的价格区间成交量表明当前价格区间为价格接受区或公允区域，反之为价格拒绝区或非公允区域。日内价格的运动便是从一个公允区域转到下一个公允区域，对于非公允区域仅会短暂停留。
#
# 另一个重要的概率是POC（Point of control），它指最高价格区间成交量对应的价格，通常机构在POC附近积累了最多数量的成交量，所以是市场参与者一个重要的参考点。
#

# ============================================================
# 作者原文 — 回测表现说明
# ============================================================
# ## 因子评价
# 笔者测试的时候发现，v\_p\_skewness用均值进行低频化后的因子表现最好，因此仅展示其因子评价结果。
#
# ## IC分析
# 从IC上来看，这个因子的表现是不如其在收益率上的分布的。
#
# 因为，成交量在收益率上的分布这个因子的IC累加超过了-6。
#
# ## 总结
# 这个因子在IC和分层回测上的都不如其在收益率上的分布。
#
# 不过，笔者在复现的过程中写错了一次代码，在计算vol\_group的时候没有把最后一组的结果append进去，然后对于其长度小于3的标的，笔者直接返回了nan。
#
# 在这种情况下，得到的v\_p\_reversal因子IC绝对值是这两篇文章中介绍的所有因子里面最高的。
#
# 既然您能看到这里，那一定是对这篇文章还有那么一丁点儿兴趣，不知道您能否点赞推荐关注和分享支持一下笔者。
#

# ============================================================
# 本地图片清单（共 15 张）
# ============================================================
# 001.png  <-  因子逻辑
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
# 013.png  <-  收益分析
# 014.png  <-  收益分析
# 014.png  <-  总结

# ============================================================
# 作者代码（按原文出现顺序，共 2 个代码块）
# ============================================================

# --- 代码块 1 ---
    def process_single_day(self, idx):
        # 加载当日分钟数据
        file_name = self.files[idx]
        date_str = file_name.split('.')[0]
        cur_time = pd.to_datetime(date_str) + timedelta(hours=15)
        full_path = os.path.join(self.file_pth, file_name)
        data = BaseDataLoader.load_data(full_path, fields=['close', 'volume', 'open'])
        res = []
        for i in range(len(data.codes)):
            tmp = pd.DataFrame(data.data[:, :, i], columns=['close', 'volume', 'open'])
            res.append(self.cal_factor(tmp))
        res = pd.DataFrame(res, index=data.codes, columns=['v_p_skewness', 'v_p_reversal'])
        res['datetime'] = cur_time
        return res

# (作者注) 第一段代码主要就是读取数据，然后遍历每一个标的并调用cal\_factor方法计算因子（第9-11行）。

# --- 代码块 2 ---
@staticmethod
def cal_factor(data):
    close_idx = None
    close = data.iloc[-1, 0]
    rtn = data.iloc[-1, 0] / data.iloc[0, -1] - 1
    q = data['close'].quantile([i / 10 for i in range(11)])
    data.sort_values(by='close', inplace=True)
    vol_group = []
    end = 1
    tmp_vol = 0
    for i in range(len(data)):
        if data.iloc[i, 0] <= q.iloc[end]:
            tmp_vol += data.iloc[i, 1]
        else:
            vol_group.append(tmp_vol)
            tmp_vol = data.iloc[i, 1]
            end += 1
        if data.iloc[i, 0] == close and close_idx is None:
            close_idx = end
    vol_group.append(tmp_vol)
    if len(vol_group) < 10:
        vol_group += [0] * (10 - len(vol_group))
    vol_group = np.array(vol_group) / np.sum(vol_group)
    v_p_skewness = 3 * (np.mean(vol_group) - np.median(vol_group)) / np.std(vol_group)
    poc_list = []
    for i in range(len(vol_group)):
        if i == 0:
            poc_list.append(2 * vol_group[i] + vol_group[i + 1])
        elif i == len(vol_group) - 1:
            poc_list.append(2 * vol_group[i] + vol_group[i - 1])
        else:
            poc_list.append(vol_group[i - 1] + vol_group[i] + vol_group[i + 1])
    poc_idx = np.argmax(poc_list)
    if rtn < 0:
        v_p_reversal = (poc_idx - close_idx + 1) * rtn
    else:
        v_p_reversal = (close_idx - poc_idx + 1) * rtn
    return [v_p_skewness, v_p_reversal]

# (作者注) 第3-4行，为计算C做准备。
#
# (作者注) 第5行，计算日内收益率。
#
# (作者注) 第6行，计算10个分位数。
#
# (作者注) 第7行，按照价格排序。
#
# (作者注) 第8-20行，计算每一组的价格的成交量之和。其中，18-19行是为了获取收盘价对应的序号。
#
# (作者注) 第21-22行，对于存在涨停的情况，可能分不了10组，就对后面的数据进行补零。补零的顺序不会影响v\_p\_skewness的计算，基本上也不会影响v\_p\_reversal的计算，因为此时POC和C很有可能是相等的。
#
# (作者注) 第23-24行，计算v\_p\_skewness。
#
# (作者注) 第25-33行，计算POC。
#
# (作者注) 第34-37行，计算v\_p\_reversal。

