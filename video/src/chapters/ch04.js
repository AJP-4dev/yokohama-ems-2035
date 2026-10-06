/* 第4章 結果① 市全体 — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 見せる動き: 実績線が2024で止まり、そこから4本の推計線が伸びる（左カラムで2035年の値がカウンターで回る）。 */
(() => {
  // 実績: 1985〜2010 は5年おき（DATA.series）、2013〜2024 は消防年報の毎年値
  const HIST = [...DATA.series.filter(([y]) => y < 2013), ...TR.years.map((y) => [y, TR.dispatch[y]])];
  // [キー, 名前, 色, 破線, 意味（チップ）]
  const SCN = [
    ['A', '人口変化のみ', COL.navy, null, '1人あたりの利用は今のまま'],
    ['M', '緩やかな利用増', COL.orange, null, '利用の増え方が半分に鈍る'],
    ['B', '利用増が続く', COL.red, null, 'ここ10年の増え方が続く'],
    ['T', '年代別トレンド', COL.purple, [10, 8], '年代ごとの増え方をそのまま延ばす'],
  ];
  const V35 = {}; SCN.forEach(([k]) => { V35[k] = SC[k](2035); });
  const pA = (V35.A / D24 - 1) * 100, pT = (V35.T / D24 - 1) * 100;
  // グラフ領域（右）
  const C = { x0: 900, x1: 1790, y0: 190, y1: 800 };
  // 横軸は実績を描き終えたあと 1985–2040 → 2010–2040 に寄る（推計の部分を広く見せる）
  let XS = 1985;
  const X = (y) => lerp(C.x0, C.x1, (y - XS) / (2040 - XS));
  const Y = (v) => lerp(C.y1, C.y0, v / 400000);
  const VAL = {}; SCN.forEach(([k]) => { VAL[k] = [[2024, D24], ...YEARS.map((y) => [y, SC[k](y)])]; });
  const T0 = (i) => 5.8 + i * 1.3;                  // 推計線 i の描き始め
  // 強調区間: [開始, 終了, 対象キー]
  const FOCUS = [[11.0, 17.2, 'A'], [17.4, 23.2, 'T'], [23.4, 26.8, 'A'], [26.8, 30.2, 'M'], [30.2, 33.6, 'B'], [33.6, 37.0, 'T']];
  const CHIPT = { A: [23.4, 29.0], M: [26.8, 32.4], B: [30.2, 35.8], T: [33.6, 39.2] };
  const ROWY = (i) => 340 + i * 112;

  window.CHAPTERS[4] = {
    title: '結果① 市全体',
    q: '2035年、市全体で何件？',
    concl: `2035年は、少なくとも${man(SC.A(2035))}件`,
    duration: 46,
    subs: [[1.6, 5.6, '1985年からの実績。ずっと増えてきた'], [6.0, 10.6, '2024年から先は、4つのシナリオ'], [11.0, 17.0, '人口は2.3%減っても、出場は7.8%増'], [17.4, 23.0, '利用の増え方しだいで、最大31%増'],
      [23.4, 37.0, '線の違いは、1人あたりの利用の増え方'], [37.4, 45.0, 'どのシナリオでも、今より多い']],
    setup(ctx) {},
    draw(ctx, lt, t) {
      XS = lerp(1985, 2010, eio(lt, 4.4, 1.3));
      const PTS = {}; SCN.forEach(([k]) => { PTS[k] = VAL[k].map(([y, v]) => [X(y), Y(v)]); });
      const fo = FOCUS.find(([a, b]) => lt >= a && lt < b);
      const focus = fo ? fo[2] : null;
      // 強調の切替は 0.3s で滑らかに（他を薄くする）
      const dimOf = (k) => {
        let d = 0;
        FOCUS.forEach(([a, b, f]) => { if (f !== k) d = Math.max(d, Math.min(E.inOut(P(lt, a, 0.3)), 1 - E.inOut(P(lt, b, 0.3)))); });
        return d;
      };
      const alOf = (k) => 1 - 0.78 * dimOf(k);

      /* ── 右: 軸 ── */
      const gu = E.outCubic(P(lt, 1.2, 0.6));
      [100000, 200000, 300000, 400000].forEach((v) => {
        if (gu > 0) line(C.x0, Y(v), lerp(C.x0, C.x1, gu), Y(v), COL.grid, 1);
        wtext(lt, 1.3, null, `${v / 10000}万`, C.x0 - 14, Y(v) + 7, { size: 20, c: COL.faint, align: 'right' });
      });
      if (gu > 0) line(C.x0, C.y1, lerp(C.x0, C.x1, gu), C.y1, COL.navy, 1);
      clipRect(C.x0 - 40, C.y1 + 4, C.x1 - C.x0 + 80, 50, () => {
        [1985, 2000, 2024, 2040].forEach((y) => wtext(lt, 1.4, null, `${y}`, X(y), C.y1 + 34, { size: 20, tab: true, c: COL.sub, align: 'center' }));
        wtext(lt, 5.4, null, '2010', X(2010), C.y1 + 34, { size: 20, tab: true, c: COL.sub, align: 'center' });
      });
      // 実績｜推計 の境（2024）
      const bu = E.outCubic(P(lt, 4.3, 0.6));
      if (bu > 0) line(X(2024), C.y1, X(2024), lerp(C.y1, C.y0, bu), COL.grey, 1, [4, 5]);
      wtext(lt, 4.5, null, '実績', X(2024) - 12, C.y0 + 4, { size: 20, c: COL.sub, align: 'right' });
      wtext(lt, 4.7, null, '推計', X(2024) + 12, C.y0 + 4, { size: 20, c: COL.sub });
      // 2035 の縦線
      const x35 = X(2035), ru = E.outCubic(P(lt, 5.8, 0.6));
      if (ru > 0) line(x35, C.y1, x35, lerp(C.y1, C.y0 + 30, ru), COL.line, 1, [4, 5]);
      wtext(lt, 6.0, null, '2035', x35, C.y1 + 34, { size: 20, tab: true, c: COL.sub, align: 'center' });

      // 幅（人口変化のみ〜年代別トレンド）の淡い帯: 20.0s から左→右に満ちる
      const fu = E.outCubic(P(lt, 20.0, 1.2));
      if (fu > 0) {
        const xe = lerp(X(2024), X(2040), fu);
        clipRect(X(2024), C.y0, xe - X(2024), C.y1 - C.y0, () => {
          g.beginPath();
          PTS.T.forEach(([x, y], j) => (j ? g.lineTo(x, y) : g.moveTo(x, y)));
          [...PTS.A].reverse().forEach(([x, y]) => g.lineTo(x, y));
          g.closePath(); g.fillStyle = 'rgba(142,59,143,0.07)'; g.fill();
        });
      }
      // 2024年の水準: +7.8% の基準として破線が2040まで走る（以後残る）
      const lu = E.outCubic(P(lt, 13.2, 1.2));
      if (lu > 0) line(X(2024), Y(D24), lerp(X(2024), X(2040), lu), Y(D24), COL.sub, 1.5, [6, 6]);
      wtext(lt, 14.6, null, '2024年の水準', X(2040), Y(D24) + 30, { size: 20, c: COL.sub, align: 'right' });

      /* ── 右: 実績線 ── */
      clipRect(C.x0 - 4, C.y0 - 10, C.x1 - C.x0 + 8, C.y1 - C.y0 + 14, () => withAlpha(focus ? 0.45 : 1, () => polyline(HIST.map(([y, v]) => [X(y), Y(v)]), E.inOut(P(lt, 1.4, 3.0)), COL.sub, 3)));
      if (lt > 4.3) dot(X(2024), Y(D24), 6 * E.outBack(P(lt, 4.3, 0.4)), COL.sub);
      wtext(lt, 4.3, 10.6, `2024年 ${fmt(D24)}件`, X(2024) - 16, Y(D24) - 22, { size: 20, tab: true, c: COL.sub, align: 'right' });
      wtext(lt, 1.8, 3.9, `1985年 ${fmt(HIST[0][1])}件`, X(1985) + 12, Y(HIST[0][1]) + 44, { size: 20, tab: true, c: COL.sub });

      /* ── 右: 推計線（見せる動き） ── */
      SCN.forEach(([k, , c, dash], i) => {
        const t0 = T0(i);
        withAlpha(alOf(k), () => {
          polyline(PTS[k], E.outCubic(P(lt, t0, 1.1)), c, 3.5, dash);
          if (lt > t0 + 0.9) dot(x35, Y(V35[k]), (focus === k ? 8 : 6) * E.outBack(P(lt, t0 + 0.9, 0.4)), c);
        });
      });
      // 2035年の増分ブラケット（2024年の水準から）
      const bracket = (t0, t1, v, c, label) => {
        const u = E.outCubic(P(lt, t0, 0.7)), out = E.inOut(P(lt, t1, 0.35));
        if (u <= 0 || out >= 1) return;
        const bx = x35 + 18, ya = Y(D24), yb = lerp(ya, Y(v), u);
        withAlpha(1 - out, () => {
          line(bx, ya, bx, yb, c, 2); line(bx - 6, ya, bx + 6, ya, c, 2); line(bx - 6, yb, bx + 6, yb, c, 2);
        });
        wtext(lt, t0 + 0.5, t1, label, bx + 14, (ya + Y(v)) / 2 + 10, { size: 28, tab: true, c, halo: 6, haloC: COL.bg });
      };
      bracket(11.4, 17.0, V35.A, COL.navy, `${sgn(pA)}%`);
      bracket(17.8, 23.0, V35.T, COL.purple, `${sgn(pT, 0)}%`);
      // 終盤: 2035年の幅（人口変化のみ〜年代別トレンド）を紺の縦線で
      const ru2 = E.outCubic(P(lt, 38.0, 0.9));
      if (ru2 > 0) {
        const bx = x35 + 18, ya = Y(V35.A), yb = lerp(ya, Y(V35.T), ru2);
        line(bx, ya, bx, yb, COL.navy, 2); line(bx - 6, ya, bx + 6, ya, COL.navy, 2); line(bx - 6, yb, bx + 6, yb, COL.navy, 2);
      }

      /* ── 左カラム ── */
      wtext(lt, 4.4, null, '2035年の出場件数', LX, 220, { size: 48 });
      wtext(lt, 5.4, 10.8, '4つのシナリオで推計', LX, 268, { size: 20, c: COL.sub });
      wtext(lt, 11.2, 23.0, `2024年比 人口変化のみで ${sgn(pA)}%（人口は ${sgn((cityPop(2035) / cityPop(2025) - 1) * 100)}%）`, LX, 268, { size: 20, c: COL.sub }, null);
      wtext(lt, 23.4, null, '色＝シナリオ。点＝2035年の値', LX, 268, { size: 20, c: COL.sub });
      SCN.forEach(([k, name, c, dash, mean], i) => {
        const t0 = T0(i) + 0.8, y = ROWY(i);
        withAlpha(dimOf(k) > 0 ? 1 - 0.55 * dimOf(k) : 1, () => {
          rule(lt, t0, LX, y + 70, LW, COL.line, 1);
          const su = E.outCubic(P(lt, t0, 0.5));
          if (su > 0) line(LX, y - 10, LX + 36 * su, y - 10, c, 4, dash ? [7, 5] : null);
          wtext(lt, t0, null, name, LX + 52, y, { size: 28 });
          if (lt > t0 + 0.1) numText(`${counter(lt, t0 + 0.1, V35[k])}件`, LX + LW, y + 4, { size: 48, align: 'right', c: k === 'A' ? COL.navy : COL.ink });
        });
        chip(lt, CHIPT[k][0], CHIPT[k][1], mean, LX + 52, y + 18, { c });
      });
      // 終盤のまとめ
      wtext(lt, 40.6, null, `2035年は ${man(V35.A)}〜${man(V35.T)}件`, LX, 820, { size: 28 });
      rule(lt, 42.2, LX, 846, tw(`2035年は ${man(V35.A)}〜${man(V35.T)}件`, 28), COL.navy, 2, 1.0);
    },
  };
})();
