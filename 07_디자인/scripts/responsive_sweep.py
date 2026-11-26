#!/usr/bin/env python3
"""폭을 촘촘히 바꿔 가며 '화면 밖으로 나가는 요소'를 찾는다 (헤드리스).

    python3 07_디자인/scripts/responsive_sweep.py                 # 320~1600, 20px 간격
    python3 07_디자인/scripts/responsive_sweep.py --from 760 --to 1300 --step 10 --page en

overflow-x 를 잘라내는 조상이 없는 요소만 센다(가로 스크롤 카드처럼 의도된 것은 제외).
body 가 overflow-x:hidden 이라 실제 가로 스크롤은 안 생기지만 '잘려 보이는' 것은 잡힌다.
"""
import argparse
from playwright.sync_api import sync_playwright
JS = """async () => {
  const H = () => document.documentElement.scrollHeight;
  for (let y = 0; y < H(); y += innerHeight * 1.5) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); }
  await new Promise(r => setTimeout(r, 400));
  const vw = document.documentElement.clientWidth, out = {};
  const clipped = el => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { if (/(hidden|clip|auto|scroll)/.test(getComputedStyle(a).overflowX)) return true; } return false; };
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el); if (cs.position === 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') return;
    const b = el.getBoundingClientRect(); if (!b.width) return;
    const over = Math.max(b.right - vw, -b.left);
    if (over > 1 && !clipped(el)) {
      const k = (el.id ? '#' + el.id : el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 2).join('.')) + ' @' + (el.closest('section[id]')?.id || '-');
      out[k] = Math.max(out[k] || 0, Math.round(over));
    }
  });
  return out;
}"""
ap = argparse.ArgumentParser()
ap.add_argument("--from", dest="lo", type=int, default=320); ap.add_argument("--to", dest="hi", type=int, default=1600)
ap.add_argument("--step", type=int, default=20); ap.add_argument("--page", default="ko")
a = ap.parse_args()
page = "haru-anbu-showcase-v8.html" if a.page == "ko" else "haru-anbu-showcase-v8.en.html"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for w in range(a.lo, a.hi + 1, a.step):
        mob = w <= 1024
        ctx = b.new_context(viewport={"width": w, "height": 900 if w > 600 else 844}, is_mobile=mob and w < 769, has_touch=mob and w < 769)
        pg = ctx.new_page(); pg.goto(f"http://127.0.0.1:8000/haru-anbu-showcase-v8-bundle/{page}#x", wait_until="load"); pg.wait_for_timeout(600)
        r = pg.evaluate(JS); ctx.close()
        # 자식까지 전부 나오므로 가장 바깥(같은 섹션에서 가장 큰 값) 몇 개만
        top = sorted(r.items(), key=lambda x: -x[1])[:4]
        print(w, "OK" if not r else "  ".join(f"{k}+{v}" for k, v in top))
    b.close()
