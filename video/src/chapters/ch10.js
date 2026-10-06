/* 第10章 示唆と案内 — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 1.4–12.4 施策5点（左）＋対象の区（右の地図）。5点そろって約1秒の一拍 → 12.4 でワイプアウト／
 * 12.8– 3D地図の上に第0章と同じロックアップ＋出典 → 終端は白で静かに止める（最後の0.5秒は静止）。 */
(() => {
  const E3G = WD.map((w) => w.pop[2035].e3 / w.pop[2025].e3);
  const topBy = (f, n) => WD.map((w, i) => i).sort((a, b) => f(WD[b], b) - f(WD[a], a)).slice(0, n).map((i) => WD[i].name);
  // [施策, 補足（なぜ）, 地図で強調する区]
  const POLICY = [
    ['北部と都心に救急隊を厚く', '伸びが大きい北部と、件数が密な都心', ['都筑', '青葉', '港北', '鶴見', '西', '中']],
    ['85歳以上は施設と事前に連携', '85歳以上は4人に1人が1年に運ばれる', topBy((w, i) => E3G[i], 5)],
    ['転院搬送は民間へ', '病院どうしの搬送を救急隊から切り離す', topBy((w) => w.transfer24 / w.disp24, 3)],
    ['南西部は到着時間を指標に', '件数は横ばいでも、現場まで遠い', ['栄', '瀬谷', '旭']],
    ['不搬送の多い区は #7119 を周知', '#7119＝救急車を呼ぶか迷ったときの電話相談', topBy((w) => w.nonTr, 3)],
  ];
  const PT = (k) => 1.4 + k * 2.0;                      // 各施策の出る時刻
  const SRC = '出典: 横浜市の公表資料から再計算。市の公式見解ではありません';
  const T3 = 12.8, TEND = 21.5;                          // 3Dロゴ部分の開始／静止の開始（最後の0.5秒）

  window.CHAPTERS[10] = {
    title: '示唆と案内',
    q: 'では、どう備える？',
    concl: null,
    duration: 22,
    subs: [[1.6, 12.2, 'データから見える5つの備え']],
    uses3D: (lt) => lt >= T3,
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── 1) 施策5点 ── */
      phase(lt, 1.4, 12.4, () => {
        const act = clamp(Math.floor((lt - 1.4) / 2.0), 0, 4);
        const all = lt >= 11.4;                          // 5点そろったら全部を濃く
        POLICY.forEach(([t1, t2], k) => {
          const t0 = PT(k), y = 250 + k * 124;
          const on = all || k === act;
          wtext(lt, t0, null, `${k + 1}`, LX, y, { size: 28, tab: true, c: on ? COL.red : COL.faint });
          wtext(lt, t0 + 0.1, null, t1, LX + 44, y, { size: 28, w: 800, c: on ? COL.ink : COL.sub });
          wtext(lt, t0 + 0.3, null, t2, LX + 44, y + 40, { size: 20, c: COL.sub });
          rule(lt, t0 + 0.2, LX, y + 72, LW, COL.line);
        });
        const box = { x: 1040, y: 200, w: 760, h: 660 };
        wipe(E.outCubic(P(lt, 1.6, 0.9)), box.x - 20, box.y - 20, box.w + 40, box.h + 40, () => {
          const kOf = (w) => (all ? -1 : POLICY[act][2].includes(w.name) ? act : -1);
          const xf = drawMap(box, (w) => {
            if (all) return '#e3e8ef';
            const on = POLICY[act][2].includes(w.name);
            const u = ein(lt, PT(act) + 0.2, 0.5);
            return on ? mix('#e3e8ef', COL.navy, u) : '#e3e8ef';
          });
          if (!all && lt >= PT(act) + 0.5) WD.forEach((w) => {
            if (kOf(w) < 0) return;
            const [x, y] = wardC(xf, w);
            text(wn(w), x, y + 7, { size: 20, w: 700, c: '#ffffff', align: 'center' });
          });
          // 5点そろった後: 地図は1区ずつ順に区名が走る（静止を避ける小さな動き）
          if (all) {
            const k = Math.floor((lt - 11.4) / 0.1);
            WD.forEach((w) => { if (rankX[WI[w.name]] <= k) { const [x, y] = wardC(xf, w); text(wn(w), x, y + 7, { size: 20, w: 600, c: COL.sub, align: 'center' }); } });
          }
        });
      }, [0, 140, W, 760]);

      /* ── 2) 3D地図の上にロックアップ → 白で静かに止める ── */
      if (lt >= T3) {
        const lq = Math.min(lt, TEND);                 // 最後の0.5秒は静止
        reset3D(); beginGL();
        WD.forEach((w, i) => setPillar(i, hOf(w.disp[2035]), divCol(wDiff35(w))));
        const s = shiftCam({ theta: -0.35 + 0.012 * (lq - T3), phi: 0.95, dist: 36, tx: -1.5, tz: 0.5 }, 11);
        setCam(s); renderView(0, W);
        // 地図を薄くする（0.62）→ 終盤は白へ
        const wu = E.inOut(P(lq, T3 + 5.3, 2.9));
        const thin = lerp(0.62, 1, wu);
        g.fillStyle = mix('#f4f6f9', '#ffffff', wu);
        g.globalAlpha = thin; g.fillRect(0, 0, W, H); g.globalAlpha = 1;
        // 背景色の板が右へ抜けて地図が現れる
        clipRect(W * E.inOut(P(lt, T3, 0.6)), 0, W, H, () => { g.fillStyle = COL.bg; g.fillRect(0, 0, W, H); });
        drawLockup(lq - (T3 + 0.3), M, 560);
        wtext(lq, T3 + 2.4, null, SRC, M, 680, { size: 20, c: COL.sub });
      }
    },
  };
})();
