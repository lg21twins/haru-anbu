#!/usr/bin/env python3
"""쇼케이스 성능 · 오류 측정 (헤드리스).

    python3 07_디자인/scripts/measure_server.py &         # 8000 번 포트. 캐시 허용 + 대기열 큼 (기본 http.server 는 ERR_CONNECTION_RESET 이 난다)
    python3 07_디자인/scripts/showcase_perf.py            # ko 데스크톱 + 390px
    python3 07_디자인/scripts/showcase_perf.py --page en  # 영문판
    python3 07_디자인/scripts/showcase_perf.py --out DIR  # 캡처 저장 위치

재는 것: 첫 화면(load 시점) 요청 수 · 바이트, 끝까지 스크롤한 뒤 누적,
LCP · CLS · long task 합(TBT 근사), 콘솔 오류, 실패 요청(4xx/5xx·중단).
창은 띄우지 않는다(headless). 결과는 표준출력 + --out 에 JSON 과 PNG.
"""
import argparse, json, os, sys, time
from collections import defaultdict
from playwright.sync_api import sync_playwright

PAGES = {
    "ko": "/haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html",
    "en": "/haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.en.html",
}
VIEWPORTS = {"desktop": (1440, 900), "mobile": (390, 844)}

OBSERVERS = """
window.__perf = {lcp: 0, cls: 0, longtask: 0, longtasks: 0};
new PerformanceObserver(l => { for (const e of l.getEntries()) __perf.lcp = e.startTime; })
  .observe({type: 'largest-contentful-paint', buffered: true});
new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) __perf.cls += e.value; })
  .observe({type: 'layout-shift', buffered: true});
try { new PerformanceObserver(l => { for (const e of l.getEntries()) { __perf.longtask += Math.max(0, e.duration - 50); __perf.longtasks++; } })
  .observe({type: 'longtask', buffered: true}); } catch (e) {}
"""


def kind(url, rtype):
    u = url.split("?")[0].lower()
    for ext, k in ((".mp4", "video"), (".webm", "video"), (".mp3", "audio"), (".webp", "image"),
                   (".png", "image"), (".jpg", "image"), (".jpeg", "image"), (".svg", "image"),
                   (".woff2", "font"), (".woff", "font"), (".js", "script"), (".css", "style"),
                   (".html", "document")):
        if u.endswith(ext):
            return k
    return rtype


def run(base, page_key, vp_key, out):
    w, h = VIEWPORTS[vp_key]
    stats = {"requests": [], "failed": [], "console": []}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(viewport={"width": w, "height": h},
                            device_scale_factor=2 if vp_key == "mobile" else 1,
                            is_mobile=vp_key == "mobile", has_touch=vp_key == "mobile")
        ctx.add_init_script(OBSERVERS)
        pg = ctx.new_page()

        def on_finished(req):
            try:
                size = req.sizes()["responseBodySize"]
            except Exception:
                size = 0
            stats["requests"].append({"url": req.url, "kind": kind(req.url, req.resource_type),
                                      "bytes": size, "t": time.time()})

        pg.on("requestfinished", on_finished)
        pg.on("requestfailed", lambda r: stats["failed"].append(f"{r.failure} {r.url}")
              if "ERR_ABORTED" not in (r.failure or "") or r.resource_type not in ("media",) else None)
        pg.on("response", lambda r: stats["failed"].append(f"{r.status} {r.url}") if r.status >= 400 else None)
        pg.on("console", lambda m: stats["console"].append(m.text[:200]) if m.type == "error" else None)
        pg.on("pageerror", lambda e: stats["console"].append("pageerror: " + str(e)[:200]))

        t0 = time.time()
        pg.goto(base + PAGES[page_key], wait_until="load", timeout=60000)
        t_load = time.time() - t0
        pg.wait_for_timeout(1500)
        first = list(stats["requests"])
        perf_first = pg.evaluate("window.__perf")
        nav = pg.evaluate("(() => { const n = performance.getEntriesByType('navigation')[0];"
                          " return {dcl: n.domContentLoadedEventEnd, load: n.loadEventEnd}; })()")
        if out:
            pg.screenshot(path=os.path.join(out, f"{page_key}-{vp_key}-top.png"))

        # 끝까지 천천히 스크롤 — lazy 자원이 실제로 얼마나 붙는지 본다
        total_h = pg.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < total_h:
            y += int(h * 0.8)
            pg.evaluate(f"window.scrollTo(0, {y})")
            pg.wait_for_timeout(250)
            total_h = pg.evaluate("document.documentElement.scrollHeight")
        pg.wait_for_timeout(1500)
        perf_end = pg.evaluate("window.__perf")
        b.close()

    def summarize(reqs):
        by = defaultdict(lambda: [0, 0])
        for r in reqs:
            by[r["kind"]][0] += 1
            by[r["kind"]][1] += r["bytes"]
        return {k: {"n": n, "kb": round(bt / 1024)} for k, (n, bt) in sorted(by.items(), key=lambda x: -x[1][1])}

    res = {
        "page": page_key, "viewport": vp_key, "load_s": round(t_load, 2),
        "dcl_ms": round(nav["dcl"]), "load_ms": round(nav["load"]),
        "lcp_ms": round(perf_first["lcp"]), "cls_first": round(perf_first["cls"], 3),
        "tbt_ms_first": round(perf_first["longtask"]), "tbt_ms_full": round(perf_end["longtask"]),
        "cls_full": round(perf_end["cls"], 3),
        "first": {"n": len(first), "kb": round(sum(r["bytes"] for r in first) / 1024), "by": summarize(first)},
        "full": {"n": len(stats["requests"]), "kb": round(sum(r["bytes"] for r in stats["requests"]) / 1024),
                 "by": summarize(stats["requests"])},
        "documents_first": sorted({r["url"].split("/")[-1][:60] for r in first if r["kind"] == "document"}),
        "failed": sorted(set(stats["failed"]))[:40],
        "console_errors": sorted(set(stats["console"]))[:40],
    }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8000")
    ap.add_argument("--page", default="ko", choices=PAGES)
    ap.add_argument("--vp", default="both", choices=["desktop", "mobile", "both"])
    ap.add_argument("--out", default="")
    ap.add_argument("--path", default="", help="PAGES 대신 쓸 경로 (예: 비교용 사본)")
    a = ap.parse_args()
    if a.path:
        PAGES[a.page] = a.path
    if a.out:
        os.makedirs(a.out, exist_ok=True)
    vps = ["desktop", "mobile"] if a.vp == "both" else [a.vp]
    results = [run(a.base, a.page, v, a.out) for v in vps]
    print(json.dumps(results, ensure_ascii=False, indent=1))
    if a.out:
        with open(os.path.join(a.out, f"perf-{a.page}.json"), "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.exit(main())
