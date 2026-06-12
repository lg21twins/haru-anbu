/* ============================================================================
   하루안부 · 요양보호사 앱 v11 · 공통 JS
   ============================================================================
   API:
     HaruCG.toast(msg, durationMs?)
     HaruCG.openSheet(html, opts?)
       opts: { variant: 'default'|'danger'|'warn'|'info' }
     HaruCG.closeSheet()
     HaruCG.bindSOS(button)        — short tap → 유형 시트, 3초 hold → 1초 countdown 후 발신
     HaruCG.sosSend(typeLabel)     — 발신 결과 toast + (optional) 로그 콜백
     HaruCG.installSOS()           — 페이지 내 .cg-sos[data-sos-bind] 모두 자동 연결
     HaruCG.installSwitches()      — .cg-switchrow의 .cg-switch a11y 바인딩

   페이지 사용:
     <button class="cg-sos" data-sos-bind aria-label="긴급 SOS · 3초 길게 누르면 즉시 발신">
       <span class="cg-sos__ring" aria-hidden="true">
         <svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="27"/></svg>
       </span>
       <iconify-icon icon="fluent:warning-24-filled"></iconify-icon>
     </button>
     <div class="cg-overlay" id="cgOverlay">
       <div class="cg-sheet">
         <div class="cg-sheet__handle"></div>
         <div id="cgSheetContent"></div>
       </div>
     </div>
     <div class="cg-toast" id="cgToast"></div>

     <script>HaruCG.installSOS(); HaruCG.installSwitches();</script>
   ============================================================================ */

(function (global) {
  'use strict';

  const SOS_HOLD_MS = 3000;       // 3초 길게 누름
  const SOS_RING_CIRCUMFERENCE = 172;  // ≈ 2π·27
  const SOS_COUNTDOWN_MS = 1000;  // confirmation 1초

  // -------------------------------------------------------------------------
  // i18n — SOS 시트/토스트 문구를 <html lang>(ko·en·zh)에 맞춰 선택 (기본 ko)
  // 다국어 화면(c0X-*.en.html / .zh.html)에서도 같은 공통 JS가 언어에 맞게 동작
  // -------------------------------------------------------------------------

  const I18N = {
    ko: {
      sosTitle: '긴급 상황 알리기',
      sosSub: '상황을 선택하면 간호사·보호자에게 즉시 전송됩니다',
      sosFall: '낙상', sosFaint: '의식 저하', sosBreath: '호흡 곤란', sosOther: '기타 · 음성',
      sosHint: '버튼을 <b>3초 길게 누르면</b> 1초 확인 후 즉시 음성 SOS가 발신됩니다 (오발신 방지)',
      cdTitle: 'SOS 발신 준비',
      cdSub: '아래 카운트가 0이 되면 자동 발신됩니다',
      cdLabel: '즉시 음성 SOS · 자동 발신',
      cdCancel: '취소',
      sendAuto: '즉시 발신 · 음성 녹음',
      sentToast: function (t, s) { return 'SOS [' + t + '] · ' + s + ' 발송 — 간호사·보호자·센터 통지'; },
      cancelToast: 'SOS 발신 취소됨',
      locale: 'ko-KR'
    },
    en: {
      sosTitle: 'Report emergency',
      sosSub: 'Select a situation to notify the nurse and family instantly',
      sosFall: 'Fall', sosFaint: 'Reduced consciousness', sosBreath: 'Difficulty breathing', sosOther: 'Other · Voice',
      sosHint: '<b>Press and hold for 3 sec</b> to send a voice SOS instantly after a 1-sec confirmation (prevents misfires)',
      cdTitle: 'Sending SOS',
      cdSub: 'Sends automatically when the count reaches 0',
      cdLabel: 'Instant voice SOS · Auto-send',
      cdCancel: 'Cancel',
      sendAuto: 'Instant send · Voice recording',
      sentToast: function (t, s) { return 'SOS [' + t + '] · ' + s + ' sent — Nurse, family & center notified'; },
      cancelToast: 'SOS canceled',
      locale: 'en-US'
    },
    zh: {
      sosTitle: '上报紧急情况',
      sosSub: '选择情况后将立即通知护士和家属',
      sosFall: '跌倒', sosFaint: '意识下降', sosBreath: '呼吸困难', sosOther: '其他 · 语音',
      sosHint: '<b>长按按钮 3 秒</b>，经 1 秒确认后立即发送语音 SOS（防止误发）',
      cdTitle: '准备发送 SOS',
      cdSub: '计数归零后自动发送',
      cdLabel: '即时语音 SOS · 自动发送',
      cdCancel: '取消',
      sendAuto: '即时发送 · 语音录音',
      sentToast: function (t, s) { return 'SOS [' + t + '] · ' + s + ' 已发送 — 已通知护士、家属与中心'; },
      cancelToast: '已取消发送 SOS',
      locale: 'zh-CN'
    }
  };

  function T() {
    const l = (document.documentElement.getAttribute('lang') || 'ko').slice(0, 2).toLowerCase();
    return I18N[l] || I18N.ko;
  }

  // -------------------------------------------------------------------------
  // util
  // -------------------------------------------------------------------------

  function $(sel, root) { return (root || document).querySelector(sel); }

  function vibrate(pattern) {
    if (navigator.vibrate) {
      try { navigator.vibrate(pattern); } catch (_) {}
    }
  }

  function escHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' })[c];
    });
  }

  // -------------------------------------------------------------------------
  // toast
  // -------------------------------------------------------------------------

  function toast(msg, durationMs) {
    const el = $('#cgToast');
    if (!el) {
      // 호환: 페이지가 #toastEl 사용 시 fallback
      const fallback = $('#toastEl');
      if (fallback) {
        fallback.textContent = msg;
        fallback.classList.add('show');
        clearTimeout(fallback._cgT);
        fallback._cgT = setTimeout(function () { fallback.classList.remove('show'); }, durationMs || 2400);
      }
      return;
    }
    el.textContent = msg;
    el.classList.add('is-shown');
    clearTimeout(el._cgT);
    el._cgT = setTimeout(function () { el.classList.remove('is-shown'); }, durationMs || 2400);
  }

  // -------------------------------------------------------------------------
  // sheet
  // -------------------------------------------------------------------------

  function openSheet(html, opts) {
    opts = opts || {};
    const overlay = $('#cgOverlay');
    const content = $('#cgSheetContent');
    if (!overlay || !content) return;
    content.innerHTML = html;
    overlay.classList.add('is-open');
    overlay.setAttribute('data-variant', opts.variant || 'default');
    document.body.style.overflow = 'hidden';
  }

  function closeSheet() {
    const overlay = $('#cgOverlay');
    if (!overlay) return;
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  // 오버레이 외곽 탭으로 닫기
  function bindOverlayDismiss() {
    const overlay = $('#cgOverlay');
    if (!overlay || overlay._cgBound) return;
    overlay._cgBound = true;
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeSheet();
    });
  }

  // -------------------------------------------------------------------------
  // SOS — short tap → type sheet, 3초 hold → 1초 countdown → send
  // -------------------------------------------------------------------------

  function openSosTypeSheet() {
    const t = T();
    openSheet(
      '<div class="cg-sheet__head">' +
        '<div class="cg-sheet__ico cg-sheet__ico--danger">' +
          '<iconify-icon icon="fluent:warning-24-filled"></iconify-icon>' +
        '</div>' +
        '<div>' +
          '<div class="cg-sheet__ttl cg-sheet__ttl--danger">' + t.sosTitle + '</div>' +
          '<div class="cg-sheet__sub">' + t.sosSub + '</div>' +
        '</div>' +
      '</div>' +
      '<div class="cg-sos-grid">' +
        sosCard(t.sosFall, 'fluent:person-arrow-back-24-filled') +
        sosCard(t.sosFaint, 'fluent:brain-circuit-24-filled') +
        sosCard(t.sosBreath, 'fluent:heart-pulse-24-filled') +
        sosCard(t.sosOther, 'fluent:mic-24-filled') +
      '</div>' +
      '<div class="cg-sos-hint">' + t.sosHint + '</div>',
      { variant: 'danger' }
    );
  }

  function sosCard(label, icon) {
    return (
      '<button class="cg-sos-card" type="button" onclick="HaruCG.sosSend(\'' + escHtml(label) + '\')">' +
        '<iconify-icon icon="' + icon + '"></iconify-icon>' +
        '<span class="cg-sos-card__t">' + escHtml(label) + '</span>' +
      '</button>'
    );
  }

  function sosSend(typeLabel) {
    closeSheet();
    const t = T();
    const stamp = new Date().toLocaleTimeString(t.locale, { hour: '2-digit', minute: '2-digit' });
    toast(t.sentToast(typeLabel, stamp), 3200);
    vibrate([30, 60, 120, 60, 30]);

    if (typeof global.onSosSent === 'function') {
      try { global.onSosSent({ type: typeLabel, time: stamp }); } catch (_) {}
    }
  }

  function openSosCountdown() {
    let remaining = SOS_COUNTDOWN_MS / 1000;
    function render() {
      const t = T();
      openSheet(
        '<div class="cg-sheet__head">' +
          '<div class="cg-sheet__ico cg-sheet__ico--danger">' +
            '<iconify-icon icon="fluent:warning-24-filled"></iconify-icon>' +
          '</div>' +
          '<div>' +
            '<div class="cg-sheet__ttl cg-sheet__ttl--danger">' + t.cdTitle + '</div>' +
            '<div class="cg-sheet__sub">' + t.cdSub + '</div>' +
          '</div>' +
        '</div>' +
        '<div class="cg-sos-countdown">' +
          '<div class="cg-sos-countdown__num" id="cgSosCount">' + remaining + '</div>' +
          '<div class="cg-sos-countdown__t">' + t.cdLabel + '</div>' +
          '<button type="button" class="cg-sos-countdown__cancel" onclick="HaruCG._cancelCountdown()">' + t.cdCancel + '</button>' +
        '</div>',
        { variant: 'danger' }
      );
    }
    render();
    let timer = setInterval(function () {
      remaining -= 1;
      const numEl = $('#cgSosCount');
      if (numEl) numEl.textContent = remaining;
      if (remaining <= 0) {
        clearInterval(timer);
        global._cgCountdownTimer = null;
        sosSend(T().sendAuto);
      }
    }, 1000);
    global._cgCountdownTimer = timer;
  }

  function cancelCountdown() {
    if (global._cgCountdownTimer) {
      clearInterval(global._cgCountdownTimer);
      global._cgCountdownTimer = null;
    }
    closeSheet();
    toast(T().cancelToast);
  }

  function bindSOS(btn) {
    if (!btn || btn._cgSosBound) return;
    btn._cgSosBound = true;

    const ringEl = btn.querySelector('.cg-sos__ring circle, .sos-ring circle');
    let holdStart = 0;
    let holdRAF = 0;
    let holdFired = false;
    let cancelled = false;

    function resetRing() {
      if (ringEl) ringEl.style.strokeDashoffset = SOS_RING_CIRCUMFERENCE;
      btn.classList.remove('is-holding', 'holding');
    }
    function animRing(ts) {
      if (cancelled) return;
      const elapsed = ts - holdStart;
      const p = Math.min(elapsed / SOS_HOLD_MS, 1);
      if (ringEl) ringEl.style.strokeDashoffset = SOS_RING_CIRCUMFERENCE - SOS_RING_CIRCUMFERENCE * p;
      if (p < 1 && !holdFired) {
        holdRAF = requestAnimationFrame(animRing);
      } else if (p >= 1 && !holdFired) {
        holdFired = true;
        vibrate([30, 60, 120]);
        resetRing();
        openSosCountdown();
      }
    }
    function start(e) {
      if (e.type === 'mousedown' && e.button !== 0) return;
      e.preventDefault();
      holdFired = false;
      cancelled = false;
      btn.classList.add('is-holding');
      holdStart = performance.now();
      holdRAF = requestAnimationFrame(animRing);
    }
    function end() {
      cancelAnimationFrame(holdRAF);
      const held = performance.now() - holdStart;
      cancelled = true;
      if (holdFired) { resetRing(); return; }
      resetRing();
      if (held < 400) openSosTypeSheet();
    }

    btn.addEventListener('mousedown', start);
    btn.addEventListener('touchstart', start, { passive: false });
    btn.addEventListener('mouseup', end);
    btn.addEventListener('mouseleave', end);
    btn.addEventListener('touchend', end);
    btn.addEventListener('touchcancel', end);
  }

  function installSOS() {
    bindOverlayDismiss();
    const buttons = document.querySelectorAll('.cg-sos[data-sos-bind], .cg-sos:not([data-no-bind])');
    buttons.forEach(bindSOS);
  }

  // -------------------------------------------------------------------------
  // Switches (a11y) — full row clickable
  // -------------------------------------------------------------------------

  function installSwitches() {
    const rows = document.querySelectorAll('.cg-switchrow');
    rows.forEach(function (row) {
      if (row._cgSwitchBound) return;
      row._cgSwitchBound = true;
      const sw = row.querySelector('.cg-switch');
      if (!sw) return;
      if (!sw.hasAttribute('role')) sw.setAttribute('role', 'switch');
      if (!sw.hasAttribute('aria-checked')) sw.setAttribute('aria-checked', sw.classList.contains('is-on') ? 'true' : 'false');
      function toggle() {
        const next = sw.getAttribute('aria-checked') !== 'true';
        sw.setAttribute('aria-checked', String(next));
        if (typeof row.dataset.onChange === 'string' && typeof global[row.dataset.onChange] === 'function') {
          global[row.dataset.onChange](next, row);
        }
      }
      row.addEventListener('click', toggle);
      sw.addEventListener('keydown', function (e) {
        if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
      });
    });
  }

  // -------------------------------------------------------------------------
  // expose
  // -------------------------------------------------------------------------

  global.HaruCG = {
    toast: toast,
    openSheet: openSheet,
    closeSheet: closeSheet,
    bindSOS: bindSOS,
    installSOS: installSOS,
    installSwitches: installSwitches,
    openSosTypeSheet: openSosTypeSheet,
    sosSend: sosSend,
    _cancelCountdown: cancelCountdown
  };

  // 자동 부트
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      installSOS();
      installSwitches();
    });
  } else {
    installSOS();
    installSwitches();
  }

})(window);
