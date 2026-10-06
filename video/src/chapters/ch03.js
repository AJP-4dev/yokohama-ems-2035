/* 第3章 どう計算したか — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 見せる動き: 上段の5ステップのフローが左→右へ組み上がる（線が走る）。各ステップの図は右に1つずつ。 */
(() => {
  // ステップの区間 [開始, 終了, フロー上のラベル]
  const ST = [[1.4, 10, '1 いまの人口'], [10, 20, '2 将来の人口'], [20, 32, '3 年齢別の搬送率'], [32, 42, '4 昼間の人'], [42, 52, '5 校正係数']];
  const OPS = ['', '×', '＋', '×'];                         // ノード k→k+1 の間の演算（2→3 が×、3→4 が＋、4→5 が×）
  const EX = 52;                                           // 都筑区の実例の開始
  const FY = 150, NX = (k) => LX + 16 + k * 356;                // フローの線の高さとノード位置
  const TZ = ward('都筑'), NISHI = ward('西');
  const TZ_EXP = TZ.disp[2035] / TZ.fac;                   // 校正前の出場（計算値）
  const TZ_TR = TZ_EXP / DATA.dispRatio;                   // 搬送相当（年齢別人口×搬送率＋昼間の人）
  const RATIO9 = Math.round(DATA.rates.e3 / DATA.rates.w); // 85歳以上 ÷ 15–64歳
  // 西区へ流れ込む矢印の出発区: 近い順に、方向が重ならないもの（30°以上離れる）を最大6つ
  const NEAR_NISHI = (() => {
    const c0 = C3[WI['西']], out = [], angs = [];
    WD.map((w, i) => i).filter((i) => WD[i].name !== '西')
      .sort((a, b) => Math.hypot(C3[a][0] - c0[0], C3[a][1] - c0[1]) - Math.hypot(C3[b][0] - c0[0], C3[b][1] - c0[1]))
      .forEach((i) => {
        const a = Math.atan2(C3[i][1] - c0[1], C3[i][0] - c0[0]);
        if (out.length < 6 && angs.every((b) => Math.abs(Math.atan2(Math.sin(a - b), Math.cos(a - b))) > 0.52)) { out.push(i); angs.push(a); }
      });
    return out;
  })();
  const popAt = (w, yv) => { const y0 = Math.floor(yv), y1 = Math.min(2040, y0 + 1), k = yv - y0; const o = {}; AGE.forEach((a) => { o[a] = lerp(w.pop[y0][a], w.pop[y1][a], k); }); return o; };
  const LBOX = [0, 250, 790, 660], RBOX = [RX0, 250, W - RX0, 660];

  // 左カラム: 見出し・言い換え・「なぜ？」チップ
  function left(lt, a, b, title, body, chipS, chipC, chipT = a + 3.0) {
    phase(lt, a, b - 0.4, () => {
      wtext(lt, a + 0.1, null, title, LX, 330, { size: 48 });
      wtext(lt, a + 0.5, null, body, LX, 410, { size: 28, lead: 44 });
    }, LBOX);
    if (chipS) chip(lt, chipT, b - 0.5, chipS, LX, 540, { c: chipC });
  }

  window.CHAPTERS[3] = {
    title: 'どう計算したか',
    q: 'どうやって計算した？',
    concl: '人口×搬送率×校正係数で区ごとに計算',
    duration: 64,
    subs: [[1.6, 9.6, 'まず、いまの人口を区×年齢で'], [10.4, 19.4, '市の推計で、年ごとの人口へ'], [20.4, 25.8, '年齢別の搬送率を掛ける'], [26.2, 31.6, '搬送率＝1年に救急車で運ばれる人の割合'], [32.4, 41.6, '通勤で入ってくる人のぶんを足す'], [42.4, 46.8, '実績に合わせる校正係数'], [47.2, 51.6, '人口では見えない事情を1つの倍率に'], [52.4, 57.0, '例：都筑区の2035年'], [57.4, 62.8, '1.236＝出場÷搬送（運ばない分を含む）']],
    uses3D: () => false,
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── 上段: 5ステップのフロー（左→右に組み上がる） ── */
      const act = ST.findIndex(([a, b]) => lt >= a && lt < b);   // 実例中は -1
      ST.forEach(([a], k) => {
        if (lt < a) return;
        if (k > 0) {
          // 前のノードから線が走って届く
          const u = E.outCubic(P(lt, a, 0.7));
          line(NX(k - 1) + 10, FY, lerp(NX(k - 1) + 10, NX(k) - 10, u), FY, COL.navy, 1.5);
          if (OPS[k - 1] && u > 0.6) text(OPS[k - 1], (NX(k - 1) + NX(k)) / 2, FY + 1, { size: 20, w: 800, align: 'center', base: 'middle', halo: 10, haloC: COL.bg, c: COL.navy });
        }
        const cur = k === act, on = E.outCubic(P(lt, a + (k ? 0.5 : 0), 0.3));
        if (on > 0) dot(NX(k), FY, (cur ? 8 : 6) * on, COL.navy);
        if (cur && on > 0) { g.beginPath(); g.arc(NX(k), FY, 15 * on, 0, Math.PI * 2); g.strokeStyle = COL.navy; g.lineWidth = 1; g.stroke(); }
        wtext(lt, a + (k ? 0.5 : 0), null, ST[k][2], NX(k) - 16, FY + 44, { size: 20, w: cur || act < 0 ? 800 : 600, c: cur || act < 0 ? COL.ink : COL.sub });
      });
      // 実例: 赤い印が 1→5 を順に走る（「順に掛ける」）
      const sw = E.inOut(P(lt, 59.6, 2.4));
      if (sw > 0 && sw < 1) { const x = lerp(NX(0), NX(4), sw); g.fillStyle = COL.red; g.fillRect(x - 6, FY - 6, 12, 12); }

      /* ── 左カラム ── */
      left(lt, 1.4, 10, '1  いまの人口', '区ごと、5歳刻みの\n年齢別人口（実績）');
      left(lt, 10, 20, '2  市の推計で将来へ', '市の将来人口推計\n（令和5年・中位）をそのまま', 'なぜ？ 区ごとに高齢化の速さが違うから', COL.purple, 13.4);
      left(lt, 20, 32, '3  年齢別の搬送率を掛ける', '搬送率＝1年に救急車で\n運ばれる人の割合', `なぜ年齢別？ 85歳以上は15–64歳の約${RATIO9}倍運ばれるから`, COL.purple, 24.4);
      left(lt, 32, 42, '4  昼間の人を足す', '通勤や通学で入ってくる\n人のぶんを足す（昼間補正）', 'なぜ？ 住んでいない人も倒れるから', COL.orange, 35.0);
      left(lt, 42, 52, '5  実績に合わせる', '校正係数＝計算と実績の\n差を埋める倍率', '人口では見えない事情＝病院、繁華街、観光をまとめて1つの倍率に', COL.red, 47.6);
      // 補足の1行（各ステップ後半の小さな動き）
      phase(lt, 2, 9.6, () => wtext(lt, 6.4, null, '18区 × 5つの年齢区分に集計', LX, 680, { size: 20, c: COL.sub }), LBOX);
      phase(lt, 20, 31.6, () => wtext(lt, 29.0, null, '人口 × 搬送率 ＝ 運ばれる人数', LX, 680, { size: 28 }), LBOX);
      phase(lt, 32, 41.6, () => {
        const s4 = `西区は、昼の人口が夜の${(NISHI.dn / 100).toFixed(1)}倍`;
        wtext(lt, 36.4, null, s4, LX, 670, { size: 28 });
        rule(lt, 36.6, LX, 690, tw(s4, 28), COL.orange, 2);
        wtext(lt, 38.4, null, '昼の人口＝住む人−出る人＋入る人', LX, 760, { size: 20, c: COL.sub });
      }, LBOX);
      phase(lt, EX, 64, () => {
        wtext(lt, EX + 0.1, null, '例：都筑区の2035年', LX, 330, { size: 48 });
        wtext(lt, EX + 0.5, null, '1から5を順に掛けると、\n2035年の出場件数になる', LX, 410, { size: 28, lead: 44 });
      }, LBOX);
      chip(lt, 60.2, 63.0, `2024年より ${sgn(wDiff35(TZ))}%`, LX, 540, { c: COL.red });

      /* ── 右: ステップ1・2 区×年齢の積み上げ棒（2025→2040） ── */
      phase(lt, 1.4, 19.6, () => {
        const yv = 2025 + 15 * eio(lt, 11, 7.2);
        const row = 30, y0 = 286, bx = 920, sc = 860 / 390000;
        // 目盛（10万人ごと）が走る
        [100000, 200000, 300000].forEach((v, k) => {
          const u = E.outCubic(P(lt, 4.4 + k * 0.15, 0.6));
          if (u > 0) line(bx + v * sc, y0 - 6, bx + v * sc, lerp(y0 - 6, y0 + 18 * row, u), COL.grid, 1);
          wtext(lt, 4.6 + k * 0.15, null, `${v / 10000}万人`, bx + v * sc, y0 - 16, { size: 20, c: COL.sub, align: 'center', tab: true });
        });
        const hi = win(lt, 6.6, 10.6, 0.5);              // 都筑を強調（他を薄く）
        WD.forEach((w, r) => {
          const y = y0 + r * row, gu = E.outCubic(P(lt, 1.6 + r * 0.06, 0.8));
          if (gu <= 0) return;
          const al = w === TZ ? 1 : 1 - 0.6 * hi;
          withAlpha(al, () => {
            text(w.name, bx - 14, y + 21, { size: 20, w: w === TZ && hi > 0.5 ? 800 : 600, c: COL.sub, align: 'right' });
            const p = popAt(w, yv); let x = bx;
            AGE.forEach((a) => { const ww = p[a] * sc * gu; g.fillStyle = AGEC[a]; g.fillRect(x, y + 4, Math.max(0, ww - 1), row - 10); x += ww; });
          });
        });
        // 都筑の総人口ラベル（実例への伏線）
        if (hi > 0) {
          const y = y0 + WI['都筑'] * row;
          wtext(lt, 6.8, 10.0, `${man(popT(TZ, 2025))}人`, bx + popT(TZ, 2025) * sc + 12, y + 21, { size: 20, tab: true });
        }
        // 凡例
        let lx = bx;
        AGE.forEach((a) => {
          wipe(E.outCubic(P(lt, 2.4, 0.6)), lx - 4, 852, 200, 36, () => { g.fillStyle = AGEC[a]; g.fillRect(lx, 862, 14, 14); });
          wtext(lt, 2.4, null, AGEL[a], lx + 22, 877, { size: 20, c: COL.sub });
          lx += 22 + tw(AGEL[a], 20) + 30;
        });
      }, RBOX);
      // ステップ2の年（左カラムで数える）
      phase(lt, 10.6, 19.6, () => {
        const yv = 2025 + 15 * eio(lt, 11, 7.2);
        wtext(lt, 10.6, null, `${Math.round(yv)}年`, LX, 760, { size: 120, w: 600, tab: true });
      }, LBOX);

      /* ── 右: ステップ3 搬送率の階段（85歳以上が最後に跳ねる） ── */
      phase(lt, 20, 31.6, () => {
        const base = 820, x0 = 880, gap = 170, bw = 120, hMax = 420, vmax = DATA.rates.e3 * 100;
        wtext(lt, 20.4, null, '人口100人あたり、1年に運ばれる人数', x0, 300, { size: 20, c: COL.sub });
        const bl = E.outCubic(P(lt, 20.4, 0.6));
        if (bl > 0) line(x0 - 20, base, lerp(x0 - 20, RX1, bl), base, COL.navy, 1);
        AGE.forEach((a, k) => {
          const v = DATA.rates[a] * 100, x = x0 + k * gap, h = hMax * v / vmax;
          const u = k === 4 ? E.outBack(P(lt, 22.6, 0.9)) : E.outCubic(P(lt, 20.8 + k * 0.35, 0.7));
          if (u <= 0) return;
          g.fillStyle = AGEC[a]; g.fillRect(x, base - h * u, bw, h * u);
          wtext(lt, 20.8 + k * 0.35, null, AGEL[a], x + bw / 2, base + 36, { size: 20, c: COL.sub, align: 'center' });
          const tl = k === 4 ? 23.3 : 21.3 + k * 0.35;
          wtext(lt, tl, null, `${v.toFixed(1)}人`, x + bw / 2, base - h - 16, { size: k === 4 ? 48 : 28, tab: true, align: 'center', c: k === 4 ? AGEC.e3 : COL.ink });
        });
        // 15–64歳の高さから85歳以上へ: 破線が走り、差が縦に伸びる
        const hw = hMax * DATA.rates.w * 100 / vmax, he = hMax;
        const xw = x0 + 1 * gap + bw, xe = x0 + 4 * gap;
        const du = E.outCubic(P(lt, 26.2, 0.9));
        if (du > 0) line(xw + 6, base - hw, lerp(xw + 6, xe + bw + 14, du), base - hw, COL.navy, 1, [5, 5]);
        const vu = E.outCubic(P(lt, 27.2, 0.9));
        if (vu > 0) arrow(xe + bw + 14, base - hw, xe + bw + 14, lerp(base - hw, base - he + 4, vu), COL.navy, 2, 10);
        wtext(lt, 27.8, null, `約${RATIO9}倍`, xe + bw + 26, base - (hw + he) / 2 + 10, { size: 28 });
      }, RBOX);

      /* ── 右: ステップ4 西区に人が流れ込む ── */
      phase(lt, 32, 41.6, () => {
        const box = { x: 900, y: 270, w: 900, h: 600 };
        const xf = mapXf(box), mu = E.outCubic(P(lt, 32.2, 0.9));
        wipe(mu, box.x - 40, box.y - 20, box.w + 80, box.h + 40, () => drawMap(box, (w) => (w === NISHI ? COL.orange : '#e3e8ef')));
        const [nx0, ny0] = wardC(xf, NISHI);
        NEAR_NISHI.forEach((i, k) => {
          const [cx, cy] = wardC(xf, WD[i]);
          // 隣の区の方向から、長さを揃えて流れ込む（隣接区は重心が近く矢印が短すぎるため）
          const dl = Math.hypot(cx - nx0, cy - ny0), L = Math.max(dl, 190);
          const sx = nx0 + (cx - nx0) / dl * L, sy = ny0 + (cy - ny0) / dl * L;
          const au = E.outCubic(P(lt, 33.4 + k * 0.25, 0.9));
          if (au <= 0) return;
          const ex = lerp(sx, nx0, 0.84 * au), ey = lerp(sy, ny0, 0.84 * au);
          arrow(sx, sy, ex, ey, COL.navy, 2.5, 12);
          // 白い点線が流れる（人の流れ）
          g.save(); g.setLineDash([3, 12]); g.lineDashOffset = -lt * 36; g.beginPath(); g.moveTo(sx, sy); g.lineTo(ex, ey); g.strokeStyle = '#ffffff'; g.lineWidth = 2.5; g.stroke(); g.restore();
          dot(sx, sy, 4, COL.navy);
        });
        wtext(lt, 32.8, null, '西', nx0, ny0 + 10, { size: 28, w: 800, align: 'center', halo: 6 });
      }, RBOX);

      /* ── 右: ステップ5 計算（灰）と実績（赤）の2本棒 → 倍率 ── */
      phase(lt, 42, 51.6, () => {
        const names = ['中', '西', '都筑'], bx = 980, sc = 640 / 19000;
        wtext(lt, 42.4, null, '計算＝人口から計算した件数、実績＝2024年の出場件数', RX0 + 40, 300, { size: 20, c: COL.sub });
        const hi = win(lt, 49.8, 52.4, 0.4);
        names.forEach((n, k) => {
          const w = ward(n), y = 350 + k * 170, t0 = 42.6 + k * 1.6;
          const calc = w.disp24 / w.fac, actv = w.disp24;
          withAlpha(n === '都筑' ? 1 : 1 - 0.6 * hi, () => {
            wtext(lt, t0, null, `${n}区`, RX0 + 40, y + 70, { size: 28, w: 800 });
            const u1 = E.outCubic(P(lt, t0 + 0.2, 0.8)), u2 = E.outCubic(P(lt, t0 + 1.0, 0.8));
            if (u1 > 0) { text('計算', bx - 14, y + 42, { size: 20, c: COL.sub, align: 'right' }); g.fillStyle = COL.grey; g.fillRect(bx, y + 20, calc * sc * u1, 30); }
            if (u2 > 0) { text('実績', bx - 14, y + 92, { size: 20, c: COL.sub, align: 'right' }); g.fillStyle = COL.red; g.fillRect(bx, y + 70, actv * sc * u2, 30); }
            // 差（計算の端→実績の端）に縦の線が走り、倍率が出る
            const ex = bx + Math.max(calc, actv) * sc + 24, du = E.outCubic(P(lt, t0 + 1.6, 0.5));
            if (du > 0) { line(bx + calc * sc, y + 50, bx + calc * sc, lerp(y + 50, y + 100, du), COL.navy, 1, [4, 4]); }
            wtext(lt, t0 + 1.8, null, `×${w.fac.toFixed(3)}`, ex, y + 80, { size: 48, tab: true });
          });
        });
      }, RBOX);

      /* ── 右: 実例 都筑区の2035年（縦に並ぶ） ── */
      phase(lt, EX, 64, () => {
        const rows = [
          ['都筑区の人口（2035年、市の推計）', `${man(popT(TZ, 2035))}人`, COL.navy, null],
          ['× 年齢別の搬送率（＋昼間の人）', `${fmt(TZ_TR)}人`, COL.navy, '＝1年に救急車で運ばれる人の見込み'],
          [`× ${DATA.dispRatio.toFixed(3)}（運ばない出場も数える）`, `${fmt(TZ_EXP)}件`, COL.navy, null],
          [`× ${TZ.fac.toFixed(3)}（校正係数）`, `${fmt(TZ.disp[2035])}件`, COL.red, '2035年の出場件数（人口変化のみ）'],
        ];
        const x0 = 900, ys = [330, 460, 590, 720];
        // 左端の縦線が上から下へ走り、各行の点をつなぐ
        const vu = E.outCubic(P(lt, EX + 0.4, 0.6 + 1.3 * 3));
        if (vu > 0) line(x0 - 40, ys[0] - 10, x0 - 40, lerp(ys[0] - 10, ys[3] - 10, vu), COL.navy, 1.5);
        rows.forEach(([l, v, c, note], k) => {
          const y = ys[k], t0 = EX + 0.6 + k * 1.3;
          if (lt >= t0) dot(x0 - 40, y - 10, k === 3 ? 7 : 5, k === 3 ? COL.red : COL.navy);
          wtext(lt, t0, null, l, x0, y, { size: 28 });
          wtext(lt, t0 + 0.3, null, v, RX1, y + 4, { size: 48, tab: true, c, align: 'right' });
          if (note) wtext(lt, t0 + 0.5, null, note, x0, y + 40, { size: 20, c: COL.sub });
          rule(lt, t0 + 0.2, x0, y + 62, RX1 - x0, k === 3 ? COL.navy : COL.line, k === 3 ? 2 : 1);
        });
      }, RBOX);
    },
  };
})();
