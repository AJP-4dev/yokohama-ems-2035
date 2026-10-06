# 「動画」タブを追加する（動画が承認されてから適用）。video/yokohama-ems-2035.mp4 をリポジトリ直下 media/ に置く前提
import pathlib
P=pathlib.Path(__file__).parent.parent/'template.html'; s=P.read_text(encoding='utf-8')
def rep(a,b):
    global s; assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
rep("['slides','スライド','<rect x=\"3\" y=\"4\" width=\"18\" height=\"12\" rx=\"2\"/><path d=\"M12 16v4M8 20h8\"/>']];",
    "['slides','スライド','<rect x=\"3\" y=\"4\" width=\"18\" height=\"12\" rx=\"2\"/><path d=\"M12 16v4M8 20h8\"/>'],['video','動画','<rect x=\"3\" y=\"5\" width=\"18\" height=\"14\" rx=\"2\"/><path d=\"M10 9l5 3-5 3z\"/>']];")
rep('<!-- ================= INTRO ================= -->',
'''<!-- ================= VIDEO ================= -->
<section class="page" id="page-video"><div class="scroll"><div class="wrap">
  <h2>動画で見る — 7分で分かる要点</h2>
  <p class="lead">何をして、何が分かったかを無音の動画にまとめました。字幕と注釈だけで読めます。会議の冒頭や事前共有にどうぞ。</p>
  <div class="card" style="padding:0;overflow:hidden"><video id="mainVideo" controls playsinline preload="metadata" poster="media/poster.jpg" style="width:100%;display:block;background:#000"><source src="media/yokohama-ems-2035.mp4" type="video/mp4">お使いのブラウザは動画を再生できません。<a href="media/yokohama-ems-2035.mp4">ファイルを開く</a></video></div>
  <div class="card"><h4>章立て</h4><ol id="videoChapters" style="padding-left:20px;margin:6px 0"></ol><p class="m">時間を押すとその章から再生します。</p></div>
  <p class="m">音声はありません。字幕は画面下、補足は画面内の注釈です。動画の数値はこのサイトと同じデータから描いています。</p>
  <button class="next" data-go="map">地図に戻る<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
</div></div></section>

<!-- ================= INTRO ================= -->''')
rep("buildWards();buildSupp();","buildWards();buildSupp();(function(){const ch=window.VIDEO_CHAPTERS||[];const v=document.getElementById('mainVideo'),ol=document.getElementById('videoChapters');if(!ol)return;ol.innerHTML=ch.map(c=>`<li><a href=\"#\" data-t=\"${c[0]}\">${Math.floor(c[0]/60)}:${String(c[0]%60).padStart(2,'0')}</a>　${c[1]}</li>`).join('');ol.querySelectorAll('a').forEach(a=>a.onclick=e=>{e.preventDefault();v.currentTime=+a.dataset.t;v.play()})})();")
P.write_text(s,encoding='utf-8'); print('patched')
