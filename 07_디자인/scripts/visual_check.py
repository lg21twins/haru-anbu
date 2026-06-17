#!/usr/bin/env python3
"""
하루안부 시각 검증 도구 v0.2 (정적 + 헤드리스 캡처)

사용:
    python3 07_디자인/scripts/visual_check.py
    python3 07_디자인/scripts/visual_check.py --capture  # 브라우저 캡처 포함

목적:
    design_audit.py가 코드 규칙 위반을 잡는다면, visual_check는 대표 화면이
    실제로 렌더링되는지 확인한다.

검증 항목 (대표 6화면):
    [정적 — 항상 실행]
    - 파일 존재 + 크기 > 1KB
    - <html lang="ko"> + viewport meta
    - tokens.css link
    - 필수 패턴(data-role, iconify-icon, 핵심 element)
    - body 텍스트 100자 이상 (빈 화면 방지)

    [--capture 옵션 시]
    - Chrome --headless로 PNG 캡처
    - 결과 이미지가 1KB 이상 (빈 캡처 방지)
    - 캡처 파일은 07_디자인/review-assets/visual-check/에 저장

사전 조건 (--capture):
    - macOS Google Chrome 설치 ("/Applications/Google Chrome.app")
    - 로컬 HTTP 서버 실행 중 (http://127.0.0.1:8765/) — 파일을 file:// 대신 http:// 로 로드
      서버 미실행이면 file://로 fallback(상대 경로 의존도 낮은 페이지만)

산출:
    07_디자인/review-reports/visual_check_v0.3_<YYYYMMDD>.md
    07_디자인/review-assets/visual-check/*.png (--capture 시)
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = REPO_ROOT / "07_디자인" / "review-reports"
CAPTURE_DIR = REPO_ROOT / "07_디자인" / "review-assets" / "visual-check"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LOCAL_SERVER = "http://127.0.0.1:8765/"


@dataclass
class ScreenCheck:
    name: str
    path: str
    role: str
    must_contain: list[str] = field(default_factory=list)


SCREENS = [
    ScreenCheck(
        name="컴포넌트 보드 (mobile triad)",
        path="07_디자인/role-component-board.html",
        role="board",
        must_contain=['data-platform="mobile"', "tokens/tokens.css", "<section class=\"section",
                      "iconify-icon"],
    ),
    ScreenCheck(
        name="보호자 홈 (대표)",
        path="v11_보호자앱/g-guardian-live.html",
        role="guardian",
        must_contain=['data-role="guardian"', "tokens.css", "iconify-icon"],
    ),
    ScreenCheck(
        name="요양보호사 오늘",
        path="v11_요양보호사앱/c01-today.html",
        role="caregiver",
        must_contain=['data-role="caregiver"', "tokens.css", "iconify-icon"],
    ),
    ScreenCheck(
        name="의료진 모바일 홈",
        path="v15_의료진앱/d01-home.html",
        role="medical-mobile",
        must_contain=['data-role="medical"', "tokens.css", "iconify-icon"],
    ),
    ScreenCheck(
        name="환자 태블릿 홈",
        path="v12_환자앱/p01-today.html",
        role="patient",
        must_contain=['data-role="patient"', "tokens.css", "iconify-icon"],
    ),
    ScreenCheck(
        name="의료진 웹 대시보드",
        path="v10_의료진웹/의료진_대시보드_v9.5.html",
        role="medical-web",
        must_contain=['data-role="medical"', 'data-platform="web"', "tokens.css"],
    ),
]


@dataclass
class Result:
    screen: str
    passed: bool
    detail: list[str] = field(default_factory=list)


def check_screen(s: ScreenCheck) -> Result:
    path = REPO_ROOT / s.path
    issues: list[str] = []
    if not path.exists():
        return Result(s.name, False, [f"파일 없음: {s.path}"])
    size = path.stat().st_size
    if size < 1024:
        issues.append(f"파일 크기 {size}B (< 1KB)")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Result(s.name, False, [f"UTF-8 디코딩 실패: {s.path}"])

    # 기본 메타 검사
    if "<html" not in text:
        issues.append("<html> 태그 없음")
    if 'lang="ko"' not in text:
        issues.append('lang="ko" 누락')
    if not re.search(r'<meta[^>]+name="viewport"', text):
        issues.append("viewport meta 누락")
    if "<title>" not in text:
        issues.append("<title> 누락")

    # must_contain 패턴
    for needle in s.must_contain:
        if needle not in text:
            issues.append(f"누락: '{needle}'")

    # iconify 사용량 (정보성)
    icon_count = text.count("<iconify-icon")
    if icon_count == 0 and "iconify-icon" in s.must_contain:
        issues.append("iconify-icon 사용 0 — 화면에 아이콘이 없을 가능성")

    # 큰 빈 본문 가능성 (body 안 텍스트 0)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL)
    if body_match:
        body_text = re.sub(r"<[^>]+>", "", body_match.group(1))
        body_chars = len(body_text.strip())
        if body_chars < 100:
            issues.append(f"body 안 텍스트 {body_chars}자 (< 100자 — 빈 화면 가능성)")

    return Result(s.name, len(issues) == 0, issues)


def server_alive() -> bool:
    try:
        with urllib.request.urlopen(LOCAL_SERVER, timeout=1) as r:
            return r.status == 200
    except Exception:
        return False


def capture_screen(s: ScreenCheck, use_server: bool) -> tuple[bool, str]:
    """Chrome --headless로 PNG 캡처. (성공, 메시지) 반환."""
    if not Path(CHROME_BIN).exists():
        return False, "Chrome 바이너리 없음"
    CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    out = CAPTURE_DIR / (s.role + ".png")
    if use_server:
        url = LOCAL_SERVER + urllib.parse.quote(s.path)
    else:
        url = "file://" + str((REPO_ROOT / s.path).resolve())
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--no-sandbox",
        "--hide-scrollbars",
        "--disable-features=ServiceWorker",   # SW가 first paint 막는 경우 회피
        "--virtual-time-budget=4000",          # fade-in 애니메이션 + JS 초기화 여유
        f"--window-size=430,932",              # iPhone Pro Max 비율 — 모바일 페이지 위주
        f"--screenshot={out}",
        url,
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=20)
        if res.returncode != 0:
            return False, f"chrome exit={res.returncode}"
    except subprocess.TimeoutExpired:
        return False, "캡처 timeout (20s)"
    if not out.exists():
        return False, "PNG 미생성"
    size = out.stat().st_size
    # 빈 화면/SW 미렌더 감지 — 일반 대표 화면은 50KB+. 10KB 미만이면 빈 화면 가능성 매우 큼.
    if size < 10 * 1024:
        return False, f"캡처 너무 작음 {size // 1024}KB (< 10KB) — 빈 화면 또는 SW 렌더 실패 가능성"
    return True, f"{out.relative_to(REPO_ROOT)} ({size // 1024}KB)"


def write_report(results: list[Result], capture_msgs: dict[str, str] | None = None) -> Path:
    today = dt.date.today().strftime("%Y%m%d")
    out = REPORT_DIR / f"visual_check_v0.3_{today}.md"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]
    lines = [
        f"# 시각 검증 리포트 v0.4",
        "",
        f"실행 일시: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"검사 대상: 대표 화면 {len(results)}개",
        "",
        "정적 검사 + 옵션으로 Chrome 헤드리스 캡처. `--capture` 옵션 시 캡처 결과 포함.",
        "",
        f"## 종합 결과 — {len(passed)}/{len(results)} 통과",
        "",
    ]
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        lines.append(f"### [{mark}] {r.screen}")
        if r.detail:
            for d in r.detail:
                lines.append(f"  - {d}")
        if capture_msgs and r.screen in capture_msgs:
            lines.append(f"  - 캡처: {capture_msgs[r.screen]}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="하루안부 시각 검증")
    parser.add_argument("--capture", action="store_true",
                        help="Chrome --headless로 PNG 캡처 포함")
    args = parser.parse_args()

    results = [check_screen(s) for s in SCREENS]
    print("\n== 시각 검증 v0.4 ==\n")
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"  [{mark}] {r.screen}")
        for d in r.detail:
            print(f"      - {d}")

    capture_msgs: dict[str, str] = {}
    if args.capture:
        use_server = server_alive()
        print(f"\n== 헤드리스 캡처 ({'서버' if use_server else 'file://'}) ==\n")
        if not use_server:
            print(f"  (서버 미실행 — file:// fallback. 권장: python3 -m http.server 8765)")
        for s in SCREENS:
            ok, msg = capture_screen(s, use_server)
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {s.name}: {msg}")
            capture_msgs[s.name] = msg
            # 캡처 실패는 정적 결과에 반영
            if not ok:
                for r in results:
                    if r.screen == s.name:
                        r.passed = False
                        r.detail.append(f"캡처 실패: {msg}")

    failed = [r for r in results if not r.passed]
    print(f"\n결과: {len(results) - len(failed)}/{len(results)} 통과")
    report = write_report(results, capture_msgs)
    print(f"리포트: {report.relative_to(REPO_ROOT)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
