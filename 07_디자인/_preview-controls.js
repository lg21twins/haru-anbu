/* ============================================================
   하루안부 디자인 시스템 · Preview 공용 컨트롤
   ----------------------------------------------------------------
   preview 페이지 상단의 역할 선택기.
   각 preview 페이지의 nav 안에 다음 markup을 두면 자동 바인딩됨:

   <div class="pv-controls">
     <select class="pv-role-select" data-pv-role>
       <option value="guardian">보호자</option>
       <option value="medical">의료진</option>
       <option value="patient">환자</option>
     </select>
   </div>

   v3.2.8 (2026-05-17): 다크 모드 제거. 라이트 단일 운영.
     · data-theme="light" 강제 코드 제거 (라이트가 기본값)
     · 다크 토글 버튼 바인딩 제거
     · 레거시 키 정리(haru-preview-theme)는 유지 — 기존 브라우저에 남아있을 수 있음
   ============================================================ */

(function () {
  const root = document.documentElement;
  const LS_ROLE = 'haru-preview-role';

  // --- 레거시 다크 키 자동 정리 ---
  if (localStorage.getItem('haru-preview-theme') !== null) {
    localStorage.removeItem('haru-preview-theme');
  }

  const savedRole = localStorage.getItem(LS_ROLE);
  if (savedRole) {
    root.setAttribute('data-role', savedRole);
  }

  // --- 다크 토글 마크업이 남아있으면 숨김 처리(레거시 preview 파일 호환) ---
  function hideLegacyThemeToggle(btn) {
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

  function init() {
    document.querySelectorAll('[data-pv-theme]').forEach(hideLegacyThemeToggle);
    document.querySelectorAll('[data-pv-role]').forEach(bindRoleSelect);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
