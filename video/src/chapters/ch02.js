/* 第2章 データの出どころ — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 見せる動き: 5枚の資料カードが「罫線が一周して」着地する。残りは強調の切替と、線が走って計算へ集まるだけ。終盤は保持＋点の輪のみ。 */
(() => {
  // 資料カード [資料名, 使い道, 意味色]（色: 紺=人口、赤=出場件数、橙=昼）
  const SRC = [
    ['横浜市 将来人口推計（令和5年・中位）', '使い道：区ごと、年齢ごとの将来の人口', COL.navy],
    ['横浜市消防局 消防年報（平成25〜令和6年）', '使い道：出場件数と年齢別の搬送人員', COL.red],
    ['令和2年 国勢調査', '使い道：昼間人口（通勤や通学で入ってくる人）', COL.orange],
    ['国土地理院 面積調', '使い道：区の面積（1km²あたりの出場件数に）', COL.navy],
    ['総務省 住民基本台帳', '使い道：毎年の年齢別人口（搬送率の推移に）', COL.navy],
  ];
  const T_IN = [1.6, 3.4, 5.2, 7.0, 8.8];                 // 着地の時刻
  const CX = 800, CW = 760, CH = 116, CY = (k) => 176 + k * 136;
  // 薄くする区間（強調で他を薄くする）
  const DIM = [
    [[3.4, 9.6], [15.0, 20.2]],
    [[5.2, 9.6], [15.0, 20.2]],
    [[7.0, 14.8]],
    [[8.8, 14.8]],
    [[9.6, 14.8]],
  ];
  // 左の説明に合わせた控えめな強調: 該当カードの左端の縦線（意味色）が 4px→10px に太る
  const EMPH = [[[9.8, 14.4]], [[11.0, 14.4]], [[15.2, 19.8]], [[16.6, 19.8]], [[18.0, 19.8]]];
  const emph = (k, lt) => Math.max(0, ...EMPH[k].map(([a, b]) => E.outCubic(P(lt, a, 0.4)) * (1 - E.outCubic(P(lt, b - 0.4, 0.4)))));
  const alphaOf = (k, lt) => 1 - 0.58 * Math.max(0, ...DIM[k].map(([a, b]) => win(lt, a, b, 0.4)));
  // 矩形の罫線が左上から時計回りに走る
  const boxRun = (u, x, y, w, h, c, lw) => polyline([[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]], u, c, lw);
  const BUS = 1610, NODE = [1660, CY(2) + CH / 2];

  window.CHAPTERS[2] = {
    title: 'データの出どころ',
    q: '何を材料にした？',
    concl: '材料はすべて公開資料',
    duration: 28,
    subs: [[1.6, 8.8, '材料は、5つの公開資料'], [9.4, 14.6, '人口は市の推計、救急は消防年報'], [15.0, 20.0, '残る3つは、国の公開資料'], [20.4, 27.0, '全部、公開されている資料']],
    uses3D: () => false,
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── 左カラム ── */
      wtext(lt, 1.4, null, '5つの公開資料', LX, 320, { size: 48 });
      rule(lt, 1.6, LX, 352, 420, COL.navy, 1);
      const L = [0, 300, 790, 560];
      phase(lt, 1.4, 9.0, () => {
        wtext(lt, 1.9, null, '人口の資料が3つ、\n救急の資料が1つ、\n面積の資料が1つ', LX, 420, { size: 28, lead: 48 });
      }, L);
      phase(lt, 9.6, 14.4, () => {
        wtext(lt, 9.6, null, '横浜市の資料', LX, 410, { size: 20, c: COL.sub });
        wtext(lt, 9.8, null, '将来の人口は、\n市の推計をそのまま使う', LX, 462, { size: 28, lead: 44 });
        wtext(lt, 11.0, null, `救急の実績は、\n消防年報の${TR.years.length}年分`, LX, 580, { size: 28, lead: 44 });
      }, L);
      phase(lt, 15.0, 19.8, () => {
        wtext(lt, 15.0, null, '国の資料', LX, 410, { size: 20, c: COL.sub });
        wtext(lt, 15.2, null, '昼の人口は国勢調査、', LX, 462, { size: 28 });
        wtext(lt, 16.6, null, '面積は国土地理院、', LX, 506, { size: 28 });
        wtext(lt, 18.0, null, '毎年の年齢別人口は\n住民基本台帳', LX, 550, { size: 28, lead: 44 });
      }, L);
      wtext(lt, 20.4, null, '出典の詳細は\nサイトの「方法」タブに', LX, 462, { size: 28, lead: 44 });

      /* ── 右: 資料カード ── */
      SRC.forEach(([t1, t2, c], k) => {
        const t0 = T_IN[k], y = CY(k);
        if (lt < t0) return;
        withAlpha(alphaOf(k, lt), () => {
          // 地（白）はマスクワイプ、罫線は一周して閉じる
          const fu = E.outCubic(P(lt, t0, 0.7));
          wipe(fu, CX, y, CW, CH, () => { g.fillStyle = COL.paper; g.fillRect(CX, y, CW, CH); });
          boxRun(E.outCubic(P(lt, t0, 0.9)), CX, y, CW, CH, COL.navy, 1);
          const bu = E.outCubic(P(lt, t0 + 0.2, 0.4));
          if (bu > 0) { const bw = 4 + 6 * emph(k, lt); g.fillStyle = c; g.fillRect(CX, y + CH * (1 - bu), bw, CH * bu); }
          wtext(lt, t0 + 0.25, null, String(k + 1).padStart(2, '0'), CX + 28, y + 52, { size: 20, tab: true, c: COL.sub });
          wtext(lt, t0 + 0.3, null, t1, CX + 80, y + 52, { size: 28, w: 800 });
          wtext(lt, t0 + 0.55, null, t2, CX + 80, y + 90, { size: 20, c: COL.sub });
        });
      });


      /* ── 20.6〜: 5本の線が右へ走り、1点に集まる（計算の材料になる） ── */
      SRC.forEach(([, , c], k) => {
        const y = CY(k) + CH / 2, u = E.outCubic(P(lt, 20.6 + k * 0.12, 0.6));
        if (u <= 0) return;
        line(CX + CW, y, lerp(CX + CW, BUS, u), y, COL.navy, 1.5);
        const v = E.inOut(P(lt, 21.2 + k * 0.12, 0.6));
        if (v > 0) line(BUS, y, BUS, lerp(y, NODE[1], v), COL.navy, 1.5);
      });
      const nu = E.outCubic(P(lt, 21.9, 0.5));
      if (nu > 0) { line(BUS, NODE[1], lerp(BUS, NODE[0], nu), NODE[1], COL.navy, 1.5); if (nu > 0.95) dot(NODE[0], NODE[1], 7, COL.navy); }
      wtext(lt, 22.2, null, '区ごとの\n計算へ', NODE[0] + 18, NODE[1] - 4, { size: 20, lead: 30 });

      /* ── 22.6〜: 全体を静かに保持。微かな動きは1つだけ＝集まった点から細い輪がゆっくり広がる ── */
      if (lt >= 22.6) {
        const v = ((lt - 22.6) % 2.2) / 2.2;
        withAlpha(0.45 * (1 - v), () => { g.strokeStyle = COL.navy; g.lineWidth = 1.5; g.beginPath(); g.arc(NODE[0], NODE[1], 9 + 16 * v, 0, Math.PI * 2); g.stroke(); });
      }
    },
  };
})();
