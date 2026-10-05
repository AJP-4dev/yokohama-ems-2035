import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# ---- consistency fixes ----
rep('推計の3本線は「人口だけ」「傾向が半分続く」「傾向が全部続く」の幅で、2035年の27.6〜32.6万件はその範囲。','推計の4本線は「人口の変化だけ」「利用増が半分続く」「利用増が全部続く」「年代別の実測トレンド」の幅で、2035年の27.6〜33.6万件はその範囲。')
rep('需要の増加はさらに続きます（2040年 A 約27.9万件）。','需要の増加はさらに続きます（2040年は人口変化のみで約27.9万件）。')
rep('利用率も上昇する場合は2040年までに金沢・栄・泉・緑・西も加わります。','「利用増が続く」シナリオでは2040年までに金沢・栄・泉・緑・西も加わります。')
rep('2035年の市全体は<span class="num" id="insT35"></span>件と利用増が続く（32.6万件）をやや上回ります。','2035年の市全体は<span class="num" id="insT35"></span>件で、「利用増が続く」（32.6万件）をやや上回ります。')
rep('<li><b>出場件数/千人</b>：出場件数 ÷ 区の人口 × 1,000。<b>件/km²</b>：出場件数 ÷ 区の面積（国土地理院 面積調、港湾・水面を含む）。</li>','<li><b>出場件数/千人</b>：出場件数 ÷ 区の人口 × 1,000（住民1,000人あたりの年間件数）。<b>出場件数/km²</b>：出場件数 ÷ 区の面積（国土地理院 面積調、港湾・水面を含む）。</li>')
rep('市全体では1隊あたり年3,000件（2024年）で、本レポートではこれを目安の線にしています。','市の年報では年間平均85.5隊で1隊あたり年3,000件（2024年）。本サイトは2024年末の87隊で割るため市全体は2,948件になりますが、目安の線は年報の3,000件に合わせています。')
rep('2013→2019年の1人あたり出場件数の伸び（年+3.1%）から高齢化の寄与を除いた残差がそのまま続く仮定。2019→2024年も同程度の伸びでしたが、2023→2024年は+0.7%に減速しており、長期の複利としては上振れ側です。','年齢構成を固定した搬送率の実測の伸び（2013〜2024年で年+1.45%、下記）がそのまま続く仮定。2023→2024年は出場の伸びが+0.7%に減速しており、長期の複利としては上振れ側です。')
rep('<li>人口の将来値は市の推計（中位）に依存します。前提が変われば区別の値は変わります。</li>','<li>人口の将来値は市の推計（中位）に依存します。市推計の前提条件（出生・死亡・転入出）が変われば区別の値は変わります。</li>')
rep('作成：2026年10月（v3）。','作成：2026年10月（v6）。')
rep('<li>85歳以上の搬送が増加分の中心。高齢者施設との事前連携','<li>85歳以上の搬送が増加分の中心（人数の増加による。1人あたりの利用は増えていない）。高齢者施設との事前連携')
rep('<p class="lead">3つの結論。人口は減っても出場は増える、主役は85歳以上、需要の重心は北部へ。各項目の「地図で」ボタンで、その条件の地図に飛べます。</p>','<p class="lead">3つの結論。人口は減っても出場は増える、主役は85歳以上、需要の重心は北部へ。6以降は隊の負担・2040年・密度と到着時間・不搬送・2025年の断面・搬送率の推移・補足グラフ・施策です。各項目の「地図で」ボタンで、その条件の地図に飛べます。</p>')
# ---- supplementary charts section ----
rep('<h3>12. 施策への示唆</h3>',
'''<h3>12. 補足グラフ — 推移と構成を一覧で</h3>
  <p>ここまでの本文で触れなかった切り口を、同じデータからまとめて描きます。</p>
  <div class="card"><h4>市全体の人口の推移 2025→2040（年齢5区分、市推計・中位）</h4><svg class="chart" id="sgPop" viewBox="0 0 600 280"></svg><div class="lg"><span><b class="c-c"></b>0–14</span><span><b class="c-w"></b>15–64</span><span><b class="c-e1"></b>65–74</span><span><b class="c-e2"></b>75–84</span><span><b class="c-e3"></b>85+</span></div><div class="ins">総人口は377万→361万人と4%減るが、85歳以上（紫）は19万→27万人、65–74歳（橙）は40万→57万人に増える。減るのは15–64歳（239万→204万人、−15%）と0–14歳。2035年に団塊世代が全員85歳を超え、2040年に団塊ジュニアが65歳に入る、という2つの波がこの15年に重なる。</div></div>
  <div class="card"><h4>区別の出場件数の推移 2025→2040（人口変化のみ）</h4><svg class="chart" id="sgWardDisp" viewBox="0 0 600 420"></svg><div class="ins">18本の線はほぼ全て右上がりだが、傾きが違う。港北（2万→2.4万件）と鶴見・戸塚が上位を保ち、都筑・青葉は傾きが急。栄・瀬谷・旭は2035年以降ほぼ横ばいか減少に転じる。線が交差する箇所（例: 2030年前後に青葉が旭を抜く）が、配置の優先順位が入れ替わる時期。</div></div>
  <div class="card"><h4>区別の人口の推移 2025→2040（2025年＝100）</h4><svg class="chart" id="sgWardPop" viewBox="0 0 600 420"></svg><div class="ins">西（+20%）だけが突出して増え、鶴見・神奈川・中・港北が微増。栄・金沢・瀬谷・泉・旭は2040年に85〜88まで下がる。出場件数の推移（上の図）と見比べると、人口が最も減る区でも出場はほぼ減らない、という非対称がはっきりする。</div></div>
  <div class="card"><h4>区別の85歳以上人口の推移 2025→2040（2025年＝100）</h4><svg class="chart" id="sgWardE3" viewBox="0 0 600 420"></svg><div class="ins">青葉・都筑・金沢・緑・戸塚は2035年に150〜160まで上がり、2040年にかけて頭打ちになる。瀬谷・旭・保土ケ谷は130前後。85歳以上の伸びが大きい区ほど出場の伸びも大きく、この図が区別推計の「主因」をそのまま示している。</div></div>
  <div class="card"><h4>区別の出場件数の内訳 — 搬送した出場と搬送に至らなかった出場（2024年、区内の救急隊の実績）</h4><svg class="chart" id="sgNonTr" viewBox="0 0 600 470"></svg><div class="lg"><span><b style="background:#14213d"></b>搬送した出場（搬送人員）</span><span><b style="background:#c9d2de"></b>不搬送</span></div><div class="ins">中区は出場1.95万件のうち7,300件が不搬送で、搬送に至った出場は1.2万件。搬送ベースで見ると中区は港北・鶴見・戸塚より少なく、「需要が市内最大の区」ではない。逆に戸塚・港南・旭は不搬送が少なく、出場のほぼ全てが搬送として病院まで続く。病院側の負荷を考えるなら、出場件数より紺の部分で比べるべき。</div></div>
  <div class="card"><h4>区別の出場の内訳 — 事故種別の構成（2024年）</h4><svg class="chart" id="sgType" viewBox="0 0 600 470"></svg><div class="lg"><span><b style="background:#3a7bd5"></b>急病</span><span><b style="background:#9ad0f5"></b>一般負傷</span><span><b style="background:#f4a259"></b>交通事故</span><span><b style="background:#8e3b8f"></b>転院搬送</span><span><b style="background:#c9d2de"></b>その他</span></div><div class="ins">急病が68〜74%でどの区も大半を占め、区の個性は残り3割に出る。転院（紫）は戸塚8%・港南7%、交通事故（橙）は都筑5.3%・鶴見4.5%・港北3.3%、一般負傷（水色）は中・西・金沢で2割近い。急病の割合が最も高いのは瀬谷・栄・南で、住民の急病だけで需要が決まる区。</div></div>
  <div class="card"><h4>区別の出場件数の年齢構成（2024年、実績ベース校正）</h4><svg class="chart" id="sgAge" viewBox="0 0 600 470"></svg><div class="lg"><span><b class="c-c"></b>0–14</span><span><b class="c-w"></b>15–64</span><span><b class="c-e1"></b>65–74</span><span><b class="c-e2"></b>75–84</span><span><b class="c-e3"></b>85+</span></div><div class="ins">85歳以上（紫）の割合は栄・金沢・旭・泉で27〜29%、都筑・港北・西では17〜19%。15–64歳（青）は逆に西・都筑・港北で4割近い。郊外では「高齢者の急病」、都心と北部では「現役世代の出場」が需要の中心で、同じ1件でも重症度と拘束時間が違う。年齢構成は市全体の搬送率を区の人口に掛けた推計値で、区別の年齢別実績ではない。</div></div>
  <div class="card"><h4>時間帯別の出場件数（市全体、2024年）</h4><svg class="chart" id="sgHour" viewBox="0 0 600 240"></svg><div class="ins">朝9〜10時台にピーク（1.5〜1.6万件/年）、深夜3〜4時台が底（4,800件）で3.3倍の差。昼65%・夜35%という本サイトの昼夜の分け方はこの分布から来ている。日勤救急隊（6隊、昼間のみ）は、このピークを平らにする配置。</div></div>
  <div class="card"><h4>1隊あたり年3,000件を超える年 — 区別・シナリオ別</h4><svg class="chart" id="sgOver" viewBox="0 0 600 470"></svg><div class="lg"><span><b style="background:#14213d"></b>人口変化のみ</span><span><b style="background:#f4a259"></b>緩やかな利用増</span><span><b style="background:#e63946"></b>利用増が続く</span><span><b style="background:#8e3b8f"></b>年代別トレンド</span></div><div class="ins">左端にある区はすでに超過。港北・都筑・鶴見はシナリオによって超える年が2026〜2034年と幅があり、ここが「利用増の抑制策が効くかどうか」で増隊時期が5年以上動く区。栄・泉・緑・西・金沢は人口変化のみなら2040年まで超えないが、利用増が続けば2029〜2037年に超える。</div></div>
  <h3>13. 施策への示唆</h3>''')
rep("/* ---------- transport-rate trend charts ---------- */",
"""/* ---------- supplementary charts (insight 12) ---------- */
function buildSupp(){
  const YR=YEARS, N=YR.length, Xy=(i,x0=50,x1=560)=>x0+i/(N-1)*(x1-x0);
  const yearTicks=(y,x0=50,x1=560)=>['2025','2030','2035','2040'].map(t=>`<text x="${Xy(YR.indexOf(t),x0,x1)}" y="${y}" font-size="10.5" fill="#8e9bae" text-anchor="middle">${t}</text>`).join('');
  // 1. city population stacked area
  {const Y=v=>250-(v/4000000)*220;let g=`<g stroke="#e3e8ef">${[1e6,2e6,3e6,4e6].map(v=>`<line x1="50" x2="560" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`+[1e6,2e6,3e6,4e6].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v/1e4}万</text>`).join('')+yearTicks(268);
   let base=YR.map(()=>0);AGES.forEach(a=>{const top=YR.map((y,i)=>base[i]+cityPop(y,a));g+=`<path d="M${YR.map((y,i)=>Xy(i)+','+Y(top[i])).join(' L')} L${YR.map((y,i)=>Xy(N-1-i)+','+Y(base[N-1-i])).join(' L')}Z" fill="${ACOL[a]}" opacity=".85"/>`;base=top});
   ['2025','2040'].forEach(y=>g+=`<text x="${Xy(YR.indexOf(y))}" y="${Y(cityPop(y))-6}" font-size="11" font-family="Manrope" font-weight="700" fill="#14213d" text-anchor="middle">${man(cityPop(y))}</text>`);
   document.getElementById('sgPop').innerHTML=g}
  // helper: multi-line chart
  function lines(id,valFn,lo,hi,fmtY,ticks,hl){const Y=v=>390-(v-lo)/(hi-lo)*360;let g=`<g stroke="#e3e8ef">${ticks.map(v=>`<line x1="50" x2="520" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`+ticks.map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${fmtY(v)}</text>`).join('')+yearTicks(410,50,520);
    const rows=W.map(w=>({w,v:YR.map(y=>valFn(w,y))})).sort((a,b)=>b.v[N-1]-a.v[N-1]);
    rows.forEach((r,k)=>{const t=wardType(r.w),col=TYPES[t][1];g+=`<polyline fill="none" stroke="${col}" stroke-width="1.8" opacity=".85" points="${r.v.map((v,i)=>Xy(i,50,520)+','+Y(v)).join(' ')}"/>`;const yy=Math.max(14,Math.min(398,Y(r.v[N-1])));g+=`<text x="524" y="${yy+4}" font-size="9.5" fill="${col}" font-weight="700">${r.w.name} ${fmtY(r.v[N-1])}</text>`});
    document.getElementById(id).innerHTML=g}
  lines('sgWardDisp',(w,y)=>w.disp[y],7000,25000,v=>v>=10000?(v/10000).toFixed(1)+'万':fmt(v),[8000,12000,16000,20000,24000]);
  lines('sgWardPop',(w,y)=>popTot(w,y)/popTot(w,'2025')*100,80,125,v=>v.toFixed(0),[80,90,100,110,120]);
  lines('sgWardE3',(w,y)=>w.pop[y].e3/w.pop['2025'].e3*100,95,170,v=>v.toFixed(0),[100,120,140,160]);
  // non-transport stacked bars
  {const rows=[...W].sort((a,b)=>b.unitDisp-a.unitDisp),rh=25,X=v=>80+v/21000*480;let g='';rows.forEach((w,i)=>{const y=6+i*rh;g+=`<text x="74" y="${y+14}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${w.name}</text><rect x="80" y="${y}" width="${X(w.unitTr)-80}" height="18" fill="#14213d"/><rect x="${X(w.unitTr)}" y="${y}" width="${X(w.unitDisp)-X(w.unitTr)}" height="18" fill="#c9d2de"/><text x="${X(w.unitDisp)+4}" y="${y+13}" font-size="10" font-family="Manrope" fill="#5b6b82">${fmt(w.unitDisp)}（不搬送${(w.nonTr*100).toFixed(0)}%）</text>`});document.getElementById('sgNonTr').innerHTML=g}
  // type composition 100%
  {const TC=[['急病','#3a7bd5'],['一般負傷','#9ad0f5'],['交通事故','#f4a259'],['転院搬送','#8e3b8f']];const rows=[...W].sort((a,b)=>a.types['急病']/a.disp24-b.types['急病']/b.disp24),rh=25;let g='';rows.forEach((w,i)=>{const y=6+i*rh;let x=80;g+=`<text x="74" y="${y+14}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${w.name}</text>`;let rest=w.disp24;TC.forEach(([k,c])=>{const wd=w.types[k]/w.disp24*480;rest-=w.types[k];g+=`<rect x="${x}" y="${y}" width="${wd}" height="18" fill="${c}"/>`;if(wd>28)g+=`<text x="${x+wd/2}" y="${y+13}" font-size="9.5" fill="#fff" font-weight="700" text-anchor="middle">${(w.types[k]/w.disp24*100).toFixed(0)}%</text>`;x+=wd});g+=`<rect x="${x}" y="${y}" width="${rest/w.disp24*480}" height="18" fill="#c9d2de"/>`});document.getElementById('sgType').innerHTML=g}
  // age composition of dispatches 100%
  {const rows=[...W].map(w=>({w,a:byAgeA(w)})).sort((p,q)=>q.a.e3/q.w.disp24-p.a.e3/p.w.disp24),rh=25;let g='';rows.forEach(({w,a},i)=>{const y=6+i*rh;let x=80;const tot=AGES.reduce((s,k)=>s+a[k],0);g+=`<text x="74" y="${y+14}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${w.name}</text>`;AGES.forEach(k=>{const wd=a[k]/tot*480;g+=`<rect x="${x}" y="${y}" width="${wd}" height="18" fill="${ACOL[k]}"/>`;if(wd>30)g+=`<text x="${x+wd/2}" y="${y+13}" font-size="9.5" fill="#fff" font-weight="700" text-anchor="middle">${(a[k]/tot*100).toFixed(0)}%</text>`;x+=wd})});document.getElementById('sgAge').innerHTML=g}
  // hourly
  {const H=DATA.hourly,mx=17000,X=i=>50+i*21,Y=v=>200-(v/mx)*170;let g=`<g stroke="#e3e8ef">${[5000,10000,15000].map(v=>`<line x1="50" x2="560" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`+[5000,10000,15000].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v/10000}万</text>`).join('');
   H.forEach((v,i)=>{const day=i>=8&&i<=19;g+=`<rect x="${X(i)}" y="${Y(v)}" width="17" height="${200-Y(v)}" fill="${day?'#f4a259':'#14213d'}" rx="2"/>`;if(i%3===0)g+=`<text x="${X(i)+8}" y="216" font-size="10" fill="#8e9bae" text-anchor="middle">${i}時</text>`});
   g+=`<text x="560" y="232" font-size="10.5" fill="#5b6b82" text-anchor="end">橙＝昼（8〜19時台）、紺＝夜</text>`;document.getElementById('sgHour').innerHTML=g}
  // over-year timeline
  {const rows=[...W].map(w=>({w,o:{A:overYear(w,'A'),M:overYear(w,'M'),B:overYear(w,'B'),T:overYear(w,'T')}})).sort((p,q)=>{const k=o=>o===null?2041:o;return k(p.o.A)-k(q.o.A)||k(p.o.B)-k(q.o.B)}),rh=25,X=y=>80+(y-2025)/16*480,COL={A:'#14213d',M:'#f4a259',B:'#e63946',T:'#8e3b8f'};
   let g=`<g stroke="#e3e8ef">${[2025,2030,2035,2040].map(y=>`<line x1="${X(y)}" x2="${X(y)}" y1="4" y2="${rows.length*rh+6}"/>`).join('')}</g>`+[2025,2030,2035,2040].map(y=>`<text x="${X(y)}" y="${rows.length*rh+20}" font-size="10.5" fill="#8e9bae" text-anchor="middle">${y}</text>`).join('');
   rows.forEach(({w,o},i)=>{const y=6+i*rh;g+=`<text x="74" y="${y+14}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${w.name}</text><line x1="80" x2="560" y1="${y+9}" y2="${y+9}" stroke="#eef1f5" stroke-width="10"/>`;['T','B','M','A'].forEach(k=>{if(o[k]!==null)g+=`<circle cx="${X(o[k])}" cy="${y+9}" r="${k==='A'?6:4.5}" fill="${COL[k]}" opacity=".9"/>`});if(o.A===null&&o.B===null&&o.T===null)g+=`<text x="564" y="${y+13}" font-size="9.5" fill="#8e9bae">2040年まで超えない</text>`});
   document.getElementById('sgOver').innerHTML=g}
}
function byAgeA(w){const o={};AGES.forEach(a=>o[a]=w.byAge['2025'][a]);return o}
buildSupp();

/* ---------- transport-rate trend charts ---------- */""")
P.write_text(s,encoding='utf-8'); print('patched',len(s))
