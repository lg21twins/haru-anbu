#!/usr/bin/env python3
"""교수님_보고서.html 을 세 문서에서 다시 묶는다.

    python3 08_제안서/시각화/종합보고_묶기.py

왜 스크립트인가 — 이걸 손으로 세 번 했다. 매번 같은 데서 틀렸다.

  1) 세 문서의 id 가 겹친다 (#sum · #unknown 이 실제로 충돌했다) → 부별 접두어가 필수
  2) <nav> 는 화면 전용이라 인쇄본에 들어가면 안 된다
  3) 세 문서의 <style> 이 같다고 가정하고 아무거나 쓰면, 한 문서에만 있는 규칙이 날아간다
     (2026-08-07: 제안서에만 .shots 를 넣었는데 종합보고에서 화면이 안 나왔다)

앞 4쪽(표지 · 지금까지 한 일 · 한 장 요약 · 목차)은 이 스크립트가 만들지 않는다.
교수님_보고서.html 안에 손으로 쓴 것이고, 그대로 보존해 재사용한다.
→ 그래서 이 스크립트는 기존 교수님_보고서.html 이 있어야 돈다.

묶은 뒤 PDF 를 다시 뽑고 쪽수가 바뀌면 `점검.py` 가 잡는다. 순서:
    종합보고_묶기.py → PDF 재생성 → 점검.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "교수님_보고서.html")

# (소스 파일, id 접두어, 부 번호, 부 제목, 부 설명)
PARTS = [
    ("제안서_시각화.html", "p1", "1부", "서비스 제안서",
     "무엇을 만들었는가 — 문제 정의부터 로드맵까지"),
    ("한계와_법적리스크_시각화.html", "p2", "2부", "한계와 법적 리스크",
     "왜 바로 현업에 못 가는가 — 국내법 · 국제법 조문 대조"),
    ("제출전략_시각화.html", "p3", "3부", "제출 전략",
     "그래서 어디로 가는가 — 8월 캘린더 · 제출처 전수 · 기관별 접근 방식"),
]


def body_of(html):
    """<body> 안쪽만. <nav> 는 화면 전용이라 뺀다."""
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    inner = m.group(1) if m else html[html.index("</head>") + 7:]
    return re.sub(r"<nav\b.*?</nav>", "", inner, flags=re.S)


def prefixed(body, pre):
    """id 와 내부 앵커에 부 접두어를 붙인다. 안 붙이면 #sum 이 두 곳을 가리킨다."""
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{pre}-{m.group(1)}"', body)
    body = re.sub(r'\bhref="#([^"]+)"', lambda m: f'href="#{pre}-{m.group(1)}"', body)
    return body


def selectors(css):
    """{ 앞에 오는 선택자 이름들. @media·주석은 무시한다. 완전한 파서가 아니라 누락 탐지용이다."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = set()
    for m in re.finditer(r"([^{}]+)\{", css):
        sel = " ".join(m.group(1).split())
        if sel and not sel.startswith("@") and not sel.endswith(";"):
            out.add(sel)
    return out


def widest_style(sources):
    """가장 긴 <style> 을 쓴다 — 한 문서에만 있는 규칙(.shots 등)을 잃지 않기 위해서다.

    **이 방식은 안전하지 않다.** 이긴 문서에 없는 선택자는 조용히 사라진다.
    2026-08-09에 2부 부록의 `.arts` 조판 규칙이 이렇게 날아갈 뻔했다 (제안서_시각화.html 이 더 길다).
    CSS 를 자동으로 합치면 같은 선택자를 다르게 정의한 경우 다른 부의 조판을 망가뜨리므로
    **합치지 않고 알린다.** 알림이 뜨면 그 규칙을 해당 섹션 안의 <style> 로 옮긴다 —
    body 는 그대로 복사되므로 거기 있으면 살아남는다.
    """
    best, best_from = "", ""
    css = {}
    for f in sources:
        s = open(os.path.join(HERE, f), encoding="utf-8").read()
        m = re.search(r"<style>.*?</style>", s, re.S)
        if not m:
            continue
        css[f] = m.group(0)
        if len(m.group(0)) > len(best):
            best, best_from = m.group(0), f

    have = selectors(best)
    for f, s in css.items():
        if f == best_from:
            continue
        lost = sorted(selectors(s) - have)
        if lost:
            print(f"  [주의] {f} 의 규칙 {len(lost)}개가 {best_from} 에 없다 — 묶은 뒤 사라진다:")
            for sel in lost[:12]:
                print(f"         {sel}")
            if len(lost) > 12:
                print(f"         … 외 {len(lost) - 12}개")
            print("         → 해당 섹션 안의 <style> 로 옮길 것 (body 는 그대로 복사된다)")
    return best, best_from


PART_PDF = {
    "제안서_시각화.html": "하루안부_제안서.pdf",
    "한계와_법적리스크_시각화.html": "하루안부_한계와법적리스크.pdf",
    "제출전략_시각화.html": "하루안부_제출전략.pdf",
}


def pages_of(pdf):
    """PDF 실제 쪽수. 없으면 None."""
    p = os.path.join(os.path.dirname(HERE), "PDF", pdf)
    if not os.path.exists(p):
        return None
    return len(re.findall(rb"/Type\s*/Page[^s]", open(p, "rb").read()))


def retoc(front):
    """목차 쪽번호를 개별 PDF에서 다시 계산해 덮어쓴다.

    앞 4쪽은 손으로 쓴 것이라 부 길이가 바뀌어도 목차가 안 따라온다.
    실제로 "전체 61쪽"이 쪽수 변경 두 번을 통과해 살아남았다.
    숫자는 전부 PDF에서 계산되므로 사람이 셀 이유가 없다 — 여기서 자동으로 맞춘다.
    """
    lens = [pages_of(PART_PDF[src]) for src, *_ in PARTS]
    if any(v is None for v in lens):
        print("  [목차] 개별 PDF가 없어 자동 정정을 건너뛴다. 각 부 PDF를 먼저 뽑을 것")
        return front

    starts, cur = [], 5          # 앞 4쪽 다음이 1부 시작
    for ln in lens:
        starts.append(cur)
        cur += ln
    total = 4 + sum(lens)

    hits = []

    def sub(m):
        i = len(hits)
        hits.append(True)
        if i >= len(starts):
            return m.group(0)
        return f'<td><strong>{starts[i]}</strong> <span class="mute">({lens[i]}쪽)</span></td>'

    front, n = re.subn(r'<td><strong>\d+</strong>\s*<span class="mute">\(\d+쪽\)</span></td>',
                       sub, front)
    front = re.sub(r"(전체\s*<strong>)\d+(쪽</strong>)", rf"\g<1>{total}\g<2>", front)
    if n != len(PARTS):
        print(f"  [목차] 행 {n}개만 찾았다 (부는 {len(PARTS)}개). 목차 구조가 바뀌었는지 확인할 것")
    print(f"  목차 자동 정정 — 시작 쪽 {starts} · 각 부 {lens}쪽 · 전체 {total}쪽")
    return front


def main():
    if not os.path.exists(OUT):
        sys.exit(f"앞 4쪽을 가져올 {OUT} 이 없다. 이 스크립트는 처음부터 만들지 못한다.")

    old = open(OUT, encoding="utf-8").read()

    # 앞 4쪽 — <body> 부터 첫 partdiv 직전까지. 손으로 쓴 것이라 그대로 보존한다.
    m = re.search(r"<body[^>]*>(.*?)(?=<div class=\"partdiv\")", old, re.S)
    if not m:
        sys.exit("앞 4쪽 구간(<body> ~ 첫 partdiv)을 찾지 못했다. 구조가 바뀌었는지 확인할 것.")
    front = m.group(1)

    # partmark 인쇄 규칙(두 번째 style 블록)도 보존한다
    styles = re.findall(r"<style>.*?</style>", old, re.S)
    partmark_css = styles[1] if len(styles) > 1 else ""

    style, style_from = widest_style([p[0] for p in PARTS])

    head = re.search(r"<head>.*?</head>", old, re.S).group(0)
    head = re.sub(r"<style>.*?</style>", lambda _: style, head, count=1, flags=re.S)
    if partmark_css and partmark_css not in head:
        head = head.replace("</head>", partmark_css + "\n</head>")

    front = retoc(front)

    chunks = [head, "<body>", front]
    for src, pre, num, title, desc in PARTS:
        path = os.path.join(HERE, src)
        if not os.path.exists(path):
            sys.exit(f"소스가 없다: {src}")
        body = prefixed(body_of(open(path, encoding="utf-8").read()), pre)
        chunks.append(
            f'<div class="partdiv"><div class="partmark"><div class="k">{num}</div>'
            f'<div class="t">{title}</div><div class="d">{desc}</div></div></div>\n{body}'
        )
    chunks.append("</body>\n</html>\n")

    out = "<!DOCTYPE html>\n<html lang=\"ko\">\n" + "\n".join(chunks)
    open(OUT, "w", encoding="utf-8").write(out)

    ids = re.findall(r'\bid="([^"]+)"', out)
    dup = {i for i in ids if ids.count(i) > 1}
    print(f"묶음 완료 — {OUT}")
    print(f"  style 출처: {style_from} ({len(style):,}자)  ·  중복 id: {sorted(dup) or '없음'}")
    print(f"  <img> {out.count('<img')}개  ·  총 {len(out):,}자")
    print("  다음: PDF 재생성 → python3 08_제안서/점검.py (쪽수가 바뀌면 여기서 잡힌다)")

    return 1 if dup else 0


if __name__ == "__main__":
    sys.exit(main())
