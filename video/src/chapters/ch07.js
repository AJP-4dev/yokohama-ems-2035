/* 第7章 — 結果④ 密度と到着、不搬送。契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * (a) 1.4–15.6  散布図: 出場密度（件/km²、対数）× 到着時間。点が密度の低い順に現れ、右下がりの回帰線
 * (b) 16–33.6   3D: 柱が2段に割れる（上＝運んだ、下＝運ばなかった＝薄い色）→ 都心（中・西）を強調
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
  const CORE = ['中', '西'];
  const CA = { theta: 0.45, phi: 1.12, dist: 30, tx: 0.5, tz: 1.0 };
  const nc = meanC(CORE);
  const CB = { theta: 0.62, phi: 0.98, dist: 27, tx: nc[0] - 2.5, tz: nc[1] - 2.0 };
  const NTY = (y) => nonTrYear(y) * 100;

  window.CHAPTERS[7] = {
    title: '結果④ 密度と到着、不搬送',
    q: '速さと「運ばない出場」は？',
    concl: '都心は速いが、運ばない出場が多い',
    duration: 50,
    subs: [[1.6, 8.0, '件数が密な区ほど、早く着く'], [8.4, 15.4, '到着時間＝119番から現場に着くまで'], [16.6, 23.0, '下の段＝運ばなかった出場'], [23.4, 32.4, '運ばない出場は都心に集中'], [33.6, 40.6, '出場の5件に1件は、運ばない'], [41.0, 48.8, '2022年に跳ね上がり、高止まり']],
    uses3D: (lt) => lt >= 16 && lt < 33.6,
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
        // 市平均の補助線（10.6〜）
        const mu = E.outCubic(P(lt, 10.6, 0.9)), my = C.Y(DATA.cityArrive);
        if (mu > 0) line(C.x0, my, lerp(C.x0, C.x1, mu), my, COL.faint, 1.5, [6, 6]);
        wtext(lt, 11.2, null, `市平均 ${DATA.cityArrive.toFixed(1)}分`, C.x1, my - 12, { size: 20, c: COL.sub, align: 'right' });
        // 回帰線（右下がり）
        const fu = E.outCubic(P(lt, 6.0, 1.2)), v0 = 370, v1 = 1650;
        if (fu > 0) {
          const ve = Math.exp(lerp(Math.log(v0), Math.log(v1), fu));
          line(C.X(v0), C.Y(FA + FB * Math.log(v0)), C.X(ve), C.Y(FA + FB * Math.log(ve)), COL.navy, 2, [10, 7]);
        }
        // 点: 密度の低い順に伸びて現れる。13.4〜 中と保土ケ谷以外を薄く
        const dim = E.inOut(P(lt, 13.2, 0.8));
        WD.forEach((w, i) => {
          const u = E.outCubic(P(lt, 2.0 + rankD[i] * 0.2, 0.45));
          if (u <= 0) return;
          const key = w.name === '中' || w.name === '保土ケ谷';
          withAlpha(key ? 1 : 1 - 0.7 * dim, () => dot(C.X(DENS[i]), C.Y(ARR[i]), 9 * u, key && lt > 8.4 ? COL.red : COL.navy));
        });
        // ラベル（保土ケ谷・中・西）
        [['保土ケ谷', 8.6, 18, -14], ['中', 8.9, 18, 8], ['西', 5.6, -18, -14]].forEach(([n, t0, dx, dy]) => {
          const i = WI[n];
          const s = `${n} ${ARR[i].toFixed(1)}分`;
          withAlpha(n === '西' ? 1 - 0.7 * dim : 1, () => wtext(lt, t0, null, s, C.X(DENS[i]) + dx, C.Y(ARR[i]) + dy, { size: 20, c: COL.ink, align: dx < 0 ? 'right' : 'left' }));
        });
        wtext(lt, 1.6, null, '出場の密度と到着時間', LX, 240, { size: 48 });
        wtext(lt, 1.9, null, '横：1km²あたりの出場件数\n縦：119番から現場に着くまで', LX, 330, { size: 28, lead: 44 });
      }, [0, 140, W, 720]);
      chip(lt, 6.4, 15.6, '密な区ほど速い', LX, 520, { c: COL.navy });
      chip(lt, 8.6, 15.6, `保土ケ谷 ${ward('保土ケ谷').arrive.toFixed(1)}分／中 ${ward('中').arrive.toFixed(1)}分`, LX, 572, { c: COL.red });
      chip(lt, 10.8, 15.6, `市平均 ${DATA.cityArrive.toFixed(1)}分・2.7km`, LX, 624, { c: COL.navy });

      /* ── (b) 3D: 柱が2段に割れる ───────────────── */
      if (lt >= 16 && lt < 33.6) {
        reset3D(); beginGL();
        const split = E.outCubic(P(lt, 18.4, 1.2));
        const gap = 0.3 * split;
        const em = E.inOut(P(lt, 23.4, 1.0));                        // 都心の強調
        WD.forEach((w, i) => {
          const h = h7(w) * E.outCubic(P(lt, 16.2 + rankN[i] * 0.06, 1.0));
          if (h <= 0.002) return;
          const hl = h * w.nonTr * split;
          const core = CORE.includes(w.name);
          const fk = core ? 0 : 0.72 * em;
          const m = meshes[i], lo = lows[i];
          setPillar(i, Math.max(0.002, h - hl), mix('#3a5f99', '#e9edf2', fk));
          m.position.y = hl + gap;
          m.userData.line.material.opacity = 0.3 * (1 - 0.6 * fk);
          if (hl > 0.002) {
            lo.visible = true; lo.scale.y = hl; lo.position.y = 0;
            lo.material.opacity = 1; lo.material.depthWrite = true; lo.castShadow = true;
            const pale = ramp(RAMPS.disp, 0.2);    // 薄い色＝運ばなかった
            lo.material.color.set(core ? mix(pale, COL.red, em) : mix(pale, '#f1f3f6', fk));
            lo.userData.line.material.opacity = (core ? 0.45 : 0.45 * (1 - 0.6 * fk));
          }
        });
        // 割れると同時に、区どうしが少し離れる（重心を中心に縮める）→ 下の段が隣の区に隠れない
        const sh = 1 - 0.1 * split;
        const shrink = (m, i, k) => { m.scale.x = k; m.scale.z = k; m.position.x = C3[i][0] * (1 - k); m.position.z = C3[i][1] * (1 - k); };
        WD.forEach((w, i) => { shrink(meshes[i], i, sh); shrink(lows[i], i, sh); });
        const base = lerpCam(CA, CB, eio(lt, 23.4, 2.2));
        const s = shiftCam({ ...base, theta: base.theta + 0.004 * (lt - 16) }, lerp(8, 5.2, eio(lt, 23.4, 2.2)));
        setCam(s); renderView(0, W);
        // reset3D は x/z を戻さないので、描いた直後に元へ（他の章に持ち越さない）
        WD.forEach((w, i) => { shrink(meshes[i], i, 1); shrink(lows[i], i, 1); });
        // 中区の手前の角に「運んだ／運ばなかった」の引き出し線（19.8〜）
        const ni = WI['中'], nw = WD[ni];
        let best = null;
        nw.rings[0].forEach((p) => {
          const [x, z] = px(p[0], p[1]);
          const X = C3[ni][0] + (x - C3[ni][0]) * sh, Z = C3[ni][1] + (z - C3[ni][1]) * sh;
          const q = proj(X, 0, Z);
          if (!best || q[1] > best.q[1]) best = { X, Z, q };
        });
        const hN = h7(nw) * E.outCubic(P(lt, 16.2 + rankN[ni] * 0.06, 1.0)), hlN = hN * nw.nonTr * split;
        const lead = (t0, yW, s, c) => {
          const u = E.outCubic(P(lt, t0, 0.5)) * (1 - E.inOut(P(lt, 32.4, 0.35)));
          if (u <= 0) return;
          const [qx, qy] = proj(best.X, yW, best.Z);
          line(qx + 6, qy, qx + 6 + 70 * u, qy, COL.navy, 1);
          dot(qx + 6, qy, 3, COL.navy);
          wtext(lt, t0 + 0.2, 32.4, s, qx + 84, qy + 7, { size: 20, c, halo: 5 });
        };
        if (split > 0.5) {
          lead(19.8, hlN / 2, '運ばなかった', COL.ink);
          lead(20.4, hlN + gap + (hN - hlN) / 2, '運んだ', COL.ink);
        }
        // ラベル
        [['中', 24.6], ['西', 25.0], ['泉', 26.6]].forEach(([n, t0]) => {
          const i = WI[n], w = WD[i];
          const a = E.outCubic(P(lt, t0, 0.5));
          if (a > 0) wardLabel3D(i, h7(w) + 0.24, n, pct0(w.nonTr), CORE.includes(n) ? COL.red : COL.ink, a, n === '西');
        });
        // 左カラム（3D の上に白地なしで置く）
        wtext(lt, 16.4, 32.4, '運ばない出場', LX, 240, { size: 48 });
        wtext(lt, 16.7, 32.4, '柱＝区内の隊の出場件数\n上の段＝運んだ\n下の段（薄い色）＝運ばなかった', LX, 330, { size: 28, lead: 44 });
        chip(lt, 19.6, 32.4, '不搬送＝出場したが運ばなかった', LX, 520, { c: COL.grey });
        chip(lt, 24.6, 32.4, `中 ${pct0(ward('中').nonTr)}、西 ${pct0(ward('西').nonTr)}、泉 ${pct0(ward('泉').nonTr)}`, LX, 572, { c: COL.red });
        chip(lt, 27.6, 32.4, `理由の${DECLINE}割は本人の辞退`, LX, 624, { c: COL.navy });
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
        chip(lt, 38.4, 49.2, '不搬送＝出場したが運ばなかった', LX, 590, { c: COL.grey });
      }
    },
  };
})();
