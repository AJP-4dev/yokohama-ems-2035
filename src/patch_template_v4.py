import pathlib,re
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)

# ---------- CSS ----------
rep("""  --nav:60px; --head:52px; --r:14px;
}""","""  --nav:60px; --head:52px; --r:14px;
  --floor:#e6ebf2; --grid1:#d3dae5; --grid2:#dce3ed; --labt:#14213d; --labs:#5b6b82; --halo:rgba(255,255,255,.95);
}
:root[data-time="day"]{ --paper:#fdf9ee; --surface:#fffdf7; --surface2:#f3ecd9; --line:#e6ddc6; --floor:#f1e9d4; --grid1:#e3d9c0; --grid2:#ebe3cf; }
:root[data-time="night"]{ --paper:#0e1730; --surface:#172244; --surface2:#213058; --ink:#eef2fb; --ink2:#aab6cc; --ink3:#7f8ca6; --line:#2b3b60; --navy:#dfe7ff; --floor:#121d3a; --grid1:#1c2b4f; --grid2:#172544; --labt:#ffffff; --labs:#c4cfe6; --halo:rgba(14,23,48,.95); }
:root[data-time="night"] .seg button[aria-pressed="true"]{background:#dfe7ff;color:#0e1730}
:root[data-time="night"] #nav button[aria-selected="true"],:root[data-time="night"] .hdtabs button[aria-selected="true"]{color:#fff}
:root[data-time="night"] .hdtabs button[aria-selected="true"]{background:#2b3b60}
:root[data-time="night"] .next,:root[data-time="night"] .step .no{background:#dfe7ff;color:#0e1730}
:root[data-time="night"] .next svg{stroke:#0e1730}
:root[data-time="night"] #total .v{color:#fff}
:root[data-time="night"] .callout{background:#2a1f33} :root[data-time="night"] .callout.b{background:#1a2a4a} :root[data-time="night"] .callout.t{background:#163a3a}
:root[data-time="night"] .ex{background:#1b2850}
:root[data-time="night"] #head{background:rgba(14,23,48,.9)} :root[data-time="night"] #nav{background:rgba(23,34,68,.95)}
:root[data-time="night"] th{background:var(--surface)}
body,#head,#nav,#stage,.seg,.card,#sheet,#legend{transition:background-color .5s,color .5s,border-color .5s}""")
rep(".seglbl{font-size:11px;color:var(--ink2);margin:0 4px 0 2px}\n.grp{display:inline-flex;align-items:center}",
""".panel{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:6px 10px;box-shadow:0 2px 12px rgba(20,33,61,.07);pointer-events:auto;display:flex;flex-direction:column;gap:2px;max-width:560px}
.prow{display:flex;align-items:center;gap:8px;min-height:40px;transition:opacity .25s}
.prow .lbl{width:44px;font-size:11.5px;color:var(--ink2);flex:none}
.prow.off{opacity:.38}
.prow .tag{font-size:10px;color:var(--ink2);border:1px solid var(--line);border-radius:999px;padding:1px 7px;margin-left:auto;white-space:nowrap;display:none}
.prow.off .tag{display:inline-block}
.prow .seg{box-shadow:none;border:0;background:var(--surface2);padding:2px}
.prow .seg button{padding:6px 10px;font-size:12.5px}
.yr{display:flex;align-items:center;gap:10px;flex:1;min-width:0}
.yr input[type=range]{flex:1;min-width:0;accent-color:var(--red);height:28px;margin:0}
.yrv{font-size:14px;font-weight:800;width:150px;text-align:left;white-space:nowrap}
.yrv small{display:block;font-size:10.5px;color:var(--ink2);font-weight:400}
#status{pointer-events:none;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:7px 10px;max-width:560px}
#status .s1{font-size:13px;font-weight:700;line-height:1.45}
#status .s2{font-size:11.5px;color:var(--ink2);line-height:1.45;margin-top:2px}""")
rep("#stage{position:absolute;inset:0;touch-action:none;cursor:grab}","#stage{position:absolute;inset:0;touch-action:none;cursor:grab;background:var(--paper)}")
rep("#total{pointer-events:none;line-height:1.1;margin:4px 0 0 2px}","#total{pointer-events:none;line-height:1.1;margin:2px 0 0 2px}")
rep(".kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}",".kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0}\n.kpi .s{font-size:10px;color:var(--ink2);margin-top:2px}")
rep("@media (max-width:360px){ .seg button{padding:7px 8px;font-size:12px} }","@media (max-width:360px){ .seg button{padding:7px 8px;font-size:12px} .yrv{width:120px} }")

# ---------- HTML controls ----------
old=s[s.index('  <div id="ctl">'):s.index('  <div id="tools">')]
new='''  <div id="ctl">
    <div class="panel">
      <div class="prow" id="rowYear"><span class="lbl">年</span><div class="yr"><input type="range" id="yearRange" min="2025" max="2040" step="1" value="2025" aria-label="年"><div class="yrv num" id="yearV">2025<small>基準＝2024年実績</small></div></div><span class="tag">影響なし</span></div>
      <div class="prow" id="rowSc"><span class="lbl">前提</span><div class="seg alt" id="scSeg"><button aria-pressed="true" data-s="A">人口の変化だけ</button><button aria-pressed="false" data-s="B">利用率も上昇</button></div><span class="tag">影響なし</span></div>
      <div class="prow" id="rowTime"><span class="lbl">時間帯</span><div class="seg" id="timeSeg"><button aria-pressed="true" data-t="all">終日</button><button aria-pressed="false" data-t="day">昼 8–19時</button><button aria-pressed="false" data-t="night">夜 20–7時</button></div><span class="tag">影響なし</span></div>
      <div class="prow" id="rowMode"><span class="lbl">指標</span><div class="seg" id="modeSeg"><button aria-pressed="true" data-m="disp">出場件数</button><button aria-pressed="false" data-m="diff">増減率</button><button aria-pressed="false" data-m="aging">高齢化率</button><button aria-pressed="false" data-m="day">昼夜間比</button></div></div>
    </div>
    <div id="status"><div class="s1" id="stL1"></div><div class="s2" id="stL2"></div></div>
    <div id="total"><div class="v num" id="totV">—</div><div class="u" id="totU">市全体の救急出場件数（件/年）</div><div class="d num" id="totD"></div></div>
  </div>
'''
s=s.replace(old,new)
rep('<div class="kpi"><div class="l">1日あたり</div><div class="v num" id="k3"></div></div>',
    '<div class="kpi"><div class="l" id="k3l">1隊あたり</div><div class="v num" id="k3"></div><div class="s" id="k3s"></div></div>')
rep('<p class="note" id="shRead"></p>','<p class="note" id="shRead"></p><p class="note" id="shUnit"></p>')
rep('<div class="lg"><span><b class="c-c"></b>0–14歳</span><span><b class="c-w"></b>15–64歳</span><span><b class="c-e1"></b>65–74歳</span><span><b class="c-e2"></b>75–84歳</span><span><b class="c-e3"></b>85歳以上</span></div>\n    <p class="note" id="shRead">',
    '<div class="lg"><span><b class="c-c"></b>0–14歳</span><span><b class="c-w"></b>15–64歳</span><span><b class="c-e1"></b>65–74歳</span><span><b class="c-e2"></b>75–84歳</span><span><b class="c-e3"></b>85歳以上</span></div>\n    <p class="note" id="shRead">')

# ---------- method page additions ----------
rep('''  <h3>2つのシナリオ</h3>''','''  <h3>昼と夜の分け方</h3>
  <p>消防年報の時間帯別出場件数から、市全体の出場の <b id="dayShareTxt">65%</b> が昼（8〜19時台）、残りが夜（20〜7時台）に起きています。各区の年間件数をこの比率で分け、通勤・通学による上乗せ分（ステップ④）は昼側だけに入れます。区ごとの時間帯別実績は公表されていないため、この分け方は市全体の比率を当てた概算です。</p>
  <div class="f" style="font-family:Manrope,sans-serif;font-size:13px;background:var(--surface2);padding:8px 10px;border-radius:8px;line-height:1.6">昼 = （年間件数 − 昼間補正）× 0.649 ＋ 昼間補正　／　夜 = （年間件数 − 昼間補正）× 0.351</div>
  <h3>1隊あたりの件数</h3>
  <p>消防年報の救急隊別活動状況から、区ごとの救急隊数（24時間隊＋日勤救急隊、2024年末時点で計87隊）を数え、区の年間出場件数を隊数で割ります。市全体では1隊あたり年3,000件（2024年）で、本レポートではこれを目安の線にしています。</p>
  <h3>2つのシナリオ</h3>''')

# ---------- JS ----------
rep("const state={year:'2025',sc:'A',mode:'disp',sel:null};","const state={year:'2025',sc:'A',mode:'disp',time:'all',sel:null};\nconst S_DAY=DATA.dayShare, BAND={all:'',day:'昼（8–19時）の',night:'夜（20–7時）の'};")
rep("const dispOf=(w,y,sc)=>{const m=(sc||state.sc)==='B'?Math.pow(1.015,(+y-2024)):1;return y==='2025'?w.disp24:w.disp[y]*m};",
"""const annualOf=(w,y,sc)=>{const m=(sc||state.sc)==='B'?Math.pow(1.015,(+y-2024)):1;return y==='2025'?w.disp24:w.disp[y]*m};
const bandOf=(w,y,t,sc)=>{const a=annualOf(w,y,sc);if(t==='all')return a;const m=(sc||state.sc)==='B'?Math.pow(1.015,(+y-2024)):1;const dE=w.dayExtra*(y==='2025'?1:m);return t==='day'?(a-dE)*S_DAY+dE:(a-dE)*(1-S_DAY)};
const dispOf=(w,y,sc)=>bandOf(w,y,state.time,sc);
const unitsOf=w=>w.units+w.unitsDay;
const overYear=(w,sc,th=3000)=>{for(let y=2025;y<=2040;y++){if(annualOf(w,String(y),sc)/unitsOf(w)>=th)return y}return null};""")
rep("const byAge=(w,y)=>{const m=(y==='2025')?1:scMul(y);const o={};AGES.forEach(a=>o[a]=w.byAge[y][a]*m);return o};",
    "const byAge=(w,y)=>{const m=(y==='2025')?1:scMul(y);const k=dispOf(w,y)/annualOf(w,y);const o={};AGES.forEach(a=>o[a]=w.byAge[y][a]*m*k);return o};")
rep("const metric=w=>{const y=state.year;switch(state.mode){case 'disp':return dispOf(w,y);case 'diff':return (dispOf(w,y)/w.disp24-1)*100;case 'aging':return agingRate(w,y);case 'day':return w.dn}};",
    "const metric=w=>{const y=state.year;switch(state.mode){case 'disp':return dispOf(w,y);case 'diff':return (dispOf(w,y)/dispOf(w,'2025')-1)*100;case 'aging':return agingRate(w,y);case 'day':return w.dn}};\nconst bandK=()=>state.time==='all'?1:state.time==='day'?S_DAY:1-S_DAY;")
rep("const heightFor=w=>{const v=metric(w);let t;if(state.mode==='disp')t=v/23000;","const heightFor=w=>{const v=metric(w);let t;if(state.mode==='disp')t=v/(23000*bandK());")
rep("const colorFor=v=>{const [lo,hi]=RANGE[state.mode];let t;if(state.mode==='day')t=Math.log(v/lo)/Math.log(hi/lo);else t=(v-lo)/(hi-lo);return ramp(RAMPS[state.mode],t)};",
    "const colorFor=v=>{let [lo,hi]=RANGE[state.mode];if(state.mode==='disp'){lo*=bandK();hi*=bandK()}let t;if(state.mode==='day')t=Math.log(v/lo)/Math.log(hi/lo);else t=(v-lo)/(hi-lo);return ramp(RAMPS[state.mode],t)};")
# labels theme-aware
rep("g.font='700 30px \"Zen Kaku Gothic New\",sans-serif';g.lineWidth=7;g.strokeStyle='rgba(255,255,255,.95)';g.strokeText(text,128,34);g.fillStyle=hot?'#e63946':'#14213d';g.fillText(text,128,34);\n  g.font='800 23px Manrope,sans-serif';g.lineWidth=6;g.strokeText(sub||'',128,70);g.fillStyle='#5b6b82';g.fillText(sub||'',128,70);spr.material.map.needsUpdate=true}",
    "const cs=getComputedStyle(document.documentElement);g.font='700 30px \"Zen Kaku Gothic New\",sans-serif';g.lineWidth=7;g.strokeStyle=cs.getPropertyValue('--halo').trim();g.strokeText(text,128,34);g.fillStyle=hot?'#e63946':cs.getPropertyValue('--labt').trim();g.fillText(text,128,34);\n  g.font='800 23px Manrope,sans-serif';g.lineWidth=6;g.strokeText(sub||'',128,70);g.fillStyle=cs.getPropertyValue('--labs').trim();g.fillText(sub||'',128,70);spr.material.map.needsUpdate=true}")
rep("const floor=new THREE.Mesh(new THREE.PlaneGeometry(220,220),new THREE.MeshBasicMaterial({color:0xe6ebf2})); floor.rotation.x=-Math.PI/2; floor.position.y=-0.05; scene.add(floor);\nconst grid=new THREE.GridHelper(120,24,0xd3dae5,0xdce3ed); grid.position.y=-0.02; scene.add(grid);",
    "const floor=new THREE.Mesh(new THREE.PlaneGeometry(220,220),new THREE.MeshBasicMaterial({color:0xe6ebf2})); floor.rotation.x=-Math.PI/2; floor.position.y=-0.05; scene.add(floor);\nlet grid=new THREE.GridHelper(120,24,0xd3dae5,0xdce3ed); grid.position.y=-0.02; scene.add(grid);\nconst hemi=new THREE.HemisphereLight(0xffffff,0xc9d3df,1.0); scene.add(hemi);\nfunction applyTheme(){const cs=getComputedStyle(document.documentElement),v=n=>cs.getPropertyValue(n).trim();renderer.setClearColor(new THREE.Color(v('--paper')),1);floor.material.color.set(v('--floor'));scene.remove(grid);grid=new THREE.GridHelper(120,24,new THREE.Color(v('--grid1')),new THREE.Color(v('--grid2')));grid.position.y=-0.02;scene.add(grid);const night=state.time==='night';hemi.intensity=night?0.55:1.0;key.intensity=night?0.5:0.75;meshes.forEach(m=>m.userData.line.material.color.set(night?0xaab6cc:0x14213d))}")
rep("scene.add(new THREE.HemisphereLight(0xffffff,0xc9d3df,1.0));\n","")
# apply metric: status, enable/disable, hash
rep("const HINT={disp:'高さと色＝年間の救急出場件数（件/年）',diff:'高さと色＝2024年実績からの増減率（2024を選ぶと全区が基準で同じ高さ）',aging:'高さと色＝65歳以上の割合',day:'高さと色＝昼間人口÷夜間人口×100。2020年国勢調査の値で全年共通（将来推計なし）'};",
"""const yearLabel=()=>state.year==='2025'?'2025年（基準＝2024年実績）':state.year+'年';
const scLabel=()=>state.sc==='B'?'利用率も上昇':'人口の変化だけ';
function statusText(){const b=BAND[state.time],y=yearLabel(),base=state.year==='2025';
  switch(state.mode){
    case 'disp':return[`${y}の${b}年間救急出場件数`+(base?'':`（${scLabel()}）`),`高さと色＝この件数。${base?'2024年の実績値です。':'区ごとの人口推計 × 年齢別搬送率 × 校正係数で計算。'}${state.time==='all'?'':'昼夜の分け方は市全体の時間帯別実績（昼65%）を当てた概算。'}`];
    case 'diff':return[`${b}出場件数の 2024年実績比（${y}${base?'':'・'+scLabel()}）`,base?'基準年なので全区0%。年を動かすと増減率が出ます。':'高さと色＝増減率。人口減と高齢化の差し引きがそのまま出ます。'];
    case 'aging':return[`${y}の65歳以上の割合（市の人口推計）`,'高さと色＝高齢化率。前提や時間帯は人口に関係しないので効きません。'];
    case 'day':return['昼夜間人口比率（2020年国勢調査、全年共通）','高さと色＝昼間人口÷夜間人口×100。100より大きいと昼に人が集まる区。将来推計はありません。'];}}
function affects(){const m=state.mode,base=state.year==='2025';return{year:m!=='day',sc:(m==='disp'||m==='diff')&&!base,time:m==='disp'||m==='diff'}}""")
rep("""  document.getElementById('legH').textContent='高さも同じ指標（平行投影で比較可）';
  document.getElementById('hint').textContent=HINT[state.mode]+(state.mode==='day'||y==='2025'?'':state.sc==='B'?'　／ '+y+'年・利用率上昇込み':'　／ '+y+'年・人口の変化だけ');
  document.querySelectorAll('#yearSeg button,#scSeg button').forEach(b=>b.disabled=(state.mode==='day'));""",
"""  document.getElementById('legH').textContent='高さも同じ指標（平行投影で比較可）';
  const [l1,l2]=statusText();document.getElementById('stL1').textContent=l1;document.getElementById('stL2').textContent=l2;
  const af=affects();[['rowYear','year'],['rowSc','sc'],['rowTime','time']].forEach(([id,k])=>{const r=document.getElementById(id);r.classList.toggle('off',!af[k]);r.querySelectorAll('button,input').forEach(b=>b.disabled=!af[k])});
  document.getElementById('totU').textContent=`市全体の${BAND[state.time]}救急出場件数（件/年）`;
  try{history.replaceState(null,'',`#y=${state.year}&s=${state.sc}&m=${state.mode}&t=${state.time}`+(state.sel!==null?`&w=${state.sel}`:''))}catch(e){}""")
rep("  if(y==='2025'){d.textContent='2024年実績 ／ 1日 701件';d.className='d num'}else{const dd=(t/cityTotal('2025')-1)*100;d.textContent=`2024年比 ${pct(dd)} ／ 1日 ${fmt(t/365)}件`;d.className='d num '+(dd>=0?'up':'dn')}",
    "  if(y==='2025'){d.textContent=`2024年実績 ／ 1日 ${fmt(t/365)}件`;d.className='d num'}else{const dd=(t/cityTotal('2025')-1)*100;d.textContent=`2024年比 ${pct(dd)} ／ 1日 ${fmt(t/365)}件`;d.className='d num '+(dd>=0?'up':'dn')}")
rep("""seg('yearSeg','y',v=>{state.year=v;applyMetric()});
seg('scSeg','s',v=>{state.sc=v;applyMetric();buildCity()});
seg('modeSeg','m',v=>{state.mode=v;applyMetric()});""",
"""const yr=document.getElementById('yearRange'),yv=document.getElementById('yearV');
function setYear(v){state.year=String(v);yr.value=v;yv.innerHTML=v==2025?'2025<small>基準＝2024年実績</small>':v+'<small>推計</small>';applyMetric()}
yr.addEventListener('input',()=>setYear(+yr.value));
seg('scSeg','s',v=>{state.sc=v;applyMetric();buildCity()});
seg('modeSeg','m',v=>{state.mode=v;applyMetric()});
seg('timeSeg','t',v=>{state.time=v;document.documentElement.dataset.time=v==='all'?'':v;applyTheme();applyMetric()});
function pressSeg(id,attr,val){document.querySelectorAll('#'+id+' button').forEach(b=>b.setAttribute('aria-pressed',b.dataset[attr]===val))}""")
# sheet: units + per-unit kpi
rep("  document.getElementById('k3').textContent=fmt(cur/365)+'件';",
    "  const u=unitsOf(w),pu=annualOf(w,y)/u;document.getElementById('k3l').textContent=`1隊あたり（年・${u}隊）`;document.getElementById('k3').textContent=fmt(pu)+'件';document.getElementById('k3').className='v num '+(pu>=3000?'up':'');document.getElementById('k3s').textContent=`1日 ${fmt(cur/365)}件${state.time==='all'?'':'（'+BAND[state.time].replace('の','')+'）'}`;\n  const oA=overYear(w,'A'),oB=overYear(w,'B');document.getElementById('shUnit').innerHTML=`<b>救急隊</b> ${w.units}隊${w.unitsDay?'＋日勤'+w.unitsDay+'隊':''}（2024年末）。1隊あたり年3,000件を超えるのは ${oA?'<b>'+oA+'年</b>':'2040年まで超えない'}（人口の変化だけ）／ ${oB?'<b>'+oB+'年</b>':'2040年まで超えない'}（利用率も上昇）。`;")
# table columns
rep("const rows=W.map(w=>`<tr><td>${w.name}</td><td>${fmt(popTot(w,'2025'))}</td><td>${fmt(popTot(w,'2035'))}</td><td>${agingRate(w,'2035').toFixed(1)}%</td><td>${w.dn}</td><td>${fmt(w.disp24)}</td><td>${fmt(w.disp['2035'])}</td><td style=\"color:${w.disp['2035']>=w.disp24?'#e63946':'#1b998b'};font-weight:700\">${pct((w.disp['2035']/w.disp24-1)*100)}</td><td>${fmt(w.disp['2035']*Math.pow(1.015,11))}</td></tr>`).join('');\n  document.getElementById('tblAll').innerHTML=`<tr><th>区</th><th>人口2025</th><th>人口2035</th><th>高齢化率35</th><th>昼夜比</th><th>出場2024</th><th>出場2035 A</th><th>増減</th><th>2035 B</th></tr>${rows}`;",
    "const rows=W.map(w=>{const oA=overYear(w,'A'),oB=overYear(w,'B');return `<tr><td>${w.name}</td><td>${fmt(popTot(w,'2025'))}</td><td>${fmt(popTot(w,'2035'))}</td><td>${agingRate(w,'2035').toFixed(1)}%</td><td>${fmt(w.disp24)}</td><td>${fmt(w.disp['2035'])}</td><td style=\"color:${w.disp['2035']>=w.disp24?'#e63946':'#1b998b'};font-weight:700\">${pct((w.disp['2035']/w.disp24-1)*100)}</td><td>${fmt(w.disp['2035']*Math.pow(1.015,11))}</td><td>${unitsOf(w)}</td><td style=\"font-weight:700;color:${w.disp['2035']/unitsOf(w)>=3000?'#e63946':'inherit'}\">${fmt(w.disp['2035']/unitsOf(w))}</td><td>${oA||'—'}</td><td>${oB||'—'}</td></tr>`}).join('');\n  document.getElementById('tblAll').innerHTML=`<tr><th>区</th><th>人口2025</th><th>人口2035</th><th>高齢化率35</th><th>出場2024</th><th>出場2035 A</th><th>増減</th><th>2035 B</th><th>隊数</th><th>1隊あたり35 A</th><th>3,000超 A</th><th>3,000超 B</th></tr>${rows}`;")
rep("<div class=\"card\"><h4>区別 推計一覧</h4><div class=\"tbl\"><table id=\"tblAll\"></table></div></div>",
    "<div class=\"card\"><h4>区別 推計一覧</h4><div class=\"tbl\"><table id=\"tblAll\"></table></div><p class=\"m\">隊数＝24時間隊＋日勤救急隊（2024年末、消防年報の救急隊別活動状況から集計）。「3,000超」＝1隊あたり年間出場件数が市平均の目安3,000件を超える最初の年（—は2040年まで超えない）。</p></div>")
# method: dayShare text
rep("buildExample(W.find(w=>w.name==='都筑'));","buildExample(W.find(w=>w.name==='都筑'));document.getElementById('dayShareTxt').textContent=(S_DAY*100).toFixed(0)+'%';")
# slides: add unit-load slide after ward slide (index 6)
rep("  ()=>`<div class=\"kick\">昼間人口と病院</div>",
"""  ()=>{const rk=[...W].map(w=>({n:w.name,u:unitsOf(w),p24:w.disp24/unitsOf(w),p35:w.disp['2035']/unitsOf(w),oA:overYear(w,'A'),oB:overYear(w,'B')})).sort((a,b)=>b.p35-a.p35);
    const row=r=>`<div class="rank"><span class="nm">${r.n}区 <span class="m">${r.u}隊</span></span><span class="barw"><i style="left:0;width:${Math.min(100,r.p24/4200*100)}%;background:#9fb3c8"></i><i style="left:0;width:${Math.min(100,r.p35/4200*100)}%;background:${r.p35>=3000?'#e63946':'#3a7bd5'};opacity:.85"></i></span><span class="pct num" style="color:${r.p35>=3000?'#e63946':'inherit'}">${fmt(r.p35)}</span></div>`;
    const over=rk.filter(r=>r.oA).map(r=>`${r.n}（${r.oA}）`).join('、');
    return `<div class="kick">救急隊の負担</div><h2>1隊あたり年3,000件の線を越える区</h2><div class="cols two"><div>${rk.slice(0,9).map(row).join('')}<p class="m">1隊あたり年間出場件数。灰＝2024、色＝2035（人口の変化だけ）。赤は3,000件超。</p></div><div><p><b>2035年に3,000件/隊を超える区</b></p><p class="m">${over||'なし'}（かっこ内は最初に超える年）</p><p style="margin-top:12px"><b>利用率も上昇する場合</b></p><p class="m">${rk.filter(r=>r.oB).map(r=>r.n+'（'+r.oB+'）').join('、')}</p><div class="callout" style="margin-top:14px">隊の増設は1隊あたり年3,000件を基準に、超える年の早い区から。</div></div></div>`},
  ()=>`<div class=\"kick\">昼間人口と病院</div>""")
# hash restore + init
rep("updCam();applyMetric();buildCity();meshes.forEach(m=>{m.userData.h=0.05;m.scale.y=0.05});requestAnimationFrame(loop);",
"""(function restore(){try{const h=new URLSearchParams(location.hash.slice(1));if(h.get('y'))setYear(Math.max(2025,Math.min(2040,+h.get('y'))));if(['A','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','diff','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['all','day','night'].includes(h.get('t'))){state.time=h.get('t');pressSeg('timeSeg','t',state.time);document.documentElement.dataset.time=state.time==='all'?'':state.time}if(h.get('w')!==null&&W[+h.get('w')]){state.sel=+h.get('w')}}catch(e){}})();
applyTheme();updCam();applyMetric();buildCity();if(state.sel!==null){fillSheet(W[state.sel]);sheet.classList.add('open');buildExample(W[state.sel])}meshes.forEach(m=>{m.userData.h=0.05;m.scale.y=0.05});requestAnimationFrame(loop);""")
# intro text tweak
rep('<div><b>1</b><span><strong>地図</strong>で全体像をつかむ。柱の高さが出場件数、色は選んだ指標。区をタップすると詳細が出ます。</span></div>',
    '<div><b>1</b><span><strong>地図</strong>で全体像をつかむ。柱の高さと色＝選んだ指標。年はスライダーで動かせます。薄くなった条件は、いまの表示に影響しません。</span></div>')
P.write_text(s,encoding='utf-8'); print('patched',len(s))
