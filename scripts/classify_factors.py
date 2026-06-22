"""Parse the unified factor_lib/*.py files and emit CSV + summary md.

factor_lib/ mixes all 来源 together; each file's source is read from its
'# 来源标识:' header line (written by build_factor_lib.py) and emitted as the
CSV `source` column so factors can be filtered by source. Files lacking the
marker default to 'general' (legacy)."""
import os
import re
import csv
import sys
import io
import traceback
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)  # project root (parent of scripts/)
FACTOR_DIR = os.path.join(ROOT, 'factor_lib')
INDEX_FILE = os.path.join(ROOT, 'factor_index.md')
OUT_CSV = os.path.join(ROOT, 'factor_classification.csv')
OUT_MD = os.path.join(ROOT, 'factor_classification_summary.md')
ERR_LOG = os.path.join(ROOT, 'errors.log')

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# ---- load index ----
def load_index():
    """Return dict[date] -> list of (title, keywords)."""
    idx = defaultdict(list)
    if not os.path.exists(INDEX_FILE):
        return idx
    with open(INDEX_FILE, encoding='utf-8') as f:
        for line in f:
            # | 99 | 2026-05-13 | [title](path) | keywords | lines | imgs |
            m = re.match(r'^\|\s*\d+\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*([^|]*?)\s*\|', line)
            if m:
                date, title, kw = m.group(1), m.group(2), m.group(3).strip()
                if kw == '—' or kw == '-':
                    kw = ''
                idx[date].append((title.strip(), kw))
    return idx

# ---- parse filename ----
def parse_fname(fname):
    base = fname[:-3] if fname.endswith('.py') else fname
    m = re.match(r'^(\d{4}-\d{2}-\d{2})_(.+)$', base)
    if not m:
        return None, base
    return m.group(1), m.group(2)

# ---- read file ----
def read_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

# ---- extract source (来源标识) ----
SOURCE_RE = re.compile(r'^#\s*来源标识\s*[:：]\s*(\S+)', re.MULTILINE)

def extract_source(text):
    """Read the '# 来源标识: <source>' header line; default 'general' if absent."""
    m = SOURCE_RE.search(text)
    return m.group(1) if m else 'general'

# ---- split into sections ----
SECTION_MARK = '# ============================================================'

def split_sections(text):
    """Return dict section_name -> body text."""
    # Strip module docstring
    lines = text.splitlines()
    sections = {}
    cur_name = '_head'
    cur_lines = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == SECTION_MARK and i + 1 < len(lines):
            name_line = lines[i+1].strip()
            if name_line.startswith('# '):
                # save previous
                sections[cur_name] = '\n'.join(cur_lines)
                cur_name = name_line[2:].strip()
                cur_lines = []
                # skip the marker, header, and following marker
                i += 2
                if i < len(lines) and lines[i].strip() == SECTION_MARK:
                    i += 1
                continue
        cur_lines.append(ln)
        i += 1
    sections[cur_name] = '\n'.join(cur_lines)
    return sections

# ---- parse code section ----
def parse_code_blocks(code_section_text):
    """Return list of code blocks (each is the raw text without separator)."""
    if not code_section_text:
        return []
    # Match "(原文未给出 python 代码)" -> empty
    if '原文未给出' in code_section_text and '代码块' not in code_section_text:
        return []
    parts = re.split(r'#\s*---\s*代码块\s*\d+\s*---', code_section_text)
    blocks = []
    for p in parts[1:]:  # skip header chunk
        # remove "(作者注) ..." trailing comments to isolate code,
        # but keep code-only portion: drop lines that are clearly author notes
        lines = p.splitlines()
        code_lines = []
        for ln in lines:
            stripped = ln.strip()
            if stripped.startswith('# (作者注)'):
                break  # author notes typically come AFTER each block
            code_lines.append(ln)
        block_text = '\n'.join(code_lines).strip('\n')
        if block_text.strip():
            blocks.append(block_text)
    return blocks

# ---- count code lines ----
def count_code_lines(blocks):
    total = 0
    for b in blocks:
        for ln in b.splitlines():
            s = ln.strip()
            if not s:
                continue
            if s.startswith('#'):
                continue
            total += 1
    return total

# ---- has_code judgment ----
def judge_has_code(blocks):
    if not blocks:
        return 'none'
    # Count function body real lines
    func_bodies = []  # list of body lines list
    for b in blocks:
        lines = b.splitlines()
        # naive: find def lines, collect indented lines after them
        cur_body = []
        in_func = False
        cur_indent = None
        for ln in lines:
            s = ln.strip()
            if re.match(r'^\s*def\s+\w+', ln) or re.match(r'^\s*class\s+\w+', ln):
                if in_func and cur_body:
                    func_bodies.append(cur_body)
                in_func = True
                cur_body = []
                cur_indent = len(ln) - len(ln.lstrip())
            elif in_func:
                if s == '':
                    continue
                if s.startswith('#'):
                    continue
                indent = len(ln) - len(ln.lstrip())
                if indent <= cur_indent and s:
                    # end of function
                    func_bodies.append(cur_body)
                    in_func = False
                    cur_body = []
                else:
                    cur_body.append(s)
            else:
                # top-level non-def code = also counts
                if s and not s.startswith('#'):
                    func_bodies.append([s])  # treat each top-level line as a tiny body
        if in_func and cur_body:
            func_bodies.append(cur_body)

    # Check for real logic vs only `pass`
    has_real = False
    real_bodies = 0
    skel_bodies = 0
    for body in func_bodies:
        body_non_empty = [l for l in body if l.strip() and not l.strip().startswith('#')]
        if not body_non_empty:
            continue
        if all(l.strip() == 'pass' for l in body_non_empty):
            skel_bodies += 1
        elif len(body_non_empty) >= 3:
            real_bodies += 1
            has_real = True
        else:
            # short but not pass = small helper, count as half real
            real_bodies += 1

    if has_real:
        return 'yes'
    if skel_bodies > 0 and real_bodies == 0:
        return 'partial'
    if real_bodies > 0:
        return 'partial'
    return 'none'

# ---- extract data source ----
LOAD_PATTERNS = [
    r"BaseDataLoader\.load_data\s*\(\s*([^)]+?)(?:,|\))",
    r"pd\.read_parquet\s*\(\s*([^)]+?)(?:,|\))",
    r"duckdb\.query\s*\(.+?FROM\s+['\"]([^'\"]+?)['\"]",
]

def extract_load_args(code_text):
    """Return list of first-arg strings from load functions."""
    args = []
    for pat in LOAD_PATTERNS:
        for m in re.finditer(pat, code_text, re.DOTALL):
            args.append(m.group(1).strip())
    return args

def classify_data_source(blocks, has_code, full_text):
    if has_code == 'none':
        return 'no_code', []
    code_text = '\n'.join(blocks)
    load_args = extract_load_args(code_text)

    found_1day = False
    found_min = []  # list of minutes (ints)
    variable_path = False
    use_filepth = 'self.file_pth' in code_text or 'self.files' in code_text

    for a in load_args:
        if 'stock_bar_1day' in a or 'index_bar_1day' in a or '_1day' in a:
            found_1day = True
        m = re.search(r'stock_bar_(\d+)min', a)
        if m:
            found_min.append(int(m.group(1)))
        m2 = re.search(r'index_bar_(\d+)min', a)
        if m2:
            found_min.append(int(m2.group(1)))
        if 'self.file_pth' in a or 'file_pth' in a or 'full_path' in a:
            variable_path = True
    # Also scan full code for stock_bar_Xmin references in os.path.join etc.
    for m in re.finditer(r'stock_bar_(\d+)min', code_text):
        found_min.append(int(m.group(1)))
    for m in re.finditer(r'index_bar_(\d+)min', code_text):
        found_min.append(int(m.group(1)))

    found_min = sorted(set(found_min))

    if found_1day and found_min:
        return 'mixed', found_min
    if found_1day:
        return '1day', []
    if found_min:
        if len(found_min) == 1:
            return f'{found_min[0]}min', found_min
        return 'multi_min', found_min

    # No explicit stock_bar_*. Try inferring from variable path + minute hints.
    # Code-level signals that data is minute-bar even when path is variable.
    minute_code_signals = (
        '.index.hour' in code_text
        or "groupby('minute'" in code_text
        or 'groupby("minute"' in code_text
        or 'data.index.hour * 60' in code_text
        or 'timedelta(hours=15)' in code_text
        or 'timedelta(minutes=' in code_text
        or "'15:00:00'" in code_text
        or '"15:00:00"' in code_text
        or 'fear_xmin' in code_text  # historical pattern
    )

    if variable_path or use_filepth or minute_code_signals:
        notes = full_text
        # Try to extract specific X-minute mention from anywhere.
        # Avoid matching inside identifiers (e.g. high2min, low2min are column names).
        # Require preceding char to NOT be alphabetic and trailing context to look right.
        code_min = []
        for m in re.finditer(r'(?:^|[^A-Za-z_])(\d+)\s*min(?:ute|s)?\b', code_text):
            try:
                code_min.append(int(m.group(1)))
            except ValueError:
                pass
        for m in re.finditer(r'(\d+)\s*分钟', code_text):
            code_min.append(int(m.group(1)))
        code_min = sorted(set([n for n in code_min if 1 <= n <= 240]))
        if len(code_min) == 1:
            return f'{code_min[0]}min_inferred', code_min
        if len(code_min) > 1:
            return 'multi_min_inferred', code_min

        # Look in 计算步骤 section preferentially
        steps = ''
        steps_match = re.search(r'作者原文 — 计算步骤\s*#\s*=+([\s\S]*?)#\s*=+', full_text)
        if steps_match:
            steps = steps_match.group(1)
        for src in (steps, notes):
            m = re.search(r'(\d+)\s*分钟数据', src)
            if m:
                return f'{m.group(1)}min_inferred', [int(m.group(1))]
            m = re.search(r'(\d+)\s*分钟[K]?线', src)
            if m:
                return f'{m.group(1)}min_inferred', [int(m.group(1))]
            m = re.search(r'每\s*(\d+)\s*分钟', src)
            if m:
                return f'{m.group(1)}min_inferred', [int(m.group(1))]

        # Generic minute hint (no explicit X)
        if '分钟' in notes and (variable_path or use_filepth or minute_code_signals):
            return 'minute_unspecified', []
        if minute_code_signals:
            return 'minute_unspecified', []
        return 'unclear', []
    return 'unclear', []

# ---- fields_used ----
def extract_fields(code_text):
    fields = set()
    # fields=[...]
    for m in re.finditer(r"fields\s*=\s*\[([^\]]+)\]", code_text):
        inside = m.group(1)
        for q in re.finditer(r"['\"]([^'\"]+)['\"]", inside):
            fields.add(q.group(1))
    # implicit: pct_change on close
    if '.pct_change' in code_text and 'close' in code_text and 'close' not in fields:
        fields.add('close')
    return sorted(fields)

# ---- external deps ----
DEP_PATTERNS = {
    'sklearn.LinearRegression': r'LinearRegression\b',
    'sklearn.KMeans': r'KMeans\b',
    'sklearn.GaussianMixture': r'GaussianMixture\b',
    'sklearn.cluster': r'from sklearn\.cluster',
    'sklearn.linear_model': r'from sklearn\.linear_model',
    'sklearn.mixture': r'from sklearn\.mixture',
    'sklearn.metrics': r'(r2_score|mean_squared_error|from sklearn\.metrics)',
    'sklearn.PCA': r'\bPCA\b',
    'sklearn.RandomForest': r'RandomForest',
    'sklearn.LogisticRegression': r'LogisticRegression',
    'sklearn.Lasso': r'\bLasso\b',
    'sklearn.Ridge': r'\bRidge\b',
    'statsmodels': r'(import statsmodels|statsmodels\.api|sm\.OLS|sm\.add_constant)',
    'scipy.stats': r'(from scipy import stats|scipy\.stats|stats\.)',
    'scipy.optimize': r'(scipy\.optimize|from scipy\.optimize)',
    'scipy.signal': r'(scipy\.signal|from scipy\.signal)',
    'scipy.spatial': r'(scipy\.spatial|cdist|pdist)',
    'scipy.linalg': r'scipy\.linalg',
    'joblib': r'(from joblib|joblib\.Parallel|Parallel\(|delayed\()',
    'duckdb': r'duckdb\.',
    'talib': r'(import talib|talib\.)',
    'lightgbm': r'(lightgbm|lgb\.)',
    'xgboost': r'(xgboost|xgb\.)',
    'hmmlearn': r'hmmlearn',
    'numba': r'(from numba|@njit|@jit|numba\.)',
    'tqdm': r'(from tqdm|tqdm\()',
    'networkx': r'networkx',
}

def extract_deps(code_text):
    deps = []
    for name, pat in DEP_PATTERNS.items():
        if re.search(pat, code_text):
            deps.append(name)
    return sorted(set(deps))

# ---- core formula ----
def extract_core_formula(blocks):
    """Pick the longest non-loader function body."""
    if not blocks:
        return ''
    # Prefer functions named like cal_factor*, process_single_day, cal_resi
    candidates = []  # list of (priority, length, text)
    PRIORITY = ['cal_resi', 'cal_factor', 'process_single_day', 'compute', 'calc', '_cal_', 'cal_']

    for b in blocks:
        # split into function chunks
        # A simple approach: scan for top-level (or method-level) def lines
        text = b
        # Find all def starts
        funcs = list(re.finditer(r'^(\s*)def\s+(\w+)\s*\([^)]*\)\s*:', text, re.MULTILINE))
        if not funcs:
            # treat whole block as one
            length = len([l for l in text.splitlines() if l.strip() and not l.strip().startswith('#')])
            candidates.append((99, length, text))
            continue
        for i, fm in enumerate(funcs):
            name = fm.group(2)
            start = fm.start()
            end = funcs[i+1].start() if i+1 < len(funcs) else len(text)
            body = text[start:end]
            # Skip if name suggests pure data loading
            if name in ('__init__', '_load_last_day_close', 'run', '__call__') and 'load_data' in body and len(body) < 600:
                continue
            length = len([l for l in body.splitlines() if l.strip() and not l.strip().startswith('#') and l.strip() != 'pass'])
            if length < 2:
                continue
            # priority by name match
            prio = 99
            for k, p in enumerate(PRIORITY):
                if p in name.lower():
                    prio = k
                    break
            candidates.append((prio, length, body))

    if not candidates:
        # fallback: concat first block raw
        return blocks[0][:1500]

    # sort by (priority asc, length desc)
    candidates.sort(key=lambda x: (x[0], -x[1]))
    best = candidates[0][2]
    if len(best) > 1500:
        best = best[:1500] + '...'
    return best.strip()

# ---- index lookup ----
def lookup_keywords(date, title, idx_map):
    entries = idx_map.get(date, [])
    if not entries:
        return ''
    if len(entries) == 1:
        return entries[0][1]
    # fuzzy
    t20 = title[:20]
    for et, kw in entries:
        if et[:20] == t20 or t20[:10] in et:
            return kw
    return entries[0][1]

# ---- IC / layer claim ----
def extract_claims(sections):
    """Return (ic_claim, layer_claim)."""
    bt = sections.get('作者原文 — 回测表现说明', '')
    if not bt:
        return '', ''
    # Strip comment marks
    lines = []
    for ln in bt.splitlines():
        s = ln.strip()
        if s.startswith('#'):
            s = s[1:].strip()
        lines.append(s)
    body = '\n'.join(lines)

    ic_text = ''
    layer_text = ''
    # Split by markdown subheaders
    parts = re.split(r'##\s*', body)
    for part in parts:
        head_line = part.splitlines()[0].strip() if part else ''
        rest = '\n'.join(part.splitlines()[1:]).strip()
        if 'IC分析' in head_line or 'IC' in head_line and len(head_line) < 12:
            ic_text = rest
        if '收益分析' in head_line or '分层' in head_line:
            layer_text = rest

    def shorten(t):
        if not t:
            return ''
        # take first ~80 chars of first meaningful sentence
        # remove blank lines
        lines = [l for l in t.splitlines() if l.strip()]
        if not lines:
            return ''
        first = lines[0]
        if len(first) > 120:
            first = first[:120] + '...'
        return first

    return shorten(ic_text), shorten(layer_text)

# ---- likely_factor_type ----
TYPE_KEYWORDS = [
    ('fund_selection', ['选基', '基金']),
    ('academic', ['BAB', 'Betting', 'CVaR', 'VCVaR', '前景价值', '尾部Beta', 'Fama', '特异市值', '巴菲特', 'Beta', '尾部']),
    ('smart_money', ['聪明钱', '算法交易', '知情交易']),
    ('turnover', ['换手率', '换手']),
    ('volatility', ['波动率', '波动', '偏度']),
    ('volume', ['成交量', '成交额', '资金流', '资金']),
    ('reversal', ['反转', '反向', '逆转', '逆向']),
    ('momentum', ['动量', '加速度']),
    ('event_driven', ['事件驱动', '异动', '异常']),
    ('tail_risk', ['尾部', '极端', 'CVaR']),
]

def guess_type(title, keywords_str, code_text):
    blob = title + ' ' + keywords_str + ' ' + code_text[:200]
    # fund_selection takes priority
    for t, kws in TYPE_KEYWORDS:
        for kw in kws:
            if kw in blob:
                return t
    return 'other'

# ---- main ----
def main():
    idx_map = load_index()
    files = sorted(os.listdir(FACTOR_DIR))
    files = [f for f in files if f.endswith('.py')]

    rows = []
    errors = []
    n_ok = 0

    for fname in files:
        path = os.path.join(FACTOR_DIR, fname)
        try:
            date, title = parse_fname(fname)
            text = read_file(path)
            source = extract_source(text)
            sections = split_sections(text)
            code_section = sections.get('作者代码（按原文出现顺序，共 0 个代码块）', '')
            # The section name varies by code count; find any section starting with 作者代码
            if not code_section:
                for k, v in sections.items():
                    if k.startswith('作者代码'):
                        code_section = v
                        break
            blocks = parse_code_blocks(code_section)
            code_text = '\n'.join(blocks)
            has_code = judge_has_code(blocks)
            data_source, _ = classify_data_source(blocks, has_code, text)
            fields = extract_fields(code_text)
            deps = extract_deps(code_text)
            core = extract_core_formula(blocks) if blocks else ''
            code_lines_n = count_code_lines(blocks)
            kw = lookup_keywords(date, title, idx_map)
            ic_claim, layer_claim = extract_claims(sections)
            ftype = guess_type(title, kw, code_text)

            rows.append({
                'date': date or '',
                'original_title': title,
                'likely_factor_type': ftype,
                'has_code': has_code,
                'data_source': data_source,
                'fields_used': '|'.join(fields),
                'external_deps': '|'.join(deps),
                'code_lines': code_lines_n,
                'author_ic_claim': ic_claim,
                'author_layer_claim': layer_claim,
                'keywords_from_index': kw,
                'core_formula': core,
                'source_file': fname,
                'source': source,
            })
            n_ok += 1
        except Exception as e:
            tb = traceback.format_exc()
            errors.append(f'{fname}: {e}\n{tb}\n')

    # ---- write CSV ----
    cols = ['date','original_title','likely_factor_type','has_code','data_source',
            'fields_used','external_deps','code_lines','author_ic_claim',
            'author_layer_claim','keywords_from_index','core_formula','source_file','source']

    with open(OUT_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ---- summary md ----
    type_dist = Counter(r['likely_factor_type'] for r in rows)
    ds_dist = Counter(r['data_source'] for r in rows)
    hc_dist = Counter(r['has_code'] for r in rows)
    src_dist = Counter(r['source'] for r in rows)
    kw_counter = Counter()
    for r in rows:
        for k in r['keywords_from_index'].split('/'):
            k = k.strip()
            if k:
                kw_counter[k] += 1

    unclear_files = [(r['date'], r['source_file']) for r in rows if r['data_source'] == 'unclear']
    nocode_files = [(r['date'], r['source_file']) for r in rows if r['has_code'] == 'none']
    academic_files = [(r['date'], r['source_file']) for r in rows if r['likely_factor_type'] in ('academic','fund_selection')]

    md = []
    md.append('# 因子分类汇总报告\n')
    md.append(f'- 总文件数: {len(rows)}\n')
    md.append(f'- 解析成功: {n_ok}, 失败: {len(errors)}\n')

    md.append('\n## likely_factor_type 分布\n')
    for t, c in type_dist.most_common():
        md.append(f'- {t}: {c}')
    md.append('')

    md.append('\n## data_source 分布\n')
    for t, c in ds_dist.most_common():
        md.append(f'- {t}: {c}')
    md.append('')

    md.append('\n## has_code 分布\n')
    for t, c in hc_dist.most_common():
        md.append(f'- {t}: {c}')
    md.append('')

    md.append('\n## source 分布\n')
    for t, c in src_dist.most_common():
        md.append(f'- {t}: {c}')
    md.append('')

    md.append('\n## keywords_from_index 频次\n')
    for k, c in kw_counter.most_common():
        md.append(f'- {k}: {c}')
    md.append('')

    md.append('\n## data_source=unclear (人工再看)\n')
    for d, f in unclear_files:
        md.append(f'- {d}  {f}')
    md.append('')

    md.append('\n## has_code=none (纯思路文章)\n')
    for d, f in nocode_files:
        md.append(f'- {d}  {f}')
    md.append('')

    md.append('\n## likely_factor_type=academic / fund_selection\n')
    for d, f in academic_files:
        md.append(f'- {d}  {f}')
    md.append('')

    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    # ---- error log ----
    if errors:
        with open(ERR_LOG, 'w', encoding='utf-8') as f:
            f.write('\n'.join(errors))

    print(f'成功 {n_ok} 个, 失败 {len(errors)} 个, 见 errors.log')
    print('\n--- 类型分布 ---')
    for t, c in type_dist.most_common():
        print(f'  {t}: {c}')
    print('\n--- 数据源分布 ---')
    for t, c in ds_dist.most_common():
        print(f'  {t}: {c}')
    print('\n--- has_code 分布 ---')
    for t, c in hc_dist.most_common():
        print(f'  {t}: {c}')
    print('\n--- source 分布 ---')
    for t, c in src_dist.most_common():
        print(f'  {t}: {c}')

if __name__ == '__main__':
    main()
