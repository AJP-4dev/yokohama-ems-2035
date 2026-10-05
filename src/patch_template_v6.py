import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)

# ===== 1. scenario generalization (A / M / B) =====
rep("const scMul=y=>state.sc==='B'?Math.pow(1.015,(+y-2024)):1;",
    "const SCR={A:0,M:0.0075,B:0.015}, SCN={A:'人口のみ',M:'中間シナリオ',B:'上限シナリオ'};\nconst scMulOf=(sc,y)=>Math.pow(1+SCR[sc||state.sc],(+y-2024));\nconst scMul=y=>scMulOf(state.sc,y);")
rep("const annualOf=(w,y,sc)=>{const m=(sc||state.sc)==='B'?Math.pow(1.015,(+y-2024)):1;return y==='2025'?w.disp24:w.disp[y]*m};",
    "const annualOf=(w,y,sc)=>{const m=scMulOf(sc,y);return y==='2025'?w.disp24:w.disp[y]*m};")
rep("const bandOf=(w,y,t,sc)=>{const a=annualOf(w,y,sc);if(t==='all')return a;const m=(sc||state.sc)==='B'?Math.pow(1.015,(+y-2024)):1;",
    "const bandOf=(w,y,t,sc)=>{const a=annualOf(w,y,sc);if(t==='all')return a;const m=scMulOf(sc,y);")
rep("const B35=W.reduce((s,w)=>s+w.disp['2035']*Math.pow(1.015,11),0),",
    "const B35=W.reduce((s,w)=>s+w.disp['2035']*Math.pow(1.015,11),0), M35=W.reduce((s,w)=>s+w.disp['2035']*Math.pow(1.0075,11),0), M30=W.reduce((s,w)=>s+w.disp['2030']*Math.pow(1.0075,6),0), M40=W.reduce((s,w)=>s+w.disp['2040']*Math.pow(1.0075,16),0),")
rep("if(['A','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v'))){state.view=h.get('v');pressSeg('viewSeg','v',state.view)}",
    "if(['A','M','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(['abs','diff'].includes(h.get('v'))){state.view=h.get('v');pressSeg('viewSeg','v',state.view)}")
rep("if(['A','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(h.get('m')==='diff')",
    "if(['A','M','B'].includes(h.get('s'))){state.sc=h.get('s');pressSeg('scSeg','s',state.sc)}if(['disp','pop','elder','aging','day'].includes(h.get('m'))){state.mode=h.get('m');pressSeg('modeSeg','m',state.mode)}if(h.get('m')==='diff')")
rep("const diffHi=()=>state.mode==='pop'?15:state.mode==='elder'?30:(state.sc==='B'&&state.year!=='2025'?40:15);",
    "const diffHi=()=>state.mode==='pop'?15:state.mode==='elder'?30:(state.year!=='2025'&&state.sc==='B'?40:state.year!=='2025'&&state.sc==='M'?25:15);")
rep("const scLabel=()=>state.sc==='B'?'利用率も上昇':'人口の変化だけ';","const scLabel=()=>SCN[state.sc];")
rep("const showB=state.mode==='disp';\n  const A=YEARS.map(y=>valueAt(ws,y,'A')),B=showB?YEARS.map(y=>valueAt(ws,y,'B')):null;\n  const all=B?A.concat(B):A;",
    "const showB=state.mode==='disp';\n  const A=YEARS.map(y=>valueAt(ws,y,'A')),B=showB?YEARS.map(y=>valueAt(ws,y,'B')):null,M=showB?YEARS.map(y=>valueAt(ws,y,'M')):null;\n  const all=B?A.concat(B):A;")
rep("const ci=YEARS.indexOf(state.year),cur=(state.sc==='B'&&B)?B:A;","const ci=YEARS.indexOf(state.year),cur=(state.sc==='B'&&B)?B:(state.sc==='M'&&M)?M:A;")
rep("  if(B)g+=`<polyline fill=\"none\" stroke=\"#e63946\" stroke-width=\"2\" stroke-dasharray=\"4 3\" points=\"${B.map((v,i)=>X(i)+','+Y(v)).join(' ')}\"/>`;\n  if(ci>=0){g+=`<line x1=\"${X(ci)}\" x2=\"${X(ci)}\" y1=\"${y0}\" y2=\"${y1}\" stroke=\"var(--ink3)\" stroke-width=\"1\"/><circle cx=\"${X(ci)}\" cy=\"${Y(cur[ci])}\" r=\"3.5\" fill=\"${state.sc==='B'&&B?'#e63946':'var(--navy)'}\"/>`;",
    "  if(M)g+=`<polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"2\" stroke-dasharray=\"4 3\" points=\"${M.map((v,i)=>X(i)+','+Y(v)).join(' ')}\"/>`;\n  if(B)g+=`<polyline fill=\"none\" stroke=\"#e63946\" stroke-width=\"2\" stroke-dasharray=\"4 3\" points=\"${B.map((v,i)=>X(i)+','+Y(v)).join(' ')}\"/>`;\n  if(ci>=0){g+=`<line x1=\"${X(ci)}\" x2=\"${X(ci)}\" y1=\"${y0}\" y2=\"${y1}\" stroke=\"var(--ink3)\" stroke-width=\"1\"/><circle cx=\"${X(ci)}\" cy=\"${Y(cur[ci])}\" r=\"3.5\" fill=\"${state.sc==='B'&&B?'#e63946':state.sc==='M'&&M?'#f4a259':'var(--navy)'}\"/>`;")
rep("T.textContent=`${name}・${lab}${isDiff()?'の増減率':''} 2025→2040${showB?'（紺A／赤B）':''}`;","T.textContent=`${name}・${lab}${isDiff()?'の増減率':''} 2025→2040${showB?'（紺＝人口のみ／橙＝中間／赤＝上限）':''}`;")
rep("`${w.name}区<span>${y==='2025'?'2024年実績':y+'年の推計'+(state.sc==='B'?'（利用率上昇込み）':'')}</span>`;","`${w.name}区<span>${y==='2025'?'2024年実績':y+'年の推計'+(state.sc==='A'?'':'（'+SCN[state.sc]+'）')}</span>`;")
rep("const oA=overYear(w,'A'),oB=overYear(w,'B'),ov=o=>o===null?'2040年まで超えない':o===2025?'<b>すでに超過</b>':'<b>'+o+'年</b>';document.getElementById('shUnit').innerHTML=`<b>救急隊</b> ${w.units}隊${w.unitsDay?'＋日勤'+w.unitsDay+'隊':''}（2024年末）。1隊あたり年3,000件の目安を超えるのは ${ov(oA)}（人口の変化だけ）／ ${ov(oB)}（利用率も上昇）。隊は区をまたいで出場するため目安です。`;",
    "const oA=overYear(w,'A'),oM=overYear(w,'M'),oB=overYear(w,'B'),ov=o=>o===null?'2040年まで超えない':o===2025?'<b>すでに超過</b>':'<b>'+o+'年</b>';document.getElementById('shUnit').innerHTML=`<b>救急隊</b> ${w.units}隊${w.unitsDay?'＋日勤'+w.unitsDay+'隊':''}（2024年末）。1隊あたり年3,000件の目安を超えるのは ${ov(oA)}（人口のみ）／ ${ov(oM)}（中間）／ ${ov(oB)}（上限）。隊は区をまたいで出場するため目安です。`;")
rep("document.getElementById('st2t').textContent=`同 ${y2}（推計${state.sc==='B'?'・利用率上昇込み':''}）`;","document.getElementById('st2t').textContent=`同 ${y2}（推計${state.sc==='A'?'':'・'+SCN[state.sc]}）`;")
rep("件（${state.sc==='B'?'利用率上昇込み':'人口の変化だけ'}）</text>`;","件（${SCN[state.sc]}）</text>`;")
# trend chart: add M
rep("const B40=A40*Math.pow(1.015,16),s=DATA.series,projA=[[2024,T24],[2030,A30],[2035,A35],[2040,A40]],projB=[[2024,T24],[2030,A30*Math.pow(1.015,6)],[2035,B35],[2040,B40]];",
    "const B40=A40*Math.pow(1.015,16),s=DATA.series,projA=[[2024,T24],[2030,A30],[2035,A35],[2040,A40]],projB=[[2024,T24],[2030,A30*Math.pow(1.015,6)],[2035,B35],[2040,B40]],projM=[[2024,T24],[2030,M30],[2035,M35],[2040,M40]];")
rep("    g+=`<polyline fill=\"none\" stroke=\"#e63946\" stroke-width=\"2.5\" stroke-dasharray=\"5 5\" points=\"${projB.map(p=>X(p[0])+','+Y(p[1])).join(' ')}\"/>`;",
    "    g+=`<polyline fill=\"none\" stroke=\"#f4a259\" stroke-width=\"2.5\" stroke-dasharray=\"5 5\" points=\"${projM.map(p=>X(p[0])+','+Y(p[1])).join(' ')}\"/>`;\n    g+=`<polyline fill=\"none\" stroke=\"#e63946\" stroke-width=\"2.5\" stroke-dasharray=\"5 5\" points=\"${projB.map(p=>X(p[0])+','+Y(p[1])).join(' ')}\"/>`;")
rep("<text x=\"${X(2035)}\" y=\"${Y(B35)-8}\" fill=\"#e63946\" font-size=\"12\" font-weight=\"700\" text-anchor=\"end\">B ${fmt(B35)}</text>",
    "<text x=\"${X(2035)}\" y=\"${Y(B35)-8}\" fill=\"#e63946\" font-size=\"12\" font-weight=\"700\" text-anchor=\"end\">上限 ${fmt(B35)}</text><text x=\"${X(2033)}\" y=\"${Y(M35)+14}\" fill=\"#f4a259\" font-size=\"11\" font-weight=\"700\" text-anchor=\"end\">中間 ${fmt(M35)}</text>")
rep("text-anchor=\"end\">A ${fmt(A35)}</text>","text-anchor=\"end\">人口のみ ${fmt(A35)}</text>")
# city page big numbers and table
rep('<div class="big"><div><div class="n num" id="cA">—</div><div class="l">2035年の出場件数（人口の変化だけ）</div></div><div><div class="n r num" id="cB">—</div><div class="l">同（1人あたり利用率が年+1.5%で上昇し続けた場合）</div></div></div>',
    '<div class="big"><div><div class="n num" id="cA">—</div><div class="l">2035年の出場件数（人口のみ＝搬送率を固定）</div></div><div><div class="n num" id="cM" style="color:#d9822b">—</div><div class="l">中間（搬送率が年+0.75%で上昇）</div></div><div><div class="n r num" id="cB">—</div><div class="l">上限（年+1.5%＝最近の傾向が続く）</div></div></div>')
rep("document.getElementById('cA').textContent=fmt(A35);document.getElementById('cB').textContent=fmt(B35);","document.getElementById('cA').textContent=fmt(A35);document.getElementById('cB').textContent=fmt(B35);document.getElementById('cM').textContent=fmt(M35);")
rep('<p class="m">実線＝実績（横浜市統計書・消防局）。点線＝本レポートの推計（2030・2035・2040）。A（紺）は人口の変化だけ、B（赤）は年齢別の利用率が年+1.5%で上がり続けた場合。2020–21年はコロナ禍の一時的な落ち込み。</p>',
    '<p class="m">実線＝実績（横浜市統計書・消防局）。点線＝本レポートの推計（2030・2035・2040）。紺＝人口のみ（搬送率を2024年で固定）、橙＝中間（搬送率が年+0.75%で上昇）、赤＝上限（年+1.5%、2013〜2024年の傾向がそのまま続く場合）。2020–21年はコロナ禍の一時的な落ち込み。</p>')
rep("<td>${fmt(w.disp['2035']*Math.pow(1.015,11))}</td><td>${unitsOf(w)}</td>","<td>${fmt(w.disp['2035']*Math.pow(1.0075,11))}</td><td>${fmt(w.disp['2035']*Math.pow(1.015,11))}</td><td>${unitsOf(w)}</td>")
rep("<th>出場2035 A</th><th>増減</th><th>2035 B</th><th>隊数</th><th>1隊あたり35 A</th><th>3,000超 A</th><th>3,000超 B</th>","<th>出場2035 人口のみ</th><th>増減</th><th>2035 中間</th><th>2035 上限</th><th>隊数</th><th>1隊あたり35</th><th>3,000超 人口のみ</th><th>3,000超 上限</th>")
# slides
rep("${pt(pct((A35/cityTotal('2025')-1)*100),'2035年の出場件数（人口の変化だけ）。市人口は−2.3%でも需要は増える',1)}","${pt(pct((A35/cityTotal('2025')-1)*100),'2035年の出場件数（人口のみ）。市人口は−2.3%でも需要は増える。搬送率の上昇が続けば+'+((M35/cityTotal('2025')-1)*100).toFixed(0)+'〜'+((B35/cityTotal('2025')-1)*100).toFixed(0)+'%',1)}")
rep("<p class=\"m\">実線＝実績、点線＝推計。A（紺）は人口の変化だけ、B（赤）は利用率が年+1.5%で上昇し続けた場合。</p>`,","<p class=\"m\">実線＝実績、点線＝推計。紺＝人口のみ（搬送率固定）、橙＝中間（搬送率 年+0.75%）、赤＝上限（年+1.5%、最近の傾向が続く場合）。</p>`,")
rep("<p style=\"margin-top:12px\"><b>利用率も上昇する場合</b></p><p class=\"m\">${soonB||'なし'}</p>","<p style=\"margin-top:12px\"><b>上限シナリオ（搬送率が年+1.5%で上昇）の場合</b></p><p class=\"m\">${soonB||'なし'}</p>")
# insight / method texts
rep("利用率の上昇傾向（2013→2019年に1人あたり年+3%、うち高齢化を除いた分が約+1.5%）が続けば、2035年は約32.6万件です。</p>",
    "搬送率（1人あたりの救急車利用）の上昇傾向が続けば、2035年は中間シナリオで約29.9万件、上限シナリオで約32.6万件です。</p>")
rep("<div class=\"callout\">救急隊数を2024年の85.5隊のままとすると、1隊あたりの年間出場件数は3,000件から約3,230件（A）〜3,810件（B）に増えます。</div>",
    "<div class=\"callout\">救急隊数を2024年の85.5隊のままとすると、1隊あたりの年間出場件数は3,000件から約3,230件（人口のみ）〜3,810件（上限）に増えます。</div>")
rep("出場件数は人口の変化だけで27.9万件（+8.9%）、利用率上昇込みでは35.4万件に達します。","出場件数は人口のみで27.9万件（+8.9%）、中間シナリオで31.5万件、上限シナリオで35.4万件に達します。上限の値は「最近15年の傾向が2040年まで複利で続く」仮定で、2040年時点では根拠が薄いことに注意してください。")
rep('<h3>2つのシナリオ</h3>\n  <p><b>A 人口の変化だけ</b>：搬送率を2024年水準で固定。<b>B 利用率も上昇</b>：全年齢の搬送率が年+1.5%で上昇し続ける（2013→2019年の1人あたり出場件数の伸び+3.1%/年から高齢化の寄与を除いた概算）。</p>',
'''<h3>3つのシナリオ（搬送率の前提）</h3>
  <p>「搬送率」は、年齢階級ごとに1年のうちに救急搬送される人の割合です（85歳以上なら25.7%）。人口推計に掛ける搬送率を将来どう置くかで3つのシナリオを用意しています。</p>
  <ul>
    <li><b>人口のみ</b>：搬送率を2024年の水準で固定。人口の増減と年齢構成の変化だけで件数が決まる、下限の推計。</li>
    <li><b>中間</b>：搬送率が全年齢で年+0.75%ずつ上昇（2035年に+8%、2040年に+13%）。上昇傾向が続くが、#7119 の普及や軽症者対策で半分に鈍る想定。</li>
    <li><b>上限</b>：搬送率が年+1.5%ずつ上昇（2035年に+18%、2040年に+27%）。2013→2019年の1人あたり出場件数の伸び（年+3.1%）から高齢化の寄与を除いた残差がそのまま続く仮定。2019→2024年も同程度の伸びでしたが、2023→2024年は+0.7%に減速しており、長期の複利としては上振れ側です。</li>
  </ul>
  <p class="m">上昇分の中身（独居高齢者の増加、軽症利用、転院搬送、病院の受入事情）は分解できていないため、中間と上限は「傾向が続いた場合」の幅として読んでください。</p>''')
rep('<li><b>前提A／B</b>：出場件数にだけ効きます。Aは搬送率を2024年で固定、Bは年+1.5%で上昇。</li>','<li><b>前提（人口のみ／中間／上限）</b>：出場件数にだけ効きます。搬送率を2024年で固定／年+0.75%で上昇／年+1.5%で上昇。</li>')

# ===== 2. control order + footnotes =====
old=s[s.index('    <div class="panel">'):s.index('    <div id="status">')]
new='''    <div class="panel">
      <div class="prow" id="rowMode"><span class="lbl">指標<button class="q" data-q="mode" aria-label="指標の説明">?</button></span><div class="seg" id="modeSeg"><button aria-pressed="true" data-m="disp">出場件数</button><button aria-pressed="false" data-m="pop">人口</button><button aria-pressed="false" data-m="elder">高齢者人口</button><button aria-pressed="false" data-m="aging">高齢化率</button><button aria-pressed="false" data-m="day">昼夜間比</button></div></div>
      <div class="prow" id="rowView"><span class="lbl">表示<button class="q" data-q="view" aria-label="表示の説明">?</button></span><div class="seg" id="viewSeg"><button aria-pressed="true" data-v="abs">実数</button><button aria-pressed="false" data-v="diff">2025年比の増減率</button></div><span class="tag">影響なし</span></div>
      <div class="prow" id="rowYear"><span class="lbl">年<button class="q" data-q="year" aria-label="年の説明">?</button></span><div class="yr"><input type="range" id="yearRange" min="2025" max="2040" step="1" value="2025" aria-label="年"><div class="yrv num" id="yearV">2025<small>基準＝2024年実績</small></div><div class="yq" id="yearQuick"><button data-y="2025" aria-pressed="true">2025</button><button data-y="2030" aria-pressed="false">2030</button><button data-y="2035" aria-pressed="false">2035</button><button data-y="2040" aria-pressed="false">2040</button></div></div><span class="tag">影響なし</span></div>
      <div class="prow" id="rowSc"><span class="lbl">前提<button class="q" data-q="sc" aria-label="前提の説明">?</button></span><div class="seg alt" id="scSeg"><button aria-pressed="true" data-s="A">人口のみ</button><button aria-pressed="false" data-s="M">中間</button><button aria-pressed="false" data-s="B">上限</button></div><span class="tag">影響なし</span></div>
      <div class="prow" id="rowTime"><span class="lbl">時間帯<button class="q" data-q="time" aria-label="時間帯の説明">?</button></span><div class="seg" id="timeSeg"><button aria-pressed="true" data-t="all">終日</button><button aria-pressed="false" data-t="day">昼 8–19時</button><button aria-pressed="false" data-t="night">夜 20–7時</button></div><span class="tag">影響なし</span></div>
      <div id="qbox" hidden><button id="qclose" aria-label="閉じる">×</button><div id="qtext"></div></div>
    </div>
'''
s=s.replace(old,new)
rep(".prow .lbl{width:44px;font-size:11.5px;color:var(--ink2);flex:none}",
""".prow .lbl{width:58px;font-size:11.5px;color:var(--ink2);flex:none;display:flex;align-items:center;gap:3px}
.q{width:16px;height:16px;border-radius:50%;border:1px solid var(--ink3);background:none;color:var(--ink3);font-size:10px;font-weight:700;line-height:1;cursor:pointer;padding:0;flex:none}
.q[aria-expanded="true"]{background:var(--navy);color:#fff;border-color:var(--navy)}
.prow.off .q{pointer-events:auto;opacity:1}
#qbox{position:relative;background:var(--surface2);border-radius:10px;padding:10px 30px 10px 12px;margin:4px 0 6px;font-size:12.5px;line-height:1.6;color:var(--ink)}
#qbox b{font-weight:700}
#qclose{position:absolute;right:6px;top:6px;width:22px;height:22px;border:0;border-radius:50%;background:var(--surface);color:var(--ink2);cursor:pointer;font-size:13px;line-height:1}
#qbox[hidden]{display:none}""")
rep("ctlT.onclick=()=>setCollapsed(!ctl.classList.contains('collapsed'));",
"""ctlT.onclick=()=>setCollapsed(!ctl.classList.contains('collapsed'));
const QTEXT={
 mode:'<b>何を見るか。</b>出場件数＝救急車が出動した年間件数（区内で発生したもの。2025年は2024年実績、以降は推計）。人口＝区の総人口。高齢者人口＝65歳以上の人数。高齢化率＝65歳以上÷総人口。昼夜間比＝昼間人口÷夜間人口×100（2020年国勢調査、年によらず固定）。',
 view:'<b>実数</b>はその年の値そのもの。<b>2025年比の増減率</b>は2025年（基準＝2024年実績）からの変化率で、出場件数・人口・高齢者人口で使えます。人口が減っても出場件数が増える区を見つけるときに便利です。',
 year:'2025年は基準年で、出場件数は2024年の実績、人口は2025年1月1日の実績。2026年以降は横浜市将来人口推計（令和5年推計・中位）にもとづく推計です。昼夜間比だけは年で変わりません。',
 sc:'<b>搬送率（＝利用率）</b>は、年齢ごとに「1年のうちに救急搬送される人の割合」です（85歳以上なら25.7%、15–64歳なら2.8%）。将来この率をどう置くかの前提で、出場件数にだけ効きます。<br><b>人口のみ</b>：率を2024年のまま固定。人口の増減と年齢構成だけで決まる下限。<br><b>中間</b>：率が年+0.75%ずつ上がる（2035年に+8%）。上昇傾向が鈍る想定。<br><b>上限</b>：率が年+1.5%ずつ上がる（2035年に+18%）。2013〜2024年の傾向がそのまま続く仮定で、上振れ側。',
 time:'市全体の時間帯別出場件数（消防年報）から、出場の65%が昼（8〜19時台）に起きています。各区の年間件数をこの比率で分け、通勤・通学による上乗せ分は昼側だけに入れます。区ごとの時間帯別実績は公表されていないため概算です。出場件数にだけ効きます。'};
const qbox=document.getElementById('qbox'),qtext=document.getElementById('qtext');
let qOpen=null;
function showQ(k){qOpen=k;document.querySelectorAll('.q').forEach(b=>b.setAttribute('aria-expanded',b.dataset.q===k));if(!k){qbox.hidden=true;return}qtext.innerHTML=QTEXT[k];qbox.hidden=false;setCollapsed(false)}
document.querySelectorAll('.q').forEach(b=>b.onclick=e=>{e.stopPropagation();showQ(qOpen===b.dataset.q?null:b.dataset.q)});
document.getElementById('qclose').onclick=()=>showQ(null);""")
# don't disable the ? buttons when a row is off
rep("r.querySelectorAll('button,input').forEach(b=>b.disabled=!af[k])","r.querySelectorAll('button:not(.q),input').forEach(b=>b.disabled=!af[k])")
# intro text
rep('<div><b>1</b><span><strong>地図</strong>で全体像をつかむ。柱の高さと色＝選んだ指標。年はスライダーで動かせます。薄くなった条件は、いまの表示に影響しません。地図は1本指で回転、2本指で移動と拡大（PCは右ドラッグで移動）。</span></div>',
    '<div><b>1</b><span><strong>地図</strong>で全体像をつかむ。まず「指標」で何を見るかを選び、次に年や前提を変えます。薄くなった条件はいまの表示に影響しません。各行の ? で用語の説明が開きます。地図は1本指で回転、2本指で移動と拡大（PCは右ドラッグで移動）。</span></div>')
P.write_text(s,encoding='utf-8'); print('patched',len(s))
