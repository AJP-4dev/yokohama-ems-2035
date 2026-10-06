/* 第10章 示唆と案内 — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
 * 1.4–12.2 施策5点（左）＋対象の区（右の地図）／12.6–20.6 サイトUIの模型／20.5–21.3 結論カード／
 * 21.3– 3D地図の上に第0章と同じロックアップ＋URL＋出典 → 終端は白で静かに止める（最後の0.5秒は静止）。 */
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
  const TABS = ['地図', '市全体', '区別', '考察', '方法', 'スライド'];
  const SRC = '出典: 横浜市の公表資料から再計算。市の公式見解ではありません';
  const diffY = (w, y) => (dispA(w, y) / w.disp24 - 1) * 100;   // 2024年比の増減%
  const T3 = 21.3, TEND = 29.5;                          // 3Dロゴ部分の開始／静止の開始

  window.CHAPTERS[10] = {
    title: '示唆と案内',
    q: 'では、どう備える？',
    concl: null,
    duration: 30,
    subs: [[1.6, 12.0, 'データから見える5つの備え'], [13.0, 20.2, '地図で、自分の区を確かめる']],
    uses3D: (lt) => lt >= T3,
    setup(ctx) {},
    draw(ctx, lt, t) {
      /* ── 1) 施策5点 ── */
      phase(lt, 1.4, 12.2, () => {
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
            text(w.name, x, y + 7, { size: 20, w: 700, c: '#ffffff', align: 'center' });
          });
          // 5点そろった後: 地図は1区ずつ順に区名が走る（静止を避ける小さな動き）
          if (all) {
            const k = Math.floor((lt - 11.4) / 0.1);
            WD.forEach((w) => { if (rankX[WI[w.name]] <= k) { const [x, y] = wardC(xf, w); text(w.name, x, y + 7, { size: 20, w: 600, c: COL.sub, align: 'center' }); } });
          }
        });
      }, [0, 140, W, 760]);

      /* ── 2) サイトUIの模型 ── */
      phase(lt, 12.6, 20.4, () => {
        wtext(lt, 12.8, null, 'サイトで確かめる', LX, 250, { size: 48 });
        wtext(lt, 13.1, null, '全区、全年、4つのシナリオを\n地図で切り替えて見られる', LX, 330, { size: 28, lead: 44, c: COL.sub });
        const F = { x: 840, y: 170, w: 1000, h: 700 };
        const fu = E.outCubic(P(lt, 12.8, 0.8));
        if (fu > 0) {
          g.fillStyle = '#ffffff'; g.fillRect(F.x, F.y, F.w * fu, F.h);
          line(F.x, F.y, F.x + F.w * fu, F.y, COL.navy, 1);
          line(F.x, F.y + F.h, F.x + F.w * fu, F.y + F.h, COL.line, 1);
          line(F.x, F.y, F.x, F.y + F.h * fu, COL.line, 1);
          if (fu > 0.99) line(F.x + F.w, F.y, F.x + F.w, F.y + F.h, COL.line, 1);
        }
        // アドレス欄
        rule(lt, 13.0, F.x, F.y + 52, F.w, COL.line);
        wtext(lt, 13.1, null, URL_TXT, F.x + 28, F.y + 34, { size: 20, c: COL.sub, num: true });
        // タイトルとタブ
        wtext(lt, 13.4, null, '救急需要の未来地図', F.x + 28, F.y + 100, { size: 20, w: 800 });
        let tx = F.x + 300;
        TABS.forEach((s, k) => {
          wtext(lt, 13.6 + k * 0.12, null, s, tx, F.y + 100, { size: 20, c: k === 0 ? COL.ink : COL.sub });
          if (k === 0) rule(lt, 14.2, tx, F.y + 114, tw(s, 20), COL.red, 2, 0.4);
          tx += tw(s, 20) + 40;
        });
        rule(lt, 13.6, F.x, F.y + 128, F.w, COL.line);
        // 条件パネル（年は 2025→2035 に切り替わる）
        const yr = Math.round(lerp(2025, 2035, E.inOut(P(lt, 15.8, 2.6))));
        const px0 = F.x + 28;
        [['年', `${yr}年`], ['シナリオ', '人口変化のみ'], ['指標', '出場件数の増減']].forEach(([k1, v], k) => {
          const y = F.y + 190 + k * 96;
          wtext(lt, 14.4 + k * 0.3, null, k1, px0, y, { size: 20, c: COL.sub });
          wtext(lt, 14.5 + k * 0.3, null, v, px0, y + 38, { size: 28, tab: k === 0 });
          rule(lt, 14.6 + k * 0.3, px0, y + 58, 230, COL.line);
        });
        // 凡例
        wipe(E.outCubic(P(lt, 15.4, 0.6)), px0 - 4, F.y + 500, 240, 80, () => {
          const lw0 = 200;
          for (let i = 0; i < lw0; i++) { g.fillStyle = divCol(lerp(-5, 15, i / lw0)); g.fillRect(px0 + i, F.y + 520, 1.2, 12); }
          numText('−5%', px0, F.y + 560, { size: 20, c: COL.sub });
          numText('+15%', px0 + lw0, F.y + 560, { size: 20, c: COL.sub, align: 'right' });
        });
        // 地図
        const mb = { x: F.x + 300, y: F.y + 150, w: 670, h: 530 };
        wipe(E.outCubic(P(lt, 15.0, 1.0)), mb.x - 10, mb.y - 10, mb.w + 20, mb.h + 20, () => {
          const yy = lerp(2025, 2035, E.inOut(P(lt, 15.8, 2.6)));
          const y0 = Math.floor(yy), y1 = Math.min(2035, y0 + 1), f = yy - y0;
          drawMap(mb, (w) => divCol(lerp(diffY(w, y0), diffY(w, y1), f)));
        });
        if (lt > 18.6) {
          const xf = mapXf(mb), w = ward('都筑'), [x, y] = wardC(xf, w);
          dot(x, y, 6, COL.navy, '#ffffff');
          chip(lt, 18.6, 20.4, `都筑区 2035年 ${sgn(wDiff35(w))}%`, x + 24, y - 60, { c: COL.red });
        }
      }, [0, 140, W, 760]);

      /* ── 3) 結論カード（この章だけ途中に置く） ── */
      if (lt >= 20.5 && lt < T3) drawConclAt(lt - 20.5, '人口が減っても、救急は減らない');

      /* ── 4) 3D地図の上にロックアップ → 白で静かに止める ── */
      if (lt >= T3) {
        const lq = Math.min(lt, TEND);                 // 最後の0.5秒は静止
        reset3D(); beginGL();
        WD.forEach((w, i) => setPillar(i, hOf(w.disp[2035]), divCol(wDiff35(w))));
        const s = shiftCam({ theta: -0.35 + 0.012 * (lq - T3), phi: 0.95, dist: 36, tx: -1.5, tz: 0.5 }, 11);
        setCam(s); renderView(0, W);
        // 地図を薄くする（0.62）→ 終盤は白へ
        const thin = lerp(0.62, 1, E.inOut(P(lq, 26.6, 2.9)));
        g.fillStyle = mix('#f4f6f9', '#ffffff', E.inOut(P(lq, 26.6, 2.9)));
        g.globalAlpha = thin; g.fillRect(0, 0, W, H); g.globalAlpha = 1;
        // 結論カードの白が右へ抜けて地図が現れる
        clipRect(W * E.inOut(P(lt, T3, 0.6)), 0, W, H, () => { g.fillStyle = '#ffffff'; g.fillRect(0, 0, W, H); });
        drawLockup(lq - 21.6, M, 560);
        wtext(lq, 23.6, null, URL_TXT, M, 700, { size: 28, w: 600, c: COL.navy, tab: true });
        wtext(lq, 24.4, null, SRC, M, 760, { size: 20, c: COL.sub });
      }
    },
  };
})();
