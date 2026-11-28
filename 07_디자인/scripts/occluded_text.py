#!/usr/bin/env python3
"""다른 요소에 가려진 글자 찾기 (헤드리스).

    python3 07_디자인/scripts/occluded_text.py [--page ko|en] [--widths 320,390,768,1440]

화면을 위에서 아래로 훑으며, 보이는 글자의 왼쪽·가운데·오른쪽 점에서 elementFromPoint 로 맨 위 요소를 본다.
그 요소가 글자 자신(또는 조상/자손)이 아니면 '가려진 글자'다. 겹쳐 놓은 원(벤 다이어그램)처럼
overflow 잘림 검사(responsive_sweep.py)와 axe 가 못 보는 결함을 잡는다
(2026-11-15: 영문 모바일 "Care team" 의 C 가 파란 원에 가려져 "are team" 으로 보였다).
고정 상단바·투어 카드·건너뛰기 링크처럼 일부러 덮는 UI 는 제외한다.
"""
import argparse
from collections import defaultdict
from playwright.sync_api import sync_playwright

PAGES = {"ko": "haru-anbu-showcase-v8.html", "en": "haru-anbu-showcase-v8.en.html"}
JS = r"""() => {
  const IGN = '.topbar, nav, #narrationPrompt, .np-card, .np-backdrop, .skip-link, .m-sheet, .m-launch, #narrHint, .feat-exit, [class*=fab], #playFab';
  const sel = e => (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/)[0] : e.tagName.toLowerCase());
  const out = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while (n = w.nextNode()) {
    const t = n.textContent.trim(); if (t.length < 2) continue;
    const el = n.parentElement; if (!el || el.closest('script,style,noscript,svg,iframe,[aria-hidden=true],.m-hide')) continue;
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    let op = 1; for (let a = el; a; a = a.parentElement) { const c = getComputedStyle(a); if (c.display === 'none') { op = 0; break } op *= parseFloat(c.opacity) }
    if (op < .5) continue;
    const range = document.createRange(); range.selectNodeContents(n);
    const rects = [...range.getClientRects()].filter(r => r.width > 4 && r.height > 4);
    if (!rects.length) continue;
    // pointer-events:none 글자(떠 있는 안내 알림 등)는 elementFromPoint 가 건너뛰어 아래 요소가 잡힌다 — 가려진 게 아니다
    let pe = false; for (let a = el; a; a = a.parentElement) { if (getComputedStyle(a).pointerEvents === 'none') { pe = true; break } }
    if (pe) continue;
    const r = rects[0];
    // 접힌 아코디언처럼 조상의 overflow 에 잘려 안 보이는 글자는 제외
    let clipped = false;
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const c = getComputedStyle(a); if (c.overflow === 'visible' && c.overflowY === 'visible' && c.overflowX === 'visible') continue;
      const ar = a.getBoundingClientRect();
      if (r.top >= ar.bottom - 1 || r.bottom <= ar.top + 1 || r.left >= ar.right - 1 || r.right <= ar.left + 1 || ar.height < 2) { clipped = true; break }
    }
    if (clipped) continue;
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) continue;
    if (r.top < 0 || r.bottom > innerHeight) continue;                       // 화면에 온전히 들어온 것만
    const pts = [[r.left + 2, r.top + r.height / 2], [r.left + r.width / 2, r.top + r.height / 2], [r.right - 2, r.top + r.height / 2]];
    for (const [x, y] of pts) {
      if (x < 0 || x > innerWidth) continue;
      const top = document.elementFromPoint(x, y); if (!top) continue;
      if (top === el || el.contains(top) || top.contains(el)) continue;
      if (top.closest(IGN) || el.closest(IGN)) continue;
      out.push({txt: t.slice(0, 24), el: sel(el), by: sel(top), x: Math.round(x), y: Math.round(y)});
      break;
    }
  }
  return out;
}"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8000/haru-anbu-showcase-v8-bundle/")
    ap.add_argument("--page", default="ko", choices=PAGES)
    ap.add_argument("--widths", default="320,390,768,1024,1440")
    a = ap.parse_args()
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        for W in [int(x) for x in a.widths.split(",")]:
            H = 900 if W >= 700 else 844
            ctx = b.new_context(viewport={"width": W, "height": H}, is_mobile=W < 700, has_touch=W < 700)
            ctx.add_init_script("try{sessionStorage.setItem('haru-tour-asked','1')}catch(e){}")
            pg = ctx.new_page(); pg.goto(a.base + PAGES[a.page], wait_until="load"); pg.wait_for_timeout(1500)
            found = defaultdict(set)
            total = pg.evaluate("document.documentElement.scrollHeight"); y = 0
            while y < total:
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(450)
                for r in pg.evaluate(JS): found[(r["el"], r["by"])].add(r["txt"])
                y += int(H * 0.7); total = pg.evaluate("document.documentElement.scrollHeight")
            print(f"{a.page} {W}px — 가려진 글자 {len(found)}종")
            for (el, by), ts in sorted(found.items()):
                print(f"   {el:34s} <- 가림: {by:30s} 예: {sorted(ts)[0]!r}")
            ctx.close()
        b.close()

if __name__ == "__main__":
    main()
