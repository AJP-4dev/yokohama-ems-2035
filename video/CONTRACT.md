# CONTRACT.md — 章ファイルの契約（並列実装用）

動画: 1920×1080 / 30fps / **DURATION = 435秒（13,050フレーム）**。無音。
構成: `src/scene.html`（骨格・触らない） + `src/lib.js`（共通基盤） + `src/chapters/ch00.js … ch10.js`（章ごと）。

```
src/scene.html      THREE を window.THREE に載せ → data.js → lib.js → ch00..ch10 を順に読み込む
                    タイムライン（確定表）・seek(t)・章レール・章見出し・問いカード・結論カード・字幕帯
src/lib.js          色/定数/イージング/文字/チップ/線・棒/2D地図/3D地図/ロゴ など（グローバル関数）
src/chapters/chNN.js window.CHAPTERS[NN] = {...} を登録するだけ
src/reference/scene-monolith.html  （読み込まれない）旧1ファイル版。第2〜10章の試作実装あり。移植の参考に
```

## 1. 確定タイムライン（scene.html の `TL` が正。章側で変えない）

| 章 | ファイル | title | 開始(s) | 長さ(s) | 開始フレーム | 3D |
|---|---|---|---:|---:|---:|---|
| 0 | ch00.js | 冒頭 | 0 | 15 | 0 | ○ 全編 |
| 1 | ch01.js | 問い | 15 | 19 | 450 | |
| 2 | ch02.js | データの出どころ | 34 | 28 | 1020 | |
| 3 | ch03.js | どう計算したか | 62 | 64 | 1860 | |
| 4 | ch04.js | 結果① 市全体 | 126 | 46 | 3780 | |
| 5 | ch05.js | 結果② 誰が | 172 | 45 | 5160 | |
| 6 | ch06.js | 結果③ どこで（見せ場） | 217 | 66 | 6510 | ○ 0〜47.6s |
| 7 | ch07.js | 結果④ 密度と到着、不搬送 | 283 | 50 | 8490 | ○ (b) 16〜33.6s |
| 8 | ch08.js | 意外だったこと | 333 | 42 | 9990 | |
| 9 | ch09.js | 隊の負担 | 375 | 30 | 11250 | |
| 10 | ch10.js | 示唆と案内 | 405 | 30 | 12150 | ○ 末尾ロゴ 21.3s〜 |
| — | | 終了 | 435 | | 13050 | |

章ローカル時刻 `lt`（0 … duration）の共通構造（scene.html が自動で描く）:
- `0.0–1.2s` **問いカード**（白板が左→右にワイプで入り、「？」と `q` が走って現れ、抜ける）。第0章は無し。本編は `lt = 1.2` から。
- `1.0s〜` 左上に章見出し（`NN  title`、20px）。上端に章レール（1本の罫線＋章境界の目盛）。
- `末尾0.8s` **結論カード**（白地に `concl` を左揃え48px、下に罫線が伸びる）。`concl: null` なら出ない。
- `subs` の字幕を画面下に表示（y=944、高さ56、左揃え、左端に赤い4px縦線、切替はクロスフェード0.25s）。

## 2. 章ファイルの雛形

```js
/* 第N章 */
(() => {                                   // ← 必ず IIFE。トップレベルに const/function を出さない（他章と衝突して全体が止まる）
  // 章専用の定数・計算はここ（DATA から計算する。SPEC の確定数値以外の数字を作らない）
  const ROWS = WD.map((w) => w.name);
  window.CHAPTERS[N] = {
    title: '章名',                          // 章見出し・問いカードに出る
    q: '問い（問いカード）？',               // 第0章のみ null
    concl: '結論の1文',                      // 末尾0.8sの結論カード。null なら無し
    duration: 46,                           // 確定表の値（変えない）
    subs: [[1.6, 7.6, '字幕1行22文字以内'], [8.0, 14.0, '…']],  // 章ローカル秒・重ねない・間は0.4s以上
    uses3D: (lt) => lt >= 16 && lt < 33.6,   // 3Dを表示する区間だけ true（省略=2Dのみ）
    setup(ctx) {},                          // 読み込み直後に1回（重い前計算はここか IIFE 内で）
    draw(ctx, lt, t) {                      // 毎フレーム。lt と t だけから全状態を決める（純関数）
      wtext(lt, 1.4, null, '見出し', LX, 240, { size: 48 });
      wtext(lt, 1.8, null, '本文1行目\n本文2行目', LX, 330, { size: 28, lead: 44 });
      chip(lt, 6.0, 15.0, '注釈は短く', LX, 520, { c: COL.red });
    },
  };
})();
```

- `ctx = { g, W, H, M, LX, LW, RX0, RX1, TL, START, DURATION }`（`g` は 1920×1080 の Canvas2D）。
- `uses3D(lt)` が true のフレームは 2D キャンバスが透明で始まり、3D キャンバスが下に見える。**3D の描画は draw の中で自分で行う**（§5）。false のフレームは背景 `#f4f6f9` で塗られた状態で draw が呼ばれる。
- draw の中で `g.save()/restore()` の対応を崩さないこと（scene.html 側でも save/restore で囲んでいる）。
- 禁止: `Date.now()`, `performance.now()` を絵に使う, `requestAnimationFrame`, `setTimeout`, CSS transition, `Math.random()`（乱数が要るなら t から作る）, ネットワーク, 外部画像・フォント。

## 3. デザイン規約（統括の方針。SPEC より優先）

- **レイアウト**: 文字は左カラム（`LX=80`〜`LX+LW=760`）、グラフは右（`RX0=800`〜`RX1=1840`）。安全マージン80px（`M`）。字幕帯（y=944〜1000）とかぶる位置（y>900）に本文を置かない。
- **文字サイズは 120 / 48 / 28 / 20 の4段だけ**。日本語は Hiragino Sans（本文 600、見出し 800）、数字は Avenir Next Demi Bold（600）で桁揃え（`numText` / `wtext(..., {tab:true})`）。数字は単位つきで同じ行に（例「25.7人」）。
- **入場の動きは3種だけ**: マスクワイプ（`wtext`, `wipe`）／線が走る（`rule`, `polyline`, `line`）／伸びる（棒の長さ・柱の高さ）。フェード入場は禁止（字幕の切替だけ例外）。退場はワイプアウト（`phase` の終わり、`wtext` の tOut）。
- **1章に「見せる動き」は1つ**。残りは静かに。ただし3秒以上の完全静止は作らない（字幕の進行線・章レールは常に動いている。それ以外にも小さな動きを）。
- **色**: 紺と白が主体。赤 `COL.red` は「出場件数」と「強調」だけ。橙・紫・緑・青・水色は年齢5区分と増減の意味色だけ（`AGEC`）。章ごとに新色を増やさない。
- **禁止**: 大きな数字＋小ラベルの中央寄せカードの多用／グラデーション背景・グロー・パーティクル／全要素の「フェード＋下からスライド」／英字の全大文字ラベル／「A · B · C」の中黒区切り（列挙は「、」）／末尾の「→」装飾／角丸カードの敷き詰め（角丸は注釈チップの6pxだけ）。
- **注釈チップは同時に最大3つ**。字幕は1行22文字以内・同時に1行。文体は体言止め・短文、専門語には言い換え（搬送率＝1年に救急車で運ばれる人の割合 など）。
- **数字**: SPEC の「画面に出す確定数値」以外を作らない。DATA から計算できるものは計算して表示（`SC.A(2035)` 等）。

## 4. lib.js の関数一覧（すべてグローバル）

### 定数・色
| 名前 | 内容 |
|---|---|
| `W, H, M` | 1920, 1080, 80（安全マージン） |
| `LX, LW, RX0, RX1` | 左カラム x=80・幅680／右エリア 800〜1840 |
| `COL` | `bg #f4f6f9, paper, ink/navy #14213d, sub #5b6b82, faint, red #e63946, purple, orange, green, blue, sky, line, grid, grey` |
| `AGE, AGEC, AGEL` | `['c','w','e1','e2','e3']`／年齢5区分の色／ラベル（0–14歳 …85歳以上） |
| `RAMPS, ramp(stops,t), mix(a,b,u)` | 色ランプ（サイトと同じ `RAMPS.disp`, `RAMPS.diff`）／2色の補間 |
| `rampDisp(v)` | 出場件数（7,000〜23,000）→ 紺系の色 |
| `rampDiv(v, hi=15, lo=-12)` | 増減率% → 0%≈白、＋は橙→赤、−は緑 |
| `divCol(v)` | `rampDiv(v, 15, -5)`（3D地図の増減率の色。凡例は −5%〜+15%） |

### イージング・時間
| 名前 | 内容 |
|---|---|
| `clamp(x,a=0,b=1)`, `lerp(a,b,u)` | |
| `E.outCubic / E.outExpo / E.inOut / E.outBack` | イージング関数（0..1） |
| `P(t, a, d)` | 区間 [a, a+d] の進捗 0..1 |
| `ein(t,a,d=0.8)` / `eio(t,a,d=1)` / `cnt(t,a,d=1.2)` | cubic-out／ease-in-out（カメラ）／ease-out-expo（カウンター） |
| `win(t,a,b,f=0.25)` | 区間 [a,b] の可視度（両端f秒で0→1→0。字幕用） |
| `counter(lt, t0, v, d=1.2)` | 0→v を ease-out-expo で数える文字列（桁区切りつき） |

### データ（DATA から）
| 名前 | 内容 |
|---|---|
| `WD`, `WI`, `ward(name)` | 18区の配列／名前→index／名前→区 |
| `TR` | `DATA.trend` |
| `popT(w,y)`, `cityPop(y, age?)` | 区の総人口／市の人口（年齢区分指定可） |
| `D24, PER_DAY, INTERVAL` | 256,481／1日あたり（366日）／何秒に1回 |
| `YEARS` | 2025…2040 |
| `dispA(w,y)` | 区の出場（人口変化のみ。2025は2024実績） |
| `SC.A/M/B/T(y)` | 市全体の出場：人口変化のみ／緩やかな利用増／利用増が続く／年代別トレンド |
| `wDiff35(w)`, `wPopDiff35(w)` | 区の2035年 出場増減%（2024比）／人口増減%（2025比） |
| `units(w)`, `overYear(w)` | 隊数（24h＋日勤）／1隊3,000件を超える最初の年（null=超えない） |
| `nonTrYear(y)` | 市の不搬送率（0..1） |
| `fmt(n)`, `man(n,d=1)`, `sgn(v,d=1)`, `sgn2(v)` | 桁区切り／「18.8万」／「+7.8」「−2.3」／相関係数用「−0.01」 |
| `corr(xs,ys)`, `fit(xs,ys)` | 相関係数／回帰 [a,b]（y=a+bx） |
| `pctRange(arr)` | 絶対値の [min,max] |

### 文字・図形（Canvas2D、`g` に描く）
| 名前 | 内容 |
|---|---|
| `text(s,x,y,{size,w,c,align,base,num,halo,ls,a})` | 1行を描いて幅を返す（はみ出し検査に記録される） |
| `numText(s,x,y,{size,c,align})` | 桁揃えの数字（Avenir Next 600）。単位の日本語も混ぜてよい |
| `tw(s,size,w=600,num=false)` | 文字幅 |
| **`wtext(lt, tIn, tOut, s, x, y, o)`** | **基本の文字**。tIn からマスクワイプで現れ、tOut（null=出たまま）でワイプアウト。`\n` で複数行、`o.lead` 行間、`o.tab:true` で数字桁揃え、`align:'right'/'center'` |
| `rule(lt, tIn, x, y, w, c=navy, lw=1, d=0.6)` | 左から伸びる罫線 |
| `phase(lt, a, b, fn, box=[x,y,w,h])` | 区間 [a,b] だけ fn を描き、b から box を左→右にワイプアウト（画面の入れ替え） |
| `wipe(u, x,y,w,h, fn, v=0)` / `clipRect(x,y,w,h,fn)` | 矩形マスク（u=現れ具合、v=消え具合） |
| `bgWipe(lt, t0, d=0.8)` | 背景色が左→右に画面を覆う（3D→2Dの切替など） |
| `line(x1,y1,x2,y2,c,lw,dash)`, `dot(x,y,r,c)`, `arrow(...)`, `rrect(...)` | 基本図形（rrect はチップ以外で角丸を使わない） |
| `polyline(pts, u, c, lw=3, dash)` | 折れ線を u(0..1) まで左から描く。先端座標を返す |
| `axes(lt, t0, C, xt, yt)` | 軸と補助線。`C={x0,x1,y0,y1,X(v),Y(v)}`, `xt/yt=[[値,'ラベル'],…]` |
| **`chip(lt, t0, t1, s, x, y, {c, align})`** | **注釈チップ**（20px W6・白地・1px紺罫・角丸6px・意味色の点）。[t0,t1] で表示、左→右ワイプで出入り。高さ40。縦に並べるなら y を52ずつ。**同時3つまで** |
| `withAlpha(a, fn)` | 透明度（強調で他を薄くするとき。入場には使わない） |
| `drawConclAt(l, s)` | 結論カードを任意の時刻に描く（通常は `concl` で自動。第10章のように途中に置くときだけ） |

### 2D 地図
| 名前 | 内容 |
|---|---|
| `drawMap(box, fillFn(w,i), {stroke, lw, alphaFn})` | 18区のポリゴンを box `{x,y,w,h}` に収めて塗る。返り値 `xf` |
| `mapXf(box)`, `wardC(xf, w)` | 座標変換／区の重心の画面座標 |

### ロゴ
| 名前 | 内容 |
|---|---|
| `drawLockup(u, x, y)` | タイトルのロックアップ（小見出し「横浜市 2025 → 2035」、120px W8「救急需要の未来地図」を左→右ワイプ、紺のルールが伸び先端の赤い正方形が止まる）。u=出現開始からの秒、(x,y)=タイトルのベースライン左端。第0章と第10章末尾で同じ形を使う |
| `ORDER_N, rankN[i], DIST_N, DMAX` | 中区→西区→中区からの距離順（同心円）の並び |
| `ORDER_X, rankX[i]` | 西→東の並び |

## 5. 3D 地図ユーティリティ（three.js、平行投影、影・エッジつき）

シーンは lib.js で1回だけ作られている（18区の押し出し柱 `meshes[i]`、2段目用 `lows[i]`、輪郭線 `outlines[i]`、床・影・グリッド・ライト）。座標はサイトと同じ `px(lon,lat)`、`C3[i]` が区の重心 [x,z]。

毎フレームの手順（`uses3D(lt)` が true のときの draw の中）:
```js
reset3D();                    // 全部を非表示・既定値に戻す（前フレームの状態を持ち越さない）
beginGL();                    // GL キャンバスを全面クリア
WD.forEach((w, i) => setPillar(i, hOf(w.disp24), rampDisp(w.disp24)));   // 高さと色
setCam({ theta: -0.35, phi: 0.95, dist: 36, tx: 0, tz: 1.0 });           // カメラ（t の関数にする）
renderView(0, W);             // 描画
wardLabel3D(WI['都筑'], hOf(ward('都筑').disp[2035]), '都筑', '+12.8%', COL.red);  // ラベルは2Dで重ねる（setCam の後）
```
| 名前 | 内容 |
|---|---|
| `reset3D()` / `beginGL()` | 状態リセット／全面クリア（毎フレーム必須） |
| `setPillar(i, h, color, op=1)` | 柱 i を高さ h・色で表示（`scale.y=h`） |
| `hOf(v)` | 出場件数 → 柱の高さ（サイトと同じ `0.4 + v/23000*7`） |
| `setColorHSL(mat, a, b, u)` | 色を HSL 補間（`meshes[i].material` に。色の切替は必ずこれで） |
| `meshes[i].userData.line.material.opacity` | エッジ線（紺）の濃さ。既定0.3。強調時に上げる |
| `lows[i]` | 2段に割る用のもう1本（`visible`, `scale.y`, `material.color` を直接設定。上段は `meshes[i].position.y` を持ち上げる） |
| `outlines[i]` | 輪郭線。`geometry.setDrawRange(0, n)` で線が走る（`userData.n` が頂点数） |
| `setCam(s, vx=0, vw=W)` | カメラ `{theta, phi, dist, tx, tz}`（theta=方位、phi=天頂からの角、dist=縦に写る幅）。vx,vw はビューポート |
| `lerpCam(a, b, u)` | カメラ補間（u は `eio(...)` で ease-in-out） |
| `shiftCam(s, dx)` | 地図を画面上で右へ dx（ワールド単位）ずらす。左カラムに文字を置くときは +6〜+10 |
| `meanC(['都筑','青葉'])` | 区群の重心 [x,z]（カメラを寄せる先） |
| `renderView(vx, vw, sx=vx, sw=vw)` | ビューポート [vx, vx+vw] に描く。sx,sw はシザー（ワイプで一部だけ見せる） |
| `proj(x,y,z)` | ワールド → 画面座標（直前の setCam のビューポート基準） |
| `wardLabel3D(i, h, l1, l2, c2, a=1, left=false)` | 柱の上に「名前 ＋ 数字」ラベル（白縁つき）。left=true で左側に出す |
| `CAM0` | サイトと同じ既定の角度 `{theta:-0.35, phi:0.95, dist:34, tx:0, tz:1.5}` |

**左右分割（同じ角度で 2025｜2035）**:
```js
reset3D(); beginGL();
WD.forEach((w, i) => setPillar(i, hOf(w.disp24), rampDisp(w.disp24)));
setCam(CS, 0, W / 2); renderView(0, W / 2);                     // 左半分
WD.forEach((w, i) => setPillar(i, hOf(w.disp[2035]), divCol(wDiff35(w))));
setCam(CS, W / 2, W / 2); renderView(W / 2, W / 2);             // 右半分（同じ CS）
line(W / 2, 0, W / 2, H, COL.navy, 1.5);                         // 中央の分割線（2D）
```
中央からの縦ワイプは `renderView(W/2, W/2, W/2, (W/2)*u)`（シザー幅を 0→W/2）。分割時は `dist` を 44 前後に（半幅でも市全体が入る）。

## 6. 確認コマンド（`video/` で実行）

```bash
node scripts/render.mjs --frames 6600,6885,7170          # 静止画 → out/frames/f-XXXX.png（フレーム = 秒×30）
node scripts/render.mjs --scale 0.5 --start 6510 --end 8490   # 章の下書き動画（out/video-only.mp4 を上書き）
node scripts/_probe.mjs 0.5     # 全編QA: 字幕22字超・チップ>3・安全マージン外の文字（OOB）・コンソールエラー
node scripts/_still.mjs         # 3秒以上ほぼ変化しない区間（章レール除く）を列挙
```
- 章の代表フレーム番号 = (開始秒 + lt) × 30。例: 第6章 lt=12.5 → (217+12.5)×30 = 6885。
- 静止画は必ず Read で目視し、文字のはみ出し・重なり・意図と違う動きを直す。`[pageerror]` / `[console]` エラーは0に（`GL Driver Message … GPU stall due to ReadPixels` は Chromium のスクリーンショット時の性能警告で、無視してよい）。
- 本番レンダ（`node scripts/render.mjs`、約13,050フレーム）は統括が実行する。
- 描画時間の目安（実測）: 2D 章 約85ms/フレーム、3D 章 約210ms/フレーム（PNG 書き出し込み）。

## 7. 複数の章を並列で作るときの注意
- 触ってよいのは自分の `src/chapters/chNN.js` だけ。lib.js に足したい関数は章ファイル内に閉じて書き、共通化は統括に提案する。
- 3D シーン（`meshes` など）は全章で共有。必ず毎フレーム `reset3D()` から始め、マテリアルの色・不透明度・`position.y` を自分で設定する（前の章の状態に頼らない）。
- 第2〜10章の試作（旧デザイン方針で作ったもの）が `src/reference/scene-monolith.html` にある（`CH.push({...})` 形式）。移植するなら `name→title`, `len→duration`, `gl→uses3D`, `draw(lt)→draw(ctx, lt, t)` に置き換え、章専用の定数を IIFE の中へ移す。
