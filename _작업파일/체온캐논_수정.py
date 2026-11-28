#!/usr/bin/env python3
"""요양보호사 앱 인수인계 — 체온이 미열이 아닌 값으로 적혀 있다

    python3 _작업파일/체온캐논_수정.py --미리보기
    python3 _작업파일/체온캐논_수정.py

무엇이 틀렸나
─────────────
`c01-today.html` 인수인계 요약 한 줄이 이렇게 돼 있다.

    마른 기침 3회 관찰. **체온 36.9℃ 미열.** 오전 중 상태 변화 시 간호사 호출.

**36.9℃ 는 미열이 아니다. 정상 체온이다.**

그런데 이건 지어낸 값도 아니고, 그냥 오타도 아니다. **같은 파일 772행**에
요양보호사가 잰 측정 계열이 그대로 들어 있다:

    06:00 36.9 → 06:20 37.1 → 06:40 37.4 (상승 추세)

즉 36.9 는 **06:00 첫 측정값**이다. 요약 줄이 계열의 **첫 값**을 가져다 놓고
현재 상태인 것처럼 "미열"이라고 부른 것이다. 같은 화면 관찰 카드는
**마지막 체크 06:40** 이라고 적고 있으니, 요약에 와야 할 값은 **37.4** 다.

37.4 가 맞다는 근거는 이 파일 밖에도 널려 있다 —
  c01-today `체온 37.4℃ · 4회 측정` · c01-일정표 `오전 37.4℃`
  c03-sotong `체온 37.4°C — 평소보다 0.8도 높음`  (36.6 + 0.8 = 37.4, 산수도 맞는다)
  en·zh 판까지 전부 37.4. **36.9 를 미열이라 부르는 곳은 이 한 줄뿐이다.**

왜 서둘러 고치나
────────────────
KHF 는 **보건의료** 전시회다. 부스에 오는 사람 상당수가 간호사이고,
`36.9℃ 미열` 은 그 사람들이 **한눈에 보는** 종류의 오류다.
제안서에서 수치를 하나하나 검증해 온 태도가 화면 한 줄로 무너진다.

건드리지 않는 것
────────────────
772행의 측정 계열(36.9 → 37.1 → 37.4)은 **그대로 둔다.** 그게 근거다.
`(상승 추세)` 라는 표현은 앱이 추세를 말하는 셈이라 SaMD 경계에서 걸릴 여지가
있지만, 요양보호사가 직접 적는 관찰 메모 영역이라 **판단이 필요한 항목으로 남긴다**
(원고 `23_의료진화면_판단.md` §3-C).
"""
import datetime
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (파일, 지금, 바꾼 뒤)
FIXES = [
    ("v11_요양보호사앱/c01-today.html",
     "체온 36.9℃ 미열", "체온 37.4℃ 미열"),
    ("v11_요양보호사앱/c01-today.en.html",
     "Temp 36.9°C, low-grade", "Temp 37.4°C, low-grade"),
    ("v11_요양보호사앱/c01-today.zh.html",
     "体温 36.9℃ 微热", "体温 37.4℃ 微热"),
    # 쇼케이스에 박제된 사본 — haruanbu.site 에 그대로 떠 있다
    ("haru-anbu-showcase-v8-bundle/07_디자인/mockup/v11_요양보호사앱/c01-today.html",
     "체온 36.9℃ 미열", "체온 37.4℃ 미열"),
]


def main():
    dry = "--미리보기" in sys.argv or "--dry" in sys.argv
    stamp = datetime.date.today().strftime("%Y%m%d")
    changed, missed = 0, 0

    for rel, old, new in FIXES:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            print(f"  없는 파일 {rel}")
            missed += 1
            continue
        body = open(path, encoding="utf-8").read()
        if old not in body:
            print(f"  못 찾음 {rel}  — 이미 고쳤는지 확인할 것")
            missed += 1
            continue
        print(f"  {rel}")
        print(f"      - {old}")
        print(f"      + {new}")
        changed += 1
        if dry:
            continue
        bak = os.path.join(REPO, os.path.dirname(rel), f"_원본백업_{stamp}")
        os.makedirs(bak, exist_ok=True)
        shutil.copy2(path, os.path.join(bak, os.path.basename(path)))
        open(path, "w", encoding="utf-8").write(body.replace(old, new))

    print()
    if dry:
        print(f"미리보기 — {changed}건 바꿀 수 있다. 적용하려면 --미리보기 없이 다시 돌린다.")
        return 0
    print(f"{changed}건 적용 (원본은 각 폴더의 _원본백업_{stamp}/ 에 있다)")
    if changed:
        print("\n다음:")
        print("  python3 07_디자인/scripts/static_integrity.py")
        print("  python3 08_제안서/점검.py        # 체온 캐논 규칙이 이걸 본다")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
