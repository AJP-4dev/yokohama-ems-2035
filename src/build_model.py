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
# 区の面積 km²（国土地理院 全国都道府県市区町村別面積調 R8_07_mencho.csv の令和6年値。港湾・水面を含む）
AREA_WARD = {'鶴見': 33.21, '神奈川': 23.73, '西': 7.03, '中': 22.01, '南': 12.65, '港南': 19.90, '保土ケ谷': 21.93, '旭': 32.73,
             '磯子': 19.02, '金沢': 30.95, '港北': 31.40, '緑': 25.51, '青葉': 35.22, '都筑': 27.87, '戸塚': 35.79, '栄': 18.52,
             '泉': 23.58, '瀬谷': 17.17}
# 救急隊別活動状況（年報 p.105）: (区, 隊名, 出場件数, 搬送人員, 現場到着までの平均時間[分], 平均距離[km])。増強隊も含む。局の2隊は除外
UNIT_ROWS = [
 ('鶴見','鶴見第1',3547,2869,7.1,2.0),('鶴見','鶴見第2',1321,1177,7.1,2.0),('鶴見','生麦',3083,2529,7.0,2.1),('鶴見','矢向',2692,2143,8.8,2.8),('鶴見','岸谷',3325,2769,8.0,2.7),('鶴見','寺尾',3206,2679,8.7,2.7),('鶴見','駒岡',3354,2840,9.1,2.8),('鶴見','鶴見増強',130,114,8.9,2.9),
 ('神奈川','神奈川第1',3349,2606,9.0,2.4),('神奈川','神奈川第2',3315,2612,9.1,2.4),('神奈川','菅田',3340,2782,8.8,3.2),('神奈川','片倉',3310,2796,8.6,2.7),('神奈川','松見',3502,2533,9.7,2.7),('神奈川','神奈川増強',78,67,10.4,3.4),
 ('西','西第1',3441,2774,8.1,2.1),('西','西第2',3390,2397,8.4,2.1),('西','西第3',1357,1114,8.5,2.2),('西','浅間町',3805,2871,7.9,2.3),('西','境之谷',3046,2059,8.2,2.1),('西','西増強',132,109,10.3,3.0),
 ('中','中第1',4469,2462,5.9,1.7),('中','中第2',4518,2478,6.0,1.7),('中','北方',2886,2152,6.7,2.1),('中','山下町第1',3636,2214,6.6,1.8),('中','山下町第2',763,493,7.0,2.1),('中','山元町',3060,2318,7.1,2.3),('中','中増強',205,123,7.0,2.2),
 ('南','南第1',3377,2613,8.0,1.9),('南','南第2',3361,2685,7.6,1.9),('南','蒔田',3533,2805,8.3,2.1),('南','大岡',3157,2628,8.1,2.5),('南','六ツ川',3070,2421,9.3,2.7),('南','南増強',103,82,8.2,2.5),
 ('港南','港南第1',3024,2480,9.6,2.9),('港南','港南第2',2978,2432,9.4,2.9),('港南','芹が谷',3237,2722,8.9,2.7),('港南','野庭',3552,3165,8.1,2.7),('港南','港南台',3117,2656,8.4,2.8),('港南','港南増強',97,81,10.8,3.7),
 ('保土ケ谷','保土ケ谷',3162,2406,8.9,2.7),('保土ケ谷','西谷',3049,2557,9.7,3.0),('保土ケ谷','今井',2752,2281,10.4,3.3),('保土ケ谷','権太坂',2947,2542,9.4,2.8),('保土ケ谷','保土ケ谷増強',49,44,10.3,3.5),
 ('旭','旭',3227,2800,9.4,2.8),('旭','都岡',2771,2378,10.0,3.2),('旭','南本宿',3201,2682,8.8,2.9),('旭','若葉台',2593,2282,9.4,3.5),('旭','今宿',3265,2758,9.4,3.1),('旭','旭増強',119,103,10.6,3.8),
 ('磯子','磯子',3079,2515,8.1,2.5),('磯子','洋光台',3149,2702,8.0,2.6),('磯子','杉田',2960,2520,8.6,2.7),('磯子','磯子増強',108,93,9.3,3.4),
 ('金沢','金沢第1',2995,2426,8.0,2.4),('金沢','金沢第2',2880,2366,8.3,2.4),('金沢','富岡',3308,2592,8.3,2.8),('金沢','釜利谷',2547,2182,9.0,3.1),('金沢','幸浦',2469,2219,8.7,3.0),('金沢','金沢増強',72,58,9.4,3.1),
 ('港北','港北第1',3101,2423,9.1,2.8),('港北','港北第2',1272,1118,9.3,2.9),('港北','綱島',789,576,9.1,2.6),('港北','日吉',3207,2427,8.6,2.5),('港北','篠原',3122,2626,8.7,2.7),('港北','高田',2917,2223,8.8,2.6),('港北','新羽',3059,2297,9.9,3.0),('港北','港北増強',110,92,10.5,3.4),
 ('緑','緑第1',2887,2275,8.9,2.9),('緑','緑第2',1258,1070,9.7,3.1),('緑','長津田',2899,2341,9.4,2.9),('緑','鴨居',2701,2252,9.9,3.0),('緑','白山',3087,2565,9.7,3.0),('緑','緑増強',43,36,10.2,3.6),
 ('青葉','青葉',2977,2549,8.7,2.9),('青葉','元石川',2943,2450,8.4,2.6),('青葉','鴨志田',2644,2167,8.2,3.0),('青葉','青葉台',3281,2715,8.5,2.5),('青葉','荏田',3186,2506,8.6,2.9),('青葉','青葉増強',103,89,10.1,3.3),
 ('都筑','都筑',2539,2285,8.0,2.8),('都筑','川和',2766,2265,9.3,3.1),('都筑','仲町台',2544,2198,9.0,3.2),('都筑','北山田',2471,2066,9.2,3.2),('都筑','都筑増強',158,136,9.9,3.6),
 ('戸塚','戸塚第1',3247,2865,9.0,2.8),('戸塚','戸塚第2',1209,1087,9.2,2.9),('戸塚','大正',3088,2756,8.7,2.7),('戸塚','吉田',3309,2644,9.3,2.8),('戸塚','東戸塚',2696,2263,9.8,3.1),('戸塚','戸塚増強',97,85,10.1,3.1),
 ('栄','栄',3321,2803,8.5,2.7),('栄','上郷',2218,1952,8.7,3.4),('栄','豊田',3045,2700,9.2,3.0),('栄','栄増強',90,75,10.1,3.7),
 ('泉','泉',2997,2782,8.9,2.8),('泉','岡津',3399,2723,8.9,3.0),('泉','中田',3244,2811,9.5,2.9),('泉','いずみ野',2841,2563,9.4,3.3),('泉','泉増強',108,96,10.5,3.7),
 ('瀬谷','瀬谷第1',2959,2575,9.1,2.7),('瀬谷','瀬谷第2',1222,1098,9.3,3.0),('瀬谷','下瀬谷',2925,2436,8.8,2.8),('瀬谷','中瀬谷',2329,1909,9.1,3.1),('瀬谷','瀬谷増強',96,88,11.3,3.9),
]
UNIT_BUREAU = [('局','横消第2',54,51,12.3,3.6),('局','WS第1',355,6,0.0,0.0)]
assert sum(r[2] for r in UNIT_ROWS+UNIT_BUREAU) == DISPATCH_TOTAL, sum(r[2] for r in UNIT_ROWS+UNIT_BUREAU)
assert sum(r[3] for r in UNIT_ROWS+UNIT_BUREAU) == TRANSPORT_TOTAL, sum(r[3] for r in UNIT_ROWS+UNIT_BUREAU)
# 行政区別 事故種別（年報 p.100）: 急病,一般負傷,交通事故,転院搬送,自損行為,加害,労働災害,運動競技,火災,水難,医師搬送,資器材等,自然災害,その他
TYPE_KEYS = ['急病','一般負傷','交通事故','転院搬送','自損行為','加害','労働災害','運動競技','火災','水難','医師搬送','資器材等','自然災害','その他']
TYPE_WARD = {
 '鶴見':[13530,3222,852,799,109,70,141,84,62,20,6,0,1,90],'神奈川':[11169,2724,594,836,72,61,78,101,65,4,99,0,0,71],
 '西':[7526,2179,301,387,73,60,85,30,33,3,83,1,0,46],'中':[12740,3545,637,858,120,236,119,92,106,14,15,0,0,121],
 '南':[11413,2700,458,535,110,79,43,48,42,5,8,0,0,93],'港南':[10757,2899,452,1087,84,62,41,50,33,0,4,0,1,72],
 '保土ケ谷':[9398,2580,557,452,73,45,50,82,38,4,114,0,0,88],'旭':[11904,3280,646,758,86,61,57,55,57,1,8,0,0,82],
 '磯子':[8239,2274,364,497,65,37,58,50,32,3,3,0,0,52],'金沢':[9474,2550,502,754,58,37,120,81,35,6,5,0,1,61],
 '港北':[14445,3631,674,940,88,55,108,169,57,7,9,0,0,130],'緑':[8534,2049,455,511,63,38,42,48,33,3,5,0,0,57],
 '青葉':[10805,3059,671,830,109,47,77,129,40,1,3,0,0,86],'都筑':[7716,1991,580,329,65,26,100,88,33,1,2,0,0,53],
 '戸塚':[12913,3393,622,1499,78,42,55,88,42,2,1,0,1,85],'栄':[5979,1536,218,187,41,16,31,48,27,1,0,0,0,43],
 '泉':[7466,1830,365,591,53,23,26,69,23,0,0,0,0,49],'瀬谷':[6486,1567,359,201,54,29,29,30,21,0,2,0,0,38]}
for w, v in TYPE_WARD.items():
    assert sum(v) == DISPATCH_WARD[w], (w, sum(v), DISPATCH_WARD[w])
# 不取扱（不搬送）理由 市全体（年報 p.108）
NON_TRANSPORT = {'辞退': 40135, '死亡': 3816, '傷病者なし': 1566, '途中帰署': 2101, '虚誤報': 1223, '搬送後': 321, '中継': 8, 'その他': 506}
assert sum(NON_TRANSPORT.values()) == 49676
def unit_stats(w):
    rows = [r for r in UNIT_ROWS if r[0] == w]
    d = sum(r[2] for r in rows); t = sum(r[3] for r in rows)
    return {'unitDisp': d, 'unitTr': t, 'nonTr': round(1 - t / d, 4),
            'arrive': round(sum(r[2] * r[4] for r in rows) / d, 2), 'dist': round(sum(r[2] * r[5] for r in rows) / d, 2)}
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
                  'dayExtra': round(day_extra_tr * DR * fac), 'units': UNITS_WARD[w][0], 'unitsDay': UNITS_WARD[w][1], 'area': AREA_WARD[w], 'types': dict(zip(TYPE_KEYS, TYPE_WARD[w])), **unit_stats(w)})

city = {y: {g: sum(wd['pop'][y][g] for wd in wards) for g in GROUPS} for y in YEARS}
for y in YEARS: city[y]['t'] = sum(city[y][g] for g in GROUPS)
city_off = {y: dict(P['city'][str(y)] if str(y) in P['city'] else P['city'][y]) for y in YEARS}

TREND = json.load(open(HERE / 'hist' / 'trend.json')) if (HERE / 'hist' / 'trend.json').exists() else None
model = {
    'trend': TREND,
    'years': YEARS, 'wards': wards, 'city': city, 'cityOfficial': city_off,
    'rates': {g: round(v, 5) for g, v in rate_group.items()},
    'rates5y': {a: round(v, 5) for a, v in RATE.items()},
    'transport5y': TRANSPORT_5Y, 'dispatchTotal': DISPATCH_TOTAL, 'transportTotal': TRANSPORT_TOTAL,
    'dispRatio': round(DR, 4), 'dayf': DAYF, 'emsUnits': EMS_UNITS, 'hourly': HOURLY, 'dayShare': round(DAY_SHARE, 4), 'dayHours': [8, 19], 'nonTransport': NON_TRANSPORT, 'typeKeys': TYPE_KEYS,
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
        'hourly': HOURLY, 'dayShare': round(DAY_SHARE, 4), 'dayHours': [8, 19], 'nonTransport': NON_TRANSPORT, 'typeKeys': TYPE_KEYS,
        'cityArrive': round(sum(r[2]*r[4] for r in UNIT_ROWS)/sum(r[2] for r in UNIT_ROWS),2), 'cityNonTr': round(1-TRANSPORT_TOTAL/DISPATCH_TOTAL,4),
        'trend': TREND and {'years': TREND['years'], 'rateGroup': TREND['rateGroup'], 'stdRate': TREND['stdRate'], 'allRate': TREND['allRate'],
                            'growthGroup': TREND['growthGroup'], 'growthStd': TREND['growthStd'], 'growthAll': TREND['growthAll'],
                            'growthPre': TREND['growthGroupPre2019'], 'growthPost': TREND['growthGroup2022_24'], 'fitYears': TREND['fitYears'],
                            'transport': TREND['transport'], 'dispatch': TREND['dispatch']}}
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
print('区別 不搬送率/到着:', {w['name']:(w['nonTr'],w['arrive'],w['dist']) for w in wards})
print('区別 2035/2024:')
for wd in sorted(wards, key=lambda x: -x['disp'][2035] / x['disp24']):
    d = wd['disp']
    print(f"  {wd['name']:<5} fac {wd['fac']:.2f}  2030 {(d[2030]/wd['disp24']-1)*100:+.1f}%  2035 {(d[2035]/wd['disp24']-1)*100:+.1f}%  2040 {(d[2040]/wd['disp24']-1)*100:+.1f}%  pop35 {(sum(wd['pop'][2035].values())/sum(wd['pop'][2025].values())-1)*100:+.1f}%  dayExtra {wd['dayExtra']:+}")
