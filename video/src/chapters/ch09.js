/* 第9章 隊の負担 — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 区（縦18行）× 年（横 2025→2040）のタイムライン。1隊あたり年3,000件を超える最初の年に点を置く。
 * 赤＝人口変化のみ（overYear）、紫の小点＝年代別トレンド（byAge×(1+growthGroup)^(y−2024)）。
 * テンポ: 1.2–2.0 枠ワイプ／2.0–2.6 9区一斉点灯／3・4・5秒 後から超える3区を1つずつ置く／
 *        6.5–7.0 紫を一斉に置く／8.0・10.5 チップ順次／11.6〜 超えない区に「2040年まで超えない」を1行ずつ／
 *        赤い点は全体に小さく呼吸する（静止対策）。 */
(() => {
  // 年代別トレンドで 1隊3,000件を超える最初の年（2025 は byAge[2025] を使う）
  const dispT = (w, y) => AGE.reduce((s, a) => s + w.byAge[y][a] * Math.pow(1 + TR.growthGroup[a], y - 2024), 0);
  const overT = (w) => { for (const y of YEARS) if (dispT(w, y) / units(w) >= 3000) return y; return null; };
  // 行の並び: すでに超えている9区（SPEC の順）→ 後から超える区（年順）→ 超えない区（年代別トレンドの年順）
  const ALREADY = ['戸塚', '磯子', '青葉', '保土ケ谷', '神奈川', '旭', '中', '南', '港南'];
  const OV = WD.map((w, i) => ({ i, name: w.name, a: overYear(w), t: overT(w) }));
  const LATER = OV.filter((o) => o.a && o.a > 2025).sort((p, q) => p.a - q.a);          // 港北2028, 都筑2033, 鶴見2034
  const REST = OV.filter((o) => !o.a).sort((p, q) => (p.t || 9999) - (q.t || 9999));
  const ROWS = [...ALREADY.map((n) => OV[WI[n]]).filter((o) => o.a === 2025), ...LATER, ...REST];
  const T_FRAME = 1.2, T_ALL = 2.0, T_PURPLE = 6.5;
  const T_LATER = [3.0, 4.0, 5.0];                                 // 1つ1秒（第10章の施策リストのテンポ）
  const T_C1 = 8.0, T_C2 = 10.5, T_NO = 11.6;                      // チップ1・2、「超えない」表記の開始

  window.CHAPTERS[9] = {
    title: '隊の負担',
    q: '救急隊は足りる？',
    concl: '北部の増隊は2030年前後が分かれ目',
    duration: 20,
    subs: [[2.0, 6.0, '今でも9区が目安を超えている'], [6.4, 12.0, '北部は2030年前後に追いつく'], [12.4, 18.8, '増隊の順番を決める材料になる']],
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── 右: タイムライン ── */
      const XN = 930, X = (y) => lerp(970, 1610, (y - 2025) / 15), XNO = 1634, row = 37, y0 = 196;
      const yRow = (r) => y0 + r * row + row / 2, yEnd = y0 + 18 * row;
      // 点の小さな呼吸（行ごとに少し位相をずらす。半径 ±0.8px）
      const breath = (r) => (lt >= 7.0 ? 0.8 * Math.sin((lt - 7.0) * Math.PI * 0.9 - r * 0.35) : 0);

      // 枠（区名・行の罫線・年軸）を左→右のワイプで
      const fu = E.outCubic(P(lt, T_FRAME, 0.8));
      if (fu > 0) wipe(fu, XN - 130, y0 - 44, RX1 - XN + 130, 18 * row + 48, () => {
        [2025, 2030, 2035, 2040].forEach((y) => {
          numText(`${y}`, X(y), y0 - 16, { size: 20, c: COL.sub, align: 'center' });
          line(X(y), y0, X(y), yEnd, COL.grid, 1);
        });
        ROWS.forEach((o, r) => {
          const y = yRow(r), kL = LATER.indexOf(o);
          const tOn = o.a === 2025 ? T_ALL : kL >= 0 ? T_LATER[kL] : null;
          const lit = tOn != null && lt >= tOn;
          text(wn(WD[o.i]), XN, y + 7, { size: 20, w: lit ? 800 : 600, c: lit ? COL.ink : COL.faint, align: 'right' });
          line(X(2025), y, X(2040), y, COL.line, 2);
        });
      });


      ROWS.forEach((o, r) => {
        const y = yRow(r);
        // 年代別トレンドの点（紫・小）: 6.5 秒に一斉に。赤と同じ年なら省く
        if (o.t && o.t !== o.a) {
          const pu = E.outBack(P(lt, T_PURPLE, 0.5));
          if (pu > 0) dot(X(o.t), y, 5.5 * clamp(pu, 0, 1.3), COL.purple);
        }
        const kL = LATER.indexOf(o);
        if (o.a === 2025) {
          // すでに超えている9区: 一斉に点と帯
          const du = E.outBack(P(lt, T_ALL, 0.4)), bu = E.outCubic(P(lt, T_ALL, 0.6));
          if (bu > 0) line(X(2025), y, lerp(X(2025), X(2040), bu), y, COL.red, 6);
          if (du > 0) dot(X(2025), y, (8 + breath(r)) * clamp(du, 0, 1.3), COL.red);
        } else if (kL >= 0) {
          // 後から超える区: 点が上から落ちて止まる → 帯が伸びる
          const t0 = T_LATER[kL], x = X(o.a);
          const fall = P(lt, t0, 0.3);
          if (fall <= 0) return;
          const bu = E.outCubic(P(lt, t0 + 0.3, 0.5));
          if (bu > 0) line(x, y, lerp(x, X(2040), bu), y, COL.red, 6);
          const ripple = P(lt, t0 + 0.3, 0.4);
          if (ripple > 0 && ripple < 1) withAlpha(1 - ripple, () => {
            g.beginPath(); g.arc(x, y, 8 + 12 * ripple, 0, Math.PI * 2);
            g.strokeStyle = COL.red; g.lineWidth = 1.5; g.stroke();
          });
          const squash = ripple > 0 && ripple < 1 ? 1 + 0.25 * Math.sin(ripple * Math.PI) : 1;
          dot(x, y - 34 * (1 - fall * fall), (8 + breath(r)) * squash, COL.red);
          wtext(lt, t0 + 0.3, null, `${o.a}年`, x - 16, y + 7, { size: 20, tab: true, c: COL.red, align: 'right' });
        } else {
          // 人口変化のみでは 2040 年まで 3,000 件を超えない区: 行の右端に小さく
          const k = r - (ROWS.length - REST.length);
          wtext(lt, T_NO + k * 0.25, null, '2040年まで超えない', XNO, y + 7, { size: 20, c: COL.sub });
        }
      });

      /* ── 左: 文字 ── */
      wtext(lt, T_FRAME, null, '1隊あたり年3,000件を超える年', LX, 200, { size: 28, c: COL.sub });
      wtext(lt, T_ALL, null, '9区', LX, 340, { size: 120, tab: true, c: COL.red });
      wtext(lt, T_ALL + 0.15, null, 'すでに目安を超えている（2024年）', LX, 400, { size: 28 });
      rule(lt, T_LATER[0] - 0.2, LX, 444, LW, COL.line, 1, 0.4);
      LATER.forEach((o, k) => {
        const t0 = T_LATER[k], y = 516 + k * 64;
        wtext(lt, t0, null, wn(o.name), LX, y, { size: 28 });
        wtext(lt, t0 + 0.1, null, `${o.a}年`, LX + 150, y + 4, { size: 48, tab: true });
      });
      // 凡例（赤＝人口変化のみ、紫＝年代別トレンド）
      wipe(E.outCubic(P(lt, T_ALL + 0.3, 0.4)), LX - 4, 690, LW, 30, () => {
        dot(LX + 7, 704, 7, COL.red);
        text('赤＝人口変化のみの場合', LX + 24, 711, { size: 20, c: COL.sub });
      });
      wipe(E.outCubic(P(lt, T_PURPLE, 0.4)), LX - 4, 724, LW, 30, () => {
        dot(LX + 7, 738, 5, COL.purple);
        text('紫＝年代別トレンドの場合（ここ10年の増え方が続く）', LX + 24, 745, { size: 20, c: COL.sub });
      });
      chip(lt, T_C1, 20.5, '1隊あたり＝区の年間出場 ÷ 区内の救急隊数', LX, 780, { c: COL.red });
      chip(lt, T_C2, 20.5, `目安の3,000件＝市平均（${DATA.emsUnits}隊）`, LX, 832, { c: COL.navy });
    },
  };
})();
