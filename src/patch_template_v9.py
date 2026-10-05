import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

rep('<h3>10. 施策への示唆</h3>',
'''<h3>10. 2025年の断面で見る — 人口構成・密度と出場件数の関係</h3>
  <p>ここまでの推計とは別に、2024〜25年の実績だけを並べて「人口と出場件数はどこまで比例するか」「比例から外れる区はどこか」を確かめます。</p>
  <div class="card"><h4>区別の年齢構成（2025年）と出場件数（2024年）</h4><svg class="chart" id="anA" viewBox="0 0 600 470"></svg><div class="lg"><span><b class="c-c"></b>0–14</span><span><b class="c-w"></b>15–64</span><span><b class="c-e1"></b>65–74</span><span><b class="c-e2"></b>75–84</span><span><b class="c-e3"></b>85+</span><span><b style="background:#14213d"></b>出場件数</span></div><p class="m">左＝年齢構成（高齢化率の高い順）、右＝出場件数と住民1,000人あたり。高齢化率が高い区（栄・金沢・旭）の1,000人あたりは68〜71件で市平均並み。最も高いのは高齢化率が低い中区（121件）・西区（101件）で、年齢構成だけでは説明できない。</p></div>
  <div class="card"><h4>人口と出場件数の比例関係</h4><svg class="chart" id="anB" viewBox="0 0 600 380"></svg><p class="m">点線＝市平均の比例線（住民1,000人あたり68件）。線より上が「人口の割に出場が多い」区。相関係数は <span class="num" id="anBr"></span>。中区は比例線の1.8倍、西区は1.5倍。都筑・青葉・港北は0.75〜0.8倍で、人口の大きさの割に出場が少ない。</p></div>
  <div class="card"><h4>市平均＝100とした指数：人口密度・出場密度・1,000人あたり</h4><svg class="chart" id="anC" viewBox="0 0 600 520"></svg><div class="lg"><span><b style="background:#8fd0c3"></b>人口密度</span><span><b style="background:#3a7bd5"></b>出場密度（件/km²）</span><span><b style="background:#e63946"></b>1,000人あたり出場</span></div><p class="m">市平均：人口密度 8,601人/km²、出場密度 585件/km²、1,000人あたり 68件。出場密度は人口密度とほぼ連動（相関 <span class="num" id="anCr"></span>）し、西・南が2倍超。一方、1,000人あたりは人口密度とほぼ無関係（相関 <span class="num" id="anCr2"></span>）で、密度の指標と「1人あたりの使われ方」は別物。</p></div>
  <div class="card"><h4>高齢化率と住民1,000人あたり出場件数</h4><svg class="chart" id="anD" viewBox="0 0 600 380"></svg><p class="m">18区全体では相関がほぼゼロ（<span class="num" id="anDr"></span>）。しかし中区・西区を除いた16区では <span class="num" id="anDr2"></span> と強い正の相関があり、高齢化率が1pt上がると1,000人あたり約<span class="num" id="anDslope"></span>件増える（点線）。中・西は「住民の高齢化」ではなく来街者・繁華街・不搬送で需要が決まる別の集団。</p></div>
  <p><b>読み取れること</b></p>
  <ul>
    <li><b>人口と出場件数の相関は0.79</b>と高いが、比例から大きく外れる区が両側にある。上側は中（1.8倍）・西（1.5倍）・南（1.15倍）、下側は都筑（0.75倍）・青葉（0.76倍）・港北（0.82倍）。年齢構成を補正しても中1.69・西1.40・都筑0.84・青葉0.82の差が残る（校正係数）。</li>
    <li><b>上側の外れは「昼間人口」と「不搬送」で説明できる。</b>昼夜間人口比率と1,000人あたりの相関は0.76。中区の不搬送率37%・西区25%は、搬送に至らない出場が件数を押し上げていることを示す。</li>
    <li><b>下側の外れは年齢構成と通勤流出。</b>都筑・青葉・港北は高齢化率20〜24%と若く、昼間は人口が流出する。1人あたりの救急利用がもともと少ない上に、昼の人が区内にいない。</li>
    <li><b>住宅地だけなら、高齢化率が1,000人あたり出場をよく説明する</b>（16区で相関0.74）。つまり郊外の需要は年齢構成でほぼ決まり、都心の需要は人の出入りで決まる。推計モデルが「年齢別搬送率 × 校正係数」の2段構えになっているのは、この2つの要因を分けるため。</li>
    <li><b>密度は配置の指標、1人あたりは需要の指標。</b>出場密度は人口密度に連動する（相関0.86）ので、隊の配置・到着時間の議論は密度で、需要の中身の議論は1人あたりで行うのが筋。</li>
    <li>高齢化率と不搬送率の相関は−0.48。高齢化した区ほど出場が搬送に結びつきやすく、「出場の削減余地」は若い都心側にある。</li>
  </ul>
  <p><a class="mapgo" href="#" data-state="m=percap">1,000人あたりを地図で</a> <a class="mapgo" href="#" data-state="m=density">出場密度を地図で</a> <a class="mapgo" href="#" data-state="m=aging">高齢化率を地図で</a></p>
  <h3>11. 施策への示唆</h3>''')

rep("/* ---------- ward profiles ---------- */",
"""/* ---------- 2025 cross-section analysis ---------- */
function corr(xs,ys){const n=xs.length,mx=xs.reduce((a,b)=>a+b,0)/n,my=ys.reduce((a,b)=>a+b,0)/n;let sxy=0,sx=0,sy=0;for(let i=0;i<n;i++){sxy+=(xs[i]-mx)*(ys[i]-my);sx+=(xs[i]-mx)**2;sy+=(ys[i]-my)**2}return sxy/Math.sqrt(sx*sy)}
function fit(xs,ys){const n=xs.length,mx=xs.reduce((a,b)=>a+b,0)/n,my=ys.reduce((a,b)=>a+b,0)/n;let a=0,b=0;for(let i=0;i<n;i++){a+=(xs[i]-mx)*(ys[i]-my);b+=(xs[i]-mx)**2}a/=b;return [a,my-a*mx]}
function buildAnalysis(){
  const R=W.map(w=>{const p=w.pop['2025'],pop=popTot(w,'2025');return {n:w.name,pop,d:w.disp24,ag:agingRate(w,'2025'),pc:w.disp24/pop*1000,pd:pop/w.area,dd:w.disp24/w.area,sh:AGES.map(a=>p[a]/pop),dn:w.dn}});
  const P=cityPop('2025'),T=cityTotal('2025'),cpc=T/P*1000,cpd=P/AREA_CITY,cdd=T/AREA_CITY;
  // A: age composition + dispatches
  {const rows=[...R].sort((a,b)=>b.ag-a.ag),rh=24;let g='';rows.forEach((r,i)=>{const y=8+i*rh;let x=70;g+=`<text x="64" y="${y+16}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${r.n}</text>`;r.sh.forEach((v,k)=>{const w=v*300;g+=`<rect x="${x}" y="${y+3}" width="${w}" height="18" fill="${ACOL[AGES[k]]}"/>`;x+=w});g+=`<text x="374" y="${y+16}" font-size="10.5" fill="#5b6b82">${r.ag.toFixed(0)}%</text>`;const bw=r.d/21000*150;g+=`<rect x="404" y="${y+5}" width="${bw}" height="14" fill="#14213d" rx="2"/><text x="${408+bw}" y="${y+16}" font-size="10.5" fill="#14213d" font-family="Manrope" font-weight="700">${fmt(r.d)}</text>`;g+=`<text x="596" y="${y+16}" font-size="10.5" fill="${r.pc>cpc*1.15?'#e63946':r.pc<cpc*0.85?'#1b998b':'#5b6b82'}" font-family="Manrope" font-weight="700" text-anchor="end">${r.pc.toFixed(0)}</text>`});
   g+=`<text x="70" y="${8+rows.length*rh+14}" font-size="10.5" fill="#8e9bae">年齢構成（%）　　　　　　　　　　　　　　高齢化率　出場件数（2024）　　　　　　　　　1,000人あたり</text>`;document.getElementById('anA').innerHTML=g}
  // B: pop vs disp scatter
  {const X=v=>50+(v/400000)*530,Y=v=>340-(v/22000)*310;let g=`<g stroke="#e3e8ef">${[5000,10000,15000,20000].map(v=>`<line x1="50" x2="580" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}${[100000,200000,300000].map(v=>`<line x1="${X(v)}" x2="${X(v)}" y1="30" y2="340"/>`).join('')}</g>`;
   g+=[5000,10000,15000,20000].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v/10000}万</text>`).join('')+[100000,200000,300000].map(v=>`<text x="${X(v)}" y="356" font-size="10.5" fill="#8e9bae" text-anchor="middle">${v/10000}万人</text>`).join('');
   g+=`<line x1="${X(0)}" y1="${Y(0)}" x2="${X(380000)}" y2="${Y(380000*cpc/1000)}" stroke="#8e9bae" stroke-dasharray="4 4"/><text x="${X(380000)-4}" y="${Y(380000*cpc/1000)-6}" font-size="10" fill="#8e9bae" text-anchor="end">市平均 ${cpc.toFixed(0)}件/千人</text>`;
   R.forEach(r=>{const k=r.pc/cpc,c=k>=1.15?'#e63946':k<=0.85?'#1b998b':'#3a7bd5';g+=`<circle cx="${X(r.pop)}" cy="${Y(r.d)}" r="6" fill="${c}" opacity=".8"/><text x="${X(r.pop)+8}" y="${Y(r.d)+4}" font-size="11" font-weight="700" fill="#14213d">${r.n}${k>=1.15||k<=0.85?' ×'+k.toFixed(2):''}</text>`});
   g+=`<text x="580" y="372" font-size="10.5" fill="#5b6b82" text-anchor="end">横軸＝人口（2025）、縦軸＝出場件数（2024）。赤＝比例線の1.15倍以上、緑＝0.85倍以下</text>`;document.getElementById('anB').innerHTML=g;document.getElementById('anBr').textContent=corr(R.map(r=>r.pop),R.map(r=>r.d)).toFixed(2)}
  // C: index bars
  {const rows=[...R].sort((a,b)=>b.dd/cdd-a.dd/cdd),rh=27,X=v=>80+Math.min(v,280)/280*500;let g=`<line x1="${X(100)}" x2="${X(100)}" y1="4" y2="${rows.length*rh+8}" stroke="#14213d" stroke-dasharray="3 3"/><text x="${X(100)}" y="${rows.length*rh+22}" font-size="10.5" fill="#14213d" text-anchor="middle">市平均＝100</text>`;
   [50,150,200,250].forEach(v=>g+=`<text x="${X(v)}" y="${rows.length*rh+22}" font-size="10" fill="#8e9bae" text-anchor="middle">${v}</text>`);
   rows.forEach((r,i)=>{const y=6+i*rh;g+=`<text x="74" y="${y+15}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${r.n}</text>`;[[r.pd/cpd*100,'#8fd0c3'],[r.dd/cdd*100,'#3a7bd5'],[r.pc/cpc*100,'#e63946']].forEach(([v,c],k)=>{g+=`<rect x="80" y="${y+k*7}" width="${X(v)-80}" height="6" fill="${c}" rx="1"/><text x="${X(v)+3}" y="${y+k*7+6}" font-size="8.5" fill="${c}" font-family="Manrope" font-weight="700">${v.toFixed(0)}</text>`})});
   document.getElementById('anC').innerHTML=g;document.getElementById('anCr').textContent=corr(R.map(r=>r.pd),R.map(r=>r.dd)).toFixed(2);document.getElementById('anCr2').textContent=corr(R.map(r=>r.pd),R.map(r=>r.pc)).toFixed(2)}
  // D: aging vs percap
  {const X=v=>50+(v-17)/(34-17)*530,Y=v=>340-(v-40)/(130-40)*310;let g=`<g stroke="#e3e8ef">${[50,75,100,125].map(v=>`<line x1="50" x2="580" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}${[20,25,30].map(v=>`<line x1="${X(v)}" x2="${X(v)}" y1="30" y2="340"/>`).join('')}</g>`;
   g+=[50,75,100,125].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v}</text>`).join('')+[20,25,30].map(v=>`<text x="${X(v)}" y="356" font-size="10.5" fill="#8e9bae" text-anchor="middle">${v}%</text>`).join('');
   const sub=R.filter(r=>r.n!=='中'&&r.n!=='西'),[a,b]=fit(sub.map(r=>r.ag),sub.map(r=>r.pc));
   g+=`<line x1="${X(19)}" y1="${Y(a*19+b)}" x2="${X(32)}" y2="${Y(a*32+b)}" stroke="#14213d" stroke-dasharray="5 4" stroke-width="1.5"/>`;
   R.forEach(r=>{const core=r.n==='中'||r.n==='西';g+=`<circle cx="${X(r.ag)}" cy="${Y(r.pc)}" r="6" fill="${core?'#e63946':'#3a7bd5'}" opacity=".8"/><text x="${X(r.ag)+8}" y="${Y(r.pc)+4}" font-size="11" font-weight="700" fill="#14213d">${r.n}</text>`});
   g+=`<text x="580" y="372" font-size="10.5" fill="#5b6b82" text-anchor="end">横軸＝高齢化率（2025）、縦軸＝住民1,000人あたり出場件数（2024）。点線＝中・西を除く16区の回帰線</text>`;document.getElementById('anD').innerHTML=g;
   document.getElementById('anDr').textContent=corr(R.map(r=>r.ag),R.map(r=>r.pc)).toFixed(2);document.getElementById('anDr2').textContent=corr(sub.map(r=>r.ag),sub.map(r=>r.pc)).toFixed(2);document.getElementById('anDslope').textContent=a.toFixed(1)}
}
buildAnalysis();

/* ---------- ward profiles ---------- */""")
# slide: add key insight slide after 'density' slide
rep("  ()=>`<div class=\"kick\">不搬送</div><h2>出場の19%は搬送に至らない</h2>",
"""  ()=>`<div class="kick">2025年の断面</div><h2>郊外の需要は年齢で決まり、都心の需要は人の出入りで決まる</h2><div class="cols two"><div><svg class="chart" id="slAnD" viewBox="0 0 600 380"></svg></div><div>${pt('0.74','中・西を除く16区での、高齢化率と1,000人あたり出場の相関。18区全体では−0.01')}${pt('0.76','昼夜間人口比率と1,000人あたり出場の相関。都心の需要は来街者で決まる',1)}<p class="m" style="margin-top:12px">推計モデルを「年齢別搬送率 × 区ごとの校正係数」の2段にしているのは、この2つの要因を分けるため。</p></div></div>`,
  ()=>`<div class="kick">不搬送</div><h2>出場の19%は搬送に至らない</h2>""")
rep("scatterChart('slScatter');","scatterChart('slScatter');document.getElementById('slAnD').innerHTML=document.getElementById('anD').innerHTML;")
P.write_text(s,encoding='utf-8'); print('patched',len(s))
