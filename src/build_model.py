"""横浜市 救急需要推計モデル v2（市公式の行政区別推計＋年齢5歳階級別搬送率）

入力:
  src/projection.json   市将来人口推計（令和5年推計・中位）区別×5歳階級×各年（extract_projection.py）
  src/base_inputs.json  2025.1.1 実績人口（区別・年齢4区分）、2020国勢調査 昼夜間人口、年次系列
  本ファイル内定数        令和6年 年齢5歳階級別搬送人員・行政区別出場件数（消防局年報 令和6年・確定値）
出力:
  src/model.json, data.js（HTML埋込用 const DATA=...）

計算:
  ① 基準人口(2025) = R7.1.1実績（区別・年齢4区分）を、市推計2025年の区別年齢構成で5歳階級(21区分)に按分
  ② 将来人口(年)   = 基準人口 × 市推計の区別・5歳階級別 変化率(年/2025)
  ③ 搬送率(2024)   = 5歳階級別搬送人員 ÷ 2025.1.1 市人口(5歳階級)
  ④ 昼間補正       = 0.35 × (流入−流出) × 15–64歳平均搬送率
  ⑤ 期待出場 = (Σ人口×搬送率 + 昼間補正) × 出場/搬送比 ； 校正係数 = 2024実績 ÷ 期待出場(2025)
  ⑥ 将来出場 = 期待出場(将来人口) × 校正係数   （シナリオBはフロントで 年+1.5% を乗算）
"""
import json, pathlib
HERE = pathlib.Path(__file__).parent
P = json.load(open(HERE / 'projection.json'))
B = json.load(open(HERE / 'base_inputs.json'))

# ---- 消防局年報（令和6年）確定値 ---------------------------------------------
# 年齢別搬送人員の状況（p.106）合計欄
TRANSPORT_5Y = {
    '0～4歳': 10817, '5～9歳': 4431, '10～14歳': 3142, '15～19歳': 4189, '20～24歳': 6142,
    '25～29歳': 6023, '30～34歳': 5736, '35～39歳': 5170, '40～44歳': 5593, '45～49歳': 6817,
    '50～54歳': 9119, '55～59歳': 9654, '60～64歳': 9299, '65～69歳': 9776, '70～74歳': 15042,
    '75～79歳': 20826, '80～84歳': 27262, '85～89歳': 26063, '90～94歳': 16530, '95～99歳': 5167,
    '100歳以上': 673}
TRANSPORT_TOTAL = 207471
DISPATCH_TOTAL = 256481
# 行政区別出場件数（p.100）合計欄（市外50件を除く）
DISPATCH_WARD = {'鶴見': 18986, '神奈川': 15874, '西': 10807, '中': 18603, '南': 15534, '港南': 15542,
                 '保土ケ谷': 13481, '旭': 16995, '磯子': 11674, '金沢': 13684, '港北': 20313, '緑': 11838,
                 '青葉': 15857, '都筑': 10984, '戸塚': 18821, '栄': 8127, '泉': 10495, '瀬谷': 8816}
# 行政区別 転院搬送（p.100）— 校正係数の説明用
TRANSFER_WARD = {'鶴見': 799, '神奈川': 836, '西': 387, '中': 858, '南': 535, '港南': 1087, '保土ケ谷': 452,
                 '旭': 758, '磯子': 497, '金沢': 754, '港北': 940, '緑': 511, '青葉': 830, '都筑': 329,
                 '戸塚': 1499, '栄': 187, '泉': 591, '瀬谷': 201}
EMS_UNITS = 85.5  # 令和6年中の隊数（うち6隊が日勤救急隊）p.98 注2
# 救急隊別活動状況（p.105）から数えた区別の隊数（2024年末時点）。[24時間隊, 日勤救急隊]
# 日勤隊＝出場1,200〜1,360件の隊（鶴見第2・西第3・港北第2・緑第2・戸塚第2・瀬谷第2）。
# 山下町第2・綱島は年途中（3か月）設置のため年報では0.25隊だが、年末時点では1隊として数える。
UNITS_WARD = {'鶴見': [6, 1], '神奈川': [5, 0], '西': [4, 1], '中': [6, 0], '南': [5, 0], '港南': [5, 0],
              '保土ケ谷': [4, 0], '旭': [5, 0], '磯子': [3, 0], '金沢': [5, 0], '港北': [6, 1], '緑': [4, 1],
              '青葉': [5, 0], '都筑': [4, 0], '戸塚': [4, 1], '栄': [3, 0], '泉': [4, 0], '瀬谷': [3, 1]}
# 時間帯別出場件数（p.102）0時台〜23時台
HOURLY = [6969, 5933, 5166, 4790, 4814, 5700, 7045, 9495, 12168, 14924, 15729, 14799,
          14564, 13922, 13494, 13282, 13440, 13856, 13351, 12944, 11732, 10762, 9463, 8139]
DAY_HOURS = list(range(8, 20))  # 昼＝8〜19時台
assert sum(HOURLY) == DISPATCH_TOTAL, sum(HOURLY)
DAY_SHARE = sum(HOURLY[h] for h in DAY_HOURS) / DISPATCH_TOTAL
DAYF = 0.35       # 通勤通学者の区内滞在時間割合（8.5h/24h）
assert sum(TRANSPORT_5Y.values()) == TRANSPORT_TOTAL
assert sum(DISPATCH_WARD.values()) + 50 == DISPATCH_TOTAL
DR = DISPATCH_TOTAL / TRANSPORT_TOTAL

A5 = list(TRANSPORT_5Y)                     # 21 階級ラベル
G_OF = {a: ('c' if i < 3 else 'w' if i < 13 else 'e1' if i < 15 else 'e2' if i < 17 else 'e3') for i, a in enumerate(A5)}
GROUPS = ['c', 'w', 'e1', 'e2', 'e3']
GROUP4 = {'c': 'c', 'w': 'w', 'e1': 'e1', 'e2': 'e2', 'e3': 'e2'}   # 実績4区分へのマップ（e2+e3=75+）
YEARS = list(range(2025, 2041))

# projection.json は5区分集計なので、5歳階級はxlsxから再読込
import openpyxl
def proj21(sheet):
    wb = openpyxl.load_workbook(HERE / '0048_20240410.xlsx', read_only=True)
    ws = wb[sheet]; rows = list(ws.iter_rows(min_row=1, max_row=145, values_only=True))
    years = [int(str(v).rstrip('年')) for v in rows[6][1:] if v]
    start = next(i for i, r in enumerate(rows) if r[0] == '■年齢５歳階級別人口（総数）')
    out = {y: {} for y in years}
    for r in rows[start + 1:start + 30]:
        lab = r[0]
        if lab in ('100～104歳', '100～104歳以上', '105歳以上'): lab = '100歳以上'
        if lab in TRANSPORT_5Y:
            for y, v in zip(years, r[1:]): out[y][lab] = out[y].get(lab, 0) + int(v or 0)
        elif isinstance(lab, str) and lab.startswith('■'): break
    assert all(len(out[y]) == 21 for y in years), sheet
    return out
PR = {w: proj21(w + '区') for w in DISPATCH_WARD}

# ① 基準人口(2025, 21区分) --------------------------------------------------------
def base21(w):
    act = B['wards'][w]['pop2025']                      # c,w,e1,e2(75+)
    pr = PR[w][2025]
    out = {}
    for g4 in ('c', 'w', 'e1', 'e2'):
        labs = [a for a in A5 if GROUP4[G_OF[a]] == g4]
        s = sum(pr[a] for a in labs)
        for a in labs: out[a] = act[g4] * pr[a] / s
    return out
BASE = {w: base21(w) for w in DISPATCH_WARD}

# ② 将来人口 ---------------------------------------------------------------------
def pop21(w, y):
    b, p0, py = BASE[w], PR[w][2025], PR[w][y]
    return {a: b[a] * py[a] / p0[a] for a in A5}

# ③ 搬送率（市全体・2025.1.1実績ベース） ----------------------------------------
city25 = {a: sum(BASE[w][a] for w in BASE) for a in A5}
RATE = {a: TRANSPORT_5Y[a] / city25[a] for a in A5}
w_labs = [a for a in A5 if G_OF[a] == 'w']
RATE_W = sum(TRANSPORT_5Y[a] for a in w_labs) / sum(city25[a] for a in w_labs)
rate_group = {g: sum(TRANSPORT_5Y[a] for a in A5 if G_OF[a] == g) / sum(city25[a] for a in A5 if G_OF[a] == g) for g in GROUPS}

# ④⑤⑥ ------------------------------------------------------------------------------
def agg(p21):
    o = {g: 0.0 for g in GROUPS}
    for a in A5: o[G_OF[a]] += p21[a]
    return o

wards = []
for w, disp24 in DISPATCH_WARD.items():
    bi = B['wards'][w]
    net = bi['in'] - bi['out']
    day_extra_tr = DAYF * net * RATE_W                       # 搬送人員ベースの昼間補正
    def expected_by_group(y):
        p = pop21(w, y); o = {g: 0.0 for g in GROUPS}
        for a in A5: o[G_OF[a]] += p[a] * RATE[a]
        o['w'] += day_extra_tr
        return {g: v * DR for g, v in o.items()}
    e25 = expected_by_group(2025)
    fac = disp24 / sum(e25.values())
    pop, disp, by_age = {}, {}, {}
    for y in YEARS:
        e = expected_by_group(y)
        pop[y] = {g: round(v) for g, v in agg(pop21(w, y)).items()}
        by_age[y] = {g: round(v * fac) for g, v in e.items()}
        disp[y] = round(sum(e.values()) * fac)
    assert disp[2025] == disp24, (w, disp[2025], disp24)
    wards.append({'name': w, 'code': bi['code'], 'pop': pop, 'disp': disp, 'byAge': by_age,
                  'disp24': disp24, 'transfer24': TRANSFER_WARD[w], 'fac': round(fac, 3),
                  'dn': bi['dn'], 'day20': bi['day20'], 'night20': bi['night20'], 'in': bi['in'], 'out': bi['out'],
                  'dayExtra': round(day_extra_tr * DR * fac), 'units': UNITS_WARD[w][0], 'unitsDay': UNITS_WARD[w][1]})

city = {y: {g: sum(wd['pop'][y][g] for wd in wards) for g in GROUPS} for y in YEARS}
for y in YEARS: city[y]['t'] = sum(city[y][g] for g in GROUPS)
city_off = {y: dict(P['city'][str(y)] if str(y) in P['city'] else P['city'][y]) for y in YEARS}

model = {
    'years': YEARS, 'wards': wards, 'city': city, 'cityOfficial': city_off,
    'rates': {g: round(v, 5) for g, v in rate_group.items()},
    'rates5y': {a: round(v, 5) for a, v in RATE.items()},
    'transport5y': TRANSPORT_5Y, 'dispatchTotal': DISPATCH_TOTAL, 'transportTotal': TRANSPORT_TOTAL,
    'dispRatio': round(DR, 4), 'dayf': DAYF, 'emsUnits': EMS_UNITS, 'hourly': HOURLY, 'dayShare': round(DAY_SHARE, 4), 'dayHours': [8, 19],
    'series': B['series'],
}
json.dump(model, open(HERE / 'model.json', 'w'), ensure_ascii=False)

# data.js（HTML埋込） -----------------------------------------------------------
geo = {g['name']: g for g in json.load(open(HERE / 'wards_geo.json'))['wards']}
dw = []
for wd in wards:
    d = dict(wd); d['pop'] = {str(y): v for y, v in wd['pop'].items()}; d['disp'] = {str(y): v for y, v in wd['disp'].items()}
    d['byAge'] = {str(y): v for y, v in wd['byAge'].items()}
    d['c'] = geo[wd['name']]['c']; d['rings'] = geo[wd['name']]['rings']
    dw.append(d)
DATA = {'wards': dw, 'rates': model['rates'], 'dispRatio': model['dispRatio'], 'dayf': DAYF,
        'city': {str(y): v for y, v in city.items()}, 'series': B['series'], 'emsUnits': EMS_UNITS,
        'hourly': HOURLY, 'dayShare': round(DAY_SHARE, 4), 'dayHours': [8, 19]}
open(HERE.parent / 'data.js', 'w').write('const DATA=' + json.dumps(DATA, ensure_ascii=False, separators=(',', ':')) + ';\n')

# ---- サマリー -----------------------------------------------------------------
tot = lambda y: sum(wd['disp'][y] for wd in wards)
print(f'出場/搬送比 {DR:.4f}  15–64平均搬送率 {RATE_W*100:.2f}%  昼(8-19時)シェア {DAY_SHARE*100:.1f}%  隊数 {sum(a+b for a,b in UNITS_WARD.values())}（日勤{sum(b for a,b in UNITS_WARD.values())}）')
print('搬送率(5区分):', {g: f'{v*100:.2f}%' for g, v in rate_group.items()})
print('市人口(実績ベース)', {y: city[y] for y in (2025, 2030, 2035, 2040)})
for y in (2025, 2030, 2035, 2040):
    print(f'{y}: A {tot(y):,}  ({(tot(y)/tot(2025)-1)*100:+.1f}%)   B {tot(y)*1.015**(y-2024):,.0f}')
    bag = {g: sum(wd['byAge'][y][g] for wd in wards) for g in GROUPS}
    print('   byAge', {g: f'{v:,} ({v/sum(bag.values())*100:.0f}%)' for g, v in bag.items()})
print('区別 2035/2024:')
for wd in sorted(wards, key=lambda x: -x['disp'][2035] / x['disp24']):
    d = wd['disp']
    print(f"  {wd['name']:<5} fac {wd['fac']:.2f}  2030 {(d[2030]/wd['disp24']-1)*100:+.1f}%  2035 {(d[2035]/wd['disp24']-1)*100:+.1f}%  2040 {(d[2040]/wd['disp24']-1)*100:+.1f}%  pop35 {(sum(wd['pop'][2035].values())/sum(wd['pop'][2025].values())-1)*100:+.1f}%  dayExtra {wd['dayExtra']:+}")
