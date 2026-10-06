/* 第7章 — 結果④ 密度と到着、不搬送。契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * (a) 1.4–15.6  散布図: 出場密度（件/km²、対数）× 到着時間。点が密度の低い順に現れ、右下がりの回帰線
 * (b) 16–32.6   3D: 柱が2段に割れる（2.8s）→ ほどけて 2D の横積み上げ棒（不搬送率の高い順）→ 中区・西区・港北区を赤で強調
 * (c) 33.4–49.2 市全体の不搬送率の推移 2013→2024（2020–21年は網掛け） */
(() => {
  const DENS = WD.map((w) => w.disp24 / w.area);                 // 出場密度（件/km²）
  const ARR = WD.map((w) => w.arrive);
  const LD = DENS.map((v) => Math.log(v));
  const [FA, FB] = fit(LD, ARR);                                  // 到着 = a + b·ln(密度)
  const ORD_D = WD.map((w, i) => i).sort((a, b) => DENS[a] - DENS[b]);
  const rankD = []; ORD_D.forEach((i, k) => { rankD[i] = k; });
  const NT = DATA.nonTransport, NT_SUM = Object.values(NT).reduce((a, b) => a + b, 0);
  const DECLINE = Math.floor(NT['辞退'] / NT_SUM * 10);            // 8（割）
  const pct0 = (v) => `${Math.round(v * 100)}%`;
  const h7 = (w) => 0.3 + (w.unitDisp / 23000) * 6;              // 区内の隊の出場件数 → 柱の高さ
  const CA = { theta: 0.45, phi: 1.12, dist: 30, tx: 0.5, tz: 1.0 };
  // (a) 点の出方: 区ごと 0.05s の遅れ、18点が 1.2s 以内に出そろう
  const P_T0 = 1.9, P_STEP = 0.05, P_D = 0.35, P_END = P_T0 + 17 * P_STEP + P_D;   // 3.1
  // (b) 3D → 2D 横積み上げ棒
  const PALE = ramp(RAMPS.disp, 0.2);                             // 薄い色＝運ばなかった
  const HOT = ['中', '西', '港北'];                               // 赤で強調する区
  const ORD_NT = WD.map((w, i) => i).sort((a, b) => WD[b].nonTr - WD[a].nonTr);   // 不搬送率の高い順
  const B_T0 = 18.8, B_STEP = 0.03, B_D = 1.0;                    // ほどけ始め・行ごとの遅れ・移動時間（cubic-out）
  const B3_END = B_T0 + 17 * B_STEP + B_D;                        // 3D を描くのはここまで（以降は 2D のみ）
  const BX0 = 966, BH = 24, UMAX = Math.max(...WD.map((w) => w.unitDisp));
  const BW = (v) => (v / UMAX) * 740;                             // 件数 → 棒の長さ
  const rowY = (k) => 190 + k * 37;                               // 行の上端（18行: 190〜853）
  const NTY = (y) => nonTrYear(y) * 100;
  const K_CITY = ORD_NT.findIndex((i) => WD[i].nonTr * 100 < NTY(2024));   // 市全体の不搬送率を下回る最初の行

  window.CHAPTERS[7] = {
    title: '結果④ 密度と到着、不搬送',
    q: '速さと「運ばない出場」は？',
    concl: '都心は速いが、運ばない出場が多い',
    duration: 50,
    subs: [[1.6, 8.0, '件数が密な区ほど、早く着く'], [8.4, 15.4, '到着時間＝119番から現場に着くまで'], [16.6, 23.0, '薄い色＝運ばなかった出場'], [23.4, 32.4, '運ばない出場は都心に集中'], [33.6, 40.6, '出場の5件に1件は、運ばない'], [41.0, 48.8, '2022年に跳ね上がり、高止まり']],
    uses3D: (lt) => lt >= 16 && lt < B3_END,
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── (a) 散布図 ───────────────────────────── */
      phase(lt, 1.4, 15.6, () => {
        const C = { x0: 900, x1: 1760, y0: 220, y1: 760 };
        const L0 = Math.log(350), L1 = Math.log(1700);
        C.X = (v) => lerp(C.x0, C.x1, (Math.log(v) - L0) / (L1 - L0));
        C.Y = (v) => lerp(C.y1, C.y0, (v - 6) / 4);
        axes(lt, 1.4, C, [[400, '400'], [600, '600'], [1000, '1,000'], [1500, '1,500件/km²']], [[6, '6分'], [7, '7分'], [8, '8分'], [9, '9分'], [10, '10分']]);
        wtext(lt, 1.8, null, '横：1km²あたりの出場件数（対数目盛）　縦：現場に着くまでの平均', C.x0, 190, { size: 20, c: COL.sub });
        // 市平均の補助線（6.4〜）
        const mu = E.outCubic(P(lt, 6.4, 0.9)), my = C.Y(DATA.cityArrive);
        if (mu > 0) line(C.x0, my, lerp(C.x0, C.x1, mu), my, COL.faint, 1.5, [6, 6]);
        wtext(lt, 7.0, null, `市平均 ${DATA.cityArrive.toFixed(1)}分`, C.x1, my - 12, { size: 20, c: COL.sub, align: 'right' });
        // 回帰線（右下がり）: 点が出そろった直後に走る
        const fu = E.outCubic(P(lt, P_END, 1.2)), v0 = 370, v1 = 1650;
        if (fu > 0) {
          const ve = Math.exp(lerp(Math.log(v0), Math.log(v1), fu));
          line(C.X(v0), C.Y(FA + FB * Math.log(v0)), C.X(ve), C.Y(FA + FB * Math.log(ve)), COL.navy, 2, [10, 7]);
        }
        // 点: 密度の低い順に、区ごと 0.05s ずつ遅れて伸びる（18点が 1.2s 以内に出そろう）。中区と保土ケ谷区以外を薄く
        const dim = E.inOut(P(lt, 10.2, 0.8));
        const red = E.inOut(P(lt, 4.6, 0.4));
        WD.forEach((w, i) => {
          const u = E.outCubic(P(lt, P_T0 + rankD[i] * P_STEP, P_D));
          if (u <= 0) return;
          const key = w.name === '中' || w.name === '保土ケ谷';
          withAlpha(key ? 1 : 1 - 0.7 * dim, () => dot(C.X(DENS[i]), C.Y(ARR[i]), 9 * u, key ? mix(COL.navy, COL.red, red) : COL.navy));
        });
        // 最も遅い区と最も速い区を赤い点線で結ぶ（11.8〜）
        const ku = E.outCubic(P(lt, 11.8, 1.2));
        if (ku > 0) { const ia = WI['保土ケ谷'], ib = WI['中']; const xa = C.X(DENS[ia]), ya = C.Y(ARR[ia]), xb = C.X(DENS[ib]), yb = C.Y(ARR[ib]); line(xa, ya, lerp(xa, xb, ku), lerp(ya, yb, ku), COL.red, 1.5, [4, 5]); }
        // ラベル（保土ケ谷区・中区・西区）
        [['保土ケ谷', 4.8, 18, -14], ['中', 5.1, 18, 8], ['西', 3.6, -18, -14]].forEach(([n, t0, dx, dy]) => {
          const i = WI[n];
          const s = `${wn(n)} ${ARR[i].toFixed(1)}分`;
          withAlpha(n === '西' ? 1 - 0.7 * dim : 1, () => wtext(lt, t0, null, s, C.X(DENS[i]) + dx, C.Y(ARR[i]) + dy, { size: 20, c: COL.ink, align: dx < 0 ? 'right' : 'left' }));
        });
        wtext(lt, 1.6, null, '出場の密度と到着時間', LX, 240, { size: 48 });
        wtext(lt, 1.9, null, '横：1km²あたりの出場件数\n縦：119番から現場に着くまで', LX, 330, { size: 28, lead: 44 });
      }, [0, 140, W, 720]);
      chip(lt, 3.6, 15.6, '密な区ほど速い', LX, 520, { c: COL.navy });
      chip(lt, 4.8, 15.6, `保土ケ谷区 ${ward('保土ケ谷').arrive.toFixed(1)}分／中区 ${ward('中').arrive.toFixed(1)}分`, LX, 572, { c: COL.red });
      chip(lt, 6.8, 15.6, `市平均 ${DATA.cityArrive.toFixed(1)}分・2.7km`, LX, 624, { c: COL.navy });

      /* ── (b) 3D の2段の柱（16〜18.8）→ ほどけて 2D の横積み上げ棒（18.8〜32.6） ── */
      if (lt >= 16 && lt < 33.4) {
        const in3D = lt < B3_END;
        const starts = [];                                           // 各区の柱の画面上の位置（ほどける前）
        if (in3D) {
          reset3D(); beginGL();
          const split = E.outCubic(P(lt, 17.4, 1.0));
          const gap = 0.3 * split;
          const hs = [];
          WD.forEach((w, i) => {
            const h = h7(w) * E.outCubic(P(lt, 16.0 + rankN[i] * 0.04, 0.8));
            hs[i] = h;
            if (h <= 0.002) return;
            const hl = h * w.nonTr * split;
            const m = meshes[i], lo = lows[i];
            setPillar(i, Math.max(0.002, h - hl), '#3a5f99');
            m.position.y = hl + gap;
            if (hl > 0.002) {
              lo.visible = true; lo.scale.y = hl; lo.position.y = 0;
              lo.material.opacity = 1; lo.material.depthWrite = true; lo.castShadow = true;
              lo.material.color.set(PALE);
              lo.userData.line.material.opacity = 0.45;
            }
          });
          setCam(shiftCam({ ...CA, theta: CA.theta + 0.004 * (lt - 16) }, 8)); renderView(0, W);
          WD.forEach((w, i) => {
            const [x, z] = C3[i], h = hs[i] || 0.002, hl = h * w.nonTr * split;
            const b = proj(x, 0, z), m = proj(x, hl, z), tp = proj(x, h + gap, z);
            starts[i] = { x: b[0], yB: b[1], yM: m[1], yT: tp[1] };
          });
          // 3D を背景色で覆っていく（棒がほどけるのと同時に）
          const fa = E.inOut(P(lt, B_T0, 0.7));
          if (fa > 0) withAlpha(fa, () => { g.fillStyle = COL.bg; g.fillRect(0, 0, W, H); });
        }
        // 2D の横積み上げ棒（不搬送率の高い順）
        const em = E.inOut(P(lt, 21.0, 0.8));                       // 中区・西区・港北区を赤で強調
        wtext(lt, 19.8, 32.4, '区内の隊の出場件数', BX0, 168, { size: 20, c: COL.sub });
        wtext(lt, 20.2, 32.4, '不搬送率', RX1, 168, { size: 20, c: COL.sub, align: 'right' });
        ORD_NT.forEach((i, k) => {
          const w = WD[i], u = E.outCubic(P(lt, B_T0 + k * B_STEP, B_D));
          if (u <= 0 && !in3D) return;
          const hot = HOT.includes(w.name), e = hot ? em : 0;
          const ry = rowY(k), lT = BW(w.unitDisp * (1 - w.nonTr)), lN = BW(w.unitDisp * w.nonTr);
          const navy = mix('#3a5f99', COL.navy, u), pale = mix(PALE, COL.red, e);
          if (u < 1) {
            if (!starts[i] || u <= 0) return;                         // ほどける前は 3D の柱がそのまま見えている
            // 縦の柱（上＝運んだ、下＝運ばなかった）→ 横の棒（左＝運んだ、右＝運ばなかった）
            const s = starts[i], wv = 16;
            const rT = [s.x - wv / 2, s.yT, wv, s.yM - s.yT], rN = [s.x - wv / 2, s.yM, wv, s.yB - s.yM];
            const eT = [BX0, ry, lT, BH], eN = [BX0 + lT, ry, lN, BH];
            // 動き: 位置は cubic-out で行へ、高さは前半で棒の太さに、長さは後半に伸びる
            const pr = P(lt, B_T0 + k * B_STEP, B_D);
            const uh = E.outCubic(clamp(pr / 0.5)), uw = E.outCubic(clamp((pr - 0.25) / 0.75));
            const ax = lerp(rT[0], eT[0], u), aw = lerp(rT[2], eT[2], uw);
            const a = [ax, lerp(rT[1], eT[1], u), aw, lerp(rT[3], eT[3], uh)];
            const b = [lerp(rN[0], ax + aw, u), lerp(rN[1], eN[1], u), lerp(rN[2], eN[2], uw), lerp(rN[3], eN[3], uh)];
            g.fillStyle = navy; g.fillRect(a[0], a[1], a[2], Math.max(1, a[3]));
            g.fillStyle = pale; g.fillRect(b[0], b[1], b[2], Math.max(1, b[3]));
          } else {
            g.fillStyle = navy; g.fillRect(BX0, ry, lT, BH);
            g.fillStyle = pale; g.fillRect(BX0 + lT, ry, lN, BH);
          }
          const tc = hot ? mix(COL.ink, COL.red, e) : COL.ink;
          wtext(lt, B_T0 + 0.5 + k * B_STEP, 32.4, wn(w), BX0 - 14, ry + BH / 2 + 7, { size: 20, c: tc, align: 'right' });
          wtext(lt, B_T0 + 0.8 + k * B_STEP, 32.4, pct0(w.nonTr), RX1, ry + BH / 2 + 7, { size: 20, tab: true, c: hot ? mix(COL.sub, COL.red, e) : COL.sub, align: 'right' });
        });
        // 市全体の不搬送率の位置に点線（27.0〜）: ここより上の区は市全体より高い
        if (!in3D) {
          const yS = rowY(K_CITY) - 6.5, su = E.outCubic(P(lt, 27.0, 1.0)) * (1 - E.inOut(P(lt, 32.4, 0.35)));
          if (su > 0) line(BX0 - 120, yS, lerp(BX0 - 120, RX1, su), yS, COL.sub, 1.5, [6, 6]);
          wtext(lt, 27.4, 32.4, `市全体 ${NTY(2024).toFixed(1)}%`, RX1 - 70, yS - 8, { size: 20, c: COL.sub, align: 'right', halo: 5 });
          // 上位3区の赤い括弧（29.4〜）
          const bu = E.outCubic(P(lt, 29.4, 0.8)) * (1 - E.inOut(P(lt, 32.4, 0.35)));
          if (bu > 0) { const xb = BX0 - 112, y0 = rowY(0), y1 = rowY(2) + BH; line(xb, y0, xb, lerp(y0, y1, bu), COL.red, 2); line(xb, y0, xb + 8, y0, COL.red, 2); if (bu > 0.98) line(xb, y1, xb + 8, y1, COL.red, 2); }
        }
        // 左カラム
        wtext(lt, 16.4, 32.4, '運ばない出場', LX, 240, { size: 48 });
        wtext(lt, 16.7, 32.4, '区内の隊の出場件数を2つに分ける\n紺＝運んだ\n薄い色＝運ばなかった', LX, 330, { size: 28, lead: 44 });
        chip(lt, 19.4, 32.4, '不搬送＝出場したが運ばなかった', LX, 520, { c: COL.grey });
        chip(lt, 21.4, 32.4, `${wn('中')} ${pct0(ward('中').nonTr)}、${wn('西')} ${pct0(ward('西').nonTr)}、${wn('泉')} ${pct0(ward('泉').nonTr)}`, LX, 572, { c: COL.red });
        chip(lt, 25.0, 32.4, `理由の${DECLINE}割は本人の辞退`, LX, 624, { c: COL.navy });
      }

      /* ── (c) 不搬送率の推移 ───────────────────── */
      if (lt >= 32.6) {
        bgWipe(lt, 32.6);
        if (lt < 33.4) return;
        const C = { x0: 900, x1: 1760, y0: 220, y1: 760 };
        C.X = (y) => lerp(C.x0, C.x1, (y - 2013) / 11);
        C.Y = (v) => lerp(C.y1, C.y0, (v - 10) / 14);
        // 2020–21年の網掛け（線より先に、薄く）
        const su = E.outCubic(P(lt, 36.8, 0.7));
        if (su > 0) {
          const xa = C.X(2019.5), xb = C.X(2021.5);
          clipRect(xa, C.y0, (xb - xa) * su, C.y1 - C.y0, () => {
            g.fillStyle = '#eaeef4'; g.fillRect(xa, C.y0, xb - xa, C.y1 - C.y0);
            g.save(); g.strokeStyle = '#d6dde7'; g.lineWidth = 1;
            for (let k = -600; k < 300; k += 14) { g.beginPath(); g.moveTo(xa + k, C.y1); g.lineTo(xa + k + 540, C.y0); g.stroke(); }
            g.restore();
          });
          wtext(lt, 37.2, null, 'コロナ禍', (xa + xb) / 2, C.y0 + 30, { size: 20, c: COL.sub, align: 'center' });
        }
        axes(lt, 33.4, C, [[2013, '2013'], [2016, '2016'], [2019, '2019'], [2022, '2022'], [2024, '2024']], [[10, '10%'], [15, '15%'], [20, '20%']]);
        const pts = TR.years.map((y) => [C.X(y), C.Y(NTY(y))]);
        polyline(pts, E.inOut(P(lt, 34.0, 2.4)), COL.navy, 3.5);
        // 2021→2022 の跳ね上がりを赤で上書き（41.2〜）
        const ju = E.outCubic(P(lt, 41.2, 0.8));
        if (ju > 0) polyline([pts[8], pts[9]], ju, COL.red, 5);
        // 2013年の水準（44〜）と、2024年との差の縦線（45.6〜）
        const bu = E.outCubic(P(lt, 43.0, 1.0)), by = C.Y(NTY(2013));
        if (bu > 0) line(C.x0, by, lerp(C.x0, C.x1, bu), by, COL.faint, 1.5, [6, 6]);
        wtext(lt, 43.6, null, '2013年の水準', C.X(2016), by + 30, { size: 20, c: COL.sub, align: 'center' });
        const vu = E.outCubic(P(lt, 44.6, 0.8)), p24 = pts[11];
        if (vu > 0) line(p24[0], by, p24[0], lerp(by, p24[1] + 8, vu), COL.red, 1.5, [3, 4]);
        // 2022→2024 の高止まりを赤でなぞる（46.6〜）
        const pu = E.outCubic(P(lt, 45.6, 1.0));
        if (pu > 0) polyline([pts[9], pts[10], pts[11]], pu, COL.red, 5);
        wtext(lt, 46.8, null, '高止まり', C.X(2023), C.Y(NTY(2023)) + 44, { size: 20, c: COL.red, align: 'center' });
        [2013, 2019, 2022, 2024].forEach((y) => {
          const tt = 34.0 + 2.4 * (y - 2013) / 11;
          if (lt < tt) return;
          const p = [C.X(y), C.Y(NTY(y))], last = y === 2024;
          dot(p[0], p[1], 6, last || (y === 2022 && ju > 0) ? COL.red : COL.navy);
          const al = last || y === 2019 ? 'right' : y === 2013 ? 'left' : 'center';
          const dx = last ? 10 : y === 2019 ? -12 : y === 2013 ? 8 : 0;
          wtext(lt, tt, null, `${NTY(y).toFixed(1)}%`, p[0] + dx, p[1] - 20, { size: 28, tab: true, align: al, c: last ? COL.red : COL.ink });
        });
        wtext(lt, 33.6, null, '市全体の不搬送率', LX, 240, { size: 28, c: COL.sub });
        wtext(lt, 34.0, null, `${NTY(2024).toFixed(1)}%`, LX, 380, { size: 120, tab: true, c: COL.red });
        wtext(lt, 34.6, null, '2024年。出場のおよそ5件に1件', LX, 450, { size: 28 });
        wtext(lt, 36.0, null, `2013年は ${NTY(2013).toFixed(1)}%`, LX, 520, { size: 28, c: COL.sub });
        chip(lt, 38.4, 51, '不搬送＝出場したが運ばなかった', LX, 590, { c: COL.grey });
      }
    },
  };
})();
