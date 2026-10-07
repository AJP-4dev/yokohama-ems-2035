import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,n,a[:80]); s=s.replace(a,b)
# --- year controls ---
rep('<input type="range" id="yearRange" min="2025" max="2040" step="1"','<input type="range" id="yearRange" min="2025" max="2070" step="1"')
rep('<button data-y="2040" aria-pressed="false">2040</button></div>','<button data-y="2040" aria-pressed="false">2040</button><button data-y="2050" aria-pressed="false">2050</button><button data-y="2060" aria-pressed="false">2060</button><button data-y="2070" aria-pressed="false">2070</button></div>')
rep('<div class="mt" id="miniT">推移 2025→2040</div>','<div class="mt" id="miniT">推移 2025→2070</div>')
rep("setYear(Math.max(2025,Math.min(2040,+h.get('y'))))","setYear(Math.max(2025,Math.min(2070,+h.get('y'))))",2)
# --- scenario multipliers: hold utilisation flat after 2040 ---
rep("const scMulOf=(sc,y)=>{sc=sc||state.sc;if(sc==='T'){const w0=W[0];return 1}return Math.pow(1+SCR[sc],(+y-2024))};\nconst tMulG=(g,y)=>Math.pow(1+TG[g],(+y-2024));",
    "const CAPY=2040;/* 利用増シナリオは2040年以降、搬送率を一定に保つ（複利を止める） */\nconst scMulOf=(sc,y)=>{sc=sc||state.sc;if(sc==='T')return 1;return Math.pow(1+SCR[sc],Math.min(+y,CAPY)-2024)};\nconst tMulG=(g,y)=>Math.pow(1+TG[g],Math.min(+y,CAPY)-2024);")
rep("const overYear=(w,sc,th=3000)=>{for(let y=2025;y<=2040;y++)","const overYear=(w,sc,th=3000)=>{for(let y=2025;y<=2070;y++)")
rep("'2040年まで超えない'","'2070年まで超えない'",2)
rep('>2040年まで超えない</text>','>2070年まで超えない</text>')
rep("—は2040年まで超えない","—は2070年まで超えない")
rep("const YEARS=[];for(let y=2025;y<=2040;y++)YEARS.push(String(y));","const YEARS=[];for(let y=2025;y<=2070;y++)YEARS.push(String(y));\nconst cityOf=(y,sc)=>W.reduce((s,w)=>s+annualOf(w,String(y),sc),0);\nconst PEAK_E3=(()=>{let b='2025';YEARS.forEach(y=>{if(cityPop(y,'e3')>cityPop(b,'e3'))b=y});return b})();")
rep("g+=['2025','2030','2035','2040'].map(y=>`<text x=\"${X(YEARS.indexOf(y))}\" y=\"${H-4}\"","g+=['2025','2040','2055','2070'].map(y=>`<text x=\"${X(YEARS.indexOf(y))}\" y=\"${H-4}\"")
rep("${isDiff()?'の増減率':''} 2025→2040${showB","${isDiff()?'の増減率':''} 2025→2070${showB")
# --- trend chart to 2070 ---
rep("""    const B40=A40*Math.pow(1.015,16),s=DATA.series,projA=[[2024,T24],[2030,A30],[2035,A35],[2040,A40]],projB=[[2024,T24],[2030,A30*Math.pow(1.015,6)],[2035,B35],[2040,B40]],projM=[[2024,T24],[2030,M30],[2035,M35],[2040,M40]],projT=[[2024,T24],[2030,T30],[2035,T35],[2040,T40]];
    const X=x=>44+(x-1985)/(2040-1985)*540,Y=v=>h-36-(v/360000)*(h-60);
    let g=`<g stroke="#e3e8ef">${[100000,200000,300000].map(v=>`<line x1="44" x2="584" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`;
    g+=[100000,200000,300000].map(v=>`<text x="40" y="${Y(v)+4}" fill="#8e9bae" font-size="11" text-anchor="end">${v/10000}万</text>`).join('');
    g+=[1985,1995,2005,2015,2025,2035,2040].map(x=>""","""    const B40=A40*Math.pow(1.015,16),s=DATA.series,PY=[2030,2035,2040,2045,2050,2055,2060,2065,2070],pr=sc=>[[2024,T24]].concat(PY.map(y=>[y,cityOf(y,sc)])),projA=pr('A'),projB=pr('B'),projM=pr('M'),projT=pr('T');
    const X=x=>44+(x-1985)/(2070-1985)*540,Y=v=>h-36-(v/400000)*(h-60);
    let g=`<g stroke="#e3e8ef">${[100000,200000,300000,400000].map(v=>`<line x1="44" x2="584" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`;
    g+=[100000,200000,300000,400000].map(v=>`<text x="40" y="${Y(v)+4}" fill="#8e9bae" font-size="11" text-anchor="end">${v/10000}万</text>`).join('');
    g+=`<line x1="${X(+PEAK_E3)}" x2="${X(+PEAK_E3)}" y1="${Y(400000)}" y2="${h-36}" stroke="#8e3b8f" stroke-dasharray="3 3" opacity=".6"/><text x="${X(+PEAK_E3)-4}" y="${Y(400000)+12}" fill="#8e3b8f" font-size="10.5" text-anchor="end">${PEAK_E3} 85歳以上ピーク</text>`;
    g+=[1985,2000,2015,2030,2045,2060,2070].map(x=>""")
rep("""    g+=`<text x="${X(2035)}" y="${Y(A35)+18}" fill="#14213d" font-size="12" font-weight="700" text-anchor="end">人口変化のみ ${fmt(A35)}</text><text x="${X(2035)}" y="${Y(B35)-8}" fill="#e63946" font-size="12" font-weight="700" text-anchor="end">利用増が続く ${fmt(B35)}</text><text x="${X(2033)}" y="${Y(M35)+14}" fill="#f4a259" font-size="11" font-weight="700" text-anchor="end">緩やかな利用増 ${fmt(M35)}</text><text x="${X(2040)}" y="${Y(A40)+18}" fill="#14213d" font-size="11" text-anchor="end">${fmt(A40)}</text><text x="${X(2040)}" y="${Y(B40)-8}" fill="#e63946" font-size="11" text-anchor="end">${fmt(B40)}</text>`;""",
"""    const pk=+PEAK_E3,Apk=cityOf(pk,'A'),Bpk=cityOf(pk,'B'),Mpk=cityOf(pk,'M');
    g+=`<text x="${X(2035)}" y="${Y(A35)+18}" fill="#14213d" font-size="12" font-weight="700" text-anchor="end">人口変化のみ ${fmt(A35)}</text><text x="${X(2035)}" y="${Y(B35)-8}" fill="#e63946" font-size="12" font-weight="700" text-anchor="end">利用増が続く ${fmt(B35)}</text><text x="${X(2033)}" y="${Y(M35)+14}" fill="#f4a259" font-size="11" font-weight="700" text-anchor="end">緩やかな利用増 ${fmt(M35)}</text><text x="${X(pk)+5}" y="${Y(Apk)+16}" fill="#14213d" font-size="11" font-weight="700">${pk}年 ${fmt(Apk)}</text><text x="${X(pk)+5}" y="${Y(Bpk)-8}" fill="#e63946" font-size="11" font-weight="700">${fmt(Bpk)}</text>`;""")
rep("点線＝本レポートの推計（2030・2035・2040）。","点線＝本レポートの推計（2030〜2070年、5年ごと）。利用増の3シナリオは2040年以降、搬送率の上昇を止めて一定とする。紫の縦線＝85歳以上人口のピーク年。")
rep("<h2>1985年から2035年まで</h2>","<h2>1985年から2070年まで</h2>")
rep("<b>2040年までに超える区（人口の変化だけ）</b>","<b>2070年までに超える区（人口の変化だけ）</b>")
# --- supplementary charts ---
rep("const yearTicks=(y,x0=50,x1=560)=>['2025','2030','2035','2040'].map(","const yearTicks=(y,x0=50,x1=560)=>['2025','2040','2055','2070'].map(")
rep("['2025','2040'].forEach(y=>g+=`<text x=\"${Xy(YR.indexOf(y))}\" y=\"${Y(cityPop(y))-6}\"","['2025','2040','2070'].forEach(y=>g+=`<text x=\"${Xy(YR.indexOf(y))}\" y=\"${Y(cityPop(y))-6}\"")
rep("lines('sgWardDisp',(w,y)=>w.disp[y],7000,25000,v=>v>=10000?(v/10000).toFixed(1)+'万':fmt(v),[8000,12000,16000,20000,24000]);\n  lines('sgWardPop',(w,y)=>popTot(w,y)/popTot(w,'2025')*100,80,125,v=>v.toFixed(0),[80,90,100,110,120]);\n  lines('sgWardE3',(w,y)=>w.pop[y].e3/w.pop['2025'].e3*100,95,170,v=>v.toFixed(0),[100,120,140,160]);",
    "lines('sgWardDisp',(w,y)=>w.disp[y],5000,29000,v=>v>=10000?(v/10000).toFixed(1)+'万':fmt(v),[5000,10000,15000,20000,25000]);\n  lines('sgWardPop',(w,y)=>popTot(w,y)/popTot(w,'2025')*100,45,165,v=>v.toFixed(0),[50,75,100,125,150]);\n  lines('sgWardE3',(w,y)=>w.pop[y].e3/w.pop['2025'].e3*100,90,335,v=>v.toFixed(0),[100,150,200,250,300]);")
rep("const k=o=>o===null?2041:o;return k(p.o.A)-k(q.o.A)||k(p.o.B)-k(q.o.B)}),rh=25,X=y=>80+(y-2025)/16*480,","const k=o=>o===null?2071:o;return k(p.o.A)-k(q.o.A)||k(p.o.B)-k(q.o.B)}),rh=25,X=y=>80+(y-2025)/45*480,")
rep("let g=`<g stroke=\"#e3e8ef\">${[2025,2030,2035,2040].map(y=>`<line x1=\"${X(y)}\" x2=\"${X(y)}\" y1=\"4\" y2=\"${rows.length*rh+6}\"/>`).join('')}</g>`+[2025,2030,2035,2040].map(",
    "let g=`<g stroke=\"#e3e8ef\">${[2025,2030,2040,2050,2060,2070].map(y=>`<line x1=\"${X(y)}\" x2=\"${X(y)}\" y1=\"4\" y2=\"${rows.length*rh+6}\"/>`).join('')}</g>`+[2025,2030,2040,2050,2060,2070].map(")
rep('<h4>市全体の人口の推移 2025→2040（年齢5区分、市推計・中位）</h4>','<h4>市全体の人口の推移 2025→2070（年齢5区分、市推計・中位）</h4>')
rep('という2つの波がこの15年に重なる。</div></div>','という2つの波がこの15年に重なる。その先、85歳以上は2050年代に再び増えて2061年に38.6万人でピーク（2025年の2.1倍）、総人口は2070年に299万人まで減る。</div></div>')
rep('<h4>区別の出場件数の推移 2025→2040（人口変化のみ）</h4>','<h4>区別の出場件数の推移 2025→2070（人口変化のみ）</h4>')
rep('が、配置の優先順位が入れ替わる時期。</div></div>','が、配置の優先順位が入れ替わる時期。2040年以降は二極化が進み、西・鶴見・港北・神奈川は2060年代まで伸び続けて2070年に2025年比1.3〜1.7倍、金沢・栄・瀬谷・泉・港南・旭は2030年前後をピークに減少へ転じ、2070年には2025年の7〜8割になる。</div></div>')
rep('<h4>区別の人口の推移 2025→2040（2025年＝100）</h4>','<h4>区別の人口の推移 2025→2070（2025年＝100）</h4>')
rep('という非対称がはっきりする。</div></div>','という非対称がはっきりする。2070年には金沢・栄・瀬谷・泉が50前後（半減）、港南・旭が60、都筑・青葉も63〜65まで落ちる一方、西は161まで増え、鶴見・神奈川・港北・中はほぼ横ばい。</div></div>')
rep('<h4>区別の85歳以上人口の推移 2025→2040（2025年＝100）</h4>','<h4>区別の85歳以上人口の推移 2025→2070（2025年＝100）</h4>')
rep('この図が区別推計の「主因」をそのまま示している。</div></div>','この図が区別推計の「主因」をそのまま示している。2040年代にいったん横ばいになった後、団塊ジュニア世代が85歳に入る2050年代に第2の山が来る。ピークは全区とも2060〜2064年で、都筑326・西278・青葉275・中262・港北252と、若い郊外・都心ほど高い。栄・旭・瀬谷は155〜165で、すでに高齢化が進んだ区は山が低い。</div></div>')
# --- section 7: add peak paragraph + table ---
rep('<h3>7. 2040年に向けて</h3>','<h3>7. 2040年、そして85歳以上がピークを迎える2061年</h3>')
rep("""  <p><a class="mapgo" href="#" data-state="m=disp&y=2040">2040年の出場件数を地図で</a> <a class="mapgo" href="#" data-state="m=aging&y=2040">2040年の高齢化率を地図で</a></p>""",
"""  <p><a class="mapgo" href="#" data-state="m=disp&y=2040">2040年の出場件数を地図で</a> <a class="mapgo" href="#" data-state="m=aging&y=2040">2040年の高齢化率を地図で</a></p>
  <p>市の推計は2070年まであります。85歳以上は2040年代にいったん横ばいになった後、団塊ジュニア世代が85歳に入る2050年代に再び増え、<b>2061年に38.6万人（2025年の2.1倍）でピーク</b>を迎えます。出場件数（人口変化のみ）のピークは2058年の29.9万件で、2061年は29.8万件。総人口が321万人（−15%）まで減る中での数字です。2070年には85歳以上が34.8万人に減り、出場件数は27.8万件まで戻ります。</p>
  <div class="card"><h4>85歳以上のピークまでの出場件数（市全体、件/年）</h4><div class="tbl"><table id="tblPeak"></table></div><p class="m">利用増の3シナリオは2040年以降、搬送率の上昇を止めて一定にしています（45年間の複利は非現実的なため）。2050年以降の人口推計は市が参考値と位置づけているものです。</p><div class="ins">2035年から2061年までの26年で、人口変化のみの出場は27.6万→29.8万件（+8%）としか増えない。85歳以上が1.4倍になるのに出場が伸びないのは、15–64歳と65–84歳が大きく減るためで、2060年の横浜は「件数は横ばい、中身はほぼ高齢者」になる。2070年に向けては出場も減り始めるので、増隊のピークは2050年代後半、その後は配置の縮小と再編が課題になる。</div></div>
  <p><a class="mapgo" href="#" data-state="m=disp&y=2061">2061年の出場件数を地図で</a> <a class="mapgo" href="#" data-state="m=elder&v=diff&y=2061">2061年の高齢者人口の増減率を地図で</a> <a class="mapgo" href="#" data-state="m=disp&v=diff&y=2070">2070年の出場件数の増減率を地図で</a></p>""")
rep("function buildSupp(){","function buildPeak(){const ys=['2025','2035','2040','2050','2060',PEAK_E3,'2070'].filter((y,i,a)=>a.indexOf(y)===i).sort();const r=ys.map(y=>`<tr${y===PEAK_E3?' style=\"font-weight:700;background:#f3f0f7\"':''}><td>${y}${y===PEAK_E3?'（85歳以上ピーク）':''}</td><td>${man(cityPop(y))}</td><td>${man(cityPop(y,'e3'))}</td><td>${fmt(cityOf(y,'A'))}</td><td>${fmt(cityOf(y,'M'))}</td><td>${fmt(cityOf(y,'B'))}</td><td>${fmt(cityOf(y,'T'))}</td></tr>`).join('');document.getElementById('tblPeak').innerHTML=`<tr><th>年</th><th>総人口</th><th>85歳以上</th><th>人口変化のみ</th><th>緩やかな利用増</th><th>利用増が続く</th><th>年代別トレンド</th></tr>${r}`}\nfunction buildSupp(){buildPeak();")
# --- method page notes ---
rep("率が年+1.5%ずつ上がる（2035年に+18%）。2013〜2024年の傾向（年齢構成固定で年+1.45%）がそのまま続く仮定。<br>","率が年+1.5%ずつ上がる（2035年に+18%）。2013〜2024年の傾向（年齢構成固定で年+1.45%）がそのまま続く仮定。<br>利用増の3シナリオは2040年以降、率の上昇を止めて一定にします。<br>")
rep("昼夜間比だけは年で変わりません。'","2070年まで動かせますが、2050年以降の人口推計は市が参考値としているもので、搬送率も2024年のままという強い仮定になります。昼夜間比だけは年で変わりません。'")
rep("0–14歳の年+6.2%を2040年まで延ばすと搬送率は2.6倍になるため、長期の値は上振れしやすい点に注意してください。</p>","0–14歳の年+6.2%を2040年まで延ばすと搬送率は2.6倍になるため、長期の値は上振れしやすい点に注意してください。</p>\n  <p><b>2040年以降の扱い</b>：地図・推移グラフは2070年まで表示できますが、「緩やかな利用増」「利用増が続く」「年代別トレンド」の搬送率の上昇は2040年で止め、以降は一定とします。45年間の複利（年+1.5%で2.0倍、0–14歳の+6.2%で16倍）は現実的でないためです。人口は市の推計をそのまま使い、2050年以降は市が参考値と位置づけている点に留意してください。</p>")
P.write_text(s,encoding='utf-8'); print('patched v14')
