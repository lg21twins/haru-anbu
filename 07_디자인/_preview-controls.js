/* ============================================================
   하루안부 디자인 시스템 · Preview 공용 컨트롤
   ----------------------------------------------------------------
   v3.2 신설. preview 페이지 상단의 다크모드 토글 + 역할 선택기.
   각 preview 페이지의 nav 안에 다음 markup을 두면 자동 바인딩됨:

   <div class="pv-controls">
     <select class="pv-role-select" data-pv-role>
       <option value="guardian">보호자</option>
       <option value="medical">의료진</option>
       <option value="patient">환자</option>
     </select>
     <button class="pv-toggle" data-pv-theme aria-pressed="false">
       <iconify-icon icon="fluent:weather-moon-24-filled"></iconify-icon>
       <span>다크</span>
     </button>
   </div>
   ============================================================ */

(function () {
  const root = document.documentElement;
  const LS_THEME = 'haru-preview-theme';
  const LS_ROLE = 'haru-preview-role';

  // --- v3.2.3: 라이트 강제 (사용자 지시 — 다크 봉인) ---
  // 다크 모드는 v9.5 페이지들과 충돌해 깨짐을 일으키므로 preview에서도 봉인.
  root.setAttribute('data-theme', 'light');
  if (localStorage.getItem(LS_THEME) === 'dark') {
    localStorage.removeItem(LS_THEME);
  }

  const savedRole = localStorage.getItem(LS_ROLE);
  if (savedRole) {
    root.setAttribute('data-role', savedRole);
  }

  // --- 다크 토글 바인딩 (v3.2.3 봉인 — 버튼은 숨기고, 클릭해도 작동 안 함) ---
  function bindThemeToggle(btn) {
    // 다크 봉인 — 토글 자체를 보이지 않게.
    btn.style.display = 'none';
  }

  // --- 역할 셀렉터 바인딩 ---
  function bindRoleSelect(sel) {
    sel.value = root.getAttribute('data-role') || 'guardian';
    sel.addEventListener('change', () => {
      root.setAttribute('data-role', sel.value);
      localStorage.setItem(LS_ROLE, sel.value);
    });
  }

  // --- DOMContentLoaded에서 바인딩 ---
  function init() {
    document.querySelectorAll('[data-pv-theme]').forEach(bindThemeToggle);
    document.querySelectorAll('[data-pv-role]').forEach(bindRoleSelect);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
