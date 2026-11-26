#!/usr/bin/env python3
"""인라인 <style> 의 죽은 규칙 찾기 / 지우기 (쇼케이스용).

    python3 07_디자인/scripts/dead_css.py FILE.html            # 보고만
    python3 07_디자인/scripts/dead_css.py FILE.html --apply    # 지운다
    python3 07_디자인/scripts/dead_css.py FILE.html --runtime http://127.0.0.1:8000/…  # 렌더 확인 추가

판정(둘 다 만족해야 '죽음'):
  1) 정적 — 셀렉터 목록의 '모든' 셀렉터가, <style> 밖(HTML 속성·JS 문자열·주석 제외 없음)
     어디에도 단어로 나오지 않는 클래스/ID 를 하나 이상 요구한다.
     JS 가 이름을 조립할 가능성('is-' + x, `pb-${k}`)을 막으려고, 토큰의 하이픈 접두어가
     <style> 밖에 따옴표·백틱 바로 뒤에 '…-' 꼴로 나오면 살아 있는 것으로 본다.
  2) 런타임(옵션) — 데스크톱·모바일로 끝까지 스크롤한 뒤에도 querySelector 가 0 개.
@keyframes 는 이름이 animation 속성·JS 어디에도 없을 때만 죽음으로 본다.
주석은 건드리지 않는다(설계 근거가 들어 있다). 규칙 바로 앞 주석이 그 규칙만 설명하면 남는다 —
사람이 나중에 정리한다.
"""
import argparse, re, sys

STYLE_RE = re.compile(r"(<style[^>]*>)(.*?)(</style>)", re.S)
TOKEN_RE = re.compile(r"([.#])(-?[_a-zA-Z][_a-zA-Z0-9-]*)")


def strip_pseudo_args(sel):
    # :not(.x) / :is(.x) / :has(.x) 안의 토큰은 '요구'가 아니다 → 괄호 내용 제거
    out, depth = [], 0
    for ch in sel:
        if ch == "(":
            depth += 1
            continue
        if ch == ")":
            depth -= 1
            continue
        if depth == 0:
            out.append(ch)
    s = "".join(out)
    s = re.sub(r"\[[^\]]*\]", "", s)              # 속성 셀렉터 안의 . 은 토큰 아님
    s = re.sub(r"url\([^)]*\)", "", s)
    return s


def parse_blocks(css, base):
    """(start, end, kind, prelude, inner_start) 목록. kind: rule | at-block | at-stmt | keyframes"""
    items, i, n = [], 0, len(css)
    while i < n:
        # 공백·주석 건너뛰기
        m = re.compile(r"\s+|/\*.*?\*/", re.S).match(css, i)
        if m and m.end() > i:
            i = m.end()
            continue
        start = i
        # 프렐루드: { 또는 ; 까지 (주석·문자열 고려)
        j, q = i, None
        while j < n:
            c = css[j]
            if q:
                if c == "\\":
                    j += 2
                    continue
                if c == q:
                    q = None
            elif c in "\"'":
                q = c
            elif css.startswith("/*", j):
                k = css.find("*/", j + 2)
                j = n if k < 0 else k + 2
                continue
            elif c in "{;}":
                break
            j += 1
        if j >= n:
            break
        prelude = css[start:j].strip()
        if css[j] == ";":
            items.append((base + start, base + j + 1, "at-stmt", prelude, None))
            i = j + 1
            continue
        if css[j] == "}":           # 짝 안 맞는 닫힘 — 건너뜀
            i = j + 1
            continue
        # { … } 짝 찾기
        depth, k, q = 0, j, None
        while k < n:
            c = css[k]
            if q:
                if c == "\\":
                    k += 2
                    continue
                if c == q:
                    q = None
            elif c in "\"'":
                q = c
            elif css.startswith("/*", k):
                e = css.find("*/", k + 2)
                k = n if e < 0 else e + 2
                continue
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        end = k + 1
        if prelude.startswith("@"):
            name = prelude.split()[0].lower()
            if "keyframes" in name:
                items.append((base + start, base + end, "keyframes", prelude, None))
            elif name in ("@media", "@supports", "@container", "@layer"):
                items.append((base + start, base + end, "at-block", prelude, None))
                items.extend(parse_blocks(css[j + 1:k], base + j + 1))
            else:
                items.append((base + start, base + end, "at-other", prelude, None))
        else:
            items.append((base + start, base + end, "rule", prelude, (base + j + 1, base + k)))
        i = end
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--runtime", default="")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()
    src = open(a.file, encoding="utf-8").read()

    styles = list(STYLE_RE.finditer(src))
    outside = STYLE_RE.sub(" ", src)
    words = set(re.findall(r"[A-Za-z_][A-Za-z0-9_-]*", outside))
    prefixes = set(re.findall(r"""["'`\s.]([A-Za-z_][A-Za-z0-9_-]*-)(?=["'`$+]|\$\{)""", outside))
    all_css = "".join(m.group(2) for m in styles)

    def token_alive(tok):
        if tok in words:
            return True
        parts = tok.split("-")
        for k in range(1, len(parts)):
            if "-".join(parts[:k]) + "-" in prefixes:
                return True
        return False

    candidates = []
    for m in styles:
        css = m.group(2)
        base = m.start(2)
        for (s, e, kind, pre, inner) in parse_blocks(css, base):
            if kind == "rule":
                sels = [x.strip() for x in pre.split(",") if x.strip()]
                dead_sels = []
                for sel in sels:
                    toks = TOKEN_RE.findall(strip_pseudo_args(sel))
                    if any(not token_alive(t) for _, t in toks):
                        dead_sels.append(sel)
                if sels and len(dead_sels) == len(sels):
                    candidates.append((s, e, "rule", pre))
            elif kind == "keyframes":
                name = pre.split()[1] if len(pre.split()) > 1 else ""
                used_css = re.search(r"animation(-name)?\s*:[^;}]*\b" + re.escape(name) + r"\b", all_css)
                if name and not used_css and name not in words:
                    candidates.append((s, e, "keyframes", pre))

    # 런타임 확인
    if a.runtime and candidates:
        from playwright.sync_api import sync_playwright
        sels = [c[3] for c in candidates if c[2] == "rule"]
        matched = set()
        js = """sels => sels.filter(s => { try { return document.querySelector(s.replace(/::?(before|after|placeholder|selection|marker|-webkit-[a-z-]+)/g,'')) } catch(e) { return true } })"""
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            for (w, h, mob) in ((1440, 900, False), (390, 844, True)):
                pg = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob).new_page()
                pg.goto(a.runtime, wait_until="load")
                pg.wait_for_timeout(1200)
                matched |= set(pg.evaluate(js, sels))
                H, y = pg.evaluate("document.documentElement.scrollHeight"), 0
                while y < H:
                    y += int(h * .8)
                    pg.evaluate(f"scrollTo(0,{y})")
                    pg.wait_for_timeout(150)
                    matched |= set(pg.evaluate(js, sels))
                    H = pg.evaluate("document.documentElement.scrollHeight")
            b.close()
        if matched:
            print(f"runtime 에서 살아 있음 → 제외: {len(matched)}", file=sys.stderr)
            for s in sorted(matched):
                print("  alive:", s[:100], file=sys.stderr)
        candidates = [c for c in candidates if not (c[2] == "rule" and c[3] in matched)]

    total = sum(e - s for s, e, *_ in candidates)
    print(f"{a.file}: 죽은 규칙 {len(candidates)}개 · {total/1024:.1f}KB")
    if a.v:
        for s, e, k, pre in candidates:
            print(f"  [{k}] {pre[:110]}")

    if a.apply and candidates:
        out, last = [], 0
        for s, e, *_ in sorted(candidates):
            if s < last:
                continue
            out.append(src[last:s])
            last = e
        out.append(src[last:])
        new = "".join(out)
        # 비어 버린 @media 블록 정리
        new = re.sub(r"@media[^{;]*\{\s*\}", "", new)
        open(a.file, "w", encoding="utf-8").write(new)
        print(f"  적용: {len(src) - len(new)} chars 제거")


if __name__ == "__main__":
    main()
