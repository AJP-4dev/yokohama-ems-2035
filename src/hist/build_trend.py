"""年代別搬送率の推移（2013〜2024）と実測トレンドを算出 → trend.json
搬送人員: 消防年報 年齢別搬送人員（各年中、5歳階級）
人口:     総務省 住民基本台帳 年齢階級別人口（翌年1月1日・総計・横浜市）
"""
import json, glob, math, pathlib, re, ast, xlrd, openpyxl
HERE = pathlib.Path(__file__).parent
A5 = ['0～4歳','5～9歳','10～14歳','15～19歳','20～24歳','25～29歳','30～34歳','35～39歳','40～44歳','45～49歳','50～54歳','55～59歳','60～64歳','65～69歳','70～74歳','75～79歳','80～84歳','85～89歳','90～94歳','95～99歳','100歳以上']
G_OF = {a: ('c' if i < 3 else 'w' if i < 13 else 'e1' if i < 15 else 'e2' if i < 17 else 'e3') for i, a in enumerate(A5)}
GROUPS = ['c', 'w', 'e1', 'e2', 'e3']
# --- 搬送人員 ---
tr = {}
for f in glob.glob(str(HERE / 'transport_by_age_*.json')):
    for y, d in json.load(open(f)).items():
        assert sum(d['rows'].values()) == d['total'], (f, y)
        assert len(d['rows']) == 21, (f, y, len(d['rows']))
        d['rows'] = dict(zip(A5, d['rows'].values()))   # 表記ゆれ（～/〜）を順序で正規化
        tr[int(y)] = d
src = open(HERE.parent / 'build_model.py', encoding='utf-8').read()
m = re.search(r'TRANSPORT_5Y = \{(.*?)\}', src, re.S)
T24 = ast.literal_eval('{' + m.group(1) + '}')  # 自作ファイル内の辞書リテラルのみ
T24 = dict(zip(A5, T24.values()))
tr[2024] = {'total': sum(T24.values()), 'dispatch': 256481, 'rows': T24}
# --- 人口（翌年1/1） ---
POP_FILES = {2014: '000291857.xls', 2015: '000366465.xls', 2016: '000428779.xls', 2017: '000494086.xls', 2018: '000563141.xls',
             2019: '000633282.xls', 2020: '000701517.xls', 2021: '000762444.xlsx', 2022: '000829118.xlsx', 2023: '000892857.xlsx',
             2024: '000959257.xlsx', 2025: '001023715.xlsx', 2026: '001083790.xlsx'}
def read_pop(path):
    if path.endswith('.xls'):
        wb = xlrd.open_workbook(path)
        for sh in wb.sheets():
            for i in range(sh.nrows):
                r = sh.row_values(i)
                if any(isinstance(c, str) and '横浜市' in c for c in r[:6]) and '計' in [c for c in r[:6] if isinstance(c, str)]:
                    return [int(v) for v in r[5:] if isinstance(v, (int, float))]
    wb = openpyxl.load_workbook(path, read_only=True)
    for ws in wb.worksheets:
        for r in ws.iter_rows(values_only=True):
            if any(isinstance(c, str) and '横浜市' in c for c in r[:6]) and '計' in [c for c in r[:6] if isinstance(c, str)]:
                return [int(v) for v in r[5:] if isinstance(v, (int, float))]
pop = {}
for jan, f in POP_FILES.items():
    if not (HERE / f).exists(): continue
    vals = read_pop(str(HERE / f))
    if len(vals) == 17:   # 平成26年(2014.1.1)版は「80歳以上」一括。2015.1.1の80歳以上内の構成比で按分（近似）
        v15 = read_pop(str(HERE / POP_FILES[2015])); tail = v15[16:]; share = [t / sum(tail) for t in tail]
        vals = vals[:16] + [vals[16] * sh for sh in share]
    pop[jan] = dict(zip(A5, vals))
years = sorted(y for y in tr if (y + 1) in pop)
rate = {y: {a: tr[y]['rows'][a] / pop[y + 1][a] for a in A5} for y in years}
grp = {y: {g: sum(tr[y]['rows'][a] for a in A5 if G_OF[a] == g) / sum(pop[y + 1][a] for a in A5 if G_OF[a] == g) for g in GROUPS} for y in years}
def loglin(ys, vals):
    n = len(ys); mx = sum(ys) / n; my = sum(math.log(v) for v in vals) / n
    a = sum((y - mx) * (math.log(v) - my) for y, v in zip(ys, vals)) / sum((y - mx) ** 2 for y in ys)
    return math.exp(a) - 1
FIT_YEARS = [y for y in years if y not in (2020, 2021)]
g_grp = {g: loglin(FIT_YEARS, [grp[y][g] for y in FIT_YEARS]) for g in GROUPS}
g_5y = {a: loglin(FIT_YEARS, [rate[y][a] for y in FIT_YEARS]) for a in A5}
g_pre = {g: loglin([y for y in FIT_YEARS if y <= 2019], [grp[y][g] for y in FIT_YEARS if y <= 2019]) for g in GROUPS}
g_post = {g: (grp[2024][g] / grp[2022][g]) ** 0.5 - 1 for g in GROUPS}
allrate = {y: tr[y]['total'] / sum(pop[y + 1].values()) for y in years}
g_all = loglin(FIT_YEARS, [allrate[y] for y in FIT_YEARS])
std = {y: sum(rate[y][a] * pop[2025][a] for a in A5) / sum(pop[2025].values()) for y in years}   # 年齢構成を2025.1.1で固定
g_std = loglin(FIT_YEARS, [std[y] for y in FIT_YEARS])
out = {'years': years, 'rate5y': {y: rate[y] for y in years}, 'rateGroup': {y: grp[y] for y in years}, 'allRate': allrate, 'stdRate': std,
       'growthGroup': g_grp, 'growth5y': g_5y, 'growthGroupPre2019': g_pre, 'growthGroup2022_24': g_post, 'growthAll': g_all, 'growthStd': g_std,
       'fitYears': FIT_YEARS, 'transport': {y: tr[y]['total'] for y in years}, 'dispatch': {y: tr[y]['dispatch'] for y in years},
       'popTotal': {y + 1: sum(pop[y + 1].values()) for y in years}}
json.dump(out, open(HERE / 'trend.json', 'w'), ensure_ascii=False, indent=1)
print('years', years)
for y in years: print(y, {g: round(grp[y][g] * 100, 2) for g in GROUPS}, 'all %.2f  age-adj %.2f' % (allrate[y] * 100, std[y] * 100))
print('growth/yr fit(2013-19,2022-24):', {g: f'{v*100:+.2f}%' for g, v in g_grp.items()}, 'all %+.2f%%  age-adj %+.2f%%' % (g_all * 100, g_std * 100))
print('growth pre2019   :', {g: f'{v*100:+.2f}%' for g, v in g_pre.items()})
print('growth 2022-24   :', {g: f'{v*100:+.2f}%' for g, v in g_post.items()})
print('growth 5y classes:', {a: f'{v*100:+.1f}' for a, v in g_5y.items()})
