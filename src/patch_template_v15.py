import pathlib,re
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,n,a[:90]); s=s.replace(a,b)
# ---- CSS ----
rep(".yq{display:flex;gap:4px;flex-basis:100%}",
""".yb{display:inline-block;font:700 11px/1 Manrope,sans-serif;padding:3px 8px;border-radius:999px;background:var(--navy);color:#fff;margin-right:6px;vertical-align:2px;letter-spacing:.02em;white-space:nowrap}
.yb.mid{background:#5b6b82}.yb.long{background:#fff;color:#8e3b8f;border:1px solid #8e3b8f}
.yguide{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;background:#f3f5f9;border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:10px 0 18px;font-size:13px;line-height:1.6;color:var(--ink2)}
.yguide .k{white-space:nowrap}.yguide .lg{margin-left:auto;font-size:12px;color:var(--ink3)}
:root[data-time="night"] .yguide{background:#1a2238;border-color:#2c3650;color:#c9d2e6}
.yq{display:flex;gap:4px;flex-basis:100%;align-items:stretch}
.yq .sep{flex:0 0 1px;background:var(--line);margin:3px 1px}
.yq button.main{box-shadow:inset 0 0 0 1.5px var(--navy)}
.yq button.long{border-style:dashed;color:#8e3b8f}
.yq button.long[aria-pressed="true"]{background:#8e3b8f;border-color:#8e3b8f;color:#fff;border-style:solid}""")
# ---- map controls ----
rep('<button data-y="2035" aria-pressed="false">2035</button>','<button data-y="2035" aria-pressed="false" class="main">2035</button>')
rep('<button data-y="2050" aria-pressed="false">2050</button><button data-y="2060" aria-pressed="false">2060</button><button data-y="2070" aria-pressed="false">2070</button>',
    '<span class="sep"></span><button data-y="2050" aria-pressed="false" class="long">2050</button><button data-y="2060" aria-pressed="false" class="long">2060</button><button data-y="2070" aria-pressed="false" class="long">2070</button>')
rep("const yearLabel=()=>state.year==='2025'?'2025年（基準＝2024年実績）':state.year+'年';",
    "const yearLabel=()=>state.year==='2025'?'2025年（基準＝2024年実績）':state.year==='2035'?'2035年（このレポートの中心年）':+state.year>2040?state.year+'年（長期・参考値）':state.year+'年';")
rep("yv.innerHTML=v==2025?'2025<small>基準＝2024年実績</small>':v+'<small>推計</small>';",
    "yv.innerHTML=v==2025?'2025<small>基準＝2024年実績</small>':v==2035?'2035<small>中心年</small>':v>2040?v+'<small>長期・参考</small>':v+'<small>推計</small>';")
rep(" year:'2025年は基準年で、"," year:'<b>2035年</b>がこのレポートの中心年です。本文の数字は断りがなければ2035年。2040年は中期の確認点、2041年以降は長期の参考値（出場のピークは2058年、85歳以上のピークは2061年）。<br>2025年は基準年で、")
# ---- year guide block ----
G='<div class="yguide"><span class="k"><span class="yb">2035</span>このレポートの中心年。数字は断りがなければ2035年</span><span class="k"><span class="yb mid">2024 実績</span>基準年（人口は2025年1月1日）</span><span class="k"><span class="yb mid">2040</span>中期の確認点</span><span class="k"><span class="yb long">2058・2061</span>長期の山＝出場ピーク・85歳以上ピーク。2041年以降は参考値</span><span class="lg">グラフ：縦の点線＝2035、◆＝ピーク、薄い紫の帯＝長期</span></div>'
rep('需要は増え続けます。</p>','需要は増え続けます。</p>\n  '+G)
rep('各項目の「地図で」ボタンで、その条件の地図に飛べます。</p>','各項目の「地図で」ボタンで、その条件の地図に飛べます。</p>\n  '+G)
rep('右が市平均より多い（長い・遅い）、左が少ない。</p>','右が市平均より多い（長い・遅い）、左が少ない。</p>\n  '+G.replace('<span class="lg">グラフ：縦の点線＝2035、◆＝ピーク、薄い紫の帯＝長期</span>',''))
rep('を区ごとに掛け合わせます。</p>','を区ごとに掛け合わせます。</p>\n  '+G)
# ---- headings: badges ----
def badge_h3(num,b):
    global s
    m=re.search(r'<h3>%s\. [^<]*</h3>'%num,s); assert m,num
    s=s.replace(m.group(0),'<h3>'+b+m.group(0)[4:],1)
Y35='<span class="yb">2035</span>'; Y24='<span class="yb mid">2024 実績</span>'
for n in (1,2,3,5,6): badge_h3(n,Y35)
badge_h3(4,Y24); badge_h3(8,Y24); badge_h3(9,Y24); badge_h3(10,'<span class="yb mid">2025 断面</span>'); badge_h3(11,Y24); badge_h3(12,'<span class="yb mid">2013→2024</span>')
badge_h3(7,'<span class="yb mid">2040</span><span class="yb long">2058・2061</span>')
def badge_h4(txt,b):
    rep('<h4>'+txt+'</h4>','<h4>'+b+txt+'</h4>')
L='<span class="yb long">長期 2025→2070</span>'
badge_h4('救急出場件数の推移と推計（件/年）',Y35+'<span class="yb long">〜2070</span>')
badge_h4('誰が救急車を使うのか — 年齢別の出場件数',Y35)
badge_h4('区別 推計一覧',Y35)
badge_h4('人口・高齢化率・出場件数を1枚で — 2025→2070（市全体）',L)
badge_h4('85歳以上のピークまでの出場件数（市全体、件/年）',L)
badge_h4('市全体の人口の推移 2025→2070（年齢5区分、市推計・中位）',L)
badge_h4('区別の出場件数の推移 2025→2070（人口変化のみ）',L)
badge_h4('区別の人口の推移 2025→2070（2025年＝100）',L)
badge_h4('区別の85歳以上人口の推移 2025→2070（2025年＝100）',L)
badge_h4('1隊あたり年3,000件を超える年 — 区別・シナリオ別',L)
badge_h4('人口は減るのに、出場件数は増える — 区別の増減率 2025→2035',Y35)
badge_h4('区別の増減率 2025→2035（人口の変化だけ）',Y35)
badge_h4('救急隊あたりの負担 — 1隊あたり年間出場件数',Y35)
for t in ['不搬送率 — 出場したが搬送しなかった割合（2024年）','年齢別の搬送率（2024年、人口100人あたり年間搬送人員）','年齢別の搬送率（2024年・実測）','時間帯別の出場件数（市全体、2024年）','区別の年齢構成（2025年）と出場件数（2024年）','区別の出場件数の年齢構成（2024年、実績ベース校正）','区別の出場件数の内訳 — 搬送した出場と搬送に至らなかった出場（2024年、区内の救急隊の実績）','区別の出場の内訳 — 事故種別の構成（2024年）','密度と到着時間 — 疎な区ほど現場が遠い','生活保護率と校正係数','高齢化率と出場件数/千人','人口と出場件数の比例関係','市平均＝100とした指数：人口密度・出場密度・出場件数/千人']:
    badge_h4(t,Y24)
badge_h4('不搬送率の推移（市全体、2013〜2024年）','<span class="yb mid">2013→2024</span>')
badge_h4('年代別の搬送率の推移（人口100人あたり年間搬送人員）','<span class="yb mid">2013→2024</span>')
# ---- chart helpers ----
rep("const PEAK_E3=(()=>{let b='2025';YEARS.forEach(y=>{if(cityPop(y,'e3')>cityPop(b,'e3'))b=y});return b})();",
"""const PEAK_E3=(()=>{let b='2025';YEARS.forEach(y=>{if(cityPop(y,'e3')>cityPop(b,'e3'))b=y});return b})();
const PEAK_D=(()=>{let b='2025';YEARS.forEach(y=>{if(cityOf(y,'A')>cityOf(b,'A'))b=y});return b})();
/* 時間軸の共通マーク: 2035の縦点線＋2041年以降の薄い帯（X は西暦→x） */
const TF=(X,top,bot,o={})=>{let g=`<rect x="${X(2040.5)}" y="${top}" width="${X(2070)-X(2040.5)}" height="${bot-top}" fill="#8e3b8f" opacity=".05"/><line x1="${X(2035)}" x2="${X(2035)}" y1="${top}" y2="${bot}" stroke="#14213d" stroke-width="1.2" stroke-dasharray="4 3" opacity=".8"/>`;if(o.label!==false)g+=`<text x="${X(2035)+4}" y="${top+11}" font-size="10.5" font-weight="700" fill="#14213d">2035</text>`;if(o.long)g+=`<text x="${X(2070)-3}" y="${top+11}" font-size="9.5" fill="#8e3b8f" text-anchor="end">長期（参考）</text>`;return g};
const PKM=(x,y,c,label,side='end')=>`<path d="M${x},${y-7} l7,7 l-7,7 l-7,-7z" fill="${c}" stroke="#fff" stroke-width="1.5"/><text x="${side==='end'?x-10:x+10}" y="${y-9}" font-size="10.5" font-weight="700" fill="${c}" text-anchor="${side}" stroke="#fff" stroke-width="3" paint-order="stroke">◆ ${label}</text>`;""")
# trend chart
rep("""    let g=`<g stroke="#e3e8ef">${[100000,200000,300000,400000].map(v=>`<line x1="44" x2="584" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`;
    g+=[100000,200000,300000,400000].map(""","""    let g=`<g stroke="#e3e8ef">${[100000,200000,300000,400000].map(v=>`<line x1="44" x2="584" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}</g>`;
    g+=TF(X,Y(400000),h-36,{long:true});
    g+=[100000,200000,300000,400000].map(""")
rep("""<text x="${X(+PEAK_E3)-4}" y="${Y(400000)+12}" fill="#8e3b8f" font-size="10.5" text-anchor="end">${PEAK_E3} 85歳以上ピーク</text>`;""","""<text x="${X(+PEAK_E3)-4}" y="${Y(400000)+24}" fill="#8e3b8f" font-size="10.5" text-anchor="end">${PEAK_E3} 85歳以上ピーク</text>`;""")
rep("""    g+=`<circle cx="${X(2024)}" cy="${Y(T24)}" r="4" fill="#14213d"/>`;""","""    g+=`<circle cx="${X(2024)}" cy="${Y(T24)}" r="4" fill="#14213d"/>`;g+=PKM(X(+PEAK_D),Y(cityOf(+PEAK_D,'A')),'#14213d','出場ピーク '+PEAK_D,'end');g+=`<circle cx="${X(2035)}" cy="${Y(A35)}" r="4.5" fill="#fff" stroke="#14213d" stroke-width="2"/>`;""")
# triple chart
rep("""   let g=`<path d="M${YEARS.map((y,i)=>X(i)+','+YR(G[i])).join(' L')} L${X(N-1)},256 L${X(0)},256Z" fill="#f4a259" opacity=".18"/>`;""",
    """   let g=`<path d="M${YEARS.map((y,i)=>X(i)+','+YR(G[i])).join(' L')} L${X(N-1)},256 L${X(0)},256Z" fill="#f4a259" opacity=".18"/>`;g+=TF(y=>X(y-2025),YL(220),256);""")
rep("""   placeLabels(lab,11);lab.forEach(l=>{if(l.lx+l.n.length*11>540)""","""   const pd=YEARS.indexOf(PEAK_D);g+=PKM(X(pd),YL(D[pd]),'#e63946','出場ピーク '+PEAK_D,'end')+PKM(X(pk),YL(E[pk]),'#8e3b8f','85歳以上ピーク '+PEAK_E3,'end');const i35=YEARS.indexOf('2035');[[P,'#14213d'],[E,'#8e3b8f'],[D,'#e63946']].forEach(([a,c])=>g+=`<circle cx="${X(i35)}" cy="${YL(a[i35])}" r="4" fill="#fff" stroke="${c}" stroke-width="2"/>`);
   lab[1].n='85歳以上 '+E[pk].toFixed(0);placeLabels(lab,11);lab.forEach(l=>{if(l.lx+l.n.length*11>540)""")
# supp: sgPop, lines, sgOver
rep("""+[1e6,2e6,3e6].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v/1e4}万</text>`).join('')+yearTicks(268);""",
    """+[1e6,2e6,3e6].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v/1e4}万</text>`).join('')+yearTicks(268)+TF(y=>Xy(y-2025),30,250,{long:true});""")
rep("""+ticks.map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${fmtY(v)}</text>`).join('')+yearTicks(410,50,520);""",
    """+ticks.map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${fmtY(v)}</text>`).join('')+yearTicks(410,50,520)+TF(y=>Xy(y-2025,50,520),30,390);""")
rep("""   rows.forEach(({w,o},i)=>{const y=6+i*rh;g+=`<text x="74" y="${y+14}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${w.name}</text><line x1="80" x2="560" y1="${y+9}" y2="${y+9}" stroke="#eef1f5" stroke-width="10"/>`;""",
    """   g+=TF(X,4,rows.length*rh+6,{label:false,long:true});
   rows.forEach(({w,o},i)=>{const y=6+i*rh;g+=`<text x="74" y="${y+14}" font-size="12" font-weight="700" fill="#14213d" text-anchor="end">${w.name}</text><line x1="80" x2="560" y1="${y+9}" y2="${y+9}" stroke="#eef1f5" stroke-width="10"/>`;""")
# mini chart
rep("""  let g=`<line x1="${x0}" x2="${x1}" y1="${Y(lo+pad)}" y2="${Y(lo+pad)}" stroke="var(--line)"/><line x1="${x0}" x2="${x1}" y1="${Y(hi-pad)}" y2="${Y(hi-pad)}" stroke="var(--line)"/>`;""",
    """  let g=`<line x1="${x0}" x2="${x1}" y1="${Y(lo+pad)}" y2="${Y(lo+pad)}" stroke="var(--line)"/><line x1="${x0}" x2="${x1}" y1="${Y(hi-pad)}" y2="${Y(hi-pad)}" stroke="var(--line)"/>`;
  {const i35=YEARS.indexOf('2035'),i41=YEARS.indexOf('2041');g+=`<rect x="${X(i41)}" y="${y0}" width="${x1-X(i41)}" height="${y1-y0}" fill="#8e3b8f" opacity=".07"/><line x1="${X(i35)}" x2="${X(i35)}" y1="${y0}" y2="${y1}" stroke="var(--navy)" stroke-dasharray="3 3" opacity=".7"/>`}""")
rep("g+=['2025','2040','2055','2070'].map(y=>`<text x=\"${X(YEARS.indexOf(y))}\" y=\"${H-4}\"","g+=['2025','2035','2050','2070'].map(y=>`<text x=\"${X(YEARS.indexOf(y))}\" y=\"${H-4}\"")
# peak table rows
rep("function buildPeak(){const ys=['2025','2035','2040','2050','2060',PEAK_E3,'2070'].filter((y,i,a)=>a.indexOf(y)===i).sort();const r=ys.map(y=>`<tr${y===PEAK_E3?' style=\"font-weight:700;background:#f3f0f7\"':''}><td>${y}${y===PEAK_E3?'（85歳以上ピーク）':''}</td>",
    "function buildPeak(){const ys=['2025','2035','2040','2050',PEAK_D,PEAK_E3,'2070'].filter((y,i,a)=>a.indexOf(y)===i).sort();const r=ys.map(y=>`<tr${y===PEAK_E3||y===PEAK_D?' style=\"font-weight:700;background:#f3f0f7\"':y==='2035'?' style=\"font-weight:700;background:#eef2f9\"':''}><td>${y==='2035'?'<span class=\"yb\">2035</span>中心年':y===PEAK_D?'<span class=\"yb long\">'+y+'</span>出場ピーク':y===PEAK_E3?'<span class=\"yb long\">'+y+'</span>85歳以上ピーク':y==='2025'?'<span class=\"yb mid\">2025</span>基準（2024年実績）':y==='2040'?'<span class=\"yb mid\">2040</span>中期':y}</td>")
P.write_text(s,encoding='utf-8'); print('patched v15')
