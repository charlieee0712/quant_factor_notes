# quant_factor_notes

本地化 + 结构化因子笔记库。**多来源**结构：每个公众号/首席一个来源目录，
但因子库 `factor_lib/` 跨来源统一（不按来源分目录），统一编号、统一索引。

> 📋 现状速览见 [PROJECT_STATUS.md](PROJECT_STATUS.md)，进度时间线见 [WORKLOG.md](WORKLOG.md)。

## 数据规模

- 来源 6 个：`general` 109 / `caochunxiao` 10 / `qinchuantao` 8 / `weijianrong` 14 / `chenshengrui` 16 / `zhengzhaolei` 22
- 文章 179 篇（Markdown 格式，图片已本地化）
- 图片约 3772 张（约 431 MB）
- 因子代码笔记 179 个（`.py` 格式，统一在根目录 `factor_lib/`，每个含 `# 来源标识`）
- 全集索引 1 个（`factor_index.md`，跨 6 来源汇总）
- 因子分类表 1 个（`factor_classification.csv`，含 `source` 列）

## 目录结构

```
quant_factor_notes/
├── README.md
├── factor_index.md             # 全集索引（跨来源统一，按日期倒序，含「来源」列）
├── factor_classification.csv   # 因子分类表（含 source 列）
├── factor_classification_summary.md
├── factor_lib/                 # 统一因子库：所有来源的 .py 结构化笔记
│                               #   不分来源目录；每个 .py 头部含「# 来源标识: <source>」
├── factor_lib.zip              # factor_lib/ 的打包快照
├── requirements.txt
├── sources/                    # 按来源分目录（爬新首席时新增 sources/<name>/）
│   └── general/                # 量化拯救散户（现有 109 篇）
│       ├── urls.txt            # 该来源待抓取链接列表
│       ├── failed.txt          # 抓取失败记录（自动追加）
│       ├── image_download.log  # 图片下载历史日志
│       ├── articles/           # 109 篇 markdown（图片路径已本地化）
│       │   └── images/         # 109 个子目录，每篇一目录，NNN.png/.jpg 编号
│       ├── articles_backup/    # 109 篇原始 markdown（图片 URL 未本地化版，回滚锚点）
│       └── html/               # 55 个 SingleFile 保存的原始 HTML（绕过反爬用）
└── scripts/                    # 共享脚本（用 --source 选择来源）
    ├── fetch.py                # 在线抓取
    ├── parse_local_html.py     # 解析本地 HTML
    ├── download_images.py      # 图片本地化
    ├── build_factor_lib.py     # 生成因子笔记（输入按来源，输出统一 factor_lib/）
    ├── build_index.py          # 生成全集索引（汇总全部来源）
    ├── classify_factors.py     # 解析 factor_lib/ 生成分类表（含 source 列）
    └── wechat_common.py        # 共享解析逻辑 + 多来源路径助手
```

## 多来源设计要点

- **来源隔离**：每个来源的抓取产物各自落在 `sources/<source>/` 下（articles / html / urls.txt / 备份 / 日志），互不干扰。
- **因子统一**：`factor_lib/` 在根目录，所有来源的因子混在一起、统一编号，**不**按来源分子目录。
- **来源可追溯**：每个 `factor_lib/*.py` 头部写 `# 来源标识: <source>`；`factor_classification.csv` 有 `source` 列；`factor_index.md` 有「来源」列。需要按来源筛因子时用这三者之一。

## 主要工具脚本

所有脚本默认 `--source general`，爬其他首席时传 `--source <name>`：

- `scripts/fetch.py` — 在线抓取公众号文章（适用小批量，反爬风险：中等）
- `scripts/parse_local_html.py` — 解析 SingleFile 浏览器扩展保存的本地 HTML（适用大批量，绕过反爬）
- `scripts/download_images.py` — 批量下载 mmbiz CDN 图片到本地，同时重写 markdown 链接
- `scripts/build_factor_lib.py` — 从某来源 markdown 生成结构化因子笔记到统一 `factor_lib/*.py`
- `scripts/build_index.py` — 汇总全部来源生成 `factor_index.md`（可 `--source` 限定单来源）
- `scripts/classify_factors.py` — 解析 `factor_lib/` 生成分类 CSV + 汇总（无需 `--source`，按文件头读来源）
- `scripts/wechat_common.py` — 共享解析逻辑（URL 规范化、front matter、markdown 转换）+ 路径助手

## 工作流（添加一个新来源，例如曹春晓 → `--source caochunxiao`）

1. **获取 HTML**：用 SingleFile 扩展把文章存到 `sources/caochunxiao/html/`，或把 URL 追加到 `sources/caochunxiao/urls.txt`
2. **解析正文**：`parse_local_html.py --source caochunxiao`（推荐）或 `fetch.py --source caochunxiao`，产物落到 `sources/caochunxiao/articles/*.md`
3. **本地化图片**：`download_images.py --source caochunxiao`，下载到 `sources/caochunxiao/articles/images/{slug}/`，重写链接
4. **生成因子笔记**：`build_factor_lib.py --source caochunxiao`，产物并入统一的 `factor_lib/*.py`（带 `# 来源标识: caochunxiao`）
5. **刷新索引**：`build_index.py`，重建根目录 `factor_index.md`（汇总全部来源）
6. **刷新分类表**：`classify_factors.py`，重建 `factor_classification.csv`（`source` 列自动区分来源）

> 增量抓取注意：`download_images.py` 的备份步骤遇到非空 `articles_backup/` 会报错退出，
> 增量时务必加 `--skip-backup`。

所有脚本用绝对路径调用 conda env 解释器：

```powershell
C:\Users\cnc\anaconda3\envs\wechat_fetch\python.exe scripts\<name>.py --source <name>
```

## 段落识别分布（全部 179 篇）

| 状态 | 篇数 | 说明 |
|---|---:|---|
| FULL | 5 | 三段齐备（计算步骤 + 因子逻辑 + 回测） |
| PARTIAL | 63 | 部分段落识别成功 |
| SKELETON_ONLY | 109 | 仅识别到回测段（IC/回归/换手率/收益） |
| NONE | 2 | 无段标题 |

字段写入每个 `factor_lib/*.py` 文件的 `# 段落识别:` 行，便于后续筛选。

## 数据备份

- `sources/<source>/articles_backup/` — 原始 markdown（图片 URL 未本地化版本）。图片本地化前的回滚锚点。
- `sources/<source>/html/` — SingleFile 保存的原始 HTML。正文解析的回滚锚点。

## 已知特性（非缺陷）

- 15 篇纯思路文章无代码块（作者原文如此，非抽取失效；另 2 篇仅骨架代码）
- 部分文章作者用图表代替文字描述，段内文字较短或为空（图仍保留在 `本地图片清单`）
- 严格中立摘录，不加 AI 推断观点；段落缺失明示 `(原文中无此段落)`
- 图片清单允许重复编号：同一张图在原文中出现多次时如实呈现
- 跨来源若出现同名 `{date}_{标题}` 文件，会共享同一个 `factor_lib/{slug}.py`，`build_index.py` 会打印 `⚠ 跨来源重名 slug` 警告
</content>
