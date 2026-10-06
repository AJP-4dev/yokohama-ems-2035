import pathlib,re
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:90]); s=s.replace(a,b)
# renumber 11-13 -> 12-14
rep('<h3>13. 施策への示唆</h3>','<h3>14. 施策への示唆</h3>')
rep('<h3>12. 補足グラフ — 推移と構成を一覧で</h3>','<h3>13. 補足グラフ — 推移と構成を一覧で</h3>')
rep('<h3>11. 搬送率はどう動いてきたか — 増えているのは高齢者の利用ではない</h3>',
'''<h3>11. 年齢で説明できない差は何か — 生活保護率との相関</h3>
  <p>校正係数（年齢構成と昼間人口で説明できない残差）を、区の生活保護率（被保護人員 ÷ 人口、令和6年4月）と外国人住民比率（令和7年1月1日）に並べました。</p>
  <div class="card"><h4>生活保護率と校正係数</h4><svg class="chart" id="anE" viewBox="0 0 600 380"></svg><p class="m">横軸＝生活保護率、縦軸＝校正係数（1.0＝人口から期待される件数どおり）。点線＝中・西を除く16区の回帰線。相関は18区で <span class="num" id="anEr"></span>、16区で <span class="num" id="anEr2"></span>。外国人比率との相関は <span class="num" id="anEr3"></span>（18区）。</p><div class="ins">年齢で説明できない救急需要の差は、生活保護率とかなり強く連動する。南区（保護率3.72%、市内2位）は回帰線に乗せると残差+0.05で、「年齢で説明できない2割」の4分の3が経済状況で説明できる。港南区の残差+0.07は転院搬送（7.0%）の分。例外は瀬谷区（保護率3.33%なのに校正係数1.01）で、団地中心で高齢化が進み、施設や家族の見守りが効いている可能性がある。青葉区は保護率0.81%で線よりさらに低く、所得・健康状態が良い層の区の典型。生活保護率は原因というより「独居・低所得・持病・かかりつけ医を持ちにくい」の代理指標で、因果ではなく相関として読む。</div></div>
  <p><a class="mapgo" href="#" data-state="m=percap&w=南">南区を地図で</a> <a class="mapgo" href="#" data-state="m=percap&w=瀬谷">瀬谷区を地図で</a></p>
  <h3>12. 搬送率はどう動いてきたか — 増えているのは高齢者の利用ではない</h3>''')
# analysis chart E
rep("  // D: aging vs percap","""  // E: welfare rate vs calibration factor
  {const X=v=>50+(v-0.5)/(6-0.5)*530,Y=v=>340-(v-0.75)/(1.8-0.75)*310;let g=`<g stroke="#e3e8ef">${[0.8,1.0,1.2,1.4,1.6].map(v=>`<line x1="50" x2="580" y1="${Y(v)}" y2="${Y(v)}"/>`).join('')}${[1,2,3,4,5].map(v=>`<line x1="${X(v)}" x2="${X(v)}" y1="30" y2="340"/>`).join('')}</g>`;
   g+=[0.8,1.0,1.2,1.4,1.6].map(v=>`<text x="46" y="${Y(v)+4}" font-size="10.5" fill="#8e9bae" text-anchor="end">${v.toFixed(1)}</text>`).join('')+[1,2,3,4,5].map(v=>`<text x="${X(v)}" y="356" font-size="10.5" fill="#8e9bae" text-anchor="middle">${v}%</text>`).join('');
   const RE=W.map(w=>({n:w.name,x:w.hogo,y:w.fac,f:w.foreign/popTot(w,'2025')*100})),sub=RE.filter(r=>r.n!=='中'&&r.n!=='西'),[a,b]=fit(sub.map(r=>r.x),sub.map(r=>r.y));
   g+=`<line x1="${X(0.6)}" y1="${Y(a*0.6+b)}" x2="${X(4)}" y2="${Y(a*4+b)}" stroke="#14213d" stroke-dasharray="5 4" stroke-width="1.5"/>`;
   const LE=RE.map(r=>({r,x:X(r.x),y:Y(r.y),ly:Y(r.y)}));spreadLabels(LE,12,40);LE.forEach(({r,x,y,ly})=>{const core=r.n==='中'||r.n==='西';g+=`<circle cx="${x}" cy="${y}" r="6" fill="${core?'#e63946':r.n==='南'?'#f4a259':'#3a7bd5'}" opacity=".85"/><text x="${x+8}" y="${ly+4}" font-size="11" font-weight="700" fill="#14213d">${r.n}</text>`});
   g+=`<text x="580" y="372" font-size="10.5" fill="#5b6b82" text-anchor="end">横軸＝生活保護率（被保護人員÷人口、R6.4）、縦軸＝校正係数。点線＝中・西を除く16区の回帰線</text>`;
   document.getElementById('anE').innerHTML=g;document.getElementById('anEr').textContent=corr(RE.map(r=>r.x),RE.map(r=>r.y)).toFixed(2);document.getElementById('anEr2').textContent=corr(sub.map(r=>r.x),sub.map(r=>r.y)).toFixed(2);document.getElementById('anEr3').textContent=corr(RE.map(r=>r.f),RE.map(r=>r.y)).toFixed(2)}
  // D: aging vs percap""")
# ward profile bars: add 生活保護率・外国人比率
rep("   {k:'dn',l:'昼夜間人口比',v:w.dn,c:cityDN,f:v=>v.toFixed(0)}]}",
    "   {k:'dn',l:'昼夜間人口比',v:w.dn,c:cityDN,f:v=>v.toFixed(0)},\n   {k:'hogo',l:'生活保護率',v:w.hogo,c:W.reduce((s,x)=>s+x.hogo*popTot(x,'2025'),0)/cityPop25,f:v=>v.toFixed(2)+'%'},\n   {k:'frn',l:'外国人住民の割合',v:w.foreign/pop*100,c:W.reduce((s,x)=>s+x.foreign,0)/cityPop25*100,f:v=>v.toFixed(1)+'%'}]}")
# ward text: add note when hogo high
rep("  else s1+=`人口から期待される件数とほぼ一致（校正係数${fac.toFixed(2)}）。`;\n  out.push(s1);",
    "  else s1+=`人口から期待される件数とほぼ一致（校正係数${fac.toFixed(2)}）。`;\n  const hr=rankOf('hogo',w);if(hr<=4)s1+=`生活保護率${w.hogo.toFixed(2)}%は18区中${hr}位で、年齢で説明できない需要の一因と考えられる。`;\n  out.push(s1);")
# sources
rep('<li>国土地理院「全国都道府県市区町村別面積調」— 区の面積（令和6年）。',
    '<li>横浜市健康福祉局「生活保護統計月報」（中区統計便覧2024 所収）— 区別の被保護世帯・人員・保護率（令和6年4月）。</li>\n    <li>総務省「住民基本台帳に基づく人口」【外国人住民】令和7年1月1日 — 区別の外国人住民数。</li>\n    <li>国土地理院「全国都道府県市区町村別面積調」— 区の面積（令和6年）。')
rep('<p class="lead">3つの結論。人口は減っても出場は増える、主役は85歳以上、需要の重心は北部へ。6以降は隊の負担・2040年・密度と到着時間・不搬送・2025年の断面・搬送率の推移・補足グラフ・施策です。',
    '<p class="lead">3つの結論。人口は減っても出場は増える、主役は85歳以上、需要の重心は北部へ。6以降は隊の負担・2040年・密度と到着時間・不搬送・2025年の断面・生活保護率との相関・搬送率の推移・補足グラフ・施策です。')
P.write_text(s,encoding='utf-8'); print('patched')
