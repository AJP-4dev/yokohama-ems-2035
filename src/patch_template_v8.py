import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

# nav
rep("const PAGES=[['map','地図','<path d=\"M9 20l-6-3V4l6 3 6-3 6 3v13l-6-3-6 3z\"/><path d=\"M9 7v13M15 4v13\"/>'],['city','市全体','<path d=\"M4 20V10M10 20V4M16 20v-7M22 20H2\"/>'],",
    "const PAGES=[['map','地図','<path d=\"M9 20l-6-3V4l6 3 6-3 6 3v13l-6-3-6 3z\"/><path d=\"M9 7v13M15 4v13\"/>'],['city','市全体','<path d=\"M4 20V10M10 20V4M16 20v-7M22 20H2\"/>'],['wards','区別','<rect x=\"3\" y=\"3\" width=\"8\" height=\"8\" rx=\"1.5\"/><rect x=\"13\" y=\"3\" width=\"8\" height=\"8\" rx=\"1.5\"/><rect x=\"3\" y=\"13\" width=\"8\" height=\"8\" rx=\"1.5\"/><rect x=\"13\" y=\"13\" width=\"8\" height=\"8\" rx=\"1.5\"/>'],")
rep("#nav button{flex:1;border:0;background:none;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:10.5px;color:var(--ink3);padding:6px 0 4px}",
    "#nav button{flex:1;border:0;background:none;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:10px;color:var(--ink3);padding:6px 0 4px}")
# city page next button → wards
rep('<button class="next" data-go="insight">考察を読む<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>\n</div></div></section>\n\n<!-- ================= INSIGHT ================= -->',
'''<button class="next" data-go="wards">区ごとの特徴を見る<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
</div></div></section>

<!-- ================= WARDS ================= -->
<section class="page" id="page-wards"><div class="scroll"><div class="wrap">
  <h2>区ごとの特徴</h2>
  <p class="lead">18区を4つのタイプに分け、市平均との差で「何が多く、何が少ない区か」を見ます。棒は市平均を中心に、右が市平均より多い（長い・遅い）、左が少ない。</p>
  <div class="card"><h4>4つのタイプ</h4><div id="typeLegend"></div><p class="m">タイプは、昼夜間人口比率・2035年の高齢化率・出場件数の増減率で機械的に分けています。</p></div>
  <div id="wardJump" class="jump"></div>
  <div id="wardCards"></div>
  <button class="next" data-go="insight">考察を読む<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
</div></div></section>

<!-- ================= INSIGHT ================= -->''')
# CSS for ward cards
rep(".callout{border-left:4px solid var(--red);",
""".jump{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}
.jump button{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:5px 11px;font-size:12.5px;cursor:pointer}
.jump button:hover{background:var(--navy);color:#fff}
.wcard{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px 18px;margin:14px 0}
.wcard h3{margin:0 0 2px;font-size:20px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.wcard h3 .typ{font-size:11.5px;font-weight:700;padding:2px 9px;border-radius:999px;color:#fff}
.wcard .one{font-size:14.5px;line-height:1.7;margin:6px 0 10px;color:var(--ink)}
.prof{display:grid;grid-template-columns:118px 1fr 64px;gap:4px 8px;align-items:center;font-size:12px;margin:8px 0}
.prof .pl{color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.prof .pb{position:relative;height:12px;background:var(--surface2);border-radius:6px}
.prof .pb:before{content:'';position:absolute;left:50%;top:-2px;bottom:-2px;width:1px;background:var(--ink3)}
.prof .pb i{position:absolute;top:0;height:100%;border-radius:6px}
.prof .pv{text-align:right;font-family:Manrope,sans-serif;font-weight:700;white-space:nowrap}
.prof .pv small{display:block;font-size:9.5px;color:var(--ink3);font-weight:400}
.wcard ul{margin:8px 0 0;padding-left:18px}
.wcard li{font-size:13.5px;line-height:1.7;margin:3px 0}
.tl{display:flex;flex-wrap:wrap;gap:8px}
.tl span{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;background:var(--surface2);border-radius:999px;padding:4px 10px}
.tl b{width:10px;height:10px;border-radius:50%;display:inline-block}
.callout{border-left:4px solid var(--red);""")

# JS: ward profiles
rep("/* ---------- slides ---------- */\nconst pt=",
"""/* ---------- ward profiles ---------- */
const TYPES={core:['都心・来街型','#e63946'],grow:['件数が伸びる住宅地型','#d9822b'],urban:['都市部住宅型','#3a7bd5'],mature:['成熟した郊外住宅地型','#1b998b']};
function wardType(w){const ag35=agingRate(w,'2035'),dg=(w.disp['2035']/w.disp24-1)*100;if(w.dn>=120)return 'core';if(ag35>=34)return 'mature';if(dg>=9.5)return 'grow';return 'urban'}
function wardMetrics(w){
  const pop=popTot(w,'2025'),cityPop25=cityPop('2025'),cityDisp=cityTotal('2025');
  const share=k=>w.types[k]/w.disp24*100,cshare=k=>W.reduce((s,x)=>s+x.types[k],0)/cityDisp*100;
  const cityDN=W.reduce((s,x)=>s+x.day20,0)/W.reduce((s,x)=>s+x.night20,0)*100;
  const e3g=(w.pop['2035'].e3/w.pop['2025'].e3-1)*100,ce3g=(cityPop('2035','e3')/cityPop('2025','e3')-1)*100;
  return [
   {k:'percap',l:'1,000人あたり出場',v:w.disp24/pop*1000,c:cityDisp/cityPop25*1000,f:v=>v.toFixed(0)+'件'},
   {k:'nontr',l:'不搬送率',v:w.nonTr*100,c:DATA.cityNonTr*100,f:v=>v.toFixed(0)+'%'},
   {k:'arrive',l:'現場到着時間',v:w.arrive,c:DATA.cityArrive,f:v=>v.toFixed(1)+'分'},
   {k:'kmu',l:'1隊あたり面積',v:w.area/unitsOf(w),c:AREA_CITY/W.reduce((s,x)=>s+unitsOf(x),0),f:v=>v.toFixed(1)+'km²'},
   {k:'pu',l:'1隊あたり件数',v:w.disp24/unitsOf(w),c:cityDisp/W.reduce((s,x)=>s+unitsOf(x),0),f:v=>fmt(v)+'件'},
   {k:'aging',l:'高齢化率 2035',v:agingRate(w,'2035'),c:(cityPop('2035','e1')+cityPop('2035','e2')+cityPop('2035','e3'))/cityPop('2035')*100,f:v=>v.toFixed(1)+'%'},
   {k:'e3g',l:'85歳以上の増加 →2035',v:e3g,c:ce3g,f:v=>pct(v,0),ratio:false},
   {k:'dg',l:'出場の増減 →2035',v:(w.disp['2035']/w.disp24-1)*100,c:(A35/cityDisp-1)*100,f:v=>pct(v,1),ratio:false},
   {k:'transfer',l:'転院搬送の割合',v:share('転院搬送'),c:cshare('転院搬送'),f:v=>v.toFixed(1)+'%'},
   {k:'dn',l:'昼夜間人口比',v:w.dn,c:cityDN,f:v=>v.toFixed(0)}]}
function rankOf(k,w,desc=true){const vals=W.map(x=>({n:x.name,v:wardMetrics(x).find(m=>m.k===k).v})).sort((a,b)=>desc?b.v-a.v:a.v-b.v);return vals.findIndex(x=>x.n===w.name)+1}
function profHTML(ms){return `<div class="prof">${ms.map(m=>{let t;if(m.ratio===false){t=(m.v-m.c)/Math.max(1,Math.abs(m.c)*1.2)}else{t=Math.log(m.v/m.c)/Math.log(2.2)}t=Math.max(-1,Math.min(1,t));const w=Math.abs(t)*50,left=t>=0?50:50-w,col=t>=0?'#e63946':'#1b998b';return `<div class="pl">${m.l}</div><div class="pb"><i style="left:${left}%;width:${w}%;background:${col};opacity:.8"></i></div><div class="pv">${m.f(m.v)}<small>市 ${m.f(m.c)}</small></div>`}).join('')}</div>`}
function wardText(w){
  const ms=wardMetrics(w),g=k=>ms.find(m=>m.k===k),out=[];
  const fac=w.fac,pop=popTot(w,'2025'),net=w.in-w.out;
  // 1. 需要の水準
  const rp=rankOf('percap',w);let s1=`住民1,000人あたりの出場は${g('percap').f(g('percap').v)}で18区中${rp}位（市平均${g('percap').f(g('percap').c)}）。`;
  if(fac>=1.12){const why=[];if(w.nonTr>DATA.cityNonTr+0.03)why.push(`不搬送率が市平均より${((w.nonTr-DATA.cityNonTr)*100).toFixed(0)}pt高い（辞退・軽症が多い）`);if(net>20000)why.push(`通勤・通学で${man(net)}人の流入超過`);if(g('transfer').v>g('transfer').c*1.3)why.push(`転院搬送が市平均の${(g('transfer').v/g('transfer').c).toFixed(1)}倍（病院立地）`);s1+=`人口と年齢構成から期待される件数の<b>${fac.toFixed(2)}倍</b>で、${why.length?why.join('、')+'が押し上げている。':'人口では説明できない需要が大きい。'}`}
  else if(fac<=0.9){s1+=`人口と年齢構成から期待される件数より<b>${((1-fac)*100).toFixed(0)}%少ない</b>。${w.dn<85?'昼間に人口が流出し、':''}若く健康な年齢構成で救急利用が少ない区。`}
  else s1+=`人口から期待される件数とほぼ一致（校正係数${fac.toFixed(2)}）。`;
  out.push(s1);
  // 2. 需要の質（事故種別）
  const keys=['急病','一般負傷','交通事故','転院搬送','加害','労働災害','運動競技','自損行為','火災'],cityDisp=cityTotal('2025');
  const odd=keys.map(k=>({k,r:(w.types[k]/w.disp24)/(W.reduce((s,x)=>s+x.types[k],0)/cityDisp),n:w.types[k]})).filter(o=>o.n>=40&&(o.r>=1.35||o.r<=0.7)).sort((a,b)=>b.r-a.r);
  const HINT2={'加害':'繁華街','転院搬送':'病院の立地','労働災害':'工場・港湾','運動競技':'スタジアム・競技施設','交通事故':'幹線道路','自損行為':'','火災':'','急病':'','一般負傷':''};
  if(odd.length){out.push('出場の内訳では'+odd.map(o=>`${o.k}が市平均の${o.r.toFixed(1)}倍（${fmt(o.n)}件${HINT2[o.k]&&o.r>1?'、'+HINT2[o.k]:''}）`).join('、')+'。')}
  else out.push(`出場の内訳は市平均に近く、急病${(w.types['急病']/w.disp24*100).toFixed(0)}%・一般負傷${(w.types['一般負傷']/w.disp24*100).toFixed(0)}%。`);
  // 3. 将来
  const dg=g('dg').v,e3g=g('e3g').v,pg=(popTot(w,'2035')/pop-1)*100,oA=overYear(w,'A'),oB=overYear(w,'B'),pu=w.disp24/unitsOf(w);
  let s3=`2035年の出場は<b>${pct(dg)}</b>（人口${pct(pg)}、85歳以上${pct(e3g,0)}）。`;
  if(dg>=9.5)s3+='人口の減少を高齢化が大きく上回る。';else if(dg<=3)s3+='人口減少が高齢化をほぼ相殺し横ばい。';
  s3+=`1隊あたり${fmt(pu)}件で、3,000件の目安を${oA===2025?'すでに超えている':oA?oA+'年に超える':'2040年まで超えない'}${oB&&oB!==oA?`（上限シナリオでは${oB===2025?'すでに超過':oB+'年'}）`:''}。`;
  out.push(s3);
  // 4. 供給側
  const ra=rankOf('arrive',w),rk=rankOf('kmu',w);
  out.push(`現場到着は平均${w.arrive.toFixed(1)}分で${ra<=4?'市内でも遅い方（'+ra+'位）':ra>=15?'市内で速い方（'+ra+'位）':ra+'位'}、1隊あたり${(w.area/unitsOf(w)).toFixed(1)}km²（${rk}位）。不搬送率${(w.nonTr*100).toFixed(0)}%${w.nonTr>DATA.cityNonTr+0.03?'は市平均を大きく上回り、#7119 や軽症対策で減らせる余地が大きい':w.nonTr<DATA.cityNonTr-0.03?'は市平均より低く、出場の大半が実際の搬送につながる':'は市平均並み'}。`);
  return out}
function buildWards(){
  document.getElementById('typeLegend').innerHTML=`<div class="tl">${Object.entries(TYPES).map(([k,[n,c]])=>`<span><b style="background:${c}"></b>${n}：${W.filter(w=>wardType(w)===k).map(w=>w.name).join('・')}</span>`).join('')}</div>`;
  document.getElementById('wardJump').innerHTML=W.map((w,i)=>`<button data-i="${i}">${w.name}</button>`).join('');
  document.querySelectorAll('#wardJump button').forEach(b=>b.onclick=()=>{const el=document.getElementById('wc-'+b.dataset.i),sc=document.querySelector('#page-wards .scroll');sc.scrollTop=el.offsetTop-70});
  document.getElementById('wardCards').innerHTML=W.map((w,i)=>{const t=wardType(w),[tn,tc]=TYPES[t];return `<div class="wcard" id="wc-${i}"><h3>${w.name}区 <span class="typ" style="background:${tc}">${tn}</span><span class="m">人口 ${man(popTot(w,'2025'))}人・出場 ${fmt(w.disp24)}件・${unitsOf(w)}隊</span></h3>${profHTML(wardMetrics(w))}<ul>${wardText(w).map(t=>`<li>${t}</li>`).join('')}</ul><p style="margin:10px 0 0"><a class="mapgo" href="#" data-state="m=disp&y=2035&w=${w.name}">2035年を地図で</a> <a class="mapgo" href="#" data-state="m=nontr&w=${w.name}">不搬送率を地図で</a> <a class="mapgo" href="#" data-state="m=arrive&w=${w.name}">到着時間を地図で</a></p></div>`}).join('');
  bindMapLinks(document.getElementById('page-wards'));
}
buildWards();

/* ---------- slides ---------- */
const pt=""")
# intro step text
rep('<div><b>2</b><span><strong>市全体</strong>と<strong>考察</strong>で、なぜ増えるのか・どこで増えるのかを読む。</span></div>',
    '<div><b>2</b><span><strong>市全体</strong>と<strong>区別</strong>、<strong>考察</strong>で、なぜ増えるのか・どこで増えるのか・各区の特徴を読む。</span></div>')
P.write_text(s,encoding='utf-8'); print('patched',len(s))
