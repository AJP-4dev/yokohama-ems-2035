/* 第8章 — 意外だったこと。契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * (a) 1.4–15.0  年代別搬送率の推移 2013→2024（対数目盛）。高齢者は平ら、0–14歳だけ立ち上がる
 * (b) 15.4–41.2 高齢化率×出場件数/千人。18点は1秒で出す → 予想線 → r=−0.01 → 中区・西区が点滅して薄くなる → 16区の回帰線 r=0.74
 *     後半（33.6〜）は中区・西区の点が小さく呼吸する（静止対策） */
(() => {
  const GG = TR.growthGroup;
  const AGING = WD.map((w) => (w.pop[2025].e1 + w.pop[2025].e2 + w.pop[2025].e3) / popT(w, 2025) * 100);
  const PERCAP = WD.map((w) => w.disp24 / popT(w, 2025) * 1000);
  const CORE = ['中', '西'];
  const IDX16 = WD.map((w, i) => i).filter((i) => !CORE.includes(WD[i].name));
  const R18 = corr(AGING, PERCAP);
  const R16 = corr(IDX16.map((i) => AGING[i]), IDX16.map((i) => PERCAP[i]));
  const [FA, FB] = fit(IDX16.map((i) => AGING[i]), IDX16.map((i) => PERCAP[i]));
  const ORD_A = WD.map((w, i) => i).sort((a, b) => AGING[a] - AGING[b]);
  const rankA = []; ORD_A.forEach((i, k) => { rankA[i] = k; });
  const Y0 = TR.years[0], Y1 = TR.years[TR.years.length - 1];
  const yr = (y, a) => TR.rateGroup[y][a] * 100;            // 人口100人あたり

  window.CHAPTERS[8] = {
    title: '意外だったこと',
    q: '意外だったことは？',
    concl: '郊外は年齢、都心は人の出入り',
    duration: 38,
    subs: [[1.6, 7.0, '年齢ごとの搬送率、12年の動き'], [7.4, 15.0, '増えているのは、高齢者の利用ではない'], [15.6, 20.2, '高齢化が進んだ区ほど多い？'], [20.6, 26.0, '全18区では関係なし（−0.01）'], [26.4, 33.4, '中区と西区を除くと、強く連動'], [33.8, 41.6, '郊外は年齢、都心は人の出入りで決まる']],
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── (a) 年代別搬送率（対数） ─────────────── */
      phase(lt, 1.4, 15.0, () => {
        const C = { x0: 900, x1: 1660, y0: 220, y1: 760 };
        C.X = (y) => lerp(C.x0, C.x1, (y - Y0) / (Y1 - Y0));
        C.Y = (v) => lerp(C.y1, C.y0, Math.log(v / 2) / Math.log(16));
        axes(lt, 1.4, C, [[2013, '2013'], [2016, '2016'], [2020, '2020'], [2024, '2024']], [[2, '2人'], [5, '5人'], [10, '10人'], [20, '20人']]);
        // 強調: 7.4〜 0–14歳だけ、9.4〜 85歳以上も、11.4〜 75–84歳も
        const fo = E.inOut(P(lt, 7.4, 0.6));
        const back = { e3: E.inOut(P(lt, 9.4, 0.5)), e2: E.inOut(P(lt, 11.4, 0.5)) };
        ['w', 'e1', 'e2', 'e3', 'c'].forEach((a) => {
          const k = AGE.indexOf(a);
          const pts = TR.years.map((y) => [C.X(y), C.Y(yr(y, a))]);
          const al = a === 'c' ? 1 : 1 - 0.72 * fo * (1 - (back[a] || 0));
          withAlpha(al, () => {
            const e = polyline(pts, E.inOut(P(lt, 1.8 + k * 0.4, 1.0)), AGEC[a], a === 'c' ? lerp(3, 5.5, fo) : 3);
            if (e) wtext(lt, 2.8 + k * 0.4, null, AGEL[a], C.x1 + 14, pts[pts.length - 1][1] + 7, { size: 20, c: a === 'c' ? COL.ink : COL.sub });
          });
        });
        // 0–14歳の始点と終点（12.8〜）
        const cu = E.outCubic(P(lt, 12.8, 0.4));
        if (cu > 0) {
          [Y0, Y1].forEach((y) => dot(C.X(y), C.Y(yr(y, 'c')), 7 * cu, AGEC.c, COL.ink));
          wtext(lt, 12.8, null, `${yr(Y0, 'c').toFixed(1)}人`, C.X(Y0) + 4, C.Y(yr(Y0, 'c')) + 36, { size: 20, tab: true });
          wtext(lt, 13.1, null, `${yr(Y1, 'c').toFixed(1)}人`, C.X(Y1) - 4, C.Y(yr(Y1, 'c')) + 36, { size: 20, tab: true, align: 'right' });
        }
        wtext(lt, 1.6, null, '年代別の搬送率', LX, 240, { size: 48 });
        wtext(lt, 1.9, null, '1年に救急車で運ばれる人の割合\n人口100人あたり、対数目盛', LX, 330, { size: 28, lead: 44 });
      }, [0, 140, W, 720]);
      chip(lt, 7.4, 15.0, `0–14歳 年${sgn(GG.c * 100)}%`, LX, 520, { c: AGEC.c });
      chip(lt, 9.4, 15.0, `85歳以上 年${sgn(GG.e3 * 100)}%`, LX, 572, { c: AGEC.e3 });
      chip(lt, 11.4, 15.0, '75–84歳 ほぼ横ばい', LX, 624, { c: AGEC.e2 });

      /* ── (b) 高齢化率 × 出場件数/千人 ─────────── */
      if (lt >= 15.4) {
        const C = { x0: 900, x1: 1760, y0: 220, y1: 760 };
        C.X = (v) => lerp(C.x0, C.x1, (v - 18) / 15);
        C.Y = (v) => lerp(C.y1, C.y0, (v - 40) / 90);
        axes(lt, 15.6, C, [[20, '20%'], [25, '25%'], [30, '30%']], [[50, '50件'], [75, '75件'], [100, '100件'], [125, '125件']]);
        wtext(lt, 15.8, null, '横：高齢化率（65歳以上の割合）　縦：出場件数/千人（住民1,000人あたり）', C.x0, 190, { size: 20, c: COL.sub });
        // 「高齢化が進んだ区ほど多い？」の予想線（17.8〜、20.6 でワイプアウト）
        const eu = E.outCubic(P(lt, 17.8, 0.8)), ev = E.inOut(P(lt, 20.6, 0.4));
        if (eu > 0 && ev < 1) {
          const ax = C.X(19.5), ay = C.Y(48), bx = C.X(32), by = C.Y(118);
          clipRect(lerp(ax - 10, bx + 120, ev), C.y0 - 10, bx + 140 - ax, C.y1 - C.y0 + 20, () => {
            line(ax, ay, lerp(ax, bx, eu), lerp(ay, by, eu), COL.faint, 2, [10, 8]);
            wtext(lt, 18.4, null, '予想？', bx + 12, by + 8, { size: 20, c: COL.sub });
          });
        }
        const blink = lt >= 20.6 && lt < 23.0 && Math.floor((lt - 20.6) * 2.5) % 2 === 0;
        const out = E.inOut(P(lt, 23.0, 0.6));
        const breath = lt >= 33.6 ? 1.5 * Math.sin((lt - 33.6) * Math.PI) : 0;   // 後半の小さな呼吸
        WD.forEach((w, i) => {
          const u = E.outCubic(P(lt, 16.2 + rankA[i] * 0.03, 0.45));   // 18点を 1.0 秒以内に if (u <= 0) return;
          const cw = CORE.includes(w.name), x = C.X(AGING[i]), y = C.Y(PERCAP[i]);
          if (cw) {
            const hot = E.inOut(P(lt, 20.6, 0.3));
            withAlpha(1 - 0.6 * out, () => {
              dot(x, y, 9 * u + breath, mix(mix(COL.navy, COL.red, hot), COL.grey, out));
              if (blink) { g.beginPath(); g.arc(x, y, 20, 0, Math.PI * 2); g.strokeStyle = COL.red; g.lineWidth = 2; g.stroke(); }
              wtext(lt, 20.6, null, wn(w), x + 20, y + 8, { size: 20, c: out > 0.5 ? COL.sub : COL.red });
            });
          } else {
            dot(x, y, 9 * u, COL.navy);
            // 後半（34.4〜）: 郊外16区の点に、高齢化率の低い順で小さな波紋が1つずつ走る（静止対策）
            if (lt >= 34.4) {
              const k = IDX16.slice().sort((p, q) => AGING[p] - AGING[q]).indexOf(i);
              const rp = ((lt - 34.4) - k * 0.4) / 1.0;
              const cyc = rp - Math.floor(rp / (16 * 0.4)) * (16 * 0.4);
              if (rp >= 0 && cyc < 1) withAlpha(1 - cyc, () => {
                g.beginPath(); g.arc(x, y, 9 + 14 * cyc, 0, Math.PI * 2);
                g.strokeStyle = COL.navy; g.lineWidth = 1.5; g.stroke();
              });
            }
          }
        });
        // 16区の回帰線（24.0〜）
        const fu = E.outCubic(P(lt, 24.0, 1.0)), xa = 19.2, xb = 32.4;
        if (fu > 0) { const xe = lerp(xa, xb, fu); line(C.X(xa), C.Y(FA + FB * xa), C.X(xe), C.Y(FA + FB * xe), COL.navy, 2.5); }
        wtext(lt, 28.8, null, '郊外の16区：年齢で決まる', C.X(27.5), C.Y(FA + FB * 27.5) + 52, { size: 20, c: COL.ink });
        const cn = WI['中'];
        wtext(lt, 33.6, null, '都心：人の出入りで決まる', C.X(AGING[cn]) + 20, C.Y(PERCAP[cn]) + 40, { size: 20, c: COL.sub });
        // 左カラム
        wtext(lt, 15.8, null, '高齢化率と出場の相関', LX, 240, { size: 28, c: COL.sub });
        wtext(lt, 20.6, 23.6, sgn2(R18), LX, 380, { size: 120, tab: true });
        wtext(lt, 20.9, 23.6, '全18区', LX, 450, { size: 28 });
        wtext(lt, 24.0, null, sgn2(R16), LX, 380, { size: 120, tab: true, c: COL.red });
        wtext(lt, 24.3, null, '中区と西区を除く16区', LX, 450, { size: 28 });
        chip(lt, 17.2, 42.5, '相関＝1に近いほど連動、0は無関係', LX, 520, { c: COL.navy });
        chip(lt, 26.4, 42.5, '中区と西区は昼に人が集まる区', LX, 572, { c: COL.orange });
        chip(lt, 31.2, 42.5, `昼夜間人口比（昼÷夜）との相関 ${sgn2(corr(WD.map((w) => w.dn), PERCAP))}`, LX, 624, { c: COL.orange });
      }
    },
  };
})();
