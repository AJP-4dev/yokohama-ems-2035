import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

# ---------- indicator buttons ----------
rep('<button aria-pressed="true" data-m="disp">出場件数</button><button aria-pressed="false" data-m="pop">人口</button><button aria-pressed="false" data-m="elder">高齢者人口</button><button aria-pressed="false" data-m="aging">高齢化率</button><button aria-pressed="false" data-m="day">昼夜間比</button></div></div>',
    '<button aria-pressed="true" data-m="disp">出場件数</button><button aria-pressed="false" data-m="percap">1,000人あたり</button><button aria-pressed="false" data-m="density">件/km²</button><button aria-pressed="false" data-m="nontr">不搬送率</button><button aria-pressed="false" data-m="arrive">到着時間</button><button aria-pressed="false" data-m="pop">人口</button><button aria-pressed="false" data-m="elder">高齢者人口</button><button aria-pressed="false" data-m="aging">高齢化率</button><button aria-pressed="false" data-m="day">昼夜間比</button></div></div>')

# ---------- core accessors ----------
rep("const COUNT_MODES=['disp','pop','elder'];","const COUNT_MODES=['disp','percap','density','pop','elder'];\nconst DISP_MODES=['disp','percap','density'];\nconst STATIC_MODES=['day','nontr','arrive'];\nconst AREA_CITY=W.reduce((s,w)=>s+w.area,0);")
rep("case 'elder':return isDiff()?(elderOf(w,y)/elderOf(w,'2025')-1)*100:elderOf(w,y);",
    "case 'elder':return isDiff()?(elderOf(w,y)/elderOf(w,'2025')-1)*100:elderOf(w,y);case 'percap':{const v=dispOf(w,y)/popTot(w,y)*1000,b=dispOf(w,'2025')/popTot(w,'2025')*1000;return isDiff()?(v/b-1)*100:v}case 'density':{const v=dispOf(w,y)/w.area;return isDiff()?(v/(dispOf(w,'2025')/w.area)-1)*100:v}case 'nontr':return w.nonTr*100;case 'arrive':return w.arrive;")
rep("const bandK=()=>state.time==='all'?1:state.time==='day'?S_DAY:1-S_DAY;","const bandK=()=>(state.time==='all'||!DISP_MODES.includes(state.mode))?1:state.time==='day'?S_DAY:1-S_DAY;")
rep("pop:['#e4f3ef','#8fd0c3','#2a9d8f','#14213d'],","pop:['#e4f3ef','#8fd0c3','#2a9d8f','#14213d'],percap:['#dbe7f3','#7fa6d6','#3a5f99','#14213d'],density:['#dbe7f3','#7fa6d6','#3a5f99','#14213d'],nontr:['#cfe8e3','#f4a259','#c0392b'],arrive:['#1b998b','#d8dee7','#f4a259','#e63946'],")
rep("const RANGE={disp:[7000,23000],pop:[90000,370000],elder:[30000,130000],","const RANGE={disp:[7000,23000],percap:[45,125],density:[350,1600],nontr:[12,40],arrive:[6,10],pop:[90000,370000],elder:[30000,130000],")
rep("const colorFor=v=>{let [lo,hi]=RANGE[state.mode];if(isDiff()){lo=diffLo();hi=diffHi()}else if(state.mode==='disp'){lo*=bandK();hi*=bandK()}",
    "const colorFor=v=>{let [lo,hi]=RANGE[state.mode];if(isDiff()){lo=diffLo();hi=diffHi()}else if(DISP_MODES.includes(state.mode)){lo*=bandK();hi*=bandK()}")
rep("else if(state.mode==='disp')t=v/(23000*bandK());else if(state.mode==='pop')t=v/370000;",
    "else if(state.mode==='disp')t=v/(23000*bandK());else if(state.mode==='percap')t=(v-40*bandK())/(90*bandK());else if(state.mode==='density')t=v/(1600*bandK());else if(state.mode==='nontr')t=(v-10)/30;else if(state.mode==='arrive')t=(v-5.5)/4.5;else if(state.mode==='pop')t=v/370000;")
rep("const diffHi=()=>state.mode==='pop'?15:state.mode==='elder'?30:(state.year!=='2025'&&state.sc==='B'?40:state.year!=='2025'&&state.sc==='M'?25:15);",
    "const diffHi=()=>state.mode==='pop'?15:state.mode==='elder'?30:state.mode==='percap'?(state.sc==='B'?50:state.sc==='M'?35:25):(state.year!=='2025'&&state.sc==='B'?40:state.year!=='2025'&&state.sc==='M'?25:15);")
# status text
rep("""    case 'aging':return[`${y}の65歳以上の割合（市の人口推計）`,""","""    case 'percap':return isDiff()?[`住民1,000人あたり出場件数の 2025年比の増減率（${y}）`,'高齢化で住民1人あたりの利用は全区で増える。伸びが大きい区ほど年齢構成の変化が急。']:[`${y}の住民1,000人あたり${b}出場件数`+(base?'':`（${scLabel()}）`),'高さと色＝出場件数 ÷ 区の人口 × 1,000。来街者・病院・繁華街の需要が多い区ほど高い。'];
    case 'density':return isDiff()?[`出場密度（件/km²）の 2025年比の増減率（${y}）`,'面積は変わらないので、増減率は出場件数と同じ。']:[`${y}の${b}出場密度（件/km²）`+(base?'':`（${scLabel()}）`),'高さと色＝出場件数 ÷ 区の面積。密な区ほど1隊で多くをさばけ、疎な区ほど現場が遠い。面積は港湾・水面を含む。'];
    case 'nontr':return['不搬送率（出場したが搬送しなかった割合、2024年）','高さと色＝1 − 搬送人員 ÷ 出場件数（区内の救急隊の実績）。市平均19%。理由の8割は本人の辞退。年・前提・時間帯は効きません。'];
    case 'arrive':return['現場到着までの平均時間（分、2024年）','高さと色＝119番入電後、区内の救急隊が現場に着くまでの平均（出場件数で加重）。市平均8.6分。年・前提・時間帯は効きません。'];
    case 'aging':return[`${y}の65歳以上の割合（市の人口推計）`,""")
rep("function affects(){const m=state.mode,base=state.year==='2025';return{year:m!=='day',sc:m==='disp'&&!base,time:m==='disp',view:COUNT_MODES.includes(m)}}",
    "function affects(){const m=state.mode,base=state.year==='2025';return{year:!STATIC_MODES.includes(m),sc:DISP_MODES.includes(m)&&!base,time:DISP_MODES.includes(m),view:COUNT_MODES.includes(m)}}")
# labels
rep("else if(state.mode==='pop'||state.mode==='elder')sub=man(v);","else if(state.mode==='pop'||state.mode==='elder')sub=man(v);else if(state.mode==='percap')sub=v.toFixed(0);else if(state.mode==='density')sub=fmt(v);else if(state.mode==='nontr')sub=v.toFixed(0)+'%';else if(state.mode==='arrive')sub=v.toFixed(1)+'分';")
rep("pop:['人口（人）','9万','37万'],","pop:['人口（人）','9万','37万'],percap:['住民1,000人あたり出場件数','45','125'],density:['出場密度（件/km²）','350','1,600'],nontr:['不搬送率','12%','40%'],arrive:['現場到着時間（分）','6','10'],")
rep("if(isDiff()){L[0]=(state.mode==='pop'?'人口の2025年比':state.mode==='elder'?'65歳以上人口の2025年比':'出場件数の2024年比');L[1]=diffLo()+'%';L[2]='+'+diffHi()+'%'}else if(state.mode==='disp'){L[1]=fmt(7000*bandK());L[2]=fmt(23000*bandK())}",
    "if(isDiff()){L[0]=({pop:'人口の2025年比',elder:'65歳以上人口の2025年比',percap:'1,000人あたりの2025年比',density:'出場密度の2025年比'})[state.mode]||'出場件数の2024年比';L[1]=diffLo()+'%';L[2]='+'+diffHi()+'%'}else if(state.mode==='disp'){L[1]=fmt(7000*bandK());L[2]=fmt(23000*bandK())}else if(state.mode==='percap'){L[1]=(45*bandK()).toFixed(0);L[2]=(125*bandK()).toFixed(0)}else if(state.mode==='density'){L[1]=fmt(350*bandK());L[2]=fmt(1600*bandK())}")
# total chip
rep("  else if(state.mode==='elder'){","  else if(state.mode==='percap'){const t=cityTotal(y)/cityPop(y)*1000,t0=cityTotal('2025')/cityPop('2025')*1000;tv.textContent=t.toFixed(1);tu.textContent=`市全体の住民1,000人あたり${BAND[state.time]}出場件数`;d.textContent=y==='2025'?'2024年実績':`2025年比 ${pct((t/t0-1)*100)}`;d.className='d num '+(y==='2025'?'':'up')}\n  else if(state.mode==='density'){const t=cityTotal(y)/AREA_CITY,t0=cityTotal('2025')/AREA_CITY;tv.textContent=fmt(t);tu.textContent=`市全体の${BAND[state.time]}出場密度（件/km²・438km²）`;d.textContent=y==='2025'?'2024年実績':`2025年比 ${pct((t/t0-1)*100)}`;d.className='d num '+(y==='2025'?'':(t>=t0?'up':'dn'))}\n  else if(state.mode==='nontr'){tv.textContent=(DATA.cityNonTr*100).toFixed(1)+'%';tu.textContent='市全体の不搬送率（2024年）';d.textContent='不搬送 49,676件。うち辞退 81%・死亡 8%・途中帰署 4%';d.className='d num'}\n  else if(state.mode==='arrive'){tv.textContent=DATA.cityArrive.toFixed(1)+'分';tu.textContent='市全体の現場到着までの平均時間（2024年）';d.textContent='平均距離 2.7km。119番から病院到着まで平均46.7分';d.className='d num'}\n  else if(state.mode==='elder'){")
rep("  if(state.mode==='disp')document.getElementById('totU').textContent=","  if(state.mode==='disp')document.getElementById('totU').textContent=")
# hash accept
rep("if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v'))){state.view=h.get('v');pressSeg('viewSeg','v',state.view)}if(['all','day','night'].includes(h.get('t')))",
    "if(['disp','percap','density','nontr','arrive','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v'))){state.view=h.get('v');pressSeg('viewSeg','v',state.view)}if(['all','day','night'].includes(h.get('t')))")
rep("if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(h.get('m')==='diff')",
    "if(['disp','percap','density','nontr','arrive','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(h.get('m')==='diff')")
# mini chart
rep("let v;if(m==='disp')v=sum(w=>bandOf(w,y,state.time,sc));else if(m==='pop')v=sum(w=>popTot(w,y));else if(m==='elder')v=sum(w=>elderOf(w,y));else if(m==='aging')v=sum(w=>elderOf(w,y))/sum(w=>popTot(w,y))*100;else return null;\n  if(isDiff()){let b;if(m==='disp')b=sum(w=>bandOf(w,'2025',state.time,sc));else if(m==='pop')b=sum(w=>popTot(w,'2025'));else b=sum(w=>elderOf(w,'2025'));v=(v/b-1)*100}return v}",
    "let v;if(m==='disp')v=sum(w=>bandOf(w,y,state.time,sc));else if(m==='percap')v=sum(w=>bandOf(w,y,state.time,sc))/sum(w=>popTot(w,y))*1000;else if(m==='density')v=sum(w=>bandOf(w,y,state.time,sc))/sum(w=>w.area);else if(m==='pop')v=sum(w=>popTot(w,y));else if(m==='elder')v=sum(w=>elderOf(w,y));else if(m==='aging')v=sum(w=>elderOf(w,y))/sum(w=>popTot(w,y))*100;else return null;\n  if(isDiff()){let b;if(m==='disp')b=sum(w=>bandOf(w,'2025',state.time,sc));else if(m==='percap')b=sum(w=>bandOf(w,'2025',state.time,sc))/sum(w=>popTot(w,'2025'))*1000;else if(m==='density')b=sum(w=>bandOf(w,'2025',state.time,sc))/sum(w=>w.area);else if(m==='pop')b=sum(w=>popTot(w,'2025'));else b=sum(w=>elderOf(w,'2025'));v=(v/b-1)*100}return v}")
rep("if(state.mode==='day'){T.textContent=`推移なし — 昼夜間比は2020年固定（${name}）`;S.innerHTML='';return}",
    "if(STATIC_MODES.includes(state.mode)){T.textContent=state.mode==='day'?`推移なし — 昼夜間比は2020年固定（${name}）`:`推移なし — 2024年の実績値（${name}）`;S.innerHTML='';return}")
rep("const showB=state.mode==='disp';","const showB=DISP_MODES.includes(state.mode);")
rep("const f=v=>isDiff()||state.mode==='aging'?(v>0&&isDiff()?'+':'')+v.toFixed(isDiff()?0:0)+'%':(v>=100000?(v/10000).toFixed(0)+'万':v>=10000?(v/10000).toFixed(1)+'万':fmt(v));",
    "const f=v=>isDiff()||state.mode==='aging'?(v>0&&isDiff()?'+':'')+v.toFixed(0)+'%':state.mode==='percap'?v.toFixed(0):(v>=100000?(v/10000).toFixed(0)+'万':v>=10000?(v/10000).toFixed(1)+'万':fmt(v));")
rep("const lab={disp:BAND[state.time]+'出場件数',pop:'人口',elder:'65歳以上人口',aging:'高齢化率'}[state.mode];","const lab={disp:BAND[state.time]+'出場件数',percap:BAND[state.time]+'1,000人あたり出場',density:BAND[state.time]+'出場密度',pop:'人口',elder:'65歳以上人口',aging:'高齢化率'}[state.mode];")

# ---------- split columns (搬送 / 不搬送) ----------
rep("const m=new THREE.Mesh(geo,mat); m.userData={i,h:1,target:1}; group.add(m); meshes.push(m);",
    "const m=new THREE.Mesh(geo,mat); m.userData={i,h:1,target:1,split:0}; group.add(m); meshes.push(m);\n  const top=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.8,metalness:0,transparent:true,opacity:.92})); top.visible=false; group.add(top); m.userData.top=top;")
rep("meshes.forEach(m=>{const w=W[m.userData.i],v=metric(w);m.userData.target=heightFor(w);m.material.color.set(colorFor(v));",
    "const splitOn=state.mode==='disp'&&!isDiff();\n  meshes.forEach(m=>{const w=W[m.userData.i],v=metric(w);m.userData.target=heightFor(w);m.material.color.set(colorFor(v));m.userData.split=splitOn?w.nonTr:0;m.userData.top.visible=splitOn;if(splitOn){const c=new THREE.Color(colorFor(v));m.userData.top.material.color.copy(c).lerp(new THREE.Color(state.time==='night'?0x0e1730:0xffffff),0.6)}")
rep("meshes.forEach(m=>{const d=m.userData.target-m.userData.h;if(Math.abs(d)>0.002){m.userData.h+=d*Math.min(1,dt*6);m.scale.y=m.userData.h;m.userData.label.position.y=m.userData.h+0.9}});",
    "meshes.forEach(m=>{const d=m.userData.target-m.userData.h;if(Math.abs(d)>0.002||m.userData.dirty!==m.userData.split){m.userData.h+=d*Math.min(1,dt*6);const h=m.userData.h,sp=m.userData.split;m.scale.y=h*(1-sp);m.userData.top.scale.y=Math.max(0.001,h*sp);m.userData.top.position.y=h*(1-sp);m.userData.label.position.y=h+0.9;m.userData.dirty=sp}});")
rep("document.getElementById('legH').textContent='高さも同じ指標（平行投影で比較可）';","document.getElementById('legH').textContent=splitOn?'高さも同じ指標。薄い上段＝搬送しなかった出場（不搬送）':'高さも同じ指標（平行投影で比較可）';")

# ---------- sheet: ops line + types bar ----------
rep('<p class="note" id="shRead"></p><p class="note" id="shUnit"></p>',
    '<p class="note" id="shRead"></p><p class="note" id="shUnit"></p><p class="note" id="shOps"></p><div class="stack"><div class="t"><span>出場の内訳 2024（事故種別）</span><span id="st3v" class="num"></span></div><div class="b" id="st3"></div></div><div class="lg"><span><b style="background:#3a7bd5"></b>急病</span><span><b style="background:#9ad0f5"></b>一般負傷</span><span><b style="background:#f4a259"></b>交通事故</span><span><b style="background:#8e3b8f"></b>転院搬送</span><span><b style="background:#c9d2de"></b>その他</span></div>')
rep("  document.getElementById('shRead').textContent=readingOf(w);",
    """  document.getElementById('shRead').textContent=readingOf(w);
  const u2=unitsOf(w);document.getElementById('shOps').innerHTML=`<b>現場到着</b> 平均 ${w.arrive.toFixed(1)}分・${w.dist.toFixed(1)}km（市平均 ${DATA.cityArrive.toFixed(1)}分・2.7km）。<b>1隊あたり</b> ${(w.area/u2).toFixed(1)}km²（面積 ${w.area}km²）。<b>不搬送率</b> ${(w.nonTr*100).toFixed(0)}%（市平均 ${(DATA.cityNonTr*100).toFixed(0)}%）。住民1,000人あたり ${(w.disp24/popTot(w,'2025')*1000).toFixed(0)}件・${fmt(w.disp24/w.area)}件/km²。`;
  const T=w.types,tt=w.disp24,TC=[['急病','#3a7bd5'],['一般負傷','#9ad0f5'],['交通事故','#f4a259'],['転院搬送','#8e3b8f']];let other=tt;const segs=TC.map(([k,c])=>{other-=T[k];return `<i style="width:${(T[k]/tt*100).toFixed(1)}%;background:${c}" title="${k}"></i>`}).join('')+`<i style="width:${(other/tt*100).toFixed(1)}%;background:#c9d2de"></i>`;document.getElementById('st3').innerHTML=segs;document.getElementById('st3v').textContent=`急病 ${(T['急病']/tt*100).toFixed(0)}%・転院 ${(T['転院搬送']/tt*100).toFixed(1)}%`;""")

# ---------- Q text ----------
rep("mode:'<b>何を見るか。</b>出場件数＝救急車が出動した年間件数（区内で発生したもの。2025年は2024年実績、以降は推計）。人口＝区の総人口。高齢者人口＝65歳以上の人数。高齢化率＝65歳以上÷総人口。昼夜間比＝昼間人口÷夜間人口×100（2020年国勢調査、年によらず固定）。',",
    "mode:'<b>何を見るか。</b>出場件数＝救急車が出動した年間件数（区内で発生。2025年は2024年実績、以降は推計。薄い上段は不搬送分）。1,000人あたり＝出場件数÷区の人口×1,000。件/km²＝出場件数÷区の面積（港湾・水面含む）。不搬送率＝出場したが搬送しなかった割合（2024年、区内の救急隊の実績）。到着時間＝119番から現場到着までの平均分（2024年）。人口＝総人口。高齢者人口＝65歳以上。高齢化率＝65歳以上÷総人口。昼夜間比＝昼間人口÷夜間人口×100（2020年固定）。',")

# ---------- city page: density/arrive scatter + nontr ranking ----------
rep('<div class="card"><h4>救急隊あたりの負担 — 1隊あたり年間出場件数</h4>',
'''<div class="card"><h4>密度と到着時間 — 疎な区ほど現場が遠い</h4><svg class="chart" id="chScatter" viewBox="0 0 600 360"></svg><p class="m">横軸＝出場密度（件/km²、対数）、縦軸＝現場到着までの平均時間（2024年、区内の救急隊の加重平均）。円の大きさ＝1隊あたりのカバー面積。右下ほど「密で速い」、左上ほど「疎で遅い」。 <a class="mapgo" href="#" data-state="m=density">出場密度を地図で</a> <a class="mapgo" href="#" data-state="m=arrive">到着時間を地図で</a></p></div>
  <div class="card"><h4>不搬送率 — 出場したが搬送しなかった割合（2024年）</h4><div id="nontrList"></div><p class="m">区内の救急隊の出場件数と搬送人員から算出。市平均19%。不搬送49,676件の理由は、本人の辞退 81%、死亡 8%、途中帰署 4%、傷病者なし 3%、虚誤報 2%。 <a class="mapgo" href="#" data-state="m=nontr">不搬送率を地図で</a> <a class="mapgo" href="#" data-state="m=disp">搬送／不搬送の2段の柱を地図で</a></p></div>
  <div class="card"><h4>救急隊あたりの負担 — 1隊あたり年間出場件数</h4>''')
rep("function buildCity(){","""function scatterChart(id){const W2=[...W].map(w=>({n:w.name,x:w.disp24/w.area,y:w.arrive,r:w.area/unitsOf(w)}));
  const X=v=>60+(Math.log(v)-Math.log(300))/(Math.log(1800)-Math.log(300))*520,Y=v=>320-(v-5.8)/(10-5.8)*290;
  let g=`<g stroke="#e3e8ef">${[6,7,8,9,10].map(v=>`<line x1="60" x2="580" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}${[300,500,1000,1500].map(v=>`<line x1="${X(v)}" x2="${X(v)}" y1="30" y2="320"/>`).join('')}</g>`;
  g+=[6,7,8,9,10].map(v=>`<text x="54" y="${Y(v)+4}" font-size="11" fill="#8e9bae" text-anchor="end">${v}分</text>`).join('')+[300,500,1000,1500].map(v=>`<text x="${X(v)}" y="338" font-size="11" fill="#8e9bae" text-anchor="middle">${fmt(v)}</text>`).join('');
  g+=`<text x="580" y="352" font-size="11" fill="#5b6b82" text-anchor="end">出場密度（件/km²）</text>`;
  g+=`<line x1="60" x2="580" y1="${Y(DATA.cityArrive)}" y2="${Y(DATA.cityArrive)}" stroke="#8e9bae" stroke-dasharray="3 3"/><text x="64" y="${Y(DATA.cityArrive)-4}" font-size="10" fill="#8e9bae">市平均 ${DATA.cityArrive.toFixed(1)}分</text>`;
  W2.forEach(p=>{const r=4+p.r*1.6,c=p.y>=9.3?'#e63946':p.y>=8.6?'#f4a259':'#1b998b';g+=`<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="${r}" fill="${c}" opacity=".7"/><text x="${X(p.x)+r+3}" y="${Y(p.y)+4}" font-size="11" font-weight="700" fill="#14213d">${p.n}</text>`});
  document.getElementById(id).innerHTML=g}
function nontrRows(){const rk=[...W].map(w=>({n:w.name,v:w.nonTr*100,d:w.unitDisp,t:w.unitTr})).sort((a,b)=>b.v-a.v);
  return rk.map(r=>`<div class="rank"><span class="nm">${r.n}区</span><span class="barw"><i style="left:0;width:${r.v/45*100}%;background:${r.v>=25?'#e63946':r.v>=19?'#f4a259':'#1b998b'}"></i></span><span class="pct num">${r.v.toFixed(0)}%</span></div>`).join('')}
function buildCity(){""")
rep("SVG.trend('chTrend');SVG.age('chAge');SVG.rate('chRate');pairChart('chPair');document.getElementById('unitList').innerHTML=unitRows().html;",
    "SVG.trend('chTrend');SVG.age('chAge');SVG.rate('chRate');pairChart('chPair');document.getElementById('unitList').innerHTML=unitRows().html;scatterChart('chScatter');document.getElementById('nontrList').innerHTML=nontrRows();")

# ---------- insight ----------
rep('<h3>8. 施策への示唆</h3>',
'''<h3>8. 密度と到着時間 — 疎な区ほど現場が遠い</h3>
  <p>出場密度は西区1,537件/km²、南区1,228件/km²から、都筑区394件/km²、栄区439件/km²まで4倍の開きがあります。1隊あたりのカバー面積は西区1.4km²に対し、戸塚・青葉・都筑は7km²。現場到着までの平均時間は中区6.4分が最短で、保土ケ谷9.6分・緑9.5分・旭9.4分・戸塚9.2分・泉9.2分が遅く、市平均は8.6分（平均距離2.7km）です。密度が低い区は1件ごとの走行距離が長く、同じ件数でも隊の拘束時間が長くなります。</p>
  <div class="callout b">南西部（旭・泉・栄・瀬谷）は件数が横ばいでも、高齢化率35%前後と到着9分超が重なる区です。件数ではなく「到着時間」を配置の指標にすると、北部とは別の理由で手当てが要ることが見えます。</div>
  <p><a class="mapgo" href="#" data-state="m=density">出場密度を地図で</a> <a class="mapgo" href="#" data-state="m=arrive">到着時間を地図で</a> <a class="mapgo" href="#" data-state="m=percap">1,000人あたりを地図で</a></p>
  <h3>9. 不搬送 — 減らせる需要がどこにあるか</h3>
  <p>2024年の出場256,481件のうち49,676件（19%）は搬送に至っていません。理由の81%は本人の辞退で、死亡8%、途中帰署4%と続きます。区内の救急隊ベースで見ると、中区の不搬送率は37%と突出し、西区25%、港北・神奈川・南が20〜22%。郊外の泉・栄・戸塚・旭は13〜14%です。中区の校正係数1.69（人口から期待される件数の1.7倍）の相当部分は、繁華街での辞退や軽症など「搬送に至らない出場」で説明できます。</p>
  <p>不搬送の多い区は、#7119（救急相談）や軽症者対策で出場そのものを減らせる余地が大きい区でもあります。逆に不搬送率が低い郊外区は、出場のほとんどが実際の搬送なので、件数の増加がそのまま病院搬送の負荷になります。</p>
  <p><a class="mapgo" href="#" data-state="m=nontr">不搬送率を地図で</a> <a class="mapgo" href="#" data-state="m=disp&w=中">中区の搬送／不搬送を地図で</a></p>
  <h3>10. 施策への示唆</h3>''')
rep('<li>南西部（瀬谷・栄・旭・港南・泉）は件数が横ばいでも高齢化率35%前後に達し、重症度・現場滞在時間の増加への備えが課題。</li>',
    '<li>南西部（瀬谷・栄・旭・港南・泉）は件数が横ばいでも高齢化率35%前後に達し、到着時間も9分超。重症度・現場滞在時間の増加への備えと、出張所の配置見直しが課題。</li>\n    <li>中・西・港北・神奈川の不搬送率が高い区では、#7119 の周知と繁華街での軽症対応（救急相談・民間搬送）で、出場を1〜2割減らせる可能性がある。</li>')

# ---------- method ----------
rep('<li><b>昼夜間人口比率</b>：昼間人口 ÷ 夜間人口 × 100（2020年国勢調査、全年共通）。</li>',
    '<li><b>昼夜間人口比率</b>：昼間人口 ÷ 夜間人口 × 100（2020年国勢調査、全年共通）。</li>\n    <li><b>1,000人あたり</b>：出場件数 ÷ 区の人口 × 1,000。<b>件/km²</b>：出場件数 ÷ 区の面積（国土地理院 面積調、港湾・水面を含む）。</li>\n    <li><b>不搬送率</b>：1 − 搬送人員 ÷ 出場件数。消防年報の救急隊別活動状況（87隊）を区ごとに合計した2024年実績。隊は区をまたいで出場するため「区内の隊の実績」です。</li>\n    <li><b>到着時間</b>：119番入電から現場到着までの平均（分）。同じ隊別表を出場件数で加重平均。</li>')
rep('<li>区界ポリゴン：国土数値情報（行政区域データ）を加工した niiyz/JapanCityGeoJson（簡略化）。</li>',
    '<li>国土地理院「全国都道府県市区町村別面積調」— 区の面積（令和6年）。<a href="https://www.gsi.go.jp/KOKUJYOHO/MENCHO-title.htm">ページ</a></li>\n    <li>区界ポリゴン：国土数値情報（行政区域データ）を加工した niiyz/JapanCityGeoJson（簡略化）。</li>')
rep('時間帯別出場件数、救急隊数85.5隊。','時間帯別出場件数、救急隊別の出場・搬送・現場到着時間（p.105）、不取扱理由（p.108）、救急隊数85.5隊。')

# ---------- slides ----------
rep("  ()=>`<div class=\"kick\">計算方法</div><h2>5つのステップ</h2>",
"""  ()=>`<div class="kick">密度と到着時間</div><h2>疎な区ほど現場が遠い</h2><div class="cols two"><div><svg class="chart" id="slScatter" viewBox="0 0 600 360"></svg><p class="m">横軸＝出場密度（件/km²）、縦軸＝現場到着までの平均時間（2024年）。円＝1隊あたりカバー面積。</p></div><div>${pt('6.4分','中区の到着時間（最短）。1隊あたり3.7km²、1.9km')}${pt('9.6分','保土ケ谷区（最長）。緑9.5・旭9.4・戸塚9.2・泉9.2分',1)}<p class="m" style="margin-top:12px">市平均8.6分・2.7km。南西部は件数が横ばいでも、高齢化率35%と到着9分超が重なる。</p></div></div>`,
  ()=>`<div class="kick">不搬送</div><h2>出場の19%は搬送に至らない</h2><div class="cols two"><div>${nontrRows()}<p class="m">区内の救急隊ベースの不搬送率（2024年）</p></div><div>${pt('49,676件','不搬送の件数。理由は辞退81%・死亡8%・途中帰署4%',1)}${pt('37%','中区の不搬送率（市平均19%）。校正係数1.69の相当部分は搬送に至らない出場')}<div class="callout" style="margin-top:14px">不搬送の多い区（中・西・港北・神奈川）は #7119 と軽症対策で出場を減らせる余地が大きい。</div></div></div>`,
  ()=>`<div class="kick">計算方法</div><h2>5つのステップ</h2>""")
rep("SVG.trend('slTrend');SVG.rate('slRate');SVG.age('slAge');SVG.flow('slFlow');","SVG.trend('slTrend');SVG.rate('slRate');SVG.age('slAge');SVG.flow('slFlow');scatterChart('slScatter');")
P.write_text(s,encoding='utf-8'); print('patched',len(s))
