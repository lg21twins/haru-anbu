#!/usr/bin/env python3
"""쇼케이스 접근성 · 사용성 객관 점검 (axe-core + 자체 지표, 헤드리스).

    python3 07_디자인/scripts/showcase_a11y.py --axe PATH/axe.min.js [--page ko|en] [--vp desktop|mobile|both]

axe-core 는 저장소에 넣지 않는다 — `npm i axe-core` 로 아무 데나 받아 경로만 준다.
iframe 안(앱 목업)은 제외하고 쇼케이스 문서 자체만 본다. 투어 안내창은 sessionStorage 로 닫아 둔다.

위반(violations)만 보지 않고 axe 가 판정을 못 한 항목(incomplete)도 같이 낸다 — 사진 위 글자·SVG 글자·의사요소 위 글자는
대비를 계산하지 못해 위반 0건이어도 실제로는 안 읽히는 곳이 숨어 있을 수 있다(2026-11-15: 차트 축 라벨 #CCC 1.5:1 이 이렇게 빠져 있었다).
"""
import argparse, json
from playwright.sync_api import sync_playwright

# 대비 4.5:1 에 못 미치지만 "역할 색(블루·그린·오렌지) 위 흰 글씨는 시각 통일을 위해 유지"로 확정된 곳(2026-08-16 결정,
# global-fix-v24 주석). 새 위반과 섞이지 않게 따로 센다. ff-r3-label 은 아직 도착 전인 릴레이 폰을 일부러 opacity .13 으로 흐리게 둔 상태다.
# 폰에서는 "눌러보세요" 알약이 .hint-guardian 등으로 잡힌다. [data-copy] 는 자동으로 넘어가는 페르소나 카피의 페이드 중간 상태(색이 전환 중이라 순간 값을 잰다).
ACCEPTED = (".ds-color-role", ".cc-ring-tag", ".feat-tap-hint", ".hint-", ".pv-pill", ".pv-brand-word", ".uik-bubble", ".ff-r3-label", "[data-copy")
ap = argparse.ArgumentParser()
ap.add_argument("--axe", required=True); ap.add_argument("--page", default="ko")
ap.add_argument("--vp", default="both"); ap.add_argument("--base", default="http://127.0.0.1:8000/haru-anbu-showcase-v8-bundle/")
a = ap.parse_args()
page = "haru-anbu-showcase-v8.html" if a.page == "ko" else "haru-anbu-showcase-v8.en.html"
axe = open(a.axe, encoding="utf-8").read()
VP = {"desktop": (1440, 900, False), "mobile": (390, 844, True)}
OWN = """() => {
  const r = {};
  r.lang = document.documentElement.lang;
  r.h1 = document.querySelectorAll('h1').length;
  const hs = [...document.querySelectorAll('h1,h2,h3,h4')].map(h => +h.tagName[1]); let skips = 0;
  hs.forEach((n, i) => { if (i && n - hs[i-1] > 1) skips++; }); r.headingSkips = skips;
  r.imgNoAlt = [...document.querySelectorAll('img:not([alt])')].length;
  r.imgNoSize = [...document.querySelectorAll('img')].filter(i => !i.getAttribute('width') && !i.getAttribute('height') && !i.style.aspectRatio).length;
  r.imgTotal = document.images.length;
  r.btnNoName = [...document.querySelectorAll('button,a[href]')].filter(e => !(e.textContent.trim() || e.getAttribute('aria-label') || e.getAttribute('title') || e.querySelector('img[alt]'))).map(e => (e.id || e.className || e.tagName).toString().slice(0, 40)).slice(0, 8);
  r.iframeNoTitle = [...document.querySelectorAll('iframe:not([title])')].length;
  r.viewport = document.querySelector('meta[name=viewport]')?.content;
  r.skipLink = !!document.querySelector('a[href^="#"][class*="skip"], a.skip-link');
  r.reducedMotion = [...document.styleSheets].some(s => { try { return [...s.cssRules].some(x => x.conditionText && x.conditionText.includes('prefers-reduced-motion')) } catch(e) { return false } });
  r.focusVisible = [...document.styleSheets].some(s => { try { return [...s.cssRules].some(x => x.selectorText && x.selectorText.includes('focus-visible')) } catch(e) { return false } });
  r.ogImage = !!document.querySelector('meta[property="og:image"]'); r.desc = !!document.querySelector('meta[name=description]');
  r.dom = document.getElementsByTagName('*').length;
  r.revealPending = [...document.querySelectorAll('.reveal')].filter(e => { let o = 1; for (let a = e; a; a = a.parentElement) o *= parseFloat(getComputedStyle(a).opacity); return o < .9 }).length;
  return r;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for vp in (["desktop", "mobile"] if a.vp == "both" else [a.vp]):
        w, h, mob = VP[vp]
        ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
        pg = ctx.new_page(); pg.goto(a.base + page + "#x", wait_until="load"); pg.wait_for_timeout(1200)
        # reveal(스크롤 등장) 요소가 투명(opacity 0)한 채로 재면 axe 가 그 글자를 검사하지 않아 위반이 과소 집계된다
        # (2026-11-15: 빠른 스크롤로 "위반 0건" 이 나왔는데 제대로 나타난 뒤엔 59건이었다). 천천히 훑고, 남은 reveal 은 강제로 켠다.
        pg.evaluate("""async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=innerHeight*.7){scrollTo(0,y);await new Promise(r=>setTimeout(r,160))}scrollTo(0,0)}""")
        pg.evaluate("document.querySelectorAll('.reveal:not(.in)').forEach(e=>e.classList.add('in'))")
        pg.wait_for_timeout(3000)
        pg.add_script_tag(content=axe)
        res = pg.evaluate("""async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']},resultTypes:['violations','incomplete']});
          window.__incomplete = r.incomplete.map(v=>({id:v.id,n:v.nodes.length,ex:v.nodes.slice(0,6).map(n=>n.target.join(' ').slice(0,70))}));
          return r.violations.map(v=>({id:v.id,impact:v.impact,help:v.help,n:v.nodes.length,all:v.nodes.map(n=>n.target.join(' ')),ex:v.nodes.map(n=>n.target.join(' ').slice(0,90)+' :: '+(n.failureSummary||'').split('\\n')[1]?.slice(0,110))}))}""")
        own = pg.evaluate(OWN)
        inc = pg.evaluate('window.__incomplete')
        print(f"\n===== {page} · {vp} =====")
        print("자체 지표:", json.dumps(own, ensure_ascii=False))
        order = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}
        accepted = 0
        for v in sorted(res, key=lambda v: order.get(v["impact"], 9)):
            if v["id"] == "color-contrast":
                keep = [e for t, e in zip(v["all"], v["ex"]) if not any(a in t for a in ACCEPTED)]
                accepted += v["n"] - len(keep)
                v = dict(v, n=len(keep), ex=keep)
                if not keep: continue
            print(f"[{v['impact']}] {v['id']} ×{v['n']} — {v['help']}")
            for e in v["ex"][:3]: print("     ", e)
        print(f"새 위반 없음이면 위 줄이 비어 있다 · 알려진 결정(역할색 위 흰 글씨 등) {accepted}노드는 따로 센 것")
        if inc:
            print("판정 보류(incomplete) — axe 가 계산하지 못해 사람이 봐야 하는 곳:")
            for v in inc: print(f"  {v['id']} ×{v['n']}  예: {', '.join(v['ex'][:4])}")
        ctx.close()
    b.close()
