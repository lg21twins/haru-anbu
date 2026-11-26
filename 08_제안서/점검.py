#!/usr/bin/env python3
"""제안서 표현·수치 일관성 점검

왜 있는가
---------
같은 결함이 세 번 났다. **원고(md)는 고쳤는데 시각화(html)를 안 고쳐서
교수님께 가는 PDF에 옛 값이 남아 있는** 유형이다.

    2026-08-02  05_제출처_리스트가 "확인 필요"라 해놓고 다음 문단에서 그냥 씀
    2026-08-06  14_시장근거 §5의 갱신 지시 8건 중 2건만 실행
    2026-08-07  IDA 학생 €40으로 정정했으나 제출전략 16쪽 PDF엔 $80 그대로
                케어포 14,000을 "쓰지 않는다"고 써놓고 같은 PDF 안에서 사용

사람이 매번 grep으로 잡을 수 없다. 규칙을 코드로 박는다.

쓰는 법
-------
    python3 08_제안서/점검.py            # 위반만 출력
    python3 08_제안서/점검.py -v         # 통과 규칙까지 출력

종료 코드: 위반 있으면 1
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)

# 검사 대상 — 원고와 시각화를 **같이** 본다. 이게 이 도구의 핵심이다.
TARGET_DIRS = [
    os.path.join(ROOT, "원고"),
    os.path.join(ROOT, "시각화"),
    os.path.join(REPO, "01_기획"),
]
SKIP = ("_원본백업", "점검.py")

# 정정 대장 — **틀린 값을 기록하는 것이 임무**인 문서다. 규칙 검사에서 뺀다.
# (여기서 옛 값을 못 쓰게 하면 대장 구실을 못 한다)
LEDGERS = [
    "01_수치검증대장.md",
    "08_구자료_정정표.md",
    "14_시장근거_2026.md",
    "19_공모전_재조사_20260807.md",
    "06_점검_이슈로그.md",
]

# guard: 이 말이 같은 줄에 있으면 "인용 금지를 설명하는 문장"이므로 위반이 아니다
GUARDS = [
    "인용하지", "인용 금지", "인용금지", "재확인 실패", "자기보고", "2차 자료",
    "미표기", "쓰지 않", "쓰지 말", "수치 없이", "확인 실패", "금지", "확인되지 않", "출처가 확인",
    "미확인",          # 2026-08-09 — "매출은 여전히 [미확인]"이 규칙에 걸렸다. 표기 자체가 경고다
    "한정어",          # 2026-08-09 — 한정어를 붙였거나("입소시설 대상으로는 … 한정어를 반드시")
                       # 한정어 얘기를 하는 줄("한정어 없이 말하면 반박당한다")은 위반이 아니다.
                       # 규칙을 넓히는 대신 **저자가 인지했다는 신호**를 가드로 삼는다
    "정정", "폐기", "옛", "틀렸", "잘못",
]

RULES = [
    # (이름, 잡을 정규식, 설명, 올바른 값)
    ("케어포 도입 기관 수", r"14,?000\s*개",
     "케어포 공식 사이트에 도입 기관 수 표기가 없다 (2026-08-07 재확인)",
     "수치 없이 '국내 주요 사업자'로 서술"),

    # 부스 첫 30초. 원고에서 요청을 2단계로 나눈 뒤에도 시각화에만 옛 문장이 남아 있었다 — 네 번째 사고.
    ("30초 스크립트 옛 요청", r"한 병동에서 8주만|8주만 무상으로 써보게",
     "서버가 없는데 첫 30초에 8주 파일럿을 요청하면 거짓말이 된다",
     "'현장 이야기를 2시간만 들려주실 수 있는 곳' — 요청은 2단계다"),

    # 2026-08-09 — 다섯 번째 사고. 같은 유형이 표현만 바꿔 또 나왔다.
    # 인쇄물 뒷면(20부 인쇄 예정)에 "요청 — 시설 한 곳에서 8주 무상 파일럿"이 있었다.
    # 기존 규칙은 "한 병동에서 8주만"만 잡아서 그대로 통과했다.
    # 이번엔 문구가 아니라 **구조**를 잡는다 — 요청 자리에 파일럿이 오면 걸린다.
    ("요청 자리에 파일럿", r"(요청|찾는 것)[^\n]{0,30}8주\s*(무상\s*)?파일럿|^\s*<b>요청</b>[^\n]*파일럿",
     "지금 요청은 인터뷰·자문이고 8주 파일럿은 개발 완료 후다 (17_착수조건과_일정.md §1)",
     "'지금 / 나중'으로 나눠 적는다. 지금 = 현장 이야기 2시간"),

    # 2026-08-11 — 현장실행팩의 D+3 후속 메일 첨부가 `하루안부_제안서.pdf`(32쪽)로 남아 있었다.
    # 그건 종합보고 1부의 원본이라 따로 보낼 일이 없고 **학교 내부 사정이 들어 있어 수신자가 다르다.**
    # 8/7에 그 자리를 메우려고 짧은제안서 8쪽을 만들었는데 **현장 문서가 안 따라왔다.**
    ("외부 발송에 32쪽 제안서",
     r"첨부[^\n]{0,20}하루안부_제안서\.pdf|보낸다[^\n]{0,20}하루안부_제안서\.pdf",
     "시설·사업자에게 보내는 것은 짧은제안서 8쪽 하나다 (32쪽은 종합보고 1부의 원본)",
     "첨부: 하루안부_짧은제안서.pdf (8쪽) 하나뿐"),

    # 2026-08-09 — 살아있는 문서 전체에서 딱 한 곳이 위반이었는데 **하필 현장 카드**였다.
    # 팀 3인이 외워서 부스에서 입으로 말하는 줄이 "국내 경쟁 4사 어디에도 없다"였다.
    # 제안서 본문은 같은 날 "한정어 없이 말하면 케어옵스로 반박당한다"고 경고하고 있었다.
    # **가장 많이 말해지는 문장이 가장 늦게 갱신된다** — 요청·차별점에 이어 세 번째다.
    # 구조로 잡는다: 본인/입주민 앱 이야기 + 절대 부정어가 한 줄에 오면 걸린다.
    ("본인 앱 한정어 누락",
     r"(어르신|환자|입주민|본인)\s*본?인?\s*앱[^\n]{0,40}"
     r"(어디에도 없|아무 데도 없|국내 (어디|전체)[^\n]{0,10}없|우리뿐|유일하다)",
     "케어옵스(시니어타운 입주민 앱)가 반례다. 한정어 없이 말하면 그 자리에서 반박당한다",
     "'장기요양 입소시설을 대상으로는 확인하지 못했다'까지만 말한다"),

    # 2026-08-09 — "협회로 한 번에 닿는다"는 재 보기 전까지 그럴듯했다. 실측하니 약 12%였다.
    # 이것도 구조로 잡는다 — 협회가 우리 대신 회원에게 뿌려 준다는 형태면 걸린다.
    ("협회 대량 배포",
     r"협회[^\n]{0,30}회원[^\n]{0,20}(뿌리|뿌린|배포|일괄|한 번에|한번에)"
     r"|협회를 통해[^\n]{0,20}(전국|모든|전체)[^\n]{0,10}(시설|기관)",
     "협회는 대량 경로가 아니다 — 중앙회 회원 요양시설 742개소는 전국 6,361개소의 약 12% (05_제출처_리스트.md §E5)",
     "'시설 한 곳을 먼저 얻은 뒤 신뢰를 얹는 자리'로 적는다"),

    # 2026-08-07 — 케어포 가족돌봄앱 세부 기능이 공식 페이지에 공개돼 있다. "미공개"는 우리에게 유리한 옛 서술이다.
    ("케어포 가족앱 미공개 주장", r"가족앱 세부 기능도? 미공개|가족돌봄앱의 세부 기능은 페이지에 미공개",
     "공식 페이지(carefor.co.kr/addservice/family_app.php)에 시설급여 12개 항목이 공개돼 있다",
     "12개 항목 공개 확인(2026-08-07) — 항목 단위 대조표로 서술"),

    # 2026-08-07 — How's Mom 공식 페이지에 규모 표기가 없다. 재확인 실패한 2차 수치다.
    ("How's Mom 규모", r"30개\s*주|수백 개 시설",
     "howsmom.net 공식 페이지에 규모 표기가 없다 (2026-08-07 재확인)",
     "규모는 쓰지 않는다. 대신 PointClickCare·MatrixCare 연동 사실을 쓴다"),

    # 2026-08-09 — InteliChart 자기보고 3건. 규모가 커서 인용 유혹이 가장 큰 건이다.
    ("InteliChart 자기보고 규모", r"21,?000\s*(개|곳|시설|skilled)|36\s*million|3,?600\s*만\s*(명|환자)|40개 이상의? EHR|30-plus EHR",
     "21,000 시설 · 3,600만 환자 · EHR 40종은 전부 회사·파트너 자기보고다 (2026-08-09 확인)",
     "숫자 없이 'PointClickCare 연동(2020-07-06 공식 발표)' 사실만 쓴다"),

    # 2026-08-09 — 둘을 묶어 막고 있었는데 **개소 수는 실제로 맞았다.**
    # 공식 사이트에 시설 10개가 나열돼 있다(빌리지 5 · 케어센터 4 · 평창카운티 1).
    # 우리가 우리 자료를 과소평가한 첫 사례다. 매출만 계속 막는다.
    ("KB 매출", r"208\s*억",
     "KB골든라이프케어 매출 208억원은 재확인에 실패했다 (개소 수 10은 2026-08-09 공식 확인)",
     "개소 수는 써도 된다. 매출은 쓰지 않는다"),

    ("Brenna 성과", r"민원\s*0\s*건|활성화\s*85",
     "시설 자기보고 수치다. 동료심사 논문 본문은 미확보",
     "'동료심사 파일럿 연구 존재'까지만"),

    ("Nourish 인증", r"14개\s*표준",
     "벤더 자기보고다",
     "인용하지 않는다"),

    # 2026-08-09 — 공식 FAQ 확인. $239 는 출처 불명이었고 실제보다 싸게 적혀 있었다.
    ("MUSE 참가비", r"\$\s*239|MUSE[^\n]{0,40}\$\s*209",
     "공식 FAQ 기준 Regular Entry $219 + 연간 행정비 $30 = 첫 출품 $249다 (2026-08-09)",
     "$219 + $30 = $249 · 학생 할인 없음"),

    ("KDI 인력 전망", r"최대\s*3\.7",
     "범위의 위쪽만 인용하는 것은 과장이다",
     "1.5~1.9명 → 3.0~3.7명 (KDI 2026.4)"),

    ("IDA 참가비", r"학생\s*\$\s*80|학생\s*€\s*80|IDA[^\n]{0,40}\$80",
     "공식 Graphic 부문 페이지 기준 Professional €80 / Student €40이다",
     "학생 €40 · 추가 €30"),

    ("IDA 연장 단계", r"연장\s*9/15",
     "공식 페이지에 중간 연장 단계가 없다",
     "Regular 8/15 → 최종 10/15"),

    ("UXDA 마감", r"11/11|11월\s*11일",
     "공식 Dates 페이지는 15 November 2026이다",
     "11/15"),
]

# 원고↔시각화 동기화가 필요한 짝. 한쪽에만 있으면 전파 누락이다.
SYNC = [
    ("경남 K-디자인", r"경남\s*K-?디자인",
     ["원고/19_공모전_재조사_20260807.md", "원고/09_8월실행_제출처_확장.md",
      "원고/05_제출처_리스트.md", "시각화/제출전략_시각화.html"]),
    ("파기 확인서", r"파기\s*확인서",
     ["원고/21_데이터파기확인서.md", "원고/18_구조점검과_제출서식.md",
      "시각화/의향확인서.html", "시각화/데이터파기확인서.html"]),
    ("서울시 참여예산", r"참여예산",
     ["원고/22_지자체_정책제안_창구.md", "원고/09_8월실행_제출처_확장.md",
      "원고/05_제출처_리스트.md"]),
    ("의왕시 조례", r"고령친화도시",
     ["원고/22_지자체_정책제안_창구.md", "원고/09_8월실행_제출처_확장.md"]),
    ("의왕살핌 대상 구분", r"의왕살핌",
     ["원고/22_지자체_정책제안_창구.md", "원고/09_8월실행_제출처_확장.md"]),
    ("6,211 반박 대응", r"6,211",
     ["원고/14_시장근거_2026.md"]),
    ("재가 선호 반박 대응", r"69\.4%",
     ["원고/14_시장근거_2026.md", "원고/13_KHF_현장실행팩.md",
      "원고/15_교수님_보고_및_요청.md",
      "시각화/현장실행팩_시각화.html"]),   # 원고만 고치고 시각화를 놓치는 사고 방지
    # 2026-08-07 — 기관 85.8%가 개인 운영. "법인 사무국 → 기획팀" 경로는 8.4%에만 통한다.
    # 도입 전략의 전제라 원고·시각화 양쪽에 있어야 한다.
    ("개인 운영 85.8%", r"85\.8%",
     ["원고/05_제출처_리스트.md", "원고/14_시장근거_2026.md",
      "시각화/제출전략_시각화.html",
      "원고/13_KHF_현장실행팩.md", "시각화/현장실행팩_시각화.html",
      "시각화/KHF_팀브리핑.html"]),
]



# ── PDF 실제 쪽수 대조 ────────────────────────────────────────────────
# 쪽수가 문서 간에 어긋난 사고가 세 번 났다. 본문을 고치면 쪽수가 바뀌는데
# README·자료지도·메일 초안에 적힌 숫자는 안 따라온다.
# 그래서 **텍스트 패턴이 아니라 실제 PDF를 열어** 대조한다.
PDF_CLAIMS = [
    # (PDF 파일명, 그 쪽수를 주장하는 곳들 — "쪽수" 자리에 {n} 을 쓴다)
    ("하루안부_종합보고.pdf", [
        ("README.md", "| **`PDF/하루안부_종합보고.pdf`** | **{n}** |"),
        ("원고/15_교수님_보고_및_요청.md", "하루안부_종합보고.pdf ({n}쪽)"),
        ("원고/15_교수님_보고_및_요청.md", "보고서는 {n}쪽이지만"),
        ("먼저_읽기.html", "A4 {n}쪽"),
        # 종합보고가 자기 쪽수를 스스로 말한다. 병합 산출물이라 손 sweep에서 두 번 빠졌다.
        ("시각화/교수님_보고서.html", "전체 <strong>{n}쪽</strong>"),
        # 2026-08-09 — 자료지도의 종합보고 행이 **65쪽에 멈춰 있었다.** 실제는 70쪽.
        # 하필 "오랜만에 열었을 때 이거 하나만 보라"는 문서의 첫 표 첫 줄이다.
        # 열 한 행 중 네 행만 등록돼 있었다 → 아래에 나머지를 전부 넣는다.
        ("시각화/자료지도.html", '하루안부_종합보고</td><td class="pg">{n}</td>'),
    ]),
    ("하루안부_제안서.pdf", [
        ("먼저_읽기.html", '<h3>1부 · 서비스 제안서</h3><span class="pg">{n}쪽</span>'),
        ("시각화/자료지도.html", "<strong>— {n}쪽 PDF의 원본</strong>"),
        ("시각화/자료지도.html", '하루안부_제안서</td><td class="pg">{n}</td>'),
    ]),
    # 2026-08-07 신설 — 부스에서 명함 받은 뒤 D+3에 보내는 것. 61쪽과 A4 1장 사이
    ("하루안부_짧은제안서.pdf", [
        ("README.md", "| **`PDF/하루안부_짧은제안서.pdf`** | **{n}** |"),
        ("시각화/자료지도.html", '하루안부_짧은제안서</td><td class="pg">{n}</td>'),
    ]),
    ("하루안부_KHF현장실행팩.pdf", [
        ("시각화/자료지도.html", '하루안부_KHF현장실행팩</td><td class="pg">{n}</td>'),
        # 2026-08-11 — README 는 15쪽이라고 적고 있었다(실제 14). 등록이 없어서 아무도 안 봤다.
        ("README.md", "| `PDF/하루안부_KHF현장실행팩.pdf` | {n} |"),
    ]),
    # 2026-08-09 — 먼저_읽기의 1·2·3부 카드가 등록돼 있지 않았다. 1부만 있고 2·3부가 빠져
    # 3부가 17쪽에 멈춰 있었다. 같은 화면 안에서 한 줄만 낡는 게 제일 안 보인다.
    ("하루안부_제출전략.pdf", [
        ("시각화/자료지도.html", '하루안부_제출전략</td><td class="pg">{n}</td>'),
        ("먼저_읽기.html", '<h3>3부 · 제출 전략</h3><span class="pg">{n}쪽</span>'),
    ]),
    ("하루안부_한계와법적리스크.pdf", [
        ("시각화/자료지도.html", '하루안부_한계와법적리스크</td><td class="pg">{n}</td>'),
        ("먼저_읽기.html", '<h3>2부 · 한계와 법적 리스크</h3><span class="pg">{n}쪽</span>'),
    ]),
    # 2026-08-07 — 쪽수를 손으로 발견하는 일이 반복됐다. 남은 PDF 전부를 대조에 넣는다.
    ("하루안부_KHF팀브리핑.pdf", [
        ("시각화/자료지도.html", '하루안부_KHF팀브리핑</td><td class="pg">{n}</td>'),
        ("README.md", "| `PDF/하루안부_KHF팀브리핑.pdf` | {n} |"),
    ]),
    ("하루안부_KHF인쇄물.pdf", [
        ("시각화/자료지도.html", '하루안부_KHF인쇄물</td><td class="pg">{n}</td>'),
        ("README.md", "| `PDF/하루안부_KHF인쇄물.pdf` | {n} |"),
    ]),
    ("하루안부_의향확인서.pdf", [
        ("시각화/자료지도.html", '하루안부_의향확인서</td><td class="pg">{n}</td>'),
        ("README.md", "| `PDF/하루안부_의향확인서.pdf` | {n} |"),
    ]),
    ("하루안부_데이터파기확인서.pdf", [
        ("시각화/자료지도.html", '하루안부_데이터파기확인서</td><td class="pg">{n}</td>'),
        ("README.md", "| `PDF/하루안부_데이터파기확인서.pdf` | {n} |"),
    ]),
    ("하루안부_자료지도.pdf", [
        ("시각화/자료지도.html", '하루안부_자료지도</td><td class="pg">{n}</td>'),
    ]),
]


def pdf_pages(path):
    try:
        d = open(path, "rb").read()
    except OSError:
        return None
    return len(re.findall(rb"/Type\s*/Page[^s]", d))


# ── 산문으로 말하는 쪽수 ──────────────────────────────────────────────
# PDF_CLAIMS 는 "정확히 이 문자열" 방식이라 표현이 조금만 달라도 놓친다.
# 아홉 번째 쪽수 파급에서 산문 표현 열두 곳이 한꺼번에 어긋나 있었다 —
# "뒤 62쪽은" · "66쪽은 들고 가지 않는다" · "목차 (1부 5쪽 · 2부 36쪽 · 3부 50쪽)".
# 전부 PDF에서 계산되는 값이라 사람이 옮겨 적을 이유가 없다. 여기서 정규식으로 잡는다.
#
# 파생값도 여기서 계산한다 —
#   본문 = 종합보고 − 4  (앞 4쪽: 표지 · 지금까지 한 일 · 한 장 요약 · 목차)
#   시작N = 5부터 각 부 길이를 누적  (`종합보고_묶기.py` 의 retoc 과 같은 계산)

PART_PDFS = ["하루안부_제안서.pdf", "하루안부_한계와법적리스크.pdf", "하루안부_제출전략.pdf"]


def page_values():
    """산문에 등장하는 모든 쪽수 값. PDF 가 하나라도 없으면 None."""
    tot = pdf_pages(os.path.join(ROOT, "PDF", "하루안부_종합보고.pdf"))
    parts = [pdf_pages(os.path.join(ROOT, "PDF", p)) for p in PART_PDFS]
    if tot is None or any(v is None for v in parts):
        return None
    starts, cur = [], 5
    for ln in parts:
        starts.append(cur)
        cur += ln
    return {
        "총": tot, "본문": tot - 4,
        "1부": parts[0], "2부": parts[1], "3부": parts[2],
        "시작1": starts[0], "시작2": starts[1], "시작3": starts[2],
    }


PROSE = [
    # (정규식 — 그룹 수 = 키 수, 각 그룹이 뜻하는 값)
    (r"보고서는 (\d+)쪽", ["총"]),
    (r"(\d+)쪽이지만 앞", ["총"]),
    (r"(\d+)쪽은 들고 가지 않는다", ["총"]),
    (r"(\d+)쪽은 아직 부담스", ["총"]),
    (r"(\d+)쪽으로 정리한", ["총"]),
    (r"교수님용 (\d+)쪽", ["총"]),
    (r"· (\d+)쪽 전\b", ["총"]),
    (r"하루안부_종합보고\.pdf`\*\* \| \*\*(\d+)\*\*", ["총"]),
    # 두 자리 이상만. "인쇄물 4쪽 중 … 뒤 2쪽은 우리가 쓰는 카드"라는 전혀 다른 문장이 있다.
    (r"뒤 (\d\d+)쪽은", ["본문"]),
    (r"1~3부 본문 (\d+)쪽", ["본문"]),
    # 목차 줄 — 여기 숫자는 "길이"가 아니라 "시작 쪽"이다. 헷갈려서 두 번 틀렸다.
    (r"1부 (\d+)쪽 · 2부 (\d+)쪽 · 3부 (\d+)쪽", ["시작1", "시작2", "시작3"]),
    # 반대로 여기 숫자는 각 부의 "길이"다
    (r"1부 제안서\((\d+)쪽\) · 2부 한계와 법적 리스크\((\d+)쪽\) · 3부 제출 전략\((\d+)쪽\)",
     ["1부", "2부", "3부"]),
    # 2026-08-09 — 2부가 14 → 17쪽이 되면서 **"한계 문서 14쪽"이 일곱 곳에 남았다.**
    # 우리가 부스와 메일에서 실제로 말하는 문장이라 여기가 제일 눈에 띄는 자리다.
    # 현장실행팩_시각화.html 의 CSS 주석 "15쪽 → 14쪽"은 그 문서 자기 쪽수라 건드리면 안 된다 —
    # 아래 표현들은 전부 '한계 문서'를 앞에 달고 있어 그 주석과 겹치지 않는다.
    # 2026-08-09 — 자료지도가 "66쪽"이라고 두 번 말하고 있었다(실제 70).
    (r"A4 한 장과 (\d+)쪽 사이", ["총"]),
    (r"(\d+)쪽은 달라고", ["총"]),
    (r"한계 문서 (\d+)쪽", ["2부"]),
    (r"한계 문서\((\d+)쪽\)", ["2부"]),
    (r"한계와법적리스크\.pdf` (\d+)쪽", ["2부"]),
    (r"(\d+)쪽 문서에 조문별로", ["2부"]),
    (r"(\d+)쪽 — 조문 대조", ["2부"]),
    (r"2부 (\d+)쪽의 뼈대", ["2부"]),
]


# ── D-day ────────────────────────────────────────────────────────────
# 쪽수와 같은 종류의 문제인데 더 나쁘다. 쪽수는 문서를 고칠 때만 어긋나지만
# **D-day 는 아무것도 안 해도 하루에 하나씩 어긋난다.**
# 실제로 8/7에 쓴 "D-3 · 8/10"이 8/9에도 D-3으로 남아 있었다.
# 날짜(8/10)는 사람이 정하고, D-N 은 여기서 계산한다.

DDAY_RX = re.compile(r'(<span class="d(?: hot)?">D-)(\d+)(</span><span>)(\d+)/(\d+)')


def scan_dday(fix=False):
    from datetime import date
    today = date.today()
    out = []
    for p in _prose_files():
        try:
            body = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        # 조기 탈출을 두지 않는다. "D-day 가 있는 파일만" 으로 걸렀더니
        # 날짜 도장만 있는 파일(자료지도 · README)이 두 번 빠졌다. 파일 수가 적으니 전부 본다.
        orig = body

        def sub(m):
            pre, got, mid, mo, da = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
            # 연도는 적혀 있지 않다. 지난 달로 읽히면 내년으로 넘긴다.
            #
            # 다만 **막 지나간 날은 넘기지 않는다.** 2026-08-11에 8/10 항목이 `D-364`가 됐다.
            # 숫자만 보면 여유로워 보이지만 실제로는 **이미 놓친 일정**이다.
            # 지난 30일 이내면 넘기지 않고 그대로 음수로 둬서 **사람이 보고 지우게** 한다.
            y = today.year + (1 if (mo, da) < (today.month, today.day) else 0)
            try:
                want = (date(y, mo, da) - today).days
                if want > 330:                      # = 최근에 지나간 날짜
                    want = (date(today.year, mo, da) - today).days
            except ValueError:
                return m.group(0)
            if want < 0:
                ln = orig.count("\n", 0, m.start()) + 1
                out.append((rel(p), ln, f"{mo}/{da} — **{-want}일 지났다.** 항목을 지우거나 날짜를 고친다"))
                return m.group(0)
            if want == got:
                return m.group(0)
            ln = orig.count("\n", 0, m.start()) + 1
            out.append((rel(p), ln, f"{mo}/{da} — 적힌 값 D-{got} · 실제 D-{want}"))
            return f"{pre}{want}{mid}{mo}/{da}"

        body = DDAY_RX.sub(sub, body)

        # 묶음 날짜 도장. 폴더는 `데스크탑복사.sh` 가 매번 오늘 날짜로 만드는데
        # 그 안의 먼저_읽기·자료지도는 "2026-08-07 묶음"으로 남아 있었다.
        today_s = today.strftime("%Y-%m-%d")
        for rx in (r"(<title>하루안부 제안서 — )(\d{4}-\d{2}-\d{2})( 묶음</title>)",
                   r'(<p class="eyebrow">하루안부 · 제안서 묶음 · )(\d{4}-\d{2}-\d{2})(</p>)',
                   r'(<p class="eyebrow">08_제안서 · 한눈에 보는 지도 · )(\d{4}-\d{2}-\d{2})( 기준</p>)',
                   r'(<span>)(\d{4}-\d{2}-\d{2})( · \d/\d</span>)',
                   r'(> 최종 갱신 )(\d{4}-\d{2}-\d{2})(\.)'):
            # 쪽 바닥처럼 같은 도장이 여러 번 나온다(자료지도는 1/2·2/2 두 번). 전부 본다.
            def stamp(m, _b=body):
                if m.group(2) == today_s:
                    return m.group(0)
                ln = _b.count("\n", 0, m.start()) + 1
                out.append((rel(p), ln, f"묶음 날짜 — 적힌 값 {m.group(2)} · 오늘 {today_s}"))
                return m.group(1) + today_s + m.group(3)
            body = re.sub(rx, stamp, body)

        if fix and body != orig:
            open(p, "w", encoding="utf-8").write(body)
    return out


def _prose_files():
    seen = set()
    # 08_제안서/ 바로 아래(README.md · 먼저_읽기.html)는 TARGET_DIRS 에 없다.
    # 정작 쪽수를 산문으로 가장 많이 말하는 두 파일이라 여기서 따로 넣는다.
    for fn in sorted(os.listdir(ROOT)):
        if fn.endswith((".md", ".html")) and not any(s in fn for s in SKIP):
            seen.add(os.path.join(ROOT, fn))
    for p in files():
        seen.add(p)
    for p in sorted(seen):
        if not any(p.endswith(l) for l in LEDGERS):
            yield p


def scan_prose(fix=False):
    """산문 쪽수를 실제 PDF 값과 대조한다. fix=True 면 덮어쓴다."""
    v = page_values()
    if v is None:
        return [("PDF 없음", "-", "산문 쪽수 대조를 건너뛴다")]
    out = []
    for p in _prose_files():
        try:
            body = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        orig = body
        for pat, keys in PROSE:
            def sub(m):
                # 그룹 위치(span)로 잘라 붙인다. 문자열 replace 를 쓰면
                # "1부 (1)쪽" 처럼 값이 주변 글자와 같을 때 엉뚱한 자리를 고친다.
                whole, base = m.group(0), m.start()
                pieces, cur = [], 0
                for i, k in enumerate(keys, 1):
                    s, e = m.start(i) - base, m.end(i) - base
                    got, want = int(m.group(i)), v[k]
                    pieces.append(whole[cur:s])
                    if got == want:
                        pieces.append(whole[s:e])
                    else:
                        ln = body.count("\n", 0, m.start()) + 1
                        out.append((rel(p), ln, f"{k} — 적힌 값 {got} · 실제 {want}"))
                        pieces.append(str(want))
                    cur = e
                pieces.append(whole[cur:])
                return "".join(pieces)
            body = re.sub(pat, sub, body)
        if fix and body != orig:
            open(p, "w", encoding="utf-8").write(body)
    return out


def check_pages():
    """문서가 주장하는 쪽수 ↔ 실제 PDF 쪽수"""
    bad = []
    for pdf, claims in PDF_CLAIMS:
        n = pdf_pages(os.path.join(ROOT, "PDF", pdf))
        if n is None:
            bad.append((pdf, "-", "PDF 파일 없음"))
            continue
        for relp, tmpl in claims:
            f = os.path.join(ROOT, relp)
            if not os.path.exists(f):
                continue
            body = open(f, encoding="utf-8", errors="ignore").read()
            if tmpl.format(n=n) in body:
                continue
            # 다른 숫자로 적혀 있는지 찾는다
            pat = re.escape(tmpl).replace(re.escape("{n}"), r"(\d+)")
            m = re.search(pat, body)
            found = m.group(1) if m else "표기 없음"
            bad.append((pdf, f"{relp}", f"적힌 값 {found} · 실제 {n}"))
    return bad


def fix_pages():
    """문서에 적힌 쪽수를 실제 PDF 값으로 덮어쓴다.

        python3 08_제안서/점검.py --쪽수고침

    쪽수는 PDF에서 전부 계산되는 값이라 사람이 옮겨 적을 이유가 없다.
    실제로 같은 sweep을 일곱 번 손으로 했고 그때마다 몇 곳씩 빠뜨렸다.
    (목차 쪽번호는 여기가 아니라 `시각화/종합보고_묶기.py` 가 자동으로 맞춘다.)
    """
    changed = []
    for pdf, claims in PDF_CLAIMS:
        n = pdf_pages(os.path.join(ROOT, "PDF", pdf))
        if n is None:
            continue
        for relp, tmpl in claims:
            f = os.path.join(ROOT, relp)
            if not os.path.exists(f):
                continue
            body = open(f, encoding="utf-8", errors="ignore").read()
            if tmpl.format(n=n) in body:
                continue
            pat = re.escape(tmpl).replace(re.escape("{n}"), r"(\d+)")
            m = re.search(pat, body)
            if not m:
                continue
            body = body[:m.start()] + tmpl.format(n=n) + body[m.end():]
            open(f, "w", encoding="utf-8").write(body)
            changed.append(f"{relp}  {m.group(1)} → {n}  ({pdf})")
    return changed


WEEKDAYS = "월화수목금토일"
WD_RX = re.compile(
    r"(?<!\d)(\d{1,2})/(\d{1,2})\s*[\(（]\s*([월화수목금토일])\s*[\)）]"
    r"|(\d{1,2})월\s*(\d{1,2})일\s*[\(（]\s*([월화수목금토일])\s*[\)）]")


def scan_weekday():
    """문서에 적힌 `8/19(수)` 같은 요일 표기가 실제 달력과 맞는지.

    2026-08-09에 처음 돌려 보고 알았다 — 14건 중 **8/15(금)** 하나가 틀렸다. 실제는 **토요일**이다.
    그 한 글자가 일정 전체를 흔들었다: 8/15는 **광복절**이고 2026년엔 토요일이라
    **8/17(월)이 대체공휴일**이다. 그런데 현장실행팩은 **8/15에 인쇄물 20부 출력**으로 잡혀 있었다.
    **인쇄소가 닫히는 날에 인쇄를 예약해 둔 셈이다.** 밀리면 남는 날은 8/18(화) 하루,
    KHF 개막은 8/19(수)다.

    쪽수·D-day 와 같은 부류지만 더 조용하다 — 요일은 **아무도 다시 세지 않는다.**
    """
    from datetime import date
    year = date.today().year
    out = []
    for p in _prose_files():
        body = open(p, encoding="utf-8", errors="ignore").read()
        for m in WD_RX.finditer(body):
            g = m.groups()
            mo, da, wd = (g[0], g[1], g[2]) if g[0] else (g[3], g[4], g[5])
            try:
                real = WEEKDAYS[date(year, int(mo), int(da)).weekday()]
                nxt = WEEKDAYS[date(year + 1, int(mo), int(da)).weekday()]
            except ValueError:
                continue          # 2/30 같은 표기는 여기서 볼 일이 아니다
            if real == wd:
                continue
            # 내년 달력과 맞으면 내년 일정을 적은 것이다. 단정하지 않고 넘긴다.
            if nxt == wd:
                continue
            ln = body.count("\n", 0, m.start()) + 1
            out.append((rel(p), ln, f"{mo}/{da}({wd}) — {year}년에는 {real}요일"))
    return out


def unregistered_pages():
    """**등록되지 않은** 쪽수 표기를 훑는다.

    `claims_coverage()` 는 "등록해 놓고 안 걸리는 것"을 잡는다. 이건 그 반대 —
    **아예 등록된 적이 없어서 아무도 안 보는 표기**다.
    2026-08-11에 README 가 현장실행팩을 **15쪽**이라고 적고 있었다(실제 14).
    등록이 없으니 `--쪽수고침` 도 그냥 지나갔다.

    처음엔 "파일명 근처 ±60자의 아무 수"로 짰더니 **15건 중 대부분이 오탐**이었다
    (`card-3` 같은 클래스명, `P3`, `§7` …). **오탐이 많은 검사는 무시당해서 없느니만 못하다.**
    그래서 조건을 좁혔다 — 파일명 뒤 40자 안에서
    **`N쪽` 이거나 마크다운 표 칸 `| N |` 인 것만** 쪽수로 본다.
    그래도 오탐 가능성이 남으므로 **고치지 않고 알리기만 한다.**
    """
    num_rx = re.compile(r"(?<!\d)(\d{1,3})\s*쪽|\|\s*\**\s*(\d{1,3})\s*\**\s*\|")
    out = []
    for pdf, _claims in PDF_CLAIMS:
        n = pdf_pages(os.path.join(ROOT, "PDF", pdf))
        if n is None:
            continue
        stem = pdf[:-4]
        for p in _prose_files():
            body = open(p, encoding="utf-8", errors="ignore").read()
            for m in re.finditer(re.escape(stem), body):
                seg = body[m.end():m.end() + 40]
                nums = [int(a or b) for a, b in num_rx.findall(seg)]
                if not nums or n in nums:
                    continue
                ln = body.count("\n", 0, m.start()) + 1
                out.append((rel(p), ln, f"{stem} 뒤의 {nums} · 실제 {n}쪽"))
    return out


def claims_coverage():
    """등록해 놓고 **한 번도 안 걸리는** PDF_CLAIMS·PROSE 를 찾는다.

    2026-08-09에 자료지도의 종합보고 행이 **65쪽에 멈춰 있는 것**을 눈으로 발견했다.
    등록이 없었기 때문인데, 더 무서운 쪽은 **등록해 뒀는데 문구가 바뀌어 빗나가는 경우**다.
    그러면 그 자리는 검사받지 않으면서 **검사받는 것처럼 보인다.**
    위반 0건이 "확인했다"가 아니라 "안 봤다"가 되는 순간이라 반드시 알려야 한다.
    """
    out = []
    for pdf, claims in PDF_CLAIMS:
        for relp, tmpl in claims:
            f = os.path.join(ROOT, relp)
            if not os.path.exists(f):
                out.append((f"PDF_CLAIMS {pdf}", relp, "파일이 없다"))
                continue
            body = open(f, encoding="utf-8", errors="ignore").read()
            pat = re.escape(tmpl).replace(re.escape("{n}"), r"(\d+)")
            if not re.search(pat, body):
                out.append((f"PDF_CLAIMS {pdf}", relp, tmpl[:60]))

    seen = set()
    for p in _prose_files():
        body = open(p, encoding="utf-8", errors="ignore").read()
        for rx, _keys in PROSE:
            if re.search(rx, body):
                seen.add(rx)
    for rx, _keys in PROSE:
        if rx not in seen:
            out.append(("PROSE", "(어느 파일에서도)", rx))
    return out


# ── 지나간 일정 행 ────────────────────────────────────────────────────────────
# 2026-08-11 신설. `D-N` 표기는 scan_dday 가 잡는데, **날짜만 박힌 일정 행**은 아무도 안 봤다.
# 자료지도 타임라인에 `8/10 월 — MUSE 낼지 말지 결정 … 마감이 8/13이라 오늘 정해야 한다` 가
# 8/11 에도 그대로 있었다. 문서 상단은 "2026-08-11 기준"이라고 적혀 있었다.
#
# 처음 만든 판(동사 낱말로 거르기)은 11건 중 8건이 오탐이었다 — "전부 6/30 마감",
# "6/26 마감으로 종료" 같은 **지난 사실 서술**까지 잡았다. 오탐이 많은 검사는 무시당하고,
# 무시당하는 검사는 없느니만 못하다. 그래서 **일정 행의 생김새**로 좁혔다:
#   날짜 뒤에 요일이 붙거나(`8/14(금)` `8/10 월`), 볼드 안이 날짜 하나뿐이거나(`**8/13**`),
#   표/태그 칸이 날짜뿐(`>8/13<`). 지난 사실 서술은 문장 한가운데 있어 셋 다 아니다. → 오탐 0.
STALE_SKIP = ("완료", "~~", "지났", "했다", "끝냈", "보냈", "종료")
STALE_RX = re.compile(
    r"(?<!\d)(\d{1,2})/(\d{1,2})\s*[\(（]?\s*[월화수목금토일][\)）]?(?!\d)"
    r"|\*\*\s*(\d{1,2})/(\d{1,2})\s*\*\*"
    r"|>\s*(\d{1,2})/(\d{1,2})\s*<")


def scan_stale():
    """날짜가 박힌 일정 행 중 이미 지나간 것. 지웠거나 고쳤어야 할 자리다."""
    from datetime import date
    today = date.today()
    out = []
    for p in _prose_files():
        try:
            lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
        except OSError:
            continue
        for i, ln in enumerate(lines, 1):
            if any(s in ln for s in STALE_SKIP):
                continue
            for m in STALE_RX.finditer(ln):
                g = [x for x in m.groups() if x]
                if len(g) < 2:
                    continue
                try:
                    gap = (today - date(today.year, int(g[0]), int(g[1]))).days
                except ValueError:
                    continue
                # 60일 넘게 지난 것은 작년 일정이거나 그냥 기록이다. 최근 것만 본다.
                if 0 < gap <= 60:
                    out.append((rel(p), i,
                                f"{g[0]}/{g[1]} — **{gap}일 지났다.** 지우거나 날짜를 고친다"))
                    break
    return out


# ── 화면의 임상 값 ────────────────────────────────────────────────────────────
# 2026-08-11 신설. **이 도구가 처음으로 앱 화면을 본다.**
#
# 왜 필요했나 — 의료진 화면을 A안으로 찍어 보다가, 요양보호사 앱 인수인계 줄이
# `체온 36.9℃ 미열` 이라고 적고 있는 것을 봤다. **36.9 는 미열이 아니다.**
# 원고를 아무리 읽어도 안 나오는 종류다. 제안서 문서만 훑는 규칙으로는 영원히 못 잡는다.
# KHF 는 보건의료 전시회고, 부스에 오는 간호사는 이걸 **한눈에 본다.**
#
# 캐논(CLAUDE.md): 박영자 78·A-3 / 최명자 82·B-1 / 김순자 79·B-2 / **이정숙 85·A-7(미열)**
APP_DIRS = ["v10_의료진웹", "v11_보호자앱", "v11_요양보호사앱", "v12_환자앱",
            "v15_의료진앱", "v13_온보딩",
            os.path.join("haru-anbu-showcase-v8-bundle", "07_디자인", "mockup")]

FEVER_WORDS = ("미열", "微热", "low-grade", "low grade")
FEVER_MIN = 37.2          # 이 아래를 미열이라 부르면 틀렸다
OTHERS = ("박영자", "최명자", "김순자")   # 캐논상 미열이 아닌 사람들
# 값이 여럿 나열된 측정 계열은 근거지 주장이 아니다 — 건너뛴다
SERIES = ("→", "->", "추세", "측정", "회 측정", "trend")


def _app_files():
    for d in APP_DIRS:
        base = os.path.join(REPO, d)
        if not os.path.isdir(base):
            continue
        for dp, _, fns in os.walk(base):
            if any(s in dp for s in SKIP) or "_원본백업" in dp:
                continue
            for fn in sorted(fns):
                if fn.endswith(".html"):
                    yield os.path.join(dp, fn)


def scan_vitals():
    """화면에 뜨는 체온이 (1) 미열 정의에 맞나 (2) 캐논상 맞는 사람에게 붙었나."""
    temp = re.compile(r"(3[5-9]\.[0-9])\s*(?:℃|°C|°)")
    out = []
    for p in _app_files():
        try:
            lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
        except OSError:
            continue
        for i, ln in enumerate(lines, 1):
            if not any(w in ln for w in FEVER_WORDS):
                continue
            if any(s in ln for s in SERIES):
                continue
            for val in temp.findall(ln):
                if float(val) < FEVER_MIN:
                    out.append((rel(p), i,
                                f"{val}℃ 를 미열이라 부른다 — 미열은 {FEVER_MIN}℃ 이상"))
            if any(n in ln for n in OTHERS) and "이정숙" not in ln:
                who = next(n for n in OTHERS if n in ln)
                out.append((rel(p), i, f"미열이 {who} 에게 붙어 있다 — 캐논에서 미열은 이정숙"))
    return out


def files():
    for d in TARGET_DIRS:
        if not os.path.isdir(d):
            continue
        for dp, _, fns in os.walk(d):
            if any(s in dp for s in SKIP):
                continue
            for fn in sorted(fns):
                if fn.endswith((".md", ".html")) and not any(s in fn for s in SKIP):
                    yield os.path.join(dp, fn)


def rel(p):
    return os.path.relpath(p, REPO)


def main():
    verbose = "-v" in sys.argv

    if "--쪽수고침" in sys.argv or "--fix-pages" in sys.argv:
        ch = fix_pages()
        pr = scan_prose(fix=True)
        dd = scan_dday(fix=True)
        if ch or pr or dd:
            print("쪽수 자동 정정")
            for c in ch:
                print("  " + c)
            for relp, ln, msg in pr:
                print(f"  {relp}:{ln}  {msg}")
            for relp, ln, msg in dd:
                print(f"  {relp}:{ln}  D-day {msg}")
            print("\n  등록 표기는 PDF_CLAIMS, 산문 표기는 PROSE, 남은 날은 DDAY 가 잡는다.")
            print("  전부 계산되는 값이라 사람이 옮겨 적을 자리는 없다.")
        else:
            print("쪽수 자동 정정 — 고칠 것 없음")
        print()
    violations = []

    for name, pat, why, right in RULES:
        hits = []
        rx = re.compile(pat)
        # 2026-08-11 — 여기가 오래 `files()` 였다. 그러면 TARGET_DIRS(원고·시각화·01_기획)만 보고
        # **`08_제안서/README.md` 와 `먼저_읽기.html` 은 어떤 표현 규칙도 지나간 적이 없다.**
        # 하필 그 폴더의 입구 문서다. 실제로 README 에 기각된 값($239)이 살아 있었다.
        # `_prose_files()` 는 그 둘을 포함하고 LEDGERS 는 그대로 뺀다.
        for p in _prose_files():
            if any(p.endswith(l) for l in LEDGERS):
                continue
            try:
                lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
            except OSError:
                continue
            for i, ln in enumerate(lines, 1):
                if not rx.search(ln):
                    continue
                # 가드는 **그 줄이 아니라 그 문단**에 걸린다. "쓰지 않는 수치:" 라고 써 놓고
                # 목록을 다음 줄부터 나열하면, 목록 줄에는 가드 낱말이 없다.
                # 문단 전체로 넓히면 HTML처럼 빈 줄이 드문 파일에서 규칙이 통째로 죽는다.
                # → **위아래 두 줄까지만** 본다. 위 사례는 전부 ±1~2 안에 들어온다.
                near = " ".join(lines[max(0, i - 3):i + 2])
                if any(g in near for g in GUARDS):
                    continue
                hits.append((rel(p), i, ln.strip()[:100]))
        if hits:
            violations.append((name, why, right, hits))
        elif verbose:
            print(f"  통과  {name}")

    sync_missing = []
    for name, pat, expected in SYNC:
        rx = re.compile(pat)
        missing = []
        for relp in expected:
            p = os.path.join(ROOT, relp)
            if not os.path.exists(p):
                missing.append(relp + " (파일 없음)")
            elif not rx.search(open(p, encoding="utf-8", errors="ignore").read()):
                missing.append(relp)
        if missing:
            sync_missing.append((name, missing))
        elif verbose:
            print(f"  통과  전파: {name}")

    page_bad = check_pages()
    prose_bad = scan_prose()
    dday_bad = scan_dday()
    wd_bad = scan_weekday()

    # 아예 등록된 적이 없는 쪽수 표기 — 자동 정정이 닿지 않는 자리다.
    unreg = unregistered_pages()
    if unreg:
        print(f"[주의] 등록되지 않은 쪽수 표기 {len(unreg)}건 — 자동 정정이 닿지 않는다")
        for f, ln, why in unreg:
            print(f"  {f}:{ln}  {why}")
        print("  맞으면 PDF_CLAIMS 에 등록하고, 틀렸으면 고친다.\n")

    # 등록해 놓고 안 걸리는 규칙 — 위반보다 먼저 알린다. "위반 0건"의 의미가 달라지기 때문이다.
    coverage = claims_coverage()
    if coverage:
        print(f"[주의] 걸리지 않는 등록 {len(coverage)}건 — 문구가 바뀌었을 수 있다")
        for kind, where, detail in coverage:
            print(f"  {kind} · {where}\n      {detail}")
        print("  등록을 문서에 맞추거나, 그 표기가 사라졌으면 목록에서 뺀다.\n")

    if wd_bad:
        print(f"[요일 불일치] {len(wd_bad)}건 — 달력과 다르다")
        for f, ln, why in wd_bad:
            print(f"  {f}:{ln}  {why}")
        print()

    stale_bad = scan_stale()
    if stale_bad:
        print(f"[지나간 일정] {len(stale_bad)}건 — 날짜가 박힌 행이 이미 지났다")
        for f, ln, why in stale_bad:
            print(f"  {f}:{ln}  {why}")
        print()

    # 화면의 임상 값 — 제안서가 아니라 **앱 HTML** 을 본다.
    # 부스에서 폰으로 열어 보여줄 것이 이 화면이라, 문서만 맞아서는 소용이 없다.
    vit_bad = scan_vitals()
    if vit_bad:
        print(f"[화면 임상 값] {len(vit_bad)}건 — 화면이 캐논·정의와 어긋난다")
        for f, ln, why in vit_bad:
            print(f"  {f}:{ln}  {why}")
        print("  고치는 도구: python3 _작업파일/체온캐논_수정.py --미리보기\n")

    if (not violations and not sync_missing and not page_bad
            and not prose_bad and not dday_bad and not wd_bad and not vit_bad
            and not stale_bad):
        print("제안서 표현·수치 점검: 위반 0건 "
              "(쪽수 + D-day + 요일 + 지나간 일정 + 화면 임상 값 대조 포함)")
        print("  검사 제외(정정 대장, 옛 값 보관이 임무): " + " · ".join(LEDGERS))
        return 1 if (coverage or unreg) else 0

    for name, why, right, hits in violations:
        print(f"\n[{name}] {why}")
        print(f"  올바른 표기: {right}")
        for f, i, ln in hits:
            print(f"    {f}:{i}")
            print(f"      {ln}")

    for pdf, where, detail in page_bad:
        print(f"\n[쪽수 불일치] {pdf}")
        print(f"    {where} — {detail}")

    if prose_bad:
        print("\n[산문 쪽수 불일치] 문장 속 쪽수가 PDF와 다르다 — `--쪽수고침` 으로 한 번에 맞춘다")
        for relp, ln, detail in prose_bad:
            print(f"    {relp}:{ln} — {detail}")

    if dday_bad:
        print("\n[D-day 불일치] 남은 날이 오늘 기준과 다르다 — `--쪽수고침` 으로 같이 맞춘다")
        for relp, ln, detail in dday_bad:
            print(f"    {relp}:{ln} — {detail}")

    for name, missing in sync_missing:
        print(f"\n[전파 누락] '{name}'가 아래 문서에 없다 — 원고만 고치고 시각화를 놓친 것일 수 있다")
        for m in missing:
            print(f"    {m}")

    total = (sum(len(h) for _, _, _, h in violations)
             + sum(len(m) for _, m in sync_missing) + len(page_bad)
             + len(prose_bad) + len(dday_bad) + len(wd_bad) + len(vit_bad)
             + len(stale_bad))
    print(f"\n위반 {total}건")
    return 1


if __name__ == "__main__":
    sys.exit(main())
