/* 第1章 — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。 */
(() => {
  const POP_S = YEARS.map((y) => [y, cityPop(y)]);
  const DSP_S = [[2024, D24], ...YEARS.map((y) => [y, SC.A(y)])];
  window.CHAPTERS[1] = {
    title: '問い', q: '人口が減れば、救急も減る？', concl: '人口が減っても、救急は増える', duration: 19,
    subs: [[1.6, 6.0, '人口は減る。救急も減る？'], [6.4, 10.8, '答えは、増える'], [11.4, 17.8, '人口が減るのに、件数は増える']],
    setup(ctx) {},
    draw(ctx, lt, t) {
      const m = eio(lt, 11, 1.8);                       // 2枚→1枚に重なる
      const A = { x: 800, y: 300, w: 470, h: 400 }, B = { x: 1370, y: 300, w: 470, h: 400 }, MG = { x: 800, y: 240, w: 880, h: 520 };
      const xr = (r, y0, y1, y) => r.x + (y - y0) / (y1 - y0) * r.w;
      const yr = (r, lo, hi, v) => r.y + r.h - (v - lo) / (hi - lo) * r.h;
      const idxY = (v) => yr(MG, 93, 111, v);
      const popPts = POP_S.map(([y, v]) => [lerp(xr(A, 2025, 2040, y), xr(MG, 2024, 2040, y), m), lerp(yr(A, 3.50e6, 3.82e6, v), idxY(v / cityPop(2025) * 100), m)]);
      const dspPts = DSP_S.map(([y, v]) => [lerp(xr(B, 2024, 2040, y), xr(MG, 2024, 2040, y), m), lerp(yr(B, 2.40e5, 2.88e5, v), idxY(v / D24 * 100), m)]);
      // 軸（細い補助線）
      const ax = E.outCubic(P(lt, 1.3, 0.6));
      if (m < 1) withAlpha(1, () => {
        line(A.x, A.y + A.h, A.x + A.w * ax, A.y + A.h, COL.line, 1);
        line(B.x, B.y + B.h, B.x + B.w * ax, B.y + B.h, COL.line, 1);
      });
      phase(lt, 1.3, 10.6, () => {
        wtext(lt, 1.3, null, '市の人口', A.x, A.y - 40, { size: 28, c: COL.navy });
        wtext(lt, 1.3, null, '救急出場', B.x, B.y - 40, { size: 28, c: COL.red });
        wtext(lt, 1.5, null, '2025', A.x, A.y + A.h + 36, { size: 20, tab: true, c: COL.sub });
        wtext(lt, 1.5, null, '2040', A.x + A.w, A.y + A.h + 36, { size: 20, tab: true, c: COL.sub, align: 'right' });
        wtext(lt, 1.5, null, '2024', B.x, B.y + B.h + 36, { size: 20, tab: true, c: COL.sub });
        wtext(lt, 1.5, null, '2040', B.x + B.w, B.y + B.h + 36, { size: 20, tab: true, c: COL.sub, align: 'right' });
      }, [790, 200, 1060, 600]);
      if (m > 0) {
        const y100 = idxY(100);
        line(MG.x, y100, MG.x + MG.w * m, y100, COL.line, 1, [6, 6]);
        wtext(lt, 12.6, null, '2024〜25年の水準', MG.x, y100 + 34, { size: 20, c: COL.sub });
        const x35 = xr(MG, 2024, 2040, 2035), ru = E.outCubic(P(lt, 13, 0.6));
        if (ru > 0) line(x35, MG.y + MG.h, x35, lerp(MG.y + MG.h, MG.y, ru), COL.line, 1);
        wtext(lt, 13, null, '2035年', x35, MG.y + MG.h + 36, { size: 20, c: COL.sub, align: 'center' });
      }
      const u = E.outCubic(P(lt, 1.4, 2.2));
      polyline(popPts, u, COL.navy, 4);
      polyline(dspPts, u, COL.red, 4);
      // 静止を避ける: 線の上を小さな点が年をなぞる（4〜10.6s）、重なった後は2035年の差を示す破線がゆっくり伸び縮みせず、点がにじむ（14〜17.8s）
      if (lt >= 4 && lt < 10.6) {
        const v = Math.min(1, Math.max(0, (lt - 4) / 6.2));
        const ip = Math.min(popPts.length - 1, Math.round(v * (popPts.length - 1))), id = Math.min(dspPts.length - 1, Math.round(v * (dspPts.length - 1)));
        dot(popPts[ip][0], popPts[ip][1], 7, COL.navy); dot(dspPts[id][0], dspPts[id][1], 7, COL.red);
      }
      if (lt >= 14.2) {
        const v = ((lt - 14.2) % 1.8) / 1.8, d35 = dspPts[11];
        withAlpha(0.5 * (1 - v), () => { g.strokeStyle = COL.red; g.lineWidth = 2; g.beginPath(); g.arc(d35[0], d35[1], 8 + 22 * v, 0, Math.PI * 2); g.stroke(); });
      }
      if (m > 0) {
        const pe = popPts[popPts.length - 1], de = dspPts[dspPts.length - 1];
        wtext(lt, 13.2, null, '人口', pe[0] + 14, pe[1] + 8, { size: 20, c: COL.navy });
        wtext(lt, 13.2, null, '救急出場', de[0] + 14, de[1] + 8, { size: 20, c: COL.red });
        // ×印が開く: 2035年の点で上下の差を示す
        const p35 = popPts[10], d35 = dspPts[11];
        const ou = E.outCubic(P(lt, 13.4, 0.8));
        if (ou > 0) { dot(p35[0], p35[1], 7 * ou, COL.navy); dot(d35[0], d35[1], 7 * ou, COL.red); line(p35[0], p35[1], p35[0], lerp(p35[1], d35[1], ou), COL.ink, 1, [3, 4]); }
      }
      // 左カラム
      phase(lt, 1.4, 10.6, () => {
        wtext(lt, 1.6, null, '市の人口（2025→2040年、市の推計）', LX, 300, { size: 20, c: COL.sub });
        wtext(lt, 1.8, null, `${man(cityPop(2025))}人 → ${man(cityPop(2040))}人`, LX, 366, { size: 48, tab: true });
        wtext(lt, 2.6, null, '救急出場（2024年実績→2040年、人口変化のみ）', LX, 470, { size: 20, c: COL.sub });
        wtext(lt, 2.8, null, `${fmt(D24)}件 → ${fmt(SC.A(2040))}件`, LX, 536, { size: 48, tab: true, c: COL.red });
      }, [0, 200, 790, 400]);
      wtext(lt, 11.4, null, '2035年の変化', LX, 300, { size: 28, c: COL.sub });
      wtext(lt, 11.8, null, `人口 ${sgn((cityPop(2035) / cityPop(2025) - 1) * 100)}%`, LX, 380, { size: 48 });
      wtext(lt, 12.6, null, '救急出場', LX, 480, { size: 28 });
      wtext(lt, 12.8, null, `${sgn((SC.A(2035) / D24 - 1) * 100)}%`, LX, 610, { size: 120, w: 600, tab: true, c: COL.red });
      wtext(lt, 13.6, null, '人口は2025年、出場は2024年実績との比較', LX, 680, { size: 20, c: COL.sub });
    },
  };
})();
