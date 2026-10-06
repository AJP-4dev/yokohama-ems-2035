/* 第5章 結果② 誰が — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 見せる動き: 出場件数の年齢構成の帯が 2024→2035 で切り替わり、紫（85歳以上）だけが太くなる。 */
(() => {
  // 年齢5区分の出場件数（人口変化のみ）。byAge[2025] は 2024年実績ベース（dispA と同じ扱い）
  const BA = (y) => { const o = {}; AGE.forEach((a) => { o[a] = sumW((w) => w.byAge[y][a]); }); return o; };
  const B24 = BA(2025), B35 = BA(2035);
  const e3a = cityPop(2025, 'e3'), e3b = cityPop(2035, 'e3');
  const pctPop = (a) => (cityPop(2035, a) / cityPop(2025, a) - 1) * 100;
  const RATE = {}; AGE.forEach((a) => { RATE[a] = DATA.rates[a] * 100; });
  const RMAX = RATE.e3;
  const TOT = (o) => AGE.reduce((s, a) => s + o[a], 0);
  const P42 = `人口 ${sgn((e3b / e3a - 1) * 100, 0)}% × 4人に1人`;
  // 階段の強調: [開始, 終了, 濃く見せる区分]（それ以外を薄く）
  const SFOC = [[21.0, 29.2, ['e3']], [29.2, 36.8, ['e3', 'e1']], [36.8, 99, ['e3', 'w']]];
  const sdim = (lt, a) => SFOC.reduce((d, [s0, s1, ks]) => (ks.includes(a) ? d : Math.max(d, Math.min(E.inOut(P(lt, s0, 0.5)), 1 - E.inOut(P(lt, s1, 0.5))))), 0);

  // 帯（右上）
  // 帯は 85歳以上 を左端に置く（左端を固定して、紫の右端だけが伸びるのを見せる）
  const BX = 980, BW = 840, SCB = BW / 290000, BH = 76;
  const BORD = [...AGE].reverse();
  function band(y, vals, u, dimK) {
    let x = BX;
    BORD.forEach((a) => {
      const ww = vals[a] * SCB * u;
      const al = a === 'e3' ? 1 : 1 - 0.6 * dimK;
      withAlpha(al, () => { g.fillStyle = AGEC[a]; g.fillRect(x, y, Math.max(0, ww - 3), BH); });
      if (ww > 150 && (a === 'w' || a === 'e2' || a === 'e3')) text(AGEL[a], x + 14, y + BH / 2 + 1, { size: 20, w: 600, c: '#ffffff', base: 'middle', a: a === 'e3' ? 1 : 1 - dimK });
      x += ww;
    });
    return x;
  }
  // 階段（右）
  const SB = 760, SH = 400, SX = 960, SS = 172, SWD = 112;

  window.CHAPTERS[5] = {
    title: '結果② 誰が',
    q: '増えるのは、誰？',
    concl: '増加の主役は85歳以上',
    duration: 45,
    subs: [[1.6, 7.6, '救急を使う人の年齢の内訳'], [8.0, 14.0, '増える分のほぼ全部は85歳以上'], [14.4, 21.0, '85歳以上の人口は18.8万→26.7万'],
      [21.4, 29.0, '85歳以上は4人に1人が1年に運ばれる'], [29.4, 36.6, '65–74歳も増えるが、運ばれる率は低い'], [37.0, 44.2, '人が増え、運ばれる率も高い年代']],
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ═════ 前半（1.2–13.8）: 年齢構成の帯 ═════ */
      phase(lt, 1.4, 13.6, () => {
        wtext(lt, 1.5, null, '救急を使う人の年齢', LX, 240, { size: 48 });
        wtext(lt, 1.9, null, '出場件数を年齢5区分に分けた内訳\n2035年は人口変化のみの推計', LX, 300, { size: 20, c: COL.sub, lead: 32 });
        wtext(lt, 8.6, null, '増える分の中心は', LX, 520, { size: 28 });
        wtext(lt, 8.9, null, '85歳以上', LX, 600, { size: 48, c: COL.purple });
        wtext(lt, 10.4, null, `85歳以上だけで ${sgn((B35.e3 - B24.e3) / 10000)}万件`, LX, 668, { size: 28, tab: true });
        wtext(lt, 11.4, null, `全体の増加は ${sgn((TOT(B35) - TOT(B24)) / 10000)}万件`, LX, 716, { size: 28, tab: true, c: COL.sub });
      }, [0, 150, 790, 720]);

      phase(lt, 1.4, 13.6, () => {
        const dk = E.inOut(P(lt, 6.6, 0.5));
        // 2024
        wtext(lt, 1.6, null, '2024年', RX0 + 10, 250, { size: 28 });
        band(212, B24, E.outCubic(P(lt, 1.8, 1.6)), dk);
        // 2035: 帯が出てから、各区分の幅が 2035 の値へ（紫だけ太くなる）
        if (lt > 5.0) {
          wtext(lt, 5.0, null, '2035年', RX0 + 10, 370, { size: 28 });
          const m = eio(lt, 6.0, 1.6), v = {};
          AGE.forEach((a) => { v[a] = lerp(B24[a], B35[a], m); });
          const xe = band(332, v, E.outCubic(P(lt, 5.0, 0.6)), dk);
          // 2024年の紫の右端を細い破線で残す（そこからの伸びが増加分）
          const x24 = BX + B24.e3 * SCB;
          const du = E.outCubic(P(lt, 6.0, 0.5));
          if (du > 0) line(x24, 296, x24, lerp(296, 418, du), COL.navy, 1, [3, 4]);
          if (m > 0.2) wtext(lt, 7.6, null, `${sgn((B35.e3 / B24.e3 - 1) * 100, 0)}%`, BX + v.e3 * SCB - 12, 322, { size: 20, tab: true, c: COL.purple, align: 'right' });
        }
        // 凡例（年齢5区分）
        let lx = BX;
        BORD.forEach((a, k) => {
          const u = E.outCubic(P(lt, 2.4 + k * 0.12, 0.4));
          if (u <= 0) return;
          withAlpha(1, () => { g.fillStyle = AGEC[a]; g.fillRect(lx, 452, 16 * u, 16); });
          wtext(lt, 2.4 + k * 0.12, null, AGEL[a], lx + 24, 468, { size: 20, c: COL.sub });
          lx += 24 + tw(AGEL[a], 20) + 30;
        });
        // 増減のバー（2024→2035、件）
        wtext(lt, 8.5, null, '2024→2035年の増減（件）', BX, 548, { size: 20, c: COL.sub });
        const zx = 1290, ks = 0.0145, y0 = 576;
        const zu = E.outCubic(P(lt, 8.5, 0.5));
        if (zu > 0) line(zx, y0, zx, lerp(y0, y0 + 5 * 52, zu), COL.navy, 1);
        AGE.forEach((a, k) => {
          const d = B35[a] - B24[a], y = y0 + 10 + k * 52, u = E.outCubic(P(lt, 9.0 + k * 0.25, 0.7));
          if (u <= 0) return;
          text(AGEL[a], BX, y + 23, { size: 20, w: 600, c: COL.sub });
          const L = d * ks * u;
          g.fillStyle = AGEC[a]; g.fillRect(L >= 0 ? zx : zx + L, y + 4, Math.abs(L), 28);
          if (a === 'e3') wtext(lt, 10.4, null, `${sgn(d / 10000)}万件`, zx + d * ks + 14, y + 28, { size: 28, tab: true, c: COL.purple });
        });
      }, [RX0, 140, 1060, 760]);

      /* ═════ 後半（14–44.2）: 85歳以上の人口 × 搬送率の階段 ═════ */
      // 左カラム
      wtext(lt, 14.2, null, '85歳以上の人口（2025→2035年）', LX, 220, { size: 20, c: COL.sub });
      if (lt >= 14.4) wtext(lt, 14.4, null, `${man(e3a)}人 → ${man(lerp(e3a, e3b, cnt(lt, 14.9, 1.4)))}人`, LX, 290, { size: 48, tab: true });
      wtext(lt, 16.2, null, `${sgn((e3b / e3a - 1) * 100, 0)}%`, LX, 430, { size: 120, w: 600, tab: true, c: COL.purple });
      rule(lt, 20.8, LX, 480, LW, COL.line, 1);
      wtext(lt, 21.2, null, '100人あたり、1年に運ばれる人数', LX, 536, { size: 20, c: COL.sub });
      wtext(lt, 21.5, null, `${RATE.e3.toFixed(1)}人＝4人に1人`, LX, 604, { size: 48, tab: true });
      { const a = tw(`${RATE.e3.toFixed(1)}人＝`, 48, 800, true), b = tw('4人に1人', 48, 800, true); rule(lt, 27.2, LX + a, 622, b, COL.purple, 3, 1.0); }
      chip(lt, 24.2, 29.0, '搬送率＝1年に救急車で運ばれる人の割合', LX, 660, { c: COL.navy });
      chip(lt, 29.4, 40.4, `65–74歳 ${man(cityPop(2025, 'e1'))}→${man(cityPop(2035, 'e1'))}人（${sgn(pctPop('e1'), 0)}%）`, LX, 660, { c: AGEC.e1 });
      chip(lt, 31.4, 40.4, `75–84歳 ${sgn(pctPop('e2'), 0)}%`, LX, 712, { c: AGEC.e2 });
      chip(lt, 33.4, 40.4, `15–64歳 ${man(cityPop(2025, 'w'), 0)}→${man(cityPop(2035, 'w'), 0)}人（${sgn(pctPop('w'), 0)}%）`, LX, 764, { c: AGEC.w });
      wtext(lt, 41.0, null, P42, LX, 712, { size: 28, c: COL.purple });
      rule(lt, 42.2, LX, 736, tw(P42, 28), COL.purple, 2, 1.0);

      // 右: 搬送率の階段
      phase(lt, 14.0, 45, () => {
        wtext(lt, 14.4, null, '搬送率（人口100人あたり、1年に運ばれる人数）', SX, 200, { size: 20, c: COL.sub });
        const bu = E.outCubic(P(lt, 14.4, 0.6));
        if (bu > 0) line(SX - 20, SB, lerp(SX - 20, RX1, bu), SB, COL.navy, 1);
        AGE.forEach((a, k) => {
          const v = RATE[a], x = SX + k * SS, hh = SH * v / RMAX;
          const u = E.outCubic(P(lt, 14.8 + k * 0.35 + (a === 'e3' ? 0.3 : 0), a === 'e3' ? 1.0 : 0.7));
          if (u <= 0) return;
          const al = 1 - 0.6 * sdim(lt, a);
          withAlpha(al, () => { g.fillStyle = AGEC[a]; g.fillRect(x, SB - hh * u, SWD, hh * u); });
          text(AGEL[a], x + SWD / 2, SB + 34, { size: 20, w: 600, c: COL.sub, align: 'center' });
          if (u > 0.9) wtext(lt, 15.4 + k * 0.35 + (a === 'e3' ? 0.5 : 0), null, `${v.toFixed(1)}人`, x + SWD / 2, SB - hh - 16, { size: 28, tab: true, align: 'center', c: a === 'e3' ? COL.purple : COL.ink });
        });
        // 4人に1人（4つの正方形のうち1つが紫に満ちる）
        const qx = SX, qy = 262, qs = 52, qg = 14;
        for (let k = 0; k < 4; k++) {
          const u = E.outCubic(P(lt, 25.2 + k * 0.15, 0.5));
          if (u <= 0) continue;
          const x = qx + k * (qs + qg);
          g.strokeStyle = COL.grey; g.lineWidth = 1.5; g.strokeRect(x + 0.75, qy + 0.75, qs - 1.5, qs - 1.5);
          if (k === 0) { const f = E.outCubic(P(lt, 26.0, 0.6)); g.fillStyle = COL.purple; g.fillRect(x, qy + qs * (1 - f), qs, qs * f); }
        }
        wtext(lt, 26.4, null, '85歳以上の4人に1人', qx + 4 * (qs + qg) + 10, qy + 36, { size: 20, c: COL.purple });
        // 37–: 15–64歳との比較（約9倍）
        const w = RATE.w, xw = SX + 1 * SS + SWD, xe = SX + 4 * SS, yw = SB - SH * w / RMAX;
        const cu = E.outCubic(P(lt, 37.4, 0.9));
        if (cu > 0) line(xw + 8, yw, lerp(xw + 8, xe - 8, cu), yw, COL.purple, 1.5, [5, 5]);
        if (lt > 38.2) {
          const au = E.outCubic(P(lt, 38.2, 0.8)), ye = SB - SH;
          line(xe - 24, yw, xe - 24, lerp(yw, ye, au), COL.purple, 2);
        }
        wtext(lt, 39.0, null, `15–64歳の約${Math.round(RATE.e3 / RATE.w)}倍`, xe - 40, SB - SH + 70, { size: 28, tab: true, c: COL.purple, align: 'right' });
      }, [RX0, 140, 1060, 760]);
    },
  };
})();
