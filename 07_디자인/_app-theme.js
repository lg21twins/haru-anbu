/* ============================================================
   하루안부 · App Theme Loader (v3.2.4)
   ----------------------------------------------------------------
   모든 모바일·웹 앱 페이지의 <head>에서 즉시 실행되어
   사용자 접근성 모드를 복원한다. (페이지 깜박임 방지)

   사용:
     <head>
       <link rel="stylesheet" href="../07_디자인/tokens/tokens.css">
       <script src="../07_디자인/_app-theme.js"></script>   <!-- defer X -->
     </head>

   localStorage 키 컨벤션 (v3.2.4 통일):
     · 모든 키는 'haru-app-*' 접두사
     · preview 전용 키는 'haru-preview-*' (별도 네임스페이스)

   현재 활성 키:
     haru-app-text-size   — 'large' (있을 때만) — 환자·시니어
     haru-app-contrast    — 'high' (있을 때만) — 환자·시니어

   레거시 / 봉인된 키 (자동 청소):
     haru-app-theme       — v3.2.3에서 봉인. 진입 시 자동 삭제.
     haru-preview-theme   — v3.2.3에서 봉인. _preview-controls.js가 청소.

   helper API (전역 window.HaruTheme):
     setTextSize(size)      — 'normal' | 'large'
     setContrast(level)     — 'normal' | 'high'
     getTextSize() / getContrast()
     setTheme() / getTheme() / isDark() — 봉인 (다크 차단)
   ============================================================ */
(function () {
  const root = document.documentElement;

  // ---- 라이트 강제 + 레거시 키 자동 청소 ----
  root.setAttribute('data-theme', 'light');

  // 봉인된 다크 관련 레거시 키 제거 (값에 관계없이 키 자체 삭제)
  ['haru-app-theme', 'haru-preview-theme'].forEach((k) => {
    if (localStorage.getItem(k) !== null) localStorage.removeItem(k);
  });

  const textSize = localStorage.getItem('haru-app-text-size');
  if (textSize === 'large') {
    root.setAttribute('data-a11y-text', 'large');
  }

  const contrast = localStorage.getItem('haru-app-contrast');
  if (contrast === 'high') {
    root.setAttribute('data-a11y-contrast', 'high');
  }

  // ---- API ----
  const api = {
    // v3.2.3 — 다크 봉인. 어떤 값을 받아도 light로 고정.
    setTheme(_t) {
      root.setAttribute('data-theme', 'light');
      localStorage.removeItem('haru-app-theme');
      window.dispatchEvent(new CustomEvent('haru:theme-change', { detail: { theme: 'light' } }));
    },
    getTheme() { return 'light'; },
    isDark() { return false; },
    setTextSize(s) {
      if (s === 'large') {
        root.setAttribute('data-a11y-text', 'large');
        localStorage.setItem('haru-app-text-size', 'large');
      } else {
        root.removeAttribute('data-a11y-text');
        localStorage.removeItem('haru-app-text-size');
      }
      window.dispatchEvent(new CustomEvent('haru:text-size-change', { detail: { size: s } }));
    },
    getTextSize() {
      return localStorage.getItem('haru-app-text-size') === 'large' ? 'large' : 'normal';
    },
    setContrast(c) {
      if (c === 'high') {
        root.setAttribute('data-a11y-contrast', 'high');
        localStorage.setItem('haru-app-contrast', 'high');
      } else {
        root.removeAttribute('data-a11y-contrast');
        localStorage.removeItem('haru-app-contrast');
      }
      window.dispatchEvent(new CustomEvent('haru:contrast-change', { detail: { contrast: c } }));
    },
    getContrast() {
      return localStorage.getItem('haru-app-contrast') === 'high' ? 'high' : 'normal';
    },
  };

  window.HaruTheme = api;
})();
