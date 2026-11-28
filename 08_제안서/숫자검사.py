#!/usr/bin/env python3
"""보고서 앞장의 "저장소에서 직접 센 수치"를 실제로 다시 센다.

    python3 08_제안서/숫자검사.py
    python3 08_제안서/숫자검사.py --고침     # 문서의 값을 실측치로 덮어쓴다

왜 있는가
---------
종합보고 2쪽은 **"아래는 저장소에서 직접 센 수치입니다"**라고 밝히고 여섯 개를 내놓는다.
그런데 그 쪽은 손으로 쓴 앞 4쪽이라 **병합 스크립트가 목차만 고치고 이 숫자들은 건드리지 않는다.**

2026-08-09에 처음 세어 봤더니 —

    디자인 토큰 468   →  **어떤 방법으로도 재현되지 않았다** (461 / 452 / 357)
    원고 23종         →  24종 (23_의료진화면_판단.md 신설 후 반영 안 됨)

**출처와 방법이 확인되지 않은 숫자는 쓰지 않는다**가 이 제안서의 원칙이다.
남의 수치에는 그 원칙을 열 번 적용했으면서 **우리 수치에는 적용한 적이 없었다.**

세는 방법 (이게 핵심이다)
-------------------------
숫자보다 **정의**가 중요하다. 정의를 적어 두지 않으면 다음 사람이 다르게 세고 또 어긋난다.

    고유 화면   앱 6곳의 한국어 HTML에서
                `_`로 시작하는 것(옵션 시트)과 `리디자인` 변형을 뺀 수
    총 파일     같은 6곳의 전체 HTML (언어 변형 포함, 위 제외는 동일하게 적용)
    디자인 토큰 tokens.css 의 **고유 토큰 이름** 수 (다크모드 재선언은 한 번으로 센다)
    검사 도구   아래 TOOLS 목록. **폴더를 세지 않는다** — 정리·빌드 스크립트가 섞여 있다
    커밋        git rev-list --count HEAD

    법 조문   `12_한계와_법적리스크.md` 부록 1 **국내 표의 줄 수**
    법률      그 표에 나오는 법령 중 시행령·시행규칙을 뺀 수 (본법만)

법 조문은 왜 뒤늦게 들어왔나 (2026-08-09)
------------------------------------------
"대조한 법 조문 25개"는 오래 손으로 관리됐다. **어디에도 열거돼 있지 않아서** 셀 수가 없었다.
전수 열거해 보니 **국내 24개**였고, 그 과정에서 **사회복지사업법 2개 조문이
법 문서에는 절조차 없다는 것**을 발견했다 (제안서 본문에만 있었다 → §A5 신설).

**세지 못하던 숫자는 틀린 숫자였을 뿐 아니라, 문서의 구멍을 가리고 있었다.**
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)

APPS = ["v11_보호자앱", "v11_요양보호사앱", "v12_환자앱",
        "v15_의료진앱", "v10_의료진웹", "v13_온보딩"]

# 화면으로 세지 않는 것 — 정의를 코드에 박아 둔다
def is_screen(fn):
    return not fn.startswith("_") and "리디자인" not in fn


def html_of(d):
    p = os.path.join(REPO, d)
    return [f for f in os.listdir(p) if f.endswith(".html")] if os.path.isdir(p) else []


# "자동 검사 도구" — **검사하는 것만.** 목록을 손으로 적는 이유는 아래에.
#
# 2026-08-09까지는 `07_디자인/scripts/*.py` 를 통째로 셌다. 그날 폰트·아이콘 빌드
# 스크립트 두 개가 그 폴더에 생기면서 8 → 9 가 됐는데, **틀린 건 숫자가 아니라 정의였다.**
# 그 폴더에는 세 종류가 섞여 있다 —
#     검사 (돌려서 결과를 보고, 어긋나면 0이 아닌 값으로 끝난다)
#     정리 (파일을 고친다: accessibility_cleanup · deduplicate_interactions · extract_shared_styles)
#     빌드 (산출물을 만든다: font_subset_glyphs · icon_bundle · 종합보고_묶기)
# 뒤 둘은 "검증 체계를 갖췄다"는 주장의 근거가 못 된다. 그래서 폴더가 아니라 목록으로 센다.
# 검사 도구가 늘면 여기 한 줄 추가한다 — 그건 자동으로 늘어나면 안 되는 숫자다.
TOOLS = [
    "07_디자인/scripts/design_audit.py",             # 토큰·이모지·아이콘·인라인스타일
    "07_디자인/scripts/static_integrity.py",         # 구조·참조·JS·CSS
    "07_디자인/scripts/visual_check.py",             # 정적 검사 + 헤드리스 캡처
    "07_디자인/scripts/component_divergence.py",     # 컴포넌트 분기 탐지
    "07_디자인/scripts/untracked_deps.py",           # 배포에 빠질 미추적 에셋
    "07_디자인/scripts/test_fixtures/test_runner.py",  # 감사 회귀 테스트
    "08_제안서/점검.py",                              # 표현·수치·쪽수·D-day
    "08_제안서/쪽검사.py",                            # PDF 쪽 모양(빈 쪽·넘침)
    "08_제안서/숫자검사.py",                          # 우리 수치 실측 대조 (이 파일)
]

LAWDOC = os.path.join(ROOT, "원고", "12_한계와_법적리스크.md")
LAWMARK = r"<!-- 조문목록:국내 시작 -->(.*?)<!-- 조문목록:국내 끝 -->"


def law_rows():
    """부록 1 국내 표에서 (조문 수, 본법 수). 표가 없으면 (None, None)."""
    if not os.path.exists(LAWDOC):
        return None, None
    m = re.search(LAWMARK, open(LAWDOC, encoding="utf-8").read(), re.S)
    if not m:
        return None, None
    laws = []
    for ln in m.group(1).splitlines():
        ln = ln.strip()
        # 표 줄만. 머리글(법령)과 구분선(---)은 뺀다.
        if not ln.startswith("|") or set(ln) <= set("|- :"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) < 2 or cells[0] == "법령":
            continue
        laws.append(cells[0])
    # 시행령·시행규칙은 조문으로는 세되 '법률' 수에서는 뺀다 — 모법에 딸린 하위법령이다
    본법 = {n for n in laws if "시행령" not in n and "시행규칙" not in n}
    return len(laws), len(본법)


def counts():
    ko = en = zh = total = 0
    per = {}
    for d in APPS:
        files = [f for f in html_of(d) if is_screen(f)]
        k = [f for f in files if not f.endswith((".en.html", ".zh.html"))]
        per[d] = len(k)
        ko += len(k)
        en += len([f for f in files if f.endswith(".en.html")])
        zh += len([f for f in files if f.endswith(".zh.html")])
        total += len(files)

    css = os.path.join(REPO, "07_디자인", "tokens", "tokens.css")
    tok = 0
    if os.path.exists(css):
        s = open(css, encoding="utf-8").read()
        tok = len({m.group(1) for m in re.finditer(r"(--[a-zA-Z0-9-]+)\s*:", s)})

    try:
        commits = int(subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=REPO,
                                     capture_output=True, text=True).stdout.strip())
    except Exception:
        commits = None

    arts, laws = law_rows()

    return {
        "고유 화면": ko,
        "총 파일": total,
        "영어 화면": en,
        "중국어 화면": zh,
        "디자인 토큰": tok,
        "검사 도구": len([p for p in TOOLS if os.path.exists(os.path.join(REPO, p))]),
        "원고": len([f for f in os.listdir(os.path.join(ROOT, "원고")) if f.endswith(".md")]),
        "완성 PDF": len([f for f in os.listdir(os.path.join(ROOT, "PDF")) if f.endswith(".pdf")]),
        "시각화": len([f for f in os.listdir(os.path.join(ROOT, "시각화")) if f.endswith(".html")]),
        "커밋": commits,
        "법 조문": arts,
        "법률": laws,
    }, per


# 문서에 그 값이 어떻게 적혀 있는가 — (파일, 정규식, 값 이름)
CLAIMS = [
    ("시각화/교수님_보고서.html", r'<div class="n">(\d+)<em>개</em></div>\s*<div class="l">고유 화면</div>', "고유 화면"),
    ("시각화/교수님_보고서.html", r"언어 변형 포함 총 (\d+)개 파일", "총 파일"),
    ("시각화/교수님_보고서.html", r'<div class="n">(\d+)<em>개</em></div>\s*<div class="l">디자인 토큰</div>', "디자인 토큰"),
    ("시각화/교수님_보고서.html", r'<div class="n">(\d+)<em>종</em></div>\s*<div class="l">자동 검사 도구</div>', "검사 도구"),
    ("시각화/교수님_보고서.html", r"원고 (\d+)종 · 완성 PDF (\d+)종", ("원고", "완성 PDF")),
    ("시각화/교수님_보고서.html", r"영어 (\d+)화면 · 중국어 (\d+)화면", ("영어 화면", "중국어 화면")),
    ("시각화/교수님_보고서.html", r"<td>(\d+)회</td>", "커밋"),
    ("시각화/제안서_시각화.html", r"고유 화면 (\d+)개\(언어 변형 포함 (\d+)개 파일\)", ("고유 화면", "총 파일")),
    ("시각화/제안서_시각화.html", r"고유 화면 (\d+)개, 언어 변형 포함 (\d+)개 파일", ("고유 화면", "총 파일")),
    ("원고/03_제안서_본문_v1.md", r"\*\*고유 화면 (\d+)개\*\*\(언어 변형 포함 (\d+)개 파일\)", ("고유 화면", "총 파일")),
    # 2026-08-09 — 토큰 수가 네 곳에 더 있었다. 앞장만 고치면 나머지가 남는다.
    ("README.md", r"화면 (\d+) · 제품 6 · 토큰 (\d+)", ("고유 화면", "디자인 토큰")),
    ("원고/15_교수님_보고_및_요청.md", r"화면 (\d+)개 · 제품 6개 · 토큰 (\d+)개", ("고유 화면", "디자인 토큰")),
    ("원고/15_교수님_보고_및_요청.md", r"수치 나열 \(토큰 (\d+)개", "디자인 토큰"),
    ("시각화/짧은_제안서.html", r"디자인 시스템\(토큰 (\d+)개\)과 자동 검사 도구 (\d+)종", ("디자인 토큰", "검사 도구")),
    # 2026-08-09 — 부록 1이 생겨 법 조문도 셀 수 있게 됐다. 손으로 관리하던 마지막 숫자였다.
    ("시각화/교수님_보고서.html",
     r'<div class="n">(\d+)<em>개</em></div>\s*<div class="l">대조한 법 조문</div>', "법 조문"),
    ("시각화/교수님_보고서.html", r"국내 (\d+)개 법률", "법률"),
    ("시각화/짧은_제안서.html", r"법 조문 (\d+)개 대조 — 국내 (\d+)개 법률", ("법 조문", "법률")),
    ("README.md", r"법 조문 (\d+) · 검사도구 (\d+) · 커밋 (\d+)", ("법 조문", "검사 도구", "커밋")),
    ("원고/15_교수님_보고_및_요청.md",
     r"법 조문 (\d+)개 · 검사도구 (\d+)종 · 커밋 (\d+)회", ("법 조문", "검사 도구", "커밋")),
    # 2026-08-09 — "PDF 11종"이 여섯 곳에 있는데 등록된 건 한 곳뿐이었다.
    # 그중 하나가 **팀 3인이 외우는 브리핑 첫 문장**이다. PDF 를 하나 더 뽑는 순간 어긋난다.
    # 자료지도의 CSS 주석("8종에서 11종이 되며")은 옛 기록이라 건드리지 않는다 — 정규식이 좁다.
    ("시각화/KHF_팀브리핑.html", r"완성 문서가 (\d+)종이지만", "완성 PDF"),
    ("시각화/자료지도.html", r"읽을 것은 <strong>PDF (\d+)종</strong>", "완성 PDF"),
    ("시각화/자료지도.html", r"<h2>PDF (\d+)종 — ", "완성 PDF"),
    ("시각화/자료지도.html", r"원고 (\d+)종은 그걸 만드는 재료이고", "원고"),
    ("시각화/자료지도.html", r"시각화 (\d+)종은 PDF를 뽑는 소스다", "시각화"),
    ("README.md", r"← 완성본 (\d+)종", "완성 PDF"),
    ("README.md", r"← 텍스트 원본 (\d+)종", "원고"),
    ("README.md", r"← PDF를 만드는 HTML 소스 (\d+)종", "시각화"),
    ("README.md", r"PDF (\d+)종이 각각 언제 쓰이는가", "완성 PDF"),
    ("README.md", r"원고 (\d+)종이 어디 있는가", "원고"),
    ("README.md", r"## 2\. 원고 (\d+)종", "원고"),
]


def main():
    fix = "--고침" in sys.argv or "--fix" in sys.argv
    real, per = counts()

    print("실측 —")
    for k, v in real.items():
        print(f"  {k:<12} {v}")
    print("  " + " · ".join(f"{d.split('_')[-1]} {n}" for d, n in per.items()))

    bad = []
    dead = []          # 한 번도 안 걸리는 규칙 — 아래 설명 참조
    for relp, rx, names in CLAIMS:
        p = os.path.join(ROOT, relp)
        if not os.path.exists(p):
            dead.append((relp, rx, "파일이 없다"))
            continue
        body = open(p, encoding="utf-8", errors="ignore").read()
        keys = names if isinstance(names, tuple) else (names,)
        if not re.search(rx, body):
            dead.append((relp, rx, "이 파일에서 한 번도 안 걸린다"))
            continue

        def sub(m):
            out, base, cur = [], m.start(), 0
            whole = m.group(0)
            for i, k in enumerate(keys, 1):
                s, e = m.start(i) - base, m.end(i) - base
                got, want = int(m.group(i)), real[k]
                out.append(whole[cur:s])
                if got == want:
                    out.append(whole[s:e])
                else:
                    ln = body.count("\n", 0, m.start()) + 1
                    bad.append((relp, ln, k, got, want))
                    out.append(str(want))
                cur = e
            out.append(whole[cur:])
            return "".join(out)

        new = re.sub(rx, sub, body)
        if fix and new != body:
            open(p, "w", encoding="utf-8").write(new)

    # 죽은 규칙 경고 —
    # 문구가 바뀌면 정규식이 조용히 빗나가고, 그때부터 그 자리는 **검사받지 않는데
    # 검사받는 것처럼 보인다.** 위반 0건이 "확인했다"가 아니라 "안 봤다"가 되는 순간이다.
    # 검사기도 검사받아야 한다 (쪽검사의 낡은 ALLOW_EMPTY 와 같은 종류의 구멍).
    if dead:
        print(f"\n[주의] 걸리지 않는 등록 {len(dead)}건 — 문구가 바뀌었을 수 있다")
        for relp, rx, why in dead:
            print(f"  {relp}  {why}\n      {rx}")
        print("  정규식을 문서에 맞추거나, 그 표기가 사라졌으면 CLAIMS 에서 뺀다.")

    if not bad:
        print("\n숫자 검사: 문서와 실측이 일치한다")
        return 1 if dead else 0

    print(f"\n{len(bad)}건 불일치")
    for relp, ln, k, got, want in bad:
        print(f"  {relp}:{ln}  {k} — 적힌 값 {got} · 실측 {want}")
    print("\n  `--고침` 으로 실측치를 덮어쓴다.")
    print("  덮어쓰기 전에 **정의가 맞는지** 본다 — 숫자가 아니라 세는 법이 틀렸을 수 있다.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
