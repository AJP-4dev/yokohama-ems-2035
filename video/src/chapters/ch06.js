/* 第6章 結果③ どこで（見せ場: 3D地図）— 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 0〜47.6s: 3D（2025｜2035 の左右分割 → 柱が伸びる → 増減率の色 → 北部へ寄る → 南西部へ → 全景）
 * 46.6s〜: 2D の小地図2枚（人口の増減率｜出場の増減率） */
(() => {
  /* ── 章専用の定数（すべて DATA から） ── */
  const NORTH = ['都筑', '青葉', '港北'];            // 寄る区（ラベルを出す）
  const NORTH_PD = ['都筑', '青葉'];                 // 人口が減る北部の区
  const SW = ['栄', '瀬谷', '旭'];
  const NC = meanC(NORTH), SWC = meanC(SW), NWC = meanC([...NORTH, '西']);
  const D35 = SC.A(2035);                            // 276,360
  const e3Up = (n) => (ward(n).pop[2035].e3 / ward(n).pop[2025].e3 - 1) * 100;
  const dN = pctRange(NORTH.map((n) => wDiff35(ward(n))));        // [12.0, 12.8]
  const e3N = pctRange(NORTH_PD.map(e3Up));                        // [55, 60]
  const pdS = pctRange(SW.map((n) => wPopDiff35(ward(n))));        // [7.9, 10.8]
  const dsS = pctRange(SW.map((n) => wDiff35(ward(n))));           // [0.5, 1.5]
  const NISHI = ward('西');
  const POP_DOWN = WD.map((w, i) => i).filter((i) => wPopDiff35(WD[i]) < 0).sort((a, b) => rankX[a] - rankX[b]);
  const DISP_DOWN = WD.filter((w) => wDiff35(w) < 0).length;
  const mapCol = (v) => rampDiv(v, 14, -12);         // 2D 小地図の共通の物差し（−12%〜+14%）

  /* ── カメラ（すべて t の関数） ── */
  const C0 = { theta: -0.35, phi: 0.95, dist: 36, tx: 0, tz: 1.0 };
  const CF = shiftCam(C0, 7);                                        // 全画面（左に文字）
  const CS = { theta: -0.35, phi: 0.95, dist: 44, tx: 0, tz: 1.0 };  // 左右分割（同じ角度）
  const CO = shiftCam({ ...C0, dist: 38 }, 7.5);                     // 分割を閉じた直後
  const CN = shiftCam({ theta: -0.26, phi: 0.86, dist: 31, tx: NC[0], tz: NC[1] + 4.6 }, 8.5);
  const CNW = shiftCam({ theta: -0.22, phi: 0.86, dist: 33, tx: NWC[0], tz: NWC[1] + 4.0 }, 9);
  const CW = shiftCam({ theta: -0.46, phi: 0.86, dist: 34, tx: SWC[0], tz: SWC[1] + 1.2 }, 8.5);
  const CE = { ...C0, dist: 37 };                                    // 最後の全景（中央）

  function camAt(lt) {
    let c;
    if (lt < 14) c = { ...CS };
    else if (lt < 15.0) c = lerpCam(CS, CO, eio(lt, 14, 1.0));
    else if (lt < 23.6) c = lerpCam(CO, CN, eio(lt, 15.0, 1.5));
    else if (lt < 30.4) c = lerpCam(CN, CNW, eio(lt, 23.6, 1.4));
    else if (lt < 44.2) { const u = eio(lt, 30.4, 2.0); c = lerpCam(CNW, CW, u); c.dist += 9 * Math.sin(Math.PI * u); }  // 引いてから寄る
    else c = lerpCam(CW, CE, eio(lt, 44.2, 2.0));
    c.theta += 0.0035 * lt;                                          // 常にごくゆっくり回る（静止を作らない）
    return c;
  }

  // 柱の設定（side: 'L' = 2025, 'R' = 2035）
  function setSide(side, lt) {
    const grow = (i) => E.outCubic(P(lt, 6.0 + rankX[i] * 0.03, 1.2));
    const colU = E.inOut(P(lt, 11.0, 0.8));
    // 強調: 北部（16〜30.4）→ 南西部（32〜44.2）。他の区は半透明に
    const emN = Math.min(E.inOut(P(lt, 15.6, 0.8)), 1 - E.inOut(P(lt, 30.2, 0.7)));
    const emW = Math.min(E.inOut(P(lt, 23.8, 0.8)), 1 - E.inOut(P(lt, 30.2, 0.7)));
    const emS = Math.min(E.inOut(P(lt, 32.0, 0.8)), 1 - E.inOut(P(lt, 44.2, 0.8)));
    WD.forEach((w, i) => {
      if (side === 'L') { setPillar(i, hOf(w.disp24), rampDisp(w.disp24)); return; }
      const u = grow(i);
      const v = lerp(w.disp24, w.disp[2035], u);
      setPillar(i, hOf(v), rampDisp(v));
      if (colU > 0) setColorHSL(meshes[i].material, rampDisp(v), divCol(wDiff35(w)), colU);
      const focus = NORTH.includes(w.name) ? emN : w.name === '西' ? emW : SW.includes(w.name) ? emS : 0;
      const dim = Math.max(0.78 * emN, 0.45 * emS) * (1 - focus);   // 南西部は「赤い周囲の中の白」を見せるため薄くしすぎない
      if (dim > 0.001) {                                // 他を薄くする（不透明のまま淡い灰へ）
        meshes[i].material.color.lerp(tmpC2.set('#eef1f5'), dim);
        meshes[i].userData.line.material.opacity = 0.3 * (1 - 0.7 * dim);
      }
      if (focus > 0) meshes[i].userData.line.material.opacity = 0.3 + 0.6 * focus;
    });
    return { emN, emW, emS };
  }

  function draw3D(lt) {
    reset3D(); beginGL();
    const open = eio(lt, 5.0, 0.8), close = eio(lt, 14.0, 1.0);
    // 左（2025）: 全画面 → 左半分 → 閉じる
    const lvw = Math.max(2, lerp(W, W / 2, open));
    const lsw = lerp(lvw, 0, close);
    if (lsw > 1) {
      setSide('L', lt);
      const c = lerpCam(CF, CS, open); c.theta += 0.0035 * lt;
      setCam(c, 0, lvw); renderView(0, lvw, 0, lsw);
    }
    let em = { emN: 0, emW: 0, emS: 0 };
    if (lt >= 5.0) {
      em = setSide('R', lt);
      const vx = lerp(W / 2, 0, close), vw = W - vx;
      setCam(camAt(lt), vx, vw);
      const sw = lt < 5.8 ? (W / 2) * open : vw;          // 中央からの縦ワイプ
      renderView(vx, vw, vx, sw);
      // ラベル（寄った区だけ）
      const lab = (n, a, left) => { const i = WI[n], w = WD[i]; wardLabel3D(i, hOf(w.disp[2035]), n, `${sgn(wDiff35(w))}%`, COL.red, a, left); };
      if (em.emN > 0.01) { lab('都筑', em.emN, true); lab('青葉', em.emN, true); lab('港北', em.emN, false); }
      if (em.emW > 0.01) lab('西', em.emW, false);
      if (em.emS > 0.01) SW.forEach((n, k) => { const i = WI[n], w = WD[i]; wardLabel3D(i, hOf(w.disp[2035]), n, `${sgn(wDiff35(w))}%`, COL.ink, em.emS, n === '瀬谷'); });
    }
    // 中央の分割線（縦に走る）
    if (lt >= 5.0 && close < 1) { const lu = E.outCubic(P(lt, 5.0, 0.5)); const x = lerp(W / 2, 0, close); line(x, 130, x, 130 + 760 * lu, COL.navy, 1.5); }

    /* ── 文字 ── */
    // 1.2〜4.6: 2025 全画面
    phase(lt, 1.2, 4.6, () => {
      wtext(lt, 1.3, null, '2025年', LX, 240, { size: 48 });
      wtext(lt, 1.6, null, '柱の高さ＝出場件数\n（2024年実績）', LX, 330, { size: 28, lead: 44 });
    }, [0, 150, 790, 300]);
    // 5.4〜14: 分割の見出し（左右とも同じ位置関係）
    if (lt >= 5.4 && lt < 14.5) {
      wtext(lt, 5.4, 13.9, '2025年', LX, 200, { size: 48 });
      wtext(lt, 5.6, 13.9, '2024年実績', LX, 244, { size: 20, c: COL.sub });
      wtext(lt, 5.6, 13.9, `${fmt(D24)}件`, W / 2 - 40, 200, { size: 48, tab: true, align: 'right' });
      wtext(lt, 5.8, 13.9, '2035年', W / 2 + 40, 200, { size: 48, c: COL.red });
      wtext(lt, 6.0, 13.9, '人口変化のみ', W / 2 + 40, 244, { size: 20, c: COL.sub });
    }
    // 右上のカウンター（2035年の市全体）: 分割中は右半分の右上、閉じてからも右上に残る
    if (lt >= 5.8 && lt < 30.6) {
      const v = lerp(D24, D35, cnt(lt, 6.0, 1.6));
      wtext(lt, 5.8, 30.2, `${fmt(v)}件`, W - M, 200, { size: 48, c: COL.red, tab: true, align: 'right', halo: 6 });
      if (lt >= 14.6) wtext(lt, 14.6, 30.2, '2035年の市全体', W - M, 244, { size: 20, c: COL.sub, align: 'right', halo: 5 });
    }
    // 凡例（右下・小さく）
    if (lt >= 11.0 && lt < 46.6) {
      const lu = E.outCubic(P(lt, 11.0, 0.6)), x0 = W - M - 360, y0 = 846;
      wipe(lu, x0 - 6, y0 - 34, 372, 84, () => {
        text('2024年比の増減率', x0, y0 - 12, { size: 20, c: COL.sub, halo: 5 });
        for (let k = 0; k < 36; k++) { g.fillStyle = divCol(-5 + (20 * k) / 35); g.fillRect(x0 + k * 10, y0, 10, 12); }
        text('−5%', x0, y0 + 36, { size: 20, num: true, c: COL.sub, halo: 5 });
        text('0%', x0 + 90, y0 + 36, { size: 20, num: true, c: COL.sub, align: 'center', halo: 5 });
        text('+15%', x0 + 360, y0 + 36, { size: 20, num: true, c: COL.sub, align: 'right', halo: 5 });
      });
    }
    // 北部（16〜30.4）
    phase(lt, 16.2, 30.2, () => {
      wtext(lt, 16.3, null, '北部', LX, 240, { size: 48 });
      wtext(lt, 16.6, null, '都筑と青葉は人口が減るのに\n出場は1割以上増える', LX, 330, { size: 28, lead: 44 });
    }, [0, 150, 790, 300]);
    chip(lt, 17.2, 30.2, `${NORTH.join('、')}：出場 +${Math.round(dN[0])}〜${Math.round(dN[1])}%`, LX, 520, { c: COL.red });
    chip(lt, 20.6, 30.2, `理由：85歳以上が${Math.floor(e3N[0] / 10)}〜${Math.round(e3N[1] / 10)}割増える（都筑、青葉）`, LX, 572, { c: COL.purple });
    chip(lt, 24.2, 30.2, `西区は人口 ${sgn(wPopDiff35(NISHI))}%、出場 ${sgn(wDiff35(NISHI))}%`, LX, 624, { c: COL.navy });
    // 南西部（32〜44.2）
    phase(lt, 32.4, 44.2, () => {
      wtext(lt, 32.5, null, '南西部', LX, 240, { size: 48 });
      wtext(lt, 32.8, null, '人口は1割近く減るのに\n出場はほぼ減らない', LX, 330, { size: 28, lead: 44 });
    }, [0, 150, 790, 300]);
    chip(lt, 33.4, 44.2, `${SW.join('、')}：人口 −${Math.round(pdS[0])}〜${Math.round(pdS[1])}%`, LX, 520, { c: COL.green });
    chip(lt, 35.8, 44.2, `それでも出場は横ばい（+${dsS[0].toFixed(1)}〜${dsS[1].toFixed(1)}%）`, LX, 572, { c: COL.red });
    chip(lt, 38.4, 44.2, '高齢化が人口減を打ち消す', LX, 624, { c: COL.purple });
  }

  function draw2D(lt) {
    bgWipe(lt, 46.6, 0.9);                        // 3D → 2D（背景が左→右に覆う）
    if (lt < 47.5) return;
    wtext(lt, 47.8, null, '人口と救急の増減', LX, 240, { size: 48 });
    wtext(lt, 48.2, null, '2025→2035年\n同じ色の物差しで18区を並べる', LX, 330, { size: 28, lead: 44 });
    // 区の数（DATA から数える）
    wtext(lt, 52.0, null, '人口が減る区', LX, 520, { size: 28, c: COL.sub });
    wtext(lt, 52.0, null, `${Math.round(POP_DOWN.length * cnt(lt, 52.2, 1.2))}区`, LX, 650, { size: 120, c: COL.green, tab: true });
    wtext(lt, 54.0, null, '出場が減る区', LX + 360, 520, { size: 28, c: COL.sub });
    wtext(lt, 54.0, null, `${DISP_DOWN}区`, LX + 360, 650, { size: 120, c: COL.red, tab: true });

    const boxes = [{ x: 820, y: 236, w: 480, h: 540 }, { x: 1360, y: 236, w: 480, h: 540 }];
    const vals = [(w) => wPopDiff35(w), (w) => wDiff35(w)];
    const titles = ['人口の増減', '出場の増減'];
    // 人口が減る区を1つずつ、両方の地図で同時に縁取る（56.6〜64.8）
    const step = 8.2 / POP_DOWN.length;
    const k = Math.floor((lt - 56.6) / step);
    const hi = lt >= 56.6 && k < POP_DOWN.length ? POP_DOWN[k] : -1;
    const ha = hi >= 0 ? win(lt, 56.6 + k * step, 56.6 + (k + 1) * step, 0.15) : 0;
    boxes.forEach((b, m) => {
      const t0 = 48.0 + m * 1.0;
      wtext(lt, t0, null, titles[m], b.x, 200, { size: 28, c: m ? COL.red : COL.navy });
      const u = E.outCubic(P(lt, t0 + 0.2, 1.2));
      wipe(u, b.x - 10, b.y - 10, b.w + 20, b.h + 20, () => {
        const xf = drawMap(b, (w) => mapCol(vals[m](w)));
        if (ha > 0) withAlpha(ha, () => {
          const w = WD[hi];
          g.beginPath(); w.rings[0].forEach((p, j) => { const [x, y] = xf.f(p[0], p[1]); if (j) g.lineTo(x, y); else g.moveTo(x, y); });
          g.closePath(); g.strokeStyle = COL.navy; g.lineWidth = 3; g.lineJoin = 'round'; g.stroke();
          const [cx, cy] = wardC(xf, w);
          text(`${sgn(vals[m](w))}%`, cx, cy + 7, { size: 20, num: true, align: 'center', halo: 5, c: COL.ink });
        });
      });
    });
    // 共通の凡例（右下）
    const lu = E.outCubic(P(lt, 50.0, 0.6)), x0 = W - M - 416, y0 = 846;
    wipe(lu, x0 - 6, y0 - 34, 428, 84, () => {
      text('2025年比（出場は2024年比）', x0, y0 - 12, { size: 20, c: COL.sub });
      for (let q = 0; q < 52; q++) { g.fillStyle = mapCol(-12 + (26 * q) / 51); g.fillRect(x0 + q * 8, y0, 8, 12); }
      text('−12%', x0, y0 + 36, { size: 20, num: true, c: COL.sub });
      text('0%', x0 + (12 / 26) * 416, y0 + 36, { size: 20, num: true, c: COL.sub, align: 'center' });
      text('+14%', x0 + 416, y0 + 36, { size: 20, num: true, c: COL.sub, align: 'right' });
    });
  }

  window.CHAPTERS[6] = {
    title: '結果③ どこで',
    q: '増えるのは、どこ？',
    concl: '北部と都心で増え、南西部は横ばい',
    duration: 66,
    subs: [
      [1.6, 4.8, '柱の高さ＝区ごとの出場件数'],
      [6.2, 10.6, '2035年、ほぼ全区で柱が伸びる'],
      [11.0, 15.6, '色＝2024年からの増減率'],
      [17.0, 23.0, '伸びるのは北部'],
      [23.4, 30.0, '若い街が一斉に歳を取る'],
      [33.0, 38.6, '南西部は人口減と高齢化が相殺'],
      [39.0, 44.0, '住む人は減っても、運ばれる人は減らない'],
      [48.4, 56.0, '左＝人口、右＝出場。同じ物差し'],
      [56.6, 65.0, '人口が減っても、救急は減らない'],
    ],
    uses3D: (lt) => lt < 47.6,
    setup(ctx) {},
    draw(ctx, lt, t) {
      if (lt < 47.6) draw3D(lt);
      if (lt >= 46.6) draw2D(lt);
    },
  };
})();
