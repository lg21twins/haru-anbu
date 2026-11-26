#!/usr/bin/env python3
"""의료진 앱 홈 화면 — SaMD 경계 문구 + 호실 캐논 수정

    python3 _작업파일/의료진화면_수정.py --미리보기   # 무엇이 바뀌는지만
    python3 _작업파일/의료진화면_수정.py --호실만     # 호실·이름만 (판단 불필요)
    python3 _작업파일/의료진화면_수정.py             # 전부 적용

무엇을 고치나 — 판단 근거는 `08_제안서/원고/23_의료진화면_판단.md`

  (1) SaMD 경계  제안서 §05는 "이상 감지·위험도 판정은 만들지 않는다"고 적었는데
                 화면에는 `AI 판단` · `권장 …` · `즉시 확인` · `오늘 처리/관찰` 이 있다.
                 전부 **전달 표현**으로 바꾼다. 판단의 주체를 앱에서 사람으로 되돌린다.

  (2) 호실 캐논  2026-07-11 전 앱 통일에서 이 파일만 빠졌다.
                 최명자 B-1 · 김순자 B-2 · 이정숙 A-7, 미열은 이정숙.

**적용 전 원본을 `_원본백업_<날짜>/` 에 복사한다.** git 추적 파일이지만
되돌릴 때 diff 를 보는 편이 빠르다.

적용 뒤에 반드시 —
    python3 07_디자인/scripts/static_integrity.py
    python3 07_디자인/scripts/design_audit.py --target mobile-apps
그리고 **스크린샷을 다시 찍어 08_제안서/assets/shot_doctor.png 를 교체**한다.
인쇄물에 들어가는 것은 화면이 아니라 PNG 다 — 이걸 잊으면 아무것도 바뀌지 않는다.
"""
import datetime
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(REPO, "v15_의료진앱", "d01-home.html")

# (설명, 지금, 바꾼 뒤)
SAMD = [
    ("긴급도 판정 태그",
     '<span class="alert-tag">즉시 확인</span>',
     '<span class="alert-tag">요양보호사 보고</span>'),

    ("직전 값 비교 — 이상 감지에 해당",
     '<span class="evi-sub">직전 162/96 대비 상승</span>',
     '<span class="evi-sub">13:50 요양보호사 기록</span>'),

    ("AI 판단 라벨",
     '<div class="sec-eyebrow">AI 판단</div>',
     '<div class="sec-eyebrow">요양보호사 기록</div>'),

    ("임상 권고 — 가장 무거운 항목. 사람의 말로 돌린다",
     '<span class="rec-label">권장</span>\n        <span class="rec-list">재측정 · 담당의 보고 · 회진 우선순위 상향</span>',
     '<span class="rec-label">메모</span>\n        <span class="rec-list">"혈압이 높아 재측정 부탁드립니다" — 이수진 요양보호사</span>'),

    ("근거 제시 주체",
     'aria-label="임상 근거"',
     'aria-label="측정값"'),
]

# 우선순위·트리아지 표현은 문맥이 여러 곳이라 따로 둔다
SAMD_LOOSE = [
    ("우선순위 → 건수", "오늘의 우선순위", "오늘 올라온 보고"),
    ("트리아지 → 읽음 상태", "오늘 처리", "확인 전"),
    ("트리아지 → 읽음 상태", ">관찰<", ">확인함<"),
]

# 캐논: 박영자 78·A-3 / 최명자 82·B-1 / 김순자 79·B-2 / 이정숙 85·A-7(미열)
ROOMS = [
    ("최명자 호실", "2층 B-2호", "2층 B-1호"),
    ("김순자 호실", "2층 A-5호", "2층 B-2호"),
    ("이정숙 호실 — 층은 다른 화면과 맞춰 2층으로", "3층 C-1호", "2층 A-7호"),
]

# 미열은 캐논상 이정숙의 것이다. 김순자에게 붙은 것을 옮긴다.
#
# 2026-08-11 — 제목만 바꾸면 반만 고쳐진다는 것을 **화면을 찍어 보고** 알았다.
# 아래 두 줄(act-main)만 있던 때, 적용 결과 화면은 "김순자 · 투약 확인" 밑에
# **37.8°C 가 그대로 남았다.** 라벨이 사라져 숫자만 뜨니 오히려 전보다 나빴다.
# 값이 붙어 있는 곳은 act-sub 다. 아래 SYMPTOM_SUB 가 그 줄을 옮긴다.
SYMPTOM = [
    ("김순자 미열 제거 — 캐논에서 미열은 이정숙",
     "김순자 · 미열 + 투약 확인", "김순자 · 투약 확인"),
    ("이정숙에 미열 부여",
     "이정숙 · 낙상 회진", "이정숙 · 미열 관찰"),
]

# act-sub 의 실제 값. **ROOMS 가 먼저 돌기 때문에 호실은 바뀐 뒤 문자열로 적는다.**
#
# 체온 값을 37.4 로 잡은 근거 — 지어낸 것이 아니라 **이미 아홉 곳에 있는 값**이다:
#   요양보호사앱 c01-today `체온 37.4℃ · 4회 측정` · c01-일정표 `오전 37.4℃`
#   c03-sotong `체온 37.4°C — 평소보다 0.8도 높음` (36.6 + 0.8 = 37.4, 산수도 맞는다)
#   en·zh 판까지 전부 37.4. **37.8 은 이 화면에만 있다.**
# 시각 06:40 은 요양보호사앱 관찰 카드의 `마지막 체크 06:40` 과 맞춘 것이다.
SYMPTOM_SUB = [
    ("김순자 체온 칩 제거 — 이게 없으면 제목만 고쳐지고 37.8°C 는 남는다",
     '2층 B-2호 · <span class="act-status">37.8°C <span class="vital">13:30</span></span> · 보호자 문의',
     '2층 B-2호 · 보호자 문의'),
    ("이정숙에 체온 부여 — '↑'는 추세 판정이라 값만 남기고 뺀다",
     '2층 A-7호 · <span class="act-status">야간 배회 ↑</span>',
     '2층 A-7호 · <span class="act-status">37.4°C <span class="vital">06:40</span></span>'),
]


def apply(pairs, body, report, dry):
    """**미리보기에서도 실제로 치환한다.** 쓰기만 안 할 뿐이다.

    2026-08-11 — 예전에는 dry 일 때 치환을 건너뛰었다. 그러면 앞 규칙의 결과를
    입력으로 받는 뒤 규칙이 전부 **거짓 '못 찾음'** 으로 뜬다(호실을 바꾼 뒤의
    문자열을 찾는 SYMPTOM_SUB 가 그랬다). 미리보기가 틀리면 미리보기를 믿을 수
    없고, 그러면 없느니만 못하다.
    """
    for why, old, new in pairs:
        hit = old in body
        report.append((why, old.strip()[:60], new.strip()[:60], hit))
        if hit:
            body = body.replace(old, new)
    return body


def main():
    dry = "--미리보기" in sys.argv or "--dry" in sys.argv
    rooms_only = "--호실만" in sys.argv

    if not os.path.exists(TARGET):
        sys.exit(f"대상이 없다: {TARGET}")
    body = open(TARGET, encoding="utf-8").read()
    orig = body

    groups = [("호실·증상 캐논", ROOMS + SYMPTOM + SYMPTOM_SUB)]
    if not rooms_only:
        groups.insert(0, ("SaMD 경계 문구", SAMD + SAMD_LOOSE))

    missed = 0
    for title, pairs in groups:
        print(f"\n── {title} ──")
        rep = []
        body = apply(pairs, body, rep, dry)
        for why, old, new, hit in rep:
            mark = "  " if hit else "  못 찾음 "
            print(f"{mark}{why}")
            print(f"      - {old}")
            print(f"      + {new}")
            if not hit:
                missed += 1

    if missed:
        print(f"\n{missed}건을 찾지 못했다. 화면이 이미 바뀌었는지 확인할 것.")

    if dry:
        print("\n미리보기였다. 적용하려면 --미리보기 없이 다시 돌린다.")
        return 0

    if body == orig:
        print("\n바뀐 것이 없다.")
        return 0

    stamp = datetime.date.today().strftime("%Y%m%d")
    bak = os.path.join(REPO, "v15_의료진앱", f"_원본백업_{stamp}")
    os.makedirs(bak, exist_ok=True)
    shutil.copy2(TARGET, os.path.join(bak, "d01-home.html"))
    open(TARGET, "w", encoding="utf-8").write(body)

    print(f"\n적용 완료 — 원본은 {os.path.relpath(bak, REPO)}/d01-home.html")
    print("\n다음:")
    print("  python3 07_디자인/scripts/static_integrity.py")
    print("  python3 07_디자인/scripts/design_audit.py --target mobile-apps")
    print("  그리고 **스크린샷 재촬영 → 08_제안서/assets/shot_doctor.png 교체 → 인쇄물 PDF 재생성**")
    print("  (인쇄물에 들어가는 건 화면이 아니라 PNG 다)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
