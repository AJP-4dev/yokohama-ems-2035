"""横浜市将来人口推計（令和5年推計・中位）行政区別xlsx → projection.json

入力: src/0048_20240410.xlsx（区別の男女別・各歳・年齢3区分・年齢4区分・年齢5歳階級別人口）
出力: src/projection.json
  {"years":[2020..2070], "city":{year:{c,w,e1,e2,e3,t}}, "wards":{区名:{year:{...}}}}
  c=0-14, w=15-64, e1=65-74, e2=75-84, e3=85+, t=合計（総数・中位）
"""
import json, openpyxl, pathlib
HERE = pathlib.Path(__file__).parent
SRC = HERE / '0048_20240410.xlsx'
# 5歳階級ブロック（総数）: 行120〜141 のラベルで集計
GROUPS = {
    'c':  ['0～4歳', '5～9歳', '10～14歳'],
    'w':  ['15～19歳', '20～24歳', '25～29歳', '30～34歳', '35～39歳', '40～44歳', '45～49歳', '50～54歳', '55～59歳', '60～64歳'],
    'e1': ['65～69歳', '70～74歳'],
    'e2': ['75～79歳', '80～84歳'],
    'e3': ['85～89歳', '90～94歳', '95～99歳', '100～104歳', '100～104歳以上', '105歳以上', '100歳以上'],
}
LABEL2G = {lab: g for g, labs in GROUPS.items() for lab in labs}

def read_sheet(ws):
    rows = list(ws.iter_rows(min_row=1, max_row=170, values_only=True))
    years = [int(str(v).rstrip('年')) for v in rows[6][1:] if v]
    # 「■年齢５歳階級別人口（総数）」ブロックを探す
    start = next(i for i, r in enumerate(rows) if r[0] == '■年齢５歳階級別人口（総数）')
    out = {y: {'c': 0, 'w': 0, 'e1': 0, 'e2': 0, 'e3': 0, 't': 0} for y in years}
    seen = set()
    for r in rows[start + 1:start + 30]:
        lab = r[0]
        if lab == '合計':
            for y, v in zip(years, r[1:]): out[y]['t'] = int(v)
        elif lab in LABEL2G:
            seen.add(lab)
            g = LABEL2G[lab]
            for y, v in zip(years, r[1:]): out[y][g] += int(v or 0)
        elif isinstance(lab, str) and lab.startswith('■'):
            break
    for y in years:
        s = sum(out[y][k] for k in ('c', 'w', 'e1', 'e2', 'e3'))
        assert s == out[y]['t'], (ws.title, y, s, out[y]['t'])
    return years, out

wb = openpyxl.load_workbook(SRC, read_only=True)
years, city = read_sheet(wb['横浜市'])
wards = {}
for sn in wb.sheetnames[1:]:
    ys, d = read_sheet(wb[sn]); assert ys == years
    wards[sn.replace('区', '')] = d
# 区の合計 = 市 のチェック
for y in years:
    for k in ('c', 'w', 'e1', 'e2', 'e3', 't'):
        assert sum(wards[w][y][k] for w in wards) == city[y][k], (y, k)
json.dump({'years': years, 'city': city, 'wards': wards,
           'source': '横浜市将来人口推計（令和5年推計・中位）行政区別 0048_20240410.xlsx 年齢5歳階級別（総数）'},
          open(HERE / 'projection.json', 'w'), ensure_ascii=False)
print('years', years[0], '-', years[-1], '| wards', len(wards))
for y in (2020, 2025, 2030, 2035, 2040):
    print(y, city[y])
