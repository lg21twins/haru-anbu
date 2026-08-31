(function () {
  "use strict";

  function toast(message, durationMs) {
    var element = document.querySelector("#toast, #toastEl, #cgToast");
    if (!element) return;

    var configuredDuration = Number(document.documentElement.dataset.toastDuration);
    var duration = durationMs || configuredDuration || 1800;
    element.textContent = message;
    element.classList.add("show", "is-shown");
    window.clearTimeout(element.__haruToastTimer);
    element.__haruToastTimer = window.setTimeout(function () {
      element.classList.remove("show", "is-shown");
    }, duration);
  }

  window.toast = toast;
})();
