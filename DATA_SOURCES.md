# DATA_SOURCES — 另类数据源说明（概念 / 活跃度 / 情绪类因子）

> **用途**：写**概念类 / 活跃度类 / 情绪类**因子时来这里查数据（路径 / 结构 / 粒度 / 覆盖 / 用途）。
> **分工**：本地 `quant_factor_notes` 只产因子笔记；下面这些另类数据都在 **47**，实际加载 / 回测在 [47 的 `factor_library`](PROJECT_STATUS.md#与-47-factor_library-的关系)。
> **最后更新**：2026-06-30（新增 §5 同花顺 iFinD「数据库＋特色因子」产品目录，源自本地字典 `同花顺特色&基础高频数据.xlsx`；§1 东财覆盖按领导刷新更新——确切最新日待 ssh 47 复核）。
> **东财架构图**：仓库根 [`东财AlterDC数据库结构图.png`](东财AlterDC数据库结构图.png)（领导放的，本文件 §1.1 已转写）。
> **来源字典（本地，`.gitignore` 不入库）**：`同花顺特色&基础高频数据.xlsx`＝同花顺（§5）；`L2高频数据字典.pdf`＋`LV2特征梳理【最新】.xlsx`＋`AccountSX_CLC.txt`＝**通联/数讯 L2，另一套**（见 §5 顶部「厂商辨识」＋ §4.7）。

---

## 0. 访问方式（一次配好，复用）

| 方式 | 入口 | 备注 |
|---|---|---|
| SSH | `ssh 47` | 已配 `~/.ssh/config`：`47 → 192.168.2.47:9047, user PengSX`，**密钥登录**（无需密码）。 |
| 数据根（47 本地） | `/mnt/sda2/HuaTZ/AlterDatabase/` | 在 47 上用**这个**路径。 |
| 数据根（其它机挂载） | `/mnt/HuaTZ_47/AlterDatabase/` | 在别的机器上挂载访问；**47 本机没有这个挂载点**。 |
| Python | 47 上 `python3` = 3.10.13 / pandas 2.1.1 | 读 `.pickle`：`pd.read_pickle(path)`。另有 `env310`、`mysql` CLI(`/opt/anaconda3/bin/mysql`)。 |
| MySQL（同花顺原始库） | `host=192.168.2.47 port=3306 user=Turing pass=turing123 db=AlterDataIfind charset=utf8mb4` | **从本机 Windows 也能直连 3306**（无需先 ssh）。 |

> ⚠️ `/mnt/sda2/HuaTZ/AlterDatabase/` 是**公司整个另类数据湖**（约 19 个来源目录）：
> `alphaPie / alterDC / alterIfind / chinaScopeSAM / concept_data / datago / datamental / esgYD / gangtise / huiChao / jinmen / MSCI / newsHotCLS / newsTL / recruitmentXZ / royalFlush / themeTL …`
> 本文件目前**只覆盖领导点名的 3 个**（alterDC / concept_data / AlterDataIfind）；其余等用到再补。
> （`royalFlush`=同花顺英文名、`alterIfind` 也疑似同花顺系，未来要更多同花顺数据可先翻这两个。）

---

## 1. 东财 alterDC（东方财富 Choice ｜ 活跃度 / 人气 / 情绪）

**路径** `/mnt/sda2/HuaTZ/AlterDatabase/alterDC/` ｜ **10 个 pandas `.pickle`，共 ~8.8 GB** ｜ **静态快照·定期重拷**（不是实时库；领导按需重拷一份）。

> 📅 **覆盖更新（2026-06-30）**：原快照截至 2026-03-25；**领导已重拷、补入近三个月**，现覆盖约至 **2026-06**。⚠️ 确切最新交易日、以及 10 个 pickle 是否全部同步到同一日，**待 ssh 47 复核**——本机当前不在 `192.168.2.x` 内网/VPN，`ssh 47` 与 `:3306` 均连接超时，无法直连核对。下表「覆盖（已核）」列仍是 2026-03-25 旧值，复核后再刷新。

定位：东财的**散户行为 / 关注度 / 情绪**类指数，主要服务**活跃度因子、情绪因子、人气/拥挤度因子**。

### 1.1 架构图转写（4 大类，及更新频率）

```
数据内容
├─ 市场因子（市场级聚合）
│   ├─ 预估新开户数：开户变化率 / 开户变化趋势（非交易日测算并入下一交易日，节假日后会跳变）
│   ├─ 预估基金申赎比（申购/赎回，非交易日并入下一交易日）
│   ├─ 市场活跃度（按自由流通市值 × 当日关注度 × 社区活跃指数 合成，期望与市场情绪相关）
│   └─ 报告户数预测 / 股东户数预测（结合网页热度+券商研报关注度，季报户数+互动易，模拟买入/卖出/持仓）
├─ 投资标的内因子（个股级，基于券商/平台自选与持仓）
│   ├─ 自选关注数（全平台自选数据加工）            → 多头指标
│   ├─ 热门基金重仓持有指数（基金重仓数据加工）
│   ├─ 个人投资关注指数
│   └─ 持股基金关注指数（基金流入/流出+持仓重合）  → 市场关注指数
├─ 社区情绪因子（股吧/资讯）
│   ├─ 社区活跃指数（股吧、评论帖热度）
│   ├─ 新闻阅读指数 / 公告阅读指数 / 研报阅读指数（阅读量→指数+排名）
│   └─ 最新舆情（51job 等监测网站，按月统计）
└─ 个股人气（东财人气榜系，更新最频）
    ├─ 个股实时变动（实时排名变动）            —— 每 10 分钟
    ├─ 个股(历史)指数（历史人气）              —— 每日
    ├─ 飙升指数（排行前 100）                  —— 每日
    ├─ 人气榜指数（人气 TOP100）               —— 每小时
    ├─ 热门股指数                              —— 每小时
    └─ 粉丝特征指数                            —— 每小时
```

### 1.2 实际落地文件（pickle ↔ 架构类目映射）

10 个 pickle 全是 **`RangeIndex` + 长表（含日期/代码列）**，不是宽矩阵。日期在 `统计日期` 列（字符串 `YYYY/MM/DD`），代码在 `证券代码`（`000001.SZ` 带后缀）。

| 文件（`alterDC/`） | 大小 | 架构类目 | 粒度 | 覆盖（已核） | 关键列 / 说明 |
|---|---:|---|---|---|---|
| `市场全景.pickle` | 0.1 MB | 市场因子（聚合） | **市场级·日** | 2018-01-02 → 2026-03-25（1994 日） | `统计日期, 预估开户变化率, 预估基金申赎比, 市场活跃度, updateTime_*` |
| `股东户数预测.pickle` | 391 MB | 市场因子-报告户数 | **个股·日** | 2016-07-01 → 2026-03-25（3488 日 ×5667 只） | `证券代码, 统计日期, 股东预测户数, 回刷后股东预测户数`（回刷=回填修正） |
| `个股访问指数.pickle` | 1.14 GB | 个股人气 | **个股·日** | 2018-01-01 → ~2026-03-25（13.96M 行 ×11 列） | `SECURITY_CODE, 证券代码, 证券简称, 证券内码, 统计日期, 最新指数, 最新指数变化, 指数变化排名, 申万一级行业分类, 是否交易日` |
| `自选股关注指数.pickle` | 1.12 GB | 标的内-自选关注（多头指标） | 个股·日 | ~2018 → 2026-03-25 | schema 类似个股访问（值/变化/排名/行业）；列名待加载确认 |
| `持股基金关注指数.pickle` | 1.22 GB | 标的内-持股基金关注（市场关注指数） | 个股·日 | 同上 | 同上 |
| `热门基金重仓持有指数.pickle` | 0.99 GB | 标的内-基金重仓 | 个股·日 | 同上 | 同上 |
| `社区活跃指数.pickle` | 1.08 GB | 社区情绪-股吧活跃 | 个股·日 | 同上 | 同上 |
| `新闻阅读指数.pickle` | 1.14 GB | 社区情绪-新闻阅读 | 个股·日 | 同上 | 同上 |
| `公告阅读指数.pickle` | 1.14 GB | 社区情绪-公告阅读 | 个股·日 | 同上 | 同上 |
| `研报阅读指数.pickle` | 1.14 GB | 社区情绪-研报阅读 | 个股·日 | 同上 | 同上 |

> 说明：上面 7 个 1 GB 级 per-stock 文件只核对了**存在+大小**，未逐个 `read_pickle`（各 ~1 GB）。结构按东财同系产品推断为 `证券代码 + 统计日期 + 最新指数 + 变化 + 排名 + 申万行业` 的个股日频长表；写因子前 `pd.read_pickle` 看一眼列名即可。

### 1.3 用途（写什么因子）& 注意

- **活跃度/人气因子**：`个股访问指数`、`自选股关注指数`、`社区活跃指数`、`热门基金重仓/持股基金关注`——关注度水平、变化、排名、行业内分位都能直接做因子。
- **股东户数因子**：`股东户数预测`——户数↑≈筹码分散/散户进场，户数↓≈筹码集中；日频预测值比季报户数频率高得多，**经典 alpha**。用 `回刷后` 列（修正后）。
- **市场择时/情绪**：`市场全景` 的开户变化率、基金申赎比、市场活跃度——市场级择时/仓位信号。
- ⚠️ **静态快照·定期重拷**：不是实时库，要更新找领导重拷（最近一次已补到 ~2026-06，见本节顶部 📅；确切日待 ssh 47 复核）。**非交易日数据并入下一交易日**，节假日后开户/申赎类会跳变，做因子要按交易日对齐、注意跳变点。
- ⚠️ 代码格式 `000001.SZ`（带交易所后缀），与 concept_data 的 `ticker=600329`（纯数字）、MySQL 的 `sec_code` 不一致，跨源拼接要先统一代码。

---

## 2. 同花顺 concept_data（iFinD 概念指数·**清洗后**数据）

**路径** `/mnt/sda2/HuaTZ/AlterDatabase/concept_data/` ｜ **64 GB** ｜ 同花顺**概念指数**全套：成分股、概念指数行情（日/分钟）、概念热度。服务**概念类因子、概念轮动、概念拥挤度/热度因子**。

概念用同花顺指数码 `ifind_8xxxxx`（如 `ifind_885311`、`ifind_883300`=沪深300样本股）。主表 `concept_index_info` 共 **449 个概念**，每概念带 `concept_explain` 文字释义。

### 2.1 子目录总览

| 子目录 | 大小 | 文件数 | 内容 | 粒度 | 覆盖（按 by_date 目录名） |
|---|---:|---:|---|---|---|
| `base_data/concept_ifind/` | 126 MB | 4 | 概念主表 / 成分聚合 / 相似度 / 有效池 | — | 2012-12 起 |
| `daily_constituent_index/` | 8.2 GB | 4085 | **成分股**（按概念 long + 按日期 宽权重矩阵） | 日 | 2012-12-18 → 2026-01-30 |
| `daily_info_by_concept/` | 110 MB | 449 | **概念指数日行情**（每概念 1 文件） | 日 | 概念建立日起（如 2020-11） |
| `min_data_concept/` | 41 GB | 3491 | **概念指数分钟行情**（按概念 + 按日期） | **1 分钟** | 2013-08-01 → 2026-02-02 |
| `conceptual_attention_by_concept/` | 4.1 GB | 427 | **概念热度**（每概念 1 文件） | 5 分钟网格 | 2024-09-01 → 2026-02-13 |
| `conceptual_attention_by_date/` | 11 GB | 1062 | **概念热度**（每日 1 目录，raw+clean） | 5 分钟网格 | 2024-09-01 → 2026-02-13 |

### 2.2 各表 schema（已抽样核对）

**base_data/concept_ifind/**
- `concept_index_info.pickle`（449×8）概念主表：`index_code, concept_id, concept_name, concept_explain(释义), first_create_time/date/trade_date, index_id`。
- `concept_cons_agg_daily.pickle`（775,689×12）概念指数日聚合（= `daily_info_by_concept` 的合并版）：`index_code, tradeDate, total_stock_num_tomo, total_stock_num_today, return_close_over_close, free_turnover_rate, closeIndex, turnoverVol, turnoverValue, share_capital_free, count_uplimit_notst(涨停非ST数), weight_uplimit_notst(涨停非ST权重)`。2012-12-17 起。
- `concept_cons_similarity_daily.pickle`（752,800×4）概念两两相似度：`index_code, max_similar_index_code, similarity_value, tradeDate`——**做概念去重/聚类/拥挤传染**用。
- `valid_concept_pool.csv`（772,977 行）每日**有效概念池**：`tradeDate, index_code, weight, drop_reason, concept_name`。`drop_reason` 非空=当日被剔除——**选概念先过这张白名单**。

**daily_constituent_index/**（成分股）
- `concept_ifind/ifind_<码>_clean.csv` —— long：`tradeDate, ticker, weight`（等权时 weight=1）。
- `concept_ifind/ifind_<码>_close_weight.csv` —— 收盘价加权版。
- `concept_ifind_by_date/<YYYYMMDD>/close_weight.csv` —— **宽矩阵**：行=`ticker`(纯数字，~5475 只)、列=各 `ifind_概念码`、值=权重（稀疏，多为空）。

**daily_info_by_concept/concept_ifind/ifind_<码>.csv**（概念指数日行情，12 列，同 `concept_cons_agg_daily`）：含 `closeIndex(指数点位), return_close_over_close(日收益), free_turnover_rate(自由换手), turnoverVol/Value, count_uplimit_notst(涨停数)` 等。

**min_data_concept/**（概念指数分钟行情）
- `concept_ifind/ifind_<码>.csv` 与 `concept_ifind_by_date/<YYYYMMDD>/min_data_concept.csv`，列：`index_code, timestamp, tradeDate, minute, return_close_over_close, cum_return_close_over_close, turnoverVol, turnoverValue, total_stock_num, valid_stock_num`。**1 分钟**（09:25, 09:31…）。

**conceptual_attention_*（概念热度）**
- by_concept：`data_date, latest_trade_date, index_code, concept_name, trade_time, attention_value`。
- by_date：`<YYYYMMDD>/conceptual_attention_onehour.csv`（raw）+ `_clean.csv`，列 `index_code, concept_name, trade_time, attention_value`。
- ⚠️ **底层是小时级**（对应 MySQL `conceptual_attention_onehour`），清洗后**展开成 5 分钟网格、整点内取值恒定**（如 00:00 与 00:05 同为 12.5）——别误当成真 5 分钟分辨率。`trade_time` 是 **24 小时制**（人气 7×24 累积，非仅交易时段）。

### 2.3 用途（写什么因子）

- **概念热度/轮动**：`conceptual_attention`（热度水平、变化、日内斜率、概念间排名）+ `daily_info_by_concept`（概念收益/换手/涨停数）→ 热度动量、热度反转、概念拥挤度。
- **概念成分映射**：`daily_constituent_index` + `valid_concept_pool` → 把个股因子聚合到概念、或把概念热度下发到成分股（个股「所属热门概念」因子）。
- **概念相似/传染**：`concept_cons_similarity_daily` → 相似概念热度溢出。
- **概念内分钟微结构**：`min_data_concept`（1 分钟）→ 概念日内动量/波动/量价。

---

## 3. 同花顺 AlterDataIfind（MySQL ｜ **未清洗原始库**）

**连接** `192.168.2.47:3306 Turing/turing123 → AlterDataIfind`（本机 Windows 可直连）｜ **32 张表**。
这是 §2 `concept_data` 清洗数据的**上游原始库**，并额外含**个股/行业人气、事件驱动新闻、美联储**等 concept_data 里没有的维度。

### 3.1 表清单（按体量，含 information_schema 估算行数 / 大小 / 中文注释）

**A. 人气 / 热度（核心活跃度源）**
| 表 | 约行数 | 大小 | 注释 |
|---|---:|---:|---|
| `astock_attention_onehour` | 934 M | 72 GB | 中国股票 **1 小时**同花顺人气（个股·热值+排名） |
| `astock_attention_24hour` | 84 M | 7.3 GB | 中国股票 **24 小时**同花顺人气（含简称） |
| `conceptual_attention_onehour` | 46 M | 4.9 GB | **概念**1 小时人气（→ §2 概念热度的原始） |
| `industry_attention_onehour` | 469 K | 45 MB | **行业**1 小时人气 |

**B. 事件驱动 / 新闻 / 舆情**
| 表 | 约行数 | 大小 | 注释 |
|---|---:|---:|---|
| `ed_keyword_general_index` | 46 M | 12 GB | 事件驱动综合新闻指数（关键词级：搜索/资讯/研报/权威媒体指数） |
| `ed_applied_news_tag` | 37 M | 8.7 GB | 新闻↔标签（概念/公司/人物/事件/产业链，含相关性+产业链层级） |
| `ed_applied_news` | 11 M | 7.5 GB | 新闻正文（标题/来源/热度新旧算法/**正负面情绪+得分**/发布时间） |
| `ed_popularity_change` | 42 M | 6.8 GB | 新闻热度随时间变化 |
| `stk_concept_news` | 3.3 M | 1.3 GB | 概念板块新闻 |
| `news_event_reminder` | 65 K | 27 MB | iFinD 大事提醒 |

**C. 概念指数 & 成分变动**
| 表 | 约行数 | 大小 | 注释 |
|---|---:|---:|---|
| `stk_concept_index_quota` | 5.1 M | 1.4 GB | 同花顺**概念指数日行情**（→ §2 `daily_info_by_concept` 原始） |
| `thematicindex_stock_chg_record` | 846 K | 101 MB | 专题概念指数成分股变动 |
| `concept_stock_change_record` | 148 K | 64 MB | 概念成分股变动 |
| `concept_sub_stock_chg_record` | 5.2 K | 3.5 MB | 细分概念成分股变动 |
| `concept_change_record` / `concept_sub_change_record` | 718 / 372 | <0.5 MB | 概念 / 细分概念变动 |

**D. 证券基础 & 美联储**
| 表 | 约行数 | 大小 | 注释 |
|---|---:|---:|---|
| `sec_basic_info` | 4.2 M | 1.5 GB | 证券基本资料 |
| `mone_policy_event_text_analy` | 427 K | 86 MB | 美联储货币政策事件文本解析 |
| `monetary_policy_event` | 6.4 K | 4.5 MB | 美联储货币政策事件 |
| `ir_forecast_voting_point` | 0 | — | 美联储利率预测点阵图（空） |
| `hawk_dove_index` | 0 | — | 美联储鹰鸽指数（空） |

**E. 空表 / 占位（schema 已建，未灌数）—— 多为「派生热度因子」预留**
`thsindex1/3/4/6/7_adjusted`（**日频 HeatFactor1/3/4/6/7**）、`ashare_focus_sticky`（个股关注粘性）、`ashare_hot_self`（个股热度）、`cn_stock_half_heat / cn_stock_half_sticky`（半日热度/留存率）、`thematicindex_chg_record`、`stk_corp_ic`（行业板块成分）。
→ 公司**已规划但尚未生产**的热度衍生因子，可能是后续重点，写因子前先 `select count(*)` 确认是否已灌数。

### 3.2 关键表 schema（已抽样）

- **`astock_attention_onehour`**（11 列）：`seq, ctime, mtime, rtime, index_value(热值), sec_code, sec_short_name, index_rank(排名), trade_date, trade_time, isvalid`。个股小时热值+排名，2024-09-01 起，**934M 行/72 GB——查询务必带 `trade_date`/`sec_code` 条件 + LIMIT，别全表扫**。
- **`ed_applied_news`**（39 列，重点 NLP）：`eventtitle, eventdate, fromsource, mediatype, popularity(旧)/newpopularity(新), maxpopularity, publicsentiment(正负面)+publicsentimentscore, predictitle(标题正负面)+predicprotitle, mainlabels, mainwords, publishtime, selfweight(重要度)…`。
- **`ed_keyword_general_index`**（16 列）：`kwid, kwname, type, datestr, indexcomprehenisvenews(综合新闻指数), indexdetailsearch(搜索), indexdetailnews(资讯), indexdetailreports(研报), indexdetailsocial(权威媒体)`。
- **`ed_applied_news_tag`**（16 列）：`id(新闻id), tagid, tagname, idpath/namepath, score(相关性), supply_chain_hierarchy(产业链层级), extra001/002(概念/公司/产业链 id+类型)`。
- 多数表带统一审计列 `seq/ctime/mtime/rtime/isvalid`（`isvalid=1` 为有效，**查询记得过滤**）。

### 3.3 血缘（清洗 ↔ 原始）

```
AlterDataIfind（MySQL 原始）            →  concept_data（清洗后 CSV/pickle, §2）
  conceptual_attention_onehour(小时)   →  conceptual_attention_*（5 分钟网格 ffill）
  stk_concept_index_quota              →  daily_info_by_concept / concept_cons_agg_daily
  *_stock_chg_record（成分变动事件）   →  daily_constituent_index（每日成分快照/权重矩阵）

东财 alterDC（§1）是另一家厂商（东方财富 Choice），与同花顺两套，互不血缘；个股代码后缀/口径都不同，跨用先对齐。
```

---

## 4. 跨源注意事项（写因子前必看）

1. **代码口径不统一**：东财 `000001.SZ`；concept_data 成分 `ticker=600329`(纯数字)、概念 `ifind_8xxxxx`；MySQL `sec_code` 有的带后缀有的纯数字。拼接前统一。
2. **快照 vs 实时**：alterDC 是静态快照·定期重拷（最近补到 ~2026-06，确切日待核，见 §1 📅）；concept_data / MySQL 是公司在维护的库（mtime 更近），但是否实时更新未确认，用前看最新日期。
3. **热度=小时底**：concept_data 的 5 分钟「概念热度」是小时数据 ffill 出来的；个股热度真要分钟级得自己从 MySQL `astock_attention_onehour` 取。
4. **大表谨慎**：`astock_attention_onehour`(72G/934M 行) 等，必须带 `trade_date`+`sec_code`/`index` 条件与 LIMIT；交易日 09:00–（次日）06:00 **避免多进程密集拉取**（账号守则）。
5. **有效性过滤**：concept 用 `valid_concept_pool`（看 `drop_reason`）；MySQL 用 `isvalid=1`。
6. **非交易日并入**：东财开户/申赎类把非交易日并入下一交易日，节后跳变——按交易日对齐。
7. **三套「高频」别混**：① 同花顺高频数据库（§5.1，多资产分钟＋逐笔＋快照＋买卖队列）② 同花顺 Level2 实时（§5.1，SDK 推送、**无历史**）③ 通联/数讯 L2 逐笔快照库（数讯机房 `TLMDSH/TLOrderSZ/TLTradeSH…`，见 §5 顶部）。①③ 数据**类型**重叠（都给沪深逐笔/快照），但**厂商、物理库、账号、字段口径全不同**；写因子务必注明用哪一套。另：同花顺「特色因子」(§5.2) 是**已算好的成品因子**，别与原始逐笔/快照行情混为一谈。

---

## 5. 同花顺 iFinD「数据库 + 特色因子」产品目录

> **字典来源**：repo 根 `同花顺特色&基础高频数据.xlsx`（~30 MB，**`.gitignore` 不入库**；出处＝公司图灵共享盘 `…\0-服务器与数据库信息\同花顺\`）。这是**同花顺官方的产品目录/字典，不是数据本体**——**数据本体不在本机**，订阅后落到公司服务器（很可能是 47 数据湖的 `royalFlush/`＝同花顺英文名 或 `alterIfind/` 目录，**待 ssh 47 确认**）。字典共 **9 个 sheet，分三块**：① 基础数据库（低频，§5.4）② 基础高频（§5.1）③ 特色（特色因子 §5.2 ＋ 特色数据 §5.3）。
> 本机读法（无 Python）：把 `.xlsx` 当 zip 解 `xl/sharedStrings.xml` ＋ `xl/worksheets/sheet*.xml`（PowerShell `System.IO.Compression`）。

> ⚠️ **厂商辨识（务必先看）**：本节全部是**同花顺（iFinD / royalFlush）**的产品，**与「通联/数讯 L2」是两套完全不同的东西**：
> 通联 L2 ＝ **数讯机房** Linux（`222.71.53.140:9062` / VPN `192.168.2.62`，账号见 `AccountSX_CLC.txt`），逐笔/快照表 `TLMDSH/TLMDSZ/TLOrderSH/TLOrderSZ/TLTradeSH/TLTradeSZ/TLBond*/TLIndex*/MinData`，取数用 `QryMDFromDBDemo.py`，字典 `L2高频数据字典.pdf`＋`LV2特征梳理【最新】.xlsx`，厂商是**通联数据（DataYes/优矿系）**。
> 同花顺高频（§5.1）与通联 L2 **数据类型重叠**（都给沪深股票逐笔成交/逐笔委托/快照），但**厂商、物理库、账号、字段口径全不一样**——勿混用，写因子要注明用的哪一套。

### 5.1 基础高频（高频数据库 + Level2 实时）

**(A) 高频数据库**（sheet「高频数据库」，≈200 行表清单）——同花顺**多资产历史高频库**。4 列：`大类 | 子类 | 表英文名 | 表中文名`。粒度从分钟到逐笔：
- **分钟 K 线** `{1,3,5,10,15,30,60}min`：沪深 股票/债券/基金/指数（`stock_basic_oneminute`…`_onehour`、`bond_/fund_/index_basic_*`）。
- **Tick/快照** `*_now`：`sh_stock_now/sz_stock_now`（上海/深圳股票快照），债/基/指数同。
- **买卖队列** `stock_queue/bond_queue/fund_queue`；**逐笔成交** `stock_trade/bond_trade/fund_trade`；**逐笔委托** `stock_order/sh_stock_order/…`（深/上分表）。
- **资金流向** `bt_capital_flow_min/3min/…/60min`。
- **衍生品/其它市场**：中金所期货＋股指期权（`cffex_*`）、沪深 ETF 期权（`sh_/sz_option_*`）、大商所/郑商所/上期所/广期所 商品期货＋期权（`dce_/czc_/shf_/gzf_*`，含 `_tick`）、北交所（`bse_*`）、申万/同花顺/富时 A50 指数（`swindex_/thsindex_/a50sif_*`）、上海黄金（`shgold_*`）、港交所（`hkstock_basic_*`/`hk_stock_now`）。
- ➜ **这一块即「基础高频」**，可做日内微结构/逐笔/委托失衡/快照盘口类因子（与通联 L2 同类，注意顶部厂商辨识）。**覆盖起始日与落库路径字典未写，待 ssh 47 确认。**

**(B) 沪深 Level2 实时行情**（sheet「沪深level2实时行情数据」）——同花顺 **Level2 实时推送（直播流，非研究库）**：逐笔＋tick（成交/委托/集合竞价），订阅方式 查询＋推送，**交易所机房→用户本地 SDK 推送**，延迟 ~10ms，全市场 5000+ 代码、不限量限频、按账号授权；**不含历史数据**。
- ➜ 实盘/盯盘用，**不能回测**（无历史）；回测要用 (A) 高频数据库 或 通联 L2。

### 5.2 特色因子库（同花顺已算好的成品因子，按文件交付）

同花顺把基于逐笔/快照/分钟/新闻算好的**成品因子**按文件推送（非原始行情）。三类：

| sheet | 体量 | 频率 | 起始 | 内容 |
|---|---:|---|---|---|
| **日频特色因子** | 938 行 | 日频，每晚 ~21:30（T-1 数据 T 日可用；集合竞价 9:28、资金流/强化学习 9:10 当日可用） | 多数 A 股类 2015-07-01；集合竞价 2016；Tick 深度模型 2019-07；Transformer 2018-05；港股 2022 起（部分止于 2025 年中） | 类别：美股日频、港股（资金流/买卖行为）、A 股（集合竞价量价 / 逐笔成交频次量价 / 逐笔委托频次量价 / Tick 快照量价 / 分钟量价技术 / 日频量价技术 / Tick 快照深度模型 / Transformer 量价预测 / 量价强化学习）、基本面强化学习、另类（新闻预测文本 / 大模型新闻文本 / 热度指数新算法脱敏 / 情绪强化学习）、卖方盈利预测、一致预期。因子明细列：`二级分类\|中文全称\|因子代码\|英文全称\|中文介绍`，代码如 `D1OIT1`(Daily_Order_Imbalance_Trend1)、`D1BSS*`(买卖力量)、`D1MIO*`(主力流入流出)。文件名形如 `TRFM_OW_500U-2023-11-16`（用 11/15 行情算、当晚入库）。 |
| **日内特色因子** | 809 行 | **30 分钟频**，盘中 9:30 起、各时点 1 分钟内交付（期货 1 分钟频） | 多数 2022-01-01（港股止于 2025 年中） | 表如 `intraday_tbtt_vol_mso`(逐笔偏量中小单)、`_abas`(逐笔主买主卖)、`intraday_tick_price_momrev`(逐笔快照偏价动量反转)、`_volcorr`(偏价量相关)、`_vol_bo`(大单)、`_vol_liq`(流动性)、`_tbtt_pv`(逐笔量价)、`intraday_tick_pv`(Tick 量价)、`intraday_futures_oneminute`(期货)、`intraday_hk_*`(港股)、ETF（量价/风险/流动性/动量反转/情绪/量价相关/波动率）。字段如 `pc_tick2m_c2_alpha0…`（中小单主动买入成交额占比 等）。**因子以「使用数据截止时点」命名**（10:30 命名＝用到 10:30:00 前数据）。 |
| **实时新闻因子** | 2552 行（1 套嵌套 schema） | 实时 | 2018 起 | 大模型新闻解析：`id/title/publish_time/result{event_type/event_name/event_summary/event_subject/sentiment_analysis{对象/主体关系/情感/理由}/sentiment_analysis_d[主体级 subject/code/influence/reason/tag]/market_impact[code/label=涨/跌/中性]}`。**event_type 共 2551 类**（各国央行加息/降息/利率决议、存准、QE/QT… 宏观事件为主），覆盖**全 A 股 90 个行业**。即「新闻→事件→主体情绪→A 股个股涨跌预测」实时因子。 |

（sheet「API接口」为空占位。）

### 5.3 特色数据（＝ §2/§3 同一批表，字典补齐官方起始日）

sheet「特色数据」「事件驱动」列的是**原始特色数据表**，与已落 47 的 §2 `concept_data`、§3 `AlterDataIfind`(MySQL) **同源同表**——字典补齐了**官方起始日**与**含义/合作背景**：

- **热度指数** `thsindex1–7`(=`h_index1–7`)：A 股 点击量占比 / 按资金 / 新闻点击 / 自选股占比 / 自选-按资金 / 新增自选 / 剔除自选，**2014 起**。合作客户：九坤、鸣石、幻方、衍复、蓝色郁金香。➜ **对应 §3.1.E 的占位空表** `thsindex1/3/4/6/7_adjusted`（日频 HeatFactor）。
- **个股/全市场人气**：`ashare_hot_self`(个股热度＝K线pv+分时pv+搜索pv，2016-11)、`ashare_focus_sticky`(关注粘性，2023-01)、`ashare_market_hot`(全市场热度，2016-11)。➜ **对应 §3.1.E** 同名占位表。
- **个股/概念/行业热榜**：`astock_attention_onehour`/`_24hour`、`conceptual_attention_onehour`、`industry_attention_onehour`，**2024-02 起**。➜ **即 §3.1.A 的人气核心表**（`astock_attention_onehour` 934M 行/72 GB）。
- **事件驱动**：`ed_applied_news`(2017)、`ed_applied_news_tag`(2017)、`ed_keyword_general_index`(2014-07)、`ed_popularity_change`(2022-02，3 天内每 15 分钟更新)、`monetary_policy_event`/`mone_policy_event_text_analy`(2000，含鹰鸽指数)。➜ **即 §3.1.B**。
- **概念**：`concept_change_record`、`concept_stock_change_record`。➜ **§3.1.C / §2**。
- **接口能力**（sheet「事件驱动」的 API 清单）：基础事件库、另类标签库、宏观政策文本、特色概念库、关键词另类数据、特色事件库（微信公众号/微博/雪球/互动平台）、**涨价题材数据**（2021 起，申万 28 行业产品价格走势＋标的池）。

➜ 写概念/活跃度/情绪/事件因子时：**原始表查 §2/§3**（已在 47），**起始日/字段含义/合作背景查本字典**。

### 5.4 基础数据库（低频，sheet「同花顺基础数据库」≈1138 表）

iFinD 标准**低频/参考/财务库**，3 级目录：公用编码库、中国股票（基础信息 / 发行上市 / 行情数据[日周月、复权、涨跌停、估值] / 财务数据[三大表新旧准则、单季、业绩预告快报、计算指标] / 财务附注…），及基金/债券/指数/宏观/期货/海外等。日频及以下，非本项目另类因子重点，用到再查字典。

### 5.5 访问方式 & 待办

- **字典**：本机 repo 根 `同花顺特色&基础高频数据.xlsx`（`.gitignore`，本机无 Python，解 zip 读 XML）。
- **数据本体**：不在本机；订阅数据 / 成品因子落公司服务器，**最可能在 47 `/mnt/sda2/HuaTZ/AlterDatabase/` 的 `royalFlush/`、`alterIfind/`**（同花顺系），**待 ssh 47 落地确认路径/覆盖**。特色数据原始表已确认在 §2/§3（47）。
- [ ] ssh 47 确认：同花顺高频库(§5.1)、特色因子(§5.2) 是否已落 47、落在哪、覆盖到哪。
- [ ] §1 东财 alterDC 重拷后的**确切最新交易日**（领导补了近三个月，现 ~2026-06，待 ssh 47 核）。
- [ ] alterDC 7 个未开的 per-stock pickle：写到对应因子时 `read_pickle` 补确切列名。
- [ ] 数据湖其余 ~16 个来源目录（esgYD / chinaScopeSAM / gangtise / royalFlush …）用到再补。
