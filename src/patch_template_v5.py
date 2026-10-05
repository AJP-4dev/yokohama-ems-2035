import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)

# ---------- A. year quick buttons ----------
rep('<div class="yr"><input type="range" id="yearRange" min="2025" max="2040" step="1" value="2025" aria-label="年"><div class="yrv num" id="yearV">2025<small>基準＝2024年実績</small></div></div>',
    '<div class="yr"><input type="range" id="yearRange" min="2025" max="2040" step="1" value="2025" aria-label="年"><div class="yrv num" id="yearV">2025<small>基準＝2024年実績</small></div><div class="yq" id="yearQuick"><button data-y="2025" aria-pressed="true">2025</button><button data-y="2030" aria-pressed="false">2030</button><button data-y="2035" aria-pressed="false">2035</button><button data-y="2040" aria-pressed="false">2040</button></div></div>')
rep(".yr{display:flex;align-items:center;gap:10px;flex:1;min-width:0}",
    ".yr{display:flex;align-items:center;gap:6px 10px;flex:1;min-width:0;flex-wrap:wrap;padding:4px 0}\n.yq{display:flex;gap:4px;flex-basis:100%}\n.yq button{flex:1;border:1px solid var(--line);background:var(--surface);border-radius:8px;padding:5px 0;font-size:12px;cursor:pointer;font-family:Manrope,sans-serif;font-weight:700;color:var(--ink2)}\n.yq button[aria-pressed=\"true\"]{background:var(--navy);color:#fff;border-color:var(--navy)}\n:root[data-time=\"night\"] .yq button[aria-pressed=\"true\"]{background:#dfe7ff;color:#0e1730}")
rep(".yrv{font-size:14px;font-weight:800;width:150px;text-align:left;white-space:nowrap}",".yrv{font-size:14px;font-weight:800;width:auto;min-width:96px;text-align:left;white-space:nowrap}")
rep("function setYear(v){state.year=String(v);yr.value=v;yv.innerHTML=v==2025?'2025<small>基準＝2024年実績</small>':v+'<small>推計</small>';applyMetric()}",
    "function setYear(v){state.year=String(v);yr.value=v;yv.innerHTML=v==2025?'2025<small>基準＝2024年実績</small>':v+'<small>推計</small>';document.querySelectorAll('#yearQuick button').forEach(b=>b.setAttribute('aria-pressed',+b.dataset.y===+v));applyMetric()}\ndocument.querySelectorAll('#yearQuick button').forEach(b=>b.onclick=()=>setYear(+b.dataset.y));")
rep("r.querySelectorAll('button,input').forEach(b=>b.disabled=!af[k])","r.querySelectorAll('button,input').forEach(b=>b.disabled=!af[k])")

# ---------- deep links from text to map ----------
rep("function go(id){","function applyState(q){const h=new URLSearchParams(q);if(h.get('y'))setYear(Math.max(2025,Math.min(2040,+h.get('y'))));if(['A','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v'))){state.view=h.get('v');pressSeg('viewSeg','v',state.view)}if(['all','day','night'].includes(h.get('t'))){state.time=h.get('t');pressSeg('timeSeg','t',state.time);document.documentElement.dataset.time=state.time==='all'?'':state.time;applyTheme()}if(h.has('w')){const i=W.findIndex(w=>w.name===h.get('w'));state.sel=i>=0?i:(W[+h.get('w')]?+h.get('w'):null)}}\nfunction bindMapLinks(root){(root||document).querySelectorAll('a.mapgo').forEach(a=>a.onclick=e=>{e.preventDefault();applyState(a.dataset.state);go('map');if(state.sel!==null){fillSheet(W[state.sel]);sheet.classList.add('open');buildExample(W[state.sel])}else sheet.classList.remove('open');applyMetric()})}\nfunction go(id){")
rep("a{color:var(--sky)}","a{color:var(--sky)}\na.mapgo{display:inline-block;margin:2px 0;padding:2px 10px;border:1px solid var(--sky);border-radius:999px;font-size:12px;text-decoration:none;font-weight:700;white-space:nowrap}\na.mapgo:before{content:'▶ ';font-size:9px}")

# ---------- B. city page ----------
rep("const X=x=>44+(x-1985)/(2035-1985)*540,Y=v=>h-36-(v/340000)*(h-60);","const X=x=>44+(x-1985)/(2040-1985)*540,Y=v=>h-36-(v/360000)*(h-60);")
rep("const s=DATA.series,projA=[[2024,T24],[2030,A30],[2035,A35]],projB=[[2024,T24],[2030,A30*Math.pow(1.015,6)],[2035,B35]];",
    "const B40=A40*Math.pow(1.015,16),s=DATA.series,projA=[[2024,T24],[2030,A30],[2035,A35],[2040,A40]],projB=[[2024,T24],[2030,A30*Math.pow(1.015,6)],[2035,B35],[2040,B40]];")
rep("g+=[1985,1995,2005,2015,2025,2035].map(x=>","g+=[1985,1995,2005,2015,2025,2035,2040].map(x=>")
rep("g+=`<text x=\"${X(2035)}\" y=\"${Y(A35)+18}\" fill=\"#14213d\" font-size=\"12\" font-weight=\"700\" text-anchor=\"end\">A ${fmt(A35)}</text><text x=\"${X(2035)}\" y=\"${Y(B35)-8}\" fill=\"#e63946\" font-size=\"12\" font-weight=\"700\" text-anchor=\"end\">B ${fmt(B35)}</text>`;",
    "g+=`<text x=\"${X(2035)}\" y=\"${Y(A35)+18}\" fill=\"#14213d\" font-size=\"12\" font-weight=\"700\" text-anchor=\"end\">A ${fmt(A35)}</text><text x=\"${X(2035)}\" y=\"${Y(B35)-8}\" fill=\"#e63946\" font-size=\"12\" font-weight=\"700\" text-anchor=\"end\">B ${fmt(B35)}</text><text x=\"${X(2040)}\" y=\"${Y(A40)+18}\" fill=\"#14213d\" font-size=\"11\" text-anchor=\"end\">${fmt(A40)}</text><text x=\"${X(2040)}\" y=\"${Y(B40)-8}\" fill=\"#e63946\" font-size=\"11\" text-anchor=\"end\">${fmt(B40)}</text>`;")
rep('<p class="m">実線＝実績（横浜市統計書・消防局）。点線＝本レポートの推計。A（紺）は人口の変化だけ、B（赤）は年齢別の利用率が年+1.5%で上がり続けた場合。2020–21年はコロナ禍の一時的な落ち込み。</p></div>',
    '<p class="m">実線＝実績（横浜市統計書・消防局）。点線＝本レポートの推計（2030・2035・2040）。A（紺）は人口の変化だけ、B（赤）は年齢別の利用率が年+1.5%で上がり続けた場合。2020–21年はコロナ禍の一時的な落ち込み。</p></div>')
# new cards after ranking card
rep('<div class="card"><h4>区別 推計一覧</h4>',
'''<div class="card"><h4>人口は減るのに、出場件数は増える — 区別の増減率 2025→2035</h4><svg class="chart" id="chPair" viewBox="0 0 600 470"></svg><p class="m">緑＝人口の増減率、赤＝出場件数の増減率（人口の変化だけ）。南西部は人口が1割減っても件数は横ばい、北部は人口減でも件数が1割以上増える。 <a class="mapgo" href="#" data-state="m=pop&v=diff&y=2035">人口の増減率を地図で</a> <a class="mapgo" href="#" data-state="m=disp&v=diff&y=2035">出場件数の増減率を地図で</a></p></div>
  <div class="card"><h4>救急隊あたりの負担 — 1隊あたり年間出場件数</h4><div id="unitList"></div><p class="m">灰＝2024年実績、色＝2035年（人口の変化だけ）。赤は市の目安3,000件/隊を超える区。隊数は24時間隊＋日勤救急隊（2024年末、消防年報から集計）。隊は区をまたいで出場するため目安です。</p></div>
  <div class="card"><h4>区別 推計一覧</h4>''')
rep("function buildCity(){\n  document.getElementById('cA').textContent=fmt(A35);document.getElementById('cB').textContent=fmt(B35);\n  SVG.trend('chTrend');SVG.age('chAge');SVG.rate('chRate');",
"""function unitRows(n){const rk=[...W].map(w=>({n:w.name,u:unitsOf(w),p24:w.disp24/unitsOf(w),p35:w.disp['2035']/unitsOf(w),oA:overYear(w,'A'),oB:overYear(w,'B')})).sort((a,b)=>b.p35-a.p35);
  const row=r=>`<div class="rank"><span class="nm">${r.n}区 <span class="m">${r.u}隊</span></span><span class="barw"><i style="left:0;width:${Math.min(100,r.p24/4400*100)}%;background:#9fb3c8"></i><i style="left:0;width:${Math.min(100,r.p35/4400*100)}%;background:${r.p35>=3000?'#e63946':'#3a7bd5'};opacity:.85"></i></span><span class="pct num" style="color:${r.p35>=3000?'#e63946':'inherit'}">${fmt(r.p35)}</span></div>`;
  return {rk,html:rk.slice(0,n||18).map(row).join('')}}
function pairChart(id){const rk=[...W].map(w=>({n:w.name,p:(popTot(w,'2035')/popTot(w,'2025')-1)*100,d:(w.disp['2035']/w.disp24-1)*100})).sort((a,b)=>b.d-a.d);
  const x0=300,sc=14,rh=24;let g=`<line x1="${x0}" x2="${x0}" y1="4" y2="${rk.length*rh+8}" stroke="#8e9bae"/>`;
  g+=[-10,0,10].map(v=>`<text x="${x0+v*sc}" y="${rk.length*rh+22}" font-size="10" fill="#8e9bae" text-anchor="middle">${v>0?'+':''}${v}%</text>`).join('');
  rk.forEach((r,i)=>{const y=6+i*rh;g+=`<text x="${x0-170}" y="${y+16}" font-size="12" fill="#14213d" font-weight="700">${r.n}</text>`;
    g+=`<rect x="${Math.min(x0,x0+r.p*sc)}" y="${y+2}" width="${Math.abs(r.p*sc)}" height="9" fill="#1b998b" rx="2"/><rect x="${Math.min(x0,x0+r.d*sc)}" y="${y+12}" width="${Math.abs(r.d*sc)}" height="9" fill="#e63946" rx="2"/>`;
    g+=`<text x="${x0+(r.p<0?r.p*sc-4:r.p*sc+4)}" y="${y+10}" font-size="9.5" fill="#1b998b" text-anchor="${r.p<0?'end':'start'}" font-family="Manrope" font-weight="700">${pct(r.p,0)}</text><text x="${x0+r.d*sc+4}" y="${y+20}" font-size="9.5" fill="#e63946" font-family="Manrope" font-weight="700">${pct(r.d,0)}</text>`});
  document.getElementById(id).innerHTML=g}
function buildCity(){
  document.getElementById('cA').textContent=fmt(A35);document.getElementById('cB').textContent=fmt(B35);
  SVG.trend('chTrend');SVG.age('chAge');SVG.rate('chRate');pairChart('chPair');document.getElementById('unitList').innerHTML=unitRows().html;""")
# slide unit rows reuse
rep("""  ()=>{const rk=[...W].map(w=>({n:w.name,u:unitsOf(w),p24:w.disp24/unitsOf(w),p35:w.disp['2035']/unitsOf(w),oA:overYear(w,'A'),oB:overYear(w,'B')})).sort((a,b)=>b.p35-a.p35);
    const row=r=>`<div class="rank"><span class="nm">${r.n}区 <span class="m">${r.u}隊</span></span><span class="barw"><i style="left:0;width:${Math.min(100,r.p24/4200*100)}%;background:#9fb3c8"></i><i style="left:0;width:${Math.min(100,r.p35/4200*100)}%;background:${r.p35>=3000?'#e63946':'#3a7bd5'};opacity:.85"></i></span><span class="pct num" style="color:${r.p35>=3000?'#e63946':'inherit'}">${fmt(r.p35)}</span></div>`;
    const already""","""  ()=>{const {rk,html}=unitRows(9);
    const already""")
rep("return `<div class=\"kick\">救急隊の負担</div><h2>1隊あたり年3,000件の線を越える区</h2><div class=\"cols two\"><div>${rk.slice(0,9).map(row).join('')}",
    "return `<div class=\"kick\">救急隊の負担</div><h2>1隊あたり年3,000件の線を越える区</h2><div class=\"cols two\"><div>${html}")
# slide: pop vs disp maps (insert after ward map slide)
rep("  ()=>{const {rk,html}=unitRows(9);",
"""  ()=>`<div class="kick">人口と出場件数</div><h2>人口は減るのに、出場件数は増える</h2><div class="cols two"><div>${SVG.map2d(null,w=>pct((popTot(w,'2035')/popTot(w,'2025')-1)*100,0),w=>ramp(['#1b998b','#d8dee7','#f4a259','#e63946'],((popTot(w,'2035')/popTot(w,'2025')-1)*100+12)/27),600,470)}<p class="m">人口の増減率 2025→2035（市推計）</p></div><div>${SVG.map2d(null,w=>pct((w.disp['2035']/w.disp24-1)*100,0),diffCol,600,470)}<p class="m">出場件数の増減率 2025→2035（人口の変化だけ）</p></div></div><p class="m">市全体では人口 −2.3%、出場件数 +7.8%。南西部は人口が1割減っても件数は横ばい、北部は人口減でも件数が1割以上増える。</p>`,
  ()=>{const {rk,html}=unitRows(9);""")

# ---------- C. insight page ----------
rep('<p class="lead">3つの結論。人口は減っても出場は増える、主役は85歳以上、需要の重心は北部へ。</p>',
    '<p class="lead">3つの結論。人口は減っても出場は増える、主役は85歳以上、需要の重心は北部へ。各項目の「地図で」ボタンで、その条件の地図に飛べます。</p>')
rep('<div class="callout">救急隊数を2024年の85.5隊のままとすると、1隊あたりの年間出場件数は3,000件から約3,230件（A）〜3,810件（B）に増えます。</div>',
    '<div class="callout">救急隊数を2024年の85.5隊のままとすると、1隊あたりの年間出場件数は3,000件から約3,230件（A）〜3,810件（B）に増えます。</div>\n  <p><a class="mapgo" href="#" data-state="m=pop&v=diff&y=2035">人口の増減率を地図で</a> <a class="mapgo" href="#" data-state="m=disp&v=diff&y=2035">出場件数の増減率を地図で</a></p>')
rep('<p>75–84歳は人口が15%減るため件数も減り、65–74歳は団塊ジュニア世代が入り始めて3割増（39.6万→51.4万人）。2040年にかけては65–74歳が57万人に達し、需要の増加はさらに続きます（2040年 A 約27.9万件）。</p>',
    '<p>75–84歳は人口が15%減るため件数も減り、65–74歳は団塊ジュニア世代が入り始めて3割増（39.6万→51.4万人）。2040年にかけては65–74歳が57万人に達し、需要の増加はさらに続きます（2040年 A 約27.9万件）。</p>\n  <p><a class="mapgo" href="#" data-state="m=elder&v=diff&y=2035">65歳以上人口の増減率を地図で</a> <a class="mapgo" href="#" data-state="m=aging&y=2035">高齢化率を地図で</a></p>')
rep('<div class="callout">救急隊の配置を現状のままにすると、北部で現場到着時間の延伸リスクが高まります。</div>',
    '<div class="callout">救急隊の配置を現状のままにすると、北部で現場到着時間の延伸リスクが高まります。</div>\n  <p><a class="mapgo" href="#" data-state="m=disp&v=diff&y=2035&w=都筑">都筑区を地図で</a> <a class="mapgo" href="#" data-state="m=disp&v=diff&y=2035&w=瀬谷">瀬谷区を地図で</a></p>')
rep('転院搬送は戸塚区が1,499件（出場の8.0%）、港南区が1,087件（7.0%）と多く、病院立地の影響も校正係数に含まれます。</p>',
    '転院搬送は戸塚区が1,499件（出場の8.0%）、港南区が1,087件（7.0%）と多く、病院立地の影響も校正係数に含まれます。</p>\n  <p><a class="mapgo" href="#" data-state="m=day">昼夜間人口比率を地図で</a> <a class="mapgo" href="#" data-state="m=disp&t=day&y=2035">昼の出場件数を地図で</a> <a class="mapgo" href="#" data-state="m=disp&t=night&y=2035">夜の出場件数を地図で</a></p>')
rep('<h3>6. 施策への示唆</h3>',
'''<h3>6. 救急隊あたりの負担 — すでに9区が目安を超えている</h3>
  <p>消防年報の救急隊別活動状況から区別の隊数を数えると、2024年末で87隊（24時間隊79＋日勤救急隊6＋年途中設置2）。市全体では1隊あたり年2,948件ですが、区別に見ると戸塚（4,130件/隊）、磯子（4,069）、青葉（3,571）、保土ケ谷、神奈川、旭、中、南、港南の9区は2024年時点で目安の3,000件を超えています。人口の変化だけでも港北は2028年、都筑は2033年、鶴見は2034年に超え、利用率も上昇する場合は2040年までに金沢・栄・泉・緑・西も加わります。</p>
  <div class="callout b">隊は区をまたいで出場するため区別の値は目安ですが、「どの区から増やすか」の順番を決める材料になります。</div>
  <p><a class="mapgo" href="#" data-state="m=disp&y=2035&w=戸塚">戸塚区を地図で</a> <a class="mapgo" href="#" data-state="m=disp&y=2028&w=港北">港北区（2028年）を地図で</a></p>
  <h3>7. 2040年に向けて</h3>
  <p>市人口は2040年に361万人（2025年比 −4.2%）まで減りますが、出場件数は人口の変化だけで27.9万件（+8.9%）、利用率上昇込みでは35.4万件に達します。65–74歳が57万人に達し、85歳以上は26.5万人で高止まりします。2035年以降は増加のペースが鈍る一方、高齢化率は32%に上がり、1件あたりの重症度と拘束時間の増加が主題になります。</p>
  <p><a class="mapgo" href="#" data-state="m=disp&y=2040">2040年の出場件数を地図で</a> <a class="mapgo" href="#" data-state="m=aging&y=2040">2040年の高齢化率を地図で</a></p>
  <h3>8. 施策への示唆</h3>''')

# ---------- D. method page: indicator definitions ----------
rep('<h3>昼と夜の分け方</h3>',
'''<h3>地図の指標の定義</h3>
  <ul class="m">
    <li><b>出場件数</b>：区内で発生した救急出場の年間件数。2025年＝2024年実績、2026年以降は推計。「昼/夜」は市全体の時間帯別比率で分けた概算。</li>
    <li><b>人口</b>：区の総人口（2025年は1月1日の実績、以降は市の推計・中位）。</li>
    <li><b>高齢者人口</b>：65歳以上の人数（65–74＋75–84＋85歳以上）。</li>
    <li><b>高齢化率</b>：65歳以上の人数 ÷ 総人口。</li>
    <li><b>昼夜間人口比率</b>：昼間人口 ÷ 夜間人口 × 100（2020年国勢調査、全年共通）。</li>
    <li><b>実数／増減率</b>：増減率は 2025年（基準）に対する変化。出場件数・人口・高齢者人口で使えます。</li>
    <li><b>前提A／B</b>：出場件数にだけ効きます。Aは搬送率を2024年で固定、Bは年+1.5%で上昇。</li>
  </ul>
  <h3>昼と夜の分け方</h3>''')

# ---------- bind links after build ----------
rep("applyTheme();updCam();applyMetric();buildCity();","applyTheme();updCam();applyMetric();buildCity();bindMapLinks();")
P.write_text(s,encoding='utf-8'); print('patched',len(s))
