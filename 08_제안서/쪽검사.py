#!/usr/bin/env python3
"""PDF 빈 쪽·넘침 검사 — 눈으로 못 보던 종류의 결함을 잡는다.

    python3 08_제안서/쪽검사.py
    python3 08_제안서/쪽검사.py 하루안부_종합보고     # 하나만

왜 있는가
---------
`점검.py` 는 **글자**를 본다. 이 도구는 **쪽 모양**을 본다. 둘은 겹치지 않는다.

2026-08-09에 처음 돌려 보고 알았다 —

    종합보고 p.35   용어 풀이 표가 두 줄 넘쳐 한 쪽이 통째로 비어 있었다
    현장실행팩 p.14  footer{break-before:page} 때문에 세 줄만 남은 쪽이 있었다

**70쪽짜리 PDF를 사람이 한 장씩 넘겨 보지 않는다.** 그래서 몇 달을 그대로 있었다.
쪽마다 잉크 비율을 재면 이런 쪽은 즉시 튀어나온다.

같은 날 오후, 2부에 조문 부록을 붙이자마자 이 도구가 **네 번 연속으로** 잡았다 —
빈 쪽(1.3%) → 강제 개페이지로 밀었더니 다시 빈 쪽 → 표를 조였더니 0.8% → 0.0%.
마지막 0.0%는 내용이 아니라 **절 아래 여백**이 쪽 경계를 넘은 것이었다.
**조판은 한 번에 맞지 않는다. 그래서 재는 도구가 있어야 한다.**

읽는 법
-------
    전체 잉크 3% 미만    거의 빈 쪽. **1쪽(표지)과 부 표지는 정상**이므로 예외로 둔다
    진한 잉크 5.5% 초과  글이 지나치게 빽빽하다. 넘침이나 조판 붕괴 의심

**두 지표를 다르게 쓰는 이유**는 아래 LOW/HIGH_DARK 주석에 적었다 —
사진을 전체 잉크로 재면 넘침으로 오인한다. 실제로 오인했다.
숫자는 절대 기준이 아니라 **이 문서군의 경험값**이다.
본문 쪽은 전체 6~11% · 진한 1.5~4.2% 사이에 있다.

필요: poppler 의 pdftoppm (`brew install poppler`)
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
PDFDIR = os.path.join(ROOT, "PDF")

# 빈 쪽은 **전체 잉크**로, 넘침은 **진한 잉크만**으로 잰다.
#
# 2026-08-09: 보호자앱 스크린샷의 빈 사진 칸을 진짜 사진으로 교체하자마자
# 짧은제안서 1·3쪽이 "넘침 의심"으로 잡혔다. 넘친 게 아니라 **사진이 들어온 것**이다.
# 전체 잉크는 사진과 빽빽한 글을 구분하지 못한다 — 실측해 보니 갈라진다:
#
#     짧은제안서 p.1·3 (사진)    진한 2.8%  중간톤 12.7%   ← 사진은 중간톤이다
#     KHF팀브리핑 p.1·2 (빽빽)   진한 4.2%  중간톤  9.2%   ← 글은 진하다
#     보통 본문 쪽                진한 1.5~3.9%
#
# 넘침은 **글이 너무 많은 것**이므로 진한 잉크로 잰다.
# 덕분에 팀브리핑용 ALLOW_DENSE 예외도 없앨 수 있었다 — 예외는 낡는다.
LOW, HIGH_DARK = 3.0, 5.5
DARK = 90          # 이보다 어두우면 글자로 본다
FAINT = 200        # 이보다 밝으면 종이로 본다

# 비어 보이는 게 정상인 쪽 — 표지와 부 표지는 원래 여백이 크다.
#
# 2026-08-09까지 종합보고는 {1, 5, 37, 51} 로 박아 뒀는데, 2부가 길어지면서
# **부 표지가 5·37·53 으로 옮겨 갔다.** 낡은 51은 그대로 남아 "그 쪽이 진짜 비어도 통과"하는
# 구멍이 됐다. 검사기가 검사받지 않으면 이렇게 된다.
# → 부 표지 위치를 각 부 PDF 쪽수에서 **계산한다.** 쪽수 관리와 같은 원칙이다.
PART_PDFS = ["하루안부_제안서.pdf", "하루안부_한계와법적리스크.pdf", "하루안부_제출전략.pdf"]
FRONT = 4      # 손으로 쓴 앞 4쪽(표지·지금까지 한 일·한 장 요약·목차)


def pages_of(name):
    p = os.path.join(PDFDIR, name)
    if not os.path.exists(p):
        return None
    return len(re.findall(rb"/Type\s*/Page[^s]", open(p, "rb").read()))


def allow_empty(name):
    if name != "하루안부_종합보고":
        return {1}                     # 나머지는 표지만
    lens = [pages_of(f) for f in PART_PDFS]
    if any(v is None for v in lens):
        return {1}                     # 부 PDF 가 없으면 표지만 봐준다
    out, cur = {1}, FRONT + 1
    for ln in lens:
        out.add(cur)                   # 부 표지
        cur += ln
    return out

def ink_ratio(pgm):
    """(전체 잉크율, 진한 잉크율). 전자는 '비었나', 후자는 '글이 넘쳤나'."""
    d = open(pgm, "rb").read()
    m = re.match(rb"P5\s+(\d+)\s+(\d+)\s+(\d+)\s", d)
    if not m:
        return None
    px = d[m.end():]
    if not px:
        return None
    dark = sum(1 for b in px if b < DARK)
    faint = sum(1 for b in px if b < FAINT)
    return faint / len(px) * 100, dark / len(px) * 100


def scan(pdf):
    """(쪽번호, 잉크율) 목록. pdftoppm 이 없으면 None."""
    tmp = tempfile.mkdtemp()
    try:
        r = subprocess.run(["pdftoppm", "-r", "28", "-gray", pdf, os.path.join(tmp, "p")],
                           capture_output=True)
        if r.returncode != 0:
            return None
        out = []
        for f in sorted(glob.glob(os.path.join(tmp, "p-*.pgm"))):
            v = ink_ratio(f)
            if v is not None:
                out.append((int(re.search(r"p-(\d+)", f).group(1)), v))
        return sorted(out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    if not shutil.which("pdftoppm"):
        print("pdftoppm 이 없다. `brew install poppler` 후 다시 돌린다.")
        return 0          # 도구가 없다고 배포를 막지는 않는다

    only = sys.argv[1] if len(sys.argv) > 1 else None
    pdfs = sorted(glob.glob(os.path.join(PDFDIR, "*.pdf")))
    if only:
        pdfs = [p for p in pdfs if only in os.path.basename(p)]
        if not pdfs:
            print(f"'{only}' 에 맞는 PDF 가 없다")
            return 1

    bad = []
    for p in pdfs:
        name = os.path.basename(p)[:-4]
        rows = scan(p)
        if not rows:
            print(f"  {name} — 읽지 못했다")
            continue
        allow = allow_empty(name)
        empty = [(n, v) for n, v in rows if v[0] < LOW and n not in allow]
        dense = [(n, v) for n, v in rows if v[1] > HIGH_DARK]
        avg = sum(v[0] for _, v in rows) / len(rows)
        mark = ""
        if empty:
            mark += f"  빈 쪽 {[n for n, _ in empty]}"
        if dense:
            mark += f"  빽빽 {[n for n, _ in dense]}"
        print(f"{name:<28} {len(rows):>3}쪽  평균 {avg:>4.1f}%{mark}")
        for n, v in empty:
            bad.append((name, n, f"잉크율 {v[0]:.1f}% — 거의 빈 쪽"))
        for n, v in dense:
            bad.append((name, n, f"진한 잉크 {v[1]:.1f}% — 글 넘침 의심"))

    if not bad:
        print("\n쪽 모양 검사: 이상 없음")
        return 0

    print(f"\n{len(bad)}건")
    for name, n, why in bad:
        print(f"  {name} p.{n} — {why}")
    print("\n  빈 쪽은 대개 표·문단이 한두 줄 넘쳐서 생긴다.")
    print("  그 절만 조이면(font-size · padding) 사라진다.")
    print("  **강제 개페이지(break-before:page)로 밀어내면 오히려 빈 쪽이 는다** — 2026-08-09에 겪었다.")
    print("  내용이 딱 맞은 뒤에도 남으면 절의 아래 여백(section padding)이 쪽 경계를 넘은 것이다.")
    print("  원래 비어야 하는 쪽은 allow_empty() 를 본다 (종합보고 부 표지는 자동 계산).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
