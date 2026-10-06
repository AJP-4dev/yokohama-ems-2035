/* 第0章 — 契約は ../../CONTRACT.md。IIFE で包み、トップレベルに名前を出さない。
   8秒版（旧15秒版を倍速化・カウンター削除）:
   0.0–1.4 境界線が走る（中区→西区→同心円）／1.2–3.2 港から波状に押し出し＋カメラが回りながら引く／
   2.6–6.0 ロックアップ（タイトル 2.6–3.6、小見出しと罫線＋赤い正方形 3.4–4.6）／6.0–8.0 保持（地図はゆっくり回り続ける） */
(() => {
  // drawLockup と同じ形（lib.js）を、第0章の時刻割りで描く。完成形は第10章末尾の drawLockup と一致する。
  const T_TITLE = 2.6, T_SUB = 3.4;
  function lockup0(lt, x, y) {
    const ts = 120, lsp = -0.02 * ts;
    g.save(); g.letterSpacing = lsp + 'px'; font(ts, 800); const wT = g.measureText(LOGO).width; g.restore();
    // 上の小見出し（マスクワイプ 3.4–4.2）
    wipe(E.outCubic(P(lt, T_SUB, 0.8)), x, y - ts - 70, 700, 50, () => {
      const a = text('横浜市', x, y - ts - 34, { size: 28, w: 600 });
      numText('2025', x + a + 18, y - ts - 34, { size: 28, w: 600 });
      text('→', x + a + 96, y - ts - 36, { size: 28, w: 600, num: true, c: COL.sub });
      numText('2035', x + a + 136, y - ts - 34, { size: 28, w: 600 });
    });
    // タイトル本体（左→右のマスクワイプ 2.6–3.6）
    wipe(E.outCubic(P(lt, T_TITLE, 1.0)), x, y - ts - 10, wT + 40, ts + 50, () => text(LOGO, x, y, { size: ts, w: 800, ls: lsp }));
    // 罫線が左から伸び、先端の赤い正方形が右端で止まる（3.4–4.6）
    const r = E.outCubic(P(lt, T_SUB, 1.2));
    if (r > 0) {
      const ry = y + 44;
      line(x, ry, x + wT * r, ry, COL.navy, 2);
      g.fillStyle = COL.red; g.fillRect(x + wT * r + 6, ry - 7, 14, 14);
    }
  }

  window.CHAPTERS[0] = {
    title: '冒頭', q: null, concl: null, duration: 8,
    subs: [],
    uses3D: () => true,
    setup(ctx) {},
    draw(ctx, lt, t) {
      reset3D();
      WD.forEach((w, i) => {
        const k = rankN[i];
        // 0.0〜1.4s: 境界線が1区ずつ走る（中区→西区→同心円、旧版の約2倍速）
        const u = E.outCubic(P(lt, 0.05 + k * 0.055, 0.3));
        const ol = outlines[i];
        ol.visible = u > 0; ol.geometry.setDrawRange(0, Math.max(2, Math.ceil(ol.userData.n * u)));
        ol.material.opacity = 0.9;
        // 1.2〜3.2s: 港（中区）から外へ波のように押し出される
        const r = E.outCubic(P(lt, 1.2 + (DIST_N[i] / DMAX) * 1.3, 0.7));
        if (r > 0) setPillar(i, hOf(w.disp24) * r, rampDisp(w.disp24));
      });
      // カメラ: サイトと同じ角度から、わずかに回りながら引く（1.2〜3.2s）。全編を通して一定速度でゆっくり回り続ける
      const c0 = { theta: -0.35, phi: 0.95, dist: 27, tx: 1.0, tz: 1.5 };
      const c1 = { theta: -0.22, phi: 0.95, dist: 36, tx: -1.5, tz: 0.5 };
      const s = lerpCam(c0, c1, eio(lt, 1.2, 2.0));
      s.theta += 0.02 * lt;
      // 引きと同時に地図を右へ寄せ、左下のタイトルとの重なりを減らす
      setCam(shiftCam(s, 4 * eio(lt, 1.2, 2.0)));
      beginGL(); renderView(0, W);
      // タイトルの背後は「地図の方を薄く」する（2.6〜3.6s）
      const thin = 0.5 * E.inOut(P(lt, 2.6, 1.0));
      if (thin > 0) { g.fillStyle = `rgba(244,246,249,${thin})`; g.fillRect(0, 0, W, H); }
      // 2.6〜8.0s: ロックアップ
      if (lt >= T_TITLE) lockup0(lt, M, 800);
    },
  };
})();
