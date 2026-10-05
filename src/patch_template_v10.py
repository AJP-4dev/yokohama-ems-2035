import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

# ---- scenario T core ----
rep("const SCR={A:0,M:0.0075,B:0.015}, SCN={A:'人口のみ',M:'中間シナリオ',B:'上限シナリオ'};\nconst scMulOf=(sc,y)=>Math.pow(1+SCR[sc||state.sc],(+y-2024));",
"""const SCR={A:0,M:0.0075,B:0.015,T:null}, SCN={A:'人口のみ',M:'中間シナリオ',B:'上限シナリオ',T:'トレンドシナリオ'};
const TG=DATA.trend?DATA.trend.growthGroup:{c:0,w:0,e1:0,e2:0,e3:0};
const scMulOf=(sc,y)=>{sc=sc||state.sc;if(sc==='T'){const w0=W[0];return 1}return Math.pow(1+SCR[sc],(+y-2024))};
const tMulG=(g,y)=>Math.pow(1+TG[g],(+y-2024));
const annualT=(w,y)=>y==='2025'?w.disp24:AGES.reduce((s,a)=>s+w.byAge[y][a]*tMulG(a,y),0);""")
rep("const annualOf=(w,y,sc)=>{const m=scMulOf(sc,y);return y==='2025'?w.disp24:w.disp[y]*m};",
    "const annualOf=(w,y,sc)=>{sc=sc||state.sc;if(sc==='T')return annualT(w,y);const m=scMulOf(sc,y);return y==='2025'?w.disp24:w.disp[y]*m};")
rep("const bandOf=(w,y,t,sc)=>{const a=annualOf(w,y,sc);if(t==='all')return a;const m=scMulOf(sc,y);",
    "const bandOf=(w,y,t,sc)=>{const a=annualOf(w,y,sc);if(t==='all')return a;const m=(sc||state.sc)==='T'?(y==='2025'?1:annualT(w,y)/w.disp[y]):scMulOf(sc,y);")
rep("const byAge=(w,y)=>{const m=(y==='2025')?1:scMul(y);const k=dispOf(w,y)/annualOf(w,y);const o={};AGES.forEach(a=>o[a]=w.byAge[y][a]*m*k);return o};",
    "const byAge=(w,y)=>{const k=dispOf(w,y)/annualOf(w,y);const o={};AGES.forEach(a=>{const m=(y==='2025')?1:(state.sc==='T'?tMulG(a,y):scMul(y));o[a]=w.byAge[y][a]*m*k});return o};")
rep("const B35=W.reduce((s,w)=>s+w.disp['2035']*Math.pow(1.015,11),0), M35=",
    "const T35=W.reduce((s,w)=>s+annualT(w,'2035'),0), T30=W.reduce((s,w)=>s+annualT(w,'2030'),0), T40=W.reduce((s,w)=>s+annualT(w,'2040'),0), B35=W.reduce((s,w)=>s+w.disp['2035']*Math.pow(1.015,11),0), M35=")
rep("if(['A','M','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','percap','density','nontr','arrive','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v')))",
    "if(['A','M','B','T'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','percap','density','nontr','arrive','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v')))")
rep("if(['A','M','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','percap','density','nontr','arrive','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(h.get('m')==='diff')",
    "if(['A','M','B','T'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','percap','density','nontr','arrive','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(h.get('m')==='diff')")
rep("const diffHi=()=>state.mode==='pop'?15:state.mode==='elder'?30:state.mode==='percap'?(state.sc==='B'?50:state.sc==='M'?35:25):(state.year!=='2025'&&state.sc==='B'?40:state.year!=='2025'&&state.sc==='M'?25:15);",
    "const diffHi=()=>state.mode==='pop'?15:state.mode==='elder'?30:state.mode==='percap'?((state.sc==='B'||state.sc==='T')?50:state.sc==='M'?35:25):(state.year!=='2025'&&(state.sc==='B'||state.sc==='T')?40:state.year!=='2025'&&state.sc==='M'?25:15);")
# UI button
rep('<button aria-pressed="false" data-s="B">上限</button></div><span class="tag">影響なし</span></div>',
    '<button aria-pressed="false" data-s="B">上限</button><button aria-pressed="false" data-s="T">トレンド</button></div><span class="tag">影響なし</span></div>')
rep("<b>上限</b>：率が年+1.5%ずつ上がる（2035年に+18%）。2013〜2024年の傾向がそのまま続く仮定で、上振れ側。',",
    "<b>上限</b>：率が年+1.5%ずつ上がる（2035年に+18%）。2013〜2024年の傾向がそのまま続く仮定で、上振れ側。<br><b>トレンド</b>：2013〜2024年（2020–21年を除く）の実測から年代別に求めた伸び率をそのまま延長。0–14歳 年+6.2%、15–64歳+1.6%、65–74歳+1.6%、75–84歳+0.3%、85歳以上+1.4%。年齢構成を固定した全体の伸びは年+1.45%で、上限とほぼ同じ水準。',")
# mini chart: T line
rep("const A=YEARS.map(y=>valueAt(ws,y,'A')),B=showB?YEARS.map(y=>valueAt(ws,y,'B')):null,M=showB?YEARS.map(y=>valueAt(ws,y,'M')):null;\n  const all=B?A.concat(B):A;",
    "const A=YEARS.map(y=>valueAt(ws,y,'A')),B=showB?YEARS.map(y=>valueAt(ws,y,'B')):null,M=showB?YEARS.map(y=>valueAt(ws,y,'M')):null,Tt=showB?YEARS.map(y=>valueAt(ws,y,'T')):null;\n  const all=B?A.concat(B).concat(Tt):A;")
rep("const ci=YEARS.indexOf(state.year),cur=(state.sc==='B'&&B)?B:(state.sc==='M'&&M)?M:A;","const ci=YEARS.indexOf(state.year),cur=(state.sc==='B'&&B)?B:(state.sc==='M'&&M)?M:(state.sc==='T'&&Tt)?Tt:A;")
rep("  if(M)g+=`<polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"2\" stroke-dasharray=\"4 3\" points=\"${M.map((v,i)=>X(i)+','+Y(v)).join(' ')}\"/>`;",
    "  if(Tt)g+=`<polyline fill=\"none\" stroke=\"#8e3b8f\" stroke-width=\"2\" stroke-dasharray=\"2 3\" points=\"${Tt.map((v,i)=>X(i)+','+Y(v)).join(' ')}\"/>`;\n  if(M)g+=`<polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"2\" stroke-dasharray=\"4 3\" points=\"${M.map((v,i)=>X(i)+','+Y(v)).join(' ')}\"/>`;")
rep("fill=\"${state.sc==='B'&&B?'#e63946':state.sc==='M'&&M?'#f4a259':'var(--navy)'}\"/>`;","fill=\"${state.sc==='B'&&B?'#e63946':state.sc==='M'&&M?'#f4a259':state.sc==='T'&&Tt?'#8e3b8f':'var(--navy)'}\"/>`;")
rep("${showB?'（紺＝人口のみ／橙＝中間／赤＝上限）':''}`;","${showB?'（紺＝人口のみ／橙＝中間／赤＝上限／紫＝トレンド）':''}`;")
# city page: numbers, trend chart, table
rep('<div><div class="n r num" id="cB">—</div><div class="l">上限（年+1.5%＝最近の傾向が続く）</div></div></div>',
    '<div><div class="n r num" id="cB">—</div><div class="l">上限（年+1.5%＝最近の傾向が続く）</div></div><div><div class="n num" id="cT" style="color:#8e3b8f">—</div><div class="l">トレンド（年代別の実測トレンドを延長）</div></div></div>')
rep("document.getElementById('cM').textContent=fmt(M35);","document.getElementById('cM').textContent=fmt(M35);document.getElementById('cT').textContent=fmt(T35);")
rep("projM=[[2024,T24],[2030,M30],[2035,M35],[2040,M40]];","projM=[[2024,T24],[2030,M30],[2035,M35],[2040,M40]],projT=[[2024,T24],[2030,T30],[2035,T35],[2040,T40]];")
rep("    g+=`<polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"2.5\" stroke-dasharray=\"5 5\" points=\"${projM.map(p=>X(p[0])+','+Y(p[1])).join(' ')}\"/>`;",
    "    g+=`<polyline fill=\"none\" stroke=\"#8e3b8f\" stroke-width=\"2\" stroke-dasharray=\"2 4\" points=\"${projT.map(p=>X(p[0])+','+Y(p[1])).join(' ')}\"/>`;\n    g+=`<polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"2.5\" stroke-dasharray=\"5 5\" points=\"${projM.map(p=>X(p[0])+','+Y(p[1])).join(' ')}\"/>`;")
rep("紺＝人口のみ（搬送率を2024年で固定）、橙＝中間（搬送率が年+0.75%で上昇）、赤＝上限（年+1.5%、2013〜2024年の傾向がそのまま続く場合）。2020–21年はコロナ禍の一時的な落ち込み。</p>",
    "紺＝人口のみ（搬送率を2024年で固定）、橙＝中間（搬送率が年+0.75%で上昇）、赤＝上限（年+1.5%一律）、紫点線＝トレンド（年代別の実測トレンドを延長）。2020–21年はコロナ禍の一時的な落ち込み。</p>")
rep("<td>${fmt(w.disp['2035']*Math.pow(1.0075,11))}</td><td>${fmt(w.disp['2035']*Math.pow(1.015,11))}</td><td>${unitsOf(w)}</td>",
    "<td>${fmt(w.disp['2035']*Math.pow(1.0075,11))}</td><td>${fmt(w.disp['2035']*Math.pow(1.015,11))}</td><td>${fmt(annualT(w,'2035'))}</td><td>${unitsOf(w)}</td>")
rep("<th>2035 中間</th><th>2035 上限</th><th>隊数</th>","<th>2035 中間</th><th>2035 上限</th><th>2035 トレンド</th><th>隊数</th>")
# ---- method page: trend section ----
rep('<h3>使用データ</h3>',
'''<h3>年代別搬送率の推移（2013〜2024年）とトレンドシナリオ</h3>
  <p>消防年報の年齢5歳階級別搬送人員（各年）を、総務省の住民基本台帳人口（翌年1月1日・同じ階級）で割り、年代別搬送率の推移を出しました。</p>
  <div class="card"><h4>年代別の搬送率の推移（人口100人あたり年間搬送人員）</h4><svg class="chart" id="chTrendRate" viewBox="0 0 600 300"></svg><div class="lg"><span><b class="c-c"></b>0–14</span><span><b class="c-w"></b>15–64</span><span><b class="c-e1"></b>65–74</span><span><b class="c-e2"></b>75–84</span><span><b class="c-e3"></b>85+</span><span><b style="background:#14213d"></b>年齢構成固定の全体（2025年人口で加重）</span></div><p class="m">対数目盛。2020–21年はコロナ禍で全年齢が落ち込んだため、トレンドの当てはめからは除外。</p><div class="ins">年齢構成を固定した全体の搬送率は2013年4.8人→2024年5.5人で年+1.45%。これまで「上限」に置いていた年+1.5%は、実測とほぼ一致する値だった。ただし年代で伸びが大きく違う。0–14歳は2.6→4.4人（年+6.2%）と突出し、15–64歳と65–74歳は年+1.6%、85歳以上は+1.4%、75–84歳はほぼ横ばい（+0.3%）。つまり「高齢者の利用が増えている」のではなく、子どもと現役世代の利用が増えている。2022年以降は65歳以上の伸びが加速（65–74歳 年+4.9%）しており、コロナ後の受診行動の変化が疑われる。</div></div>
  <div class="card"><h4>年代別の年間伸び率（当てはめ結果）</h4><div class="tbl"><table id="tblTrend"></table></div><p class="m">log-linear回帰。「2013–19」はコロナ前のみ、「2022–24」は直近3年の年率換算。</p></div>
  <p><b>トレンドシナリオ</b>：年代別の伸び率（2013–19＋2022–24の当てはめ）を2024年の搬送率に掛けて延長します。一律+1.5%の「上限」と全体の水準は近いですが、中身は0–14歳と現役世代の寄与が大きく、85歳以上の寄与は上限より小さくなります。0–14歳の年+6.2%を2040年まで延ばすと搬送率は2.6倍になるため、長期の値は上振れしやすい点に注意してください。</p>
  <h3>使用データ</h3>''')
rep('<li>横浜市統計書「救急出場件数と搬送人員（昭和60年〜令和6年）」オープンデータ CSV。',
    '<li>横浜市消防局「消防年報」平成25年〜令和5年版 災害統計 — 各年の年齢5歳階級別搬送人員（トレンド算出用）。<a href="https://www.city.yokohama.lg.jp/city-info/yokohamashi/org/shobo/sonota/nenpoh.html">ページ</a></li>\n    <li>総務省「住民基本台帳に基づく人口、人口動態及び世帯数」平成26年〜令和8年 — 各年1月1日の横浜市 年齢階級別人口（総計）。平成26年版は80歳以上が一括のため、翌年の構成比で按分。<a href="https://www.soumu.go.jp/main_sosiki/jichi_gyousei/daityo/jinkou_jinkoudoutai-setaisuu.html">ページ</a></li>\n    <li>横浜市統計書「救急出場件数と搬送人員（昭和60年〜令和6年）」オープンデータ CSV。')
rep('<li><b>前提（人口のみ／中間／上限）</b>：出場件数にだけ効きます。搬送率を2024年で固定／年+0.75%で上昇／年+1.5%で上昇。</li>',
    '<li><b>前提（人口のみ／中間／上限／トレンド）</b>：出場件数にだけ効きます。搬送率を2024年で固定／年+0.75%で上昇／年+1.5%で上昇／年代別の実測トレンドで上昇。</li>')
# JS: trend charts builder
rep("/* ---------- 2025 cross-section analysis ---------- */",
"""/* ---------- transport-rate trend charts ---------- */
function buildTrendCharts(){const T=DATA.trend;if(!T)return;const ys=T.years,X=i=>50+i/(ys.length-1)*520,lo=Math.log(2),hi=Math.log(30),Y=v=>270-(Math.log(v)-lo)/(hi-lo)*240;
  let g=`<g stroke="#e3e8ef">${[2,3,5,10,20,30].map(v=>`<line x1="50" x2="570" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`+[2,3,5,10,20,30].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v}</text>`).join('')+ys.map((y,i)=>i%2===0?`<text x="${X(i)}" y="288" font-size="10.5" fill="#8e9bae" text-anchor="middle">${y}</text>`:'').join('');
  g+=`<rect x="${X(ys.indexOf(2020))-10}" y="30" width="${X(ys.indexOf(2021))-X(ys.indexOf(2020))+20}" height="240" fill="#f4a259" opacity=".12"/>`;
  AGES.forEach(a=>{g+=`<polyline fill="none" stroke="${ACOL[a]}" stroke-width="2.2" points="${ys.map((y,i)=>X(i)+','+Y(T.rateGroup[y][a]*100)).join(' ')}"/>`;const v=T.rateGroup[ys[ys.length-1]][a]*100;g+=`<text x="574" y="${Y(v)+4}" font-size="10.5" fill="${ACOL[a]}" font-family="Manrope" font-weight="700">${v.toFixed(1)}</text>`});
  g+=`<polyline fill="none" stroke="#14213d" stroke-width="2.5" stroke-dasharray="5 4" points="${ys.map((y,i)=>X(i)+','+Y(T.stdRate[y]*100)).join(' ')}"/><text x="574" y="${Y(T.stdRate[ys[ys.length-1]]*100)+4}" font-size="10.5" fill="#14213d" font-family="Manrope" font-weight="700">${(T.stdRate[ys[ys.length-1]]*100).toFixed(1)}</text>`;
  document.getElementById('chTrendRate').innerHTML=g;
  const p=v=>(v>0?'+':'')+(v*100).toFixed(2)+'%';
  document.getElementById('tblTrend').innerHTML=`<tr><th>年齢</th><th>2013</th><th>2019</th><th>2024</th><th>伸び率/年（当てはめ）</th><th>2013–19</th><th>2022–24</th></tr>`+AGES.map(a=>`<tr><td>${LAB[a]}</td><td>${(T.rateGroup[2013][a]*100).toFixed(2)}</td><td>${(T.rateGroup[2019][a]*100).toFixed(2)}</td><td>${(T.rateGroup[2024][a]*100).toFixed(2)}</td><td style="font-weight:700">${p(T.growthGroup[a])}</td><td>${p(T.growthPre[a])}</td><td>${p(T.growthPost[a])}</td></tr>`).join('')+`<tr><td><b>年齢構成固定の全体</b></td><td>${(T.stdRate[2013]*100).toFixed(2)}</td><td>${(T.stdRate[2019]*100).toFixed(2)}</td><td>${(T.stdRate[2024]*100).toFixed(2)}</td><td style="font-weight:700">${p(T.growthStd)}</td><td>—</td><td>—</td></tr><tr><td>1人あたり（年齢調整なし）</td><td>${(T.allRate[2013]*100).toFixed(2)}</td><td>${(T.allRate[2019]*100).toFixed(2)}</td><td>${(T.allRate[2024]*100).toFixed(2)}</td><td style="font-weight:700">${p(T.growthAll)}</td><td>—</td><td>—</td></tr>`;
}
buildTrendCharts();

/* ---------- 2025 cross-section analysis ---------- */""")
# ---- insight: section before 施策 ----
rep('<h3>11. 施策への示唆</h3>',
'''<h3>11. 搬送率はどう動いてきたか — 増えているのは高齢者の利用ではない</h3>
  <p>年代別の搬送率を2013年から追うと、年齢構成を固定した全体の伸びは年+1.45%で、上限シナリオの+1.5%とほぼ同じでした。ところが年代別に分けると、伸びているのは0–14歳（年+6.2%、2.6人→4.4人）と15–64歳（+1.6%）で、75–84歳はほぼ横ばい、85歳以上も+1.4%にとどまります。</p>
  <div class="callout b">「高齢者が救急車を使いすぎている」という説明は、横浜市のデータでは成り立ちません。高齢者の件数が増えているのは人数が増えているからで、1人あたりの利用はむしろ現役世代と子どもで増えています。</div>
  <p>子どもの伸びは、少子化で分母が減る一方、RSウイルスやインフルエンザの流行、小児の夜間救急の集約などが重なった可能性があります。2022年以降は65歳以上の伸びも加速（65–74歳で年+4.9%）しており、コロナ後にかかりつけ医から救急へ受診行動が移った可能性があります。トレンドシナリオはこの年代別の伸びをそのまま延長したもので、2035年の市全体は<span class="num" id="insT35"></span>件、上限とほぼ同じ水準ですが、内訳は子ども・現役世代の寄与が大きくなります。</p>
  <p><a class="mapgo" href="#" data-state="m=disp&s=T&y=2035">トレンドシナリオを地図で</a></p>
  <h3>12. 施策への示唆</h3>''')
rep("buildTrendCharts();","buildTrendCharts();document.getElementById('insT35').textContent=fmt(T35);")
# slides: add one after trend slide (index 3)
rep("  ()=>`<div class=\"kick\">誰が使うのか</div>",
"""  ()=>`<div class="kick">搬送率の推移 2013→2024</div><h2>増えているのは高齢者の利用ではない</h2><div class="cols two"><div><svg class="chart" id="slTrendRate" viewBox="0 0 600 300"></svg><p class="m">年代別の搬送率（人口100人あたり、対数目盛）。点線＝年齢構成固定の全体。</p></div><div>${pt('+1.45%','年齢構成を固定した搬送率の年間伸び（2013–19・2022–24）。上限シナリオの+1.5%と一致')}${pt('+6.2%','0–14歳の年間伸び。2.6人→4.4人。85歳以上は+1.4%、75–84歳は+0.3%',1)}<p class="m" style="margin-top:12px">高齢者の件数増は「人数」の増加。1人あたりの利用は子どもと現役世代で増えている。</p></div></div>`,
  ()=>`<div class="kick">誰が使うのか</div>""")
rep("scatterChart('slScatter');document.getElementById('slAnD').innerHTML=document.getElementById('anD').innerHTML;",
    "scatterChart('slScatter');document.getElementById('slAnD').innerHTML=document.getElementById('anD').innerHTML;document.getElementById('slTrendRate').innerHTML=document.getElementById('chTrendRate').innerHTML;")
P.write_text(s,encoding='utf-8'); print('patched',len(s))
