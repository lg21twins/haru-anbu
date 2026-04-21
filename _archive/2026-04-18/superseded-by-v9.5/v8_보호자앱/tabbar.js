(function () {
  const TABS = [
    { key: 'home',    href: 'g-guardian-live.html', icon: 'fluent:home-24-filled' },
    { key: 'guide',   href: 'g-ai.html',            icon: 'fluent:compass-northwest-24-filled' },
    { key: 'report',  href: 'g02-ai-report.html',   icon: 'fluent:chart-multiple-24-filled' },
    { key: 'billing', href: 'g08-billing.html',     icon: 'fluent:payment-24-filled' },
    { key: 'my',      href: 'g05-mypage.html',       icon: 'fluent:person-24-filled' }
  ];

  document.querySelectorAll('.tabbar[data-active]').forEach(function (nav) {
    var active = nav.dataset.active;
    nav.innerHTML = TABS.map(function (t) {
      return '<a href="' + t.href + '" class="tab' + (t.key === active ? ' active' : '') + '">' +
        '<iconify-icon icon="' + t.icon + '" style="font-size:22px;"></iconify-icon>' +
        '</a>';
    }).join('');
  });
})();
