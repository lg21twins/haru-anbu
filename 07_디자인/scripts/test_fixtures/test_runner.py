#!/usr/bin/env python3
"""
audit fixture 회귀 테스트 v0.3

목적:
    design_audit.py가 의도된 위반 케이스를 실제로 잡는지 검증.
    "검사가 안 돼서 0건" 같은 무성 실패를 예방.

사용:
    python3 07_디자인/scripts/test_fixtures/test_runner.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# audit 모듈 경로
SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from design_audit import (  # type: ignore
    check_html_hex, check_css_hex, find_inline_styles, find_emojis,
    find_non_iconify_icons, find_broken_at_rules,
)

FIXTURES = Path(__file__).resolve().parent

# 빈 규칙 — 허용 목록/패턴 없음 (가장 엄격 모드)
EMPTY_RULES: dict = {
    "allowed_token_definition_files": [],
    "allowed_local_token_patterns": [],
    "js_hex_allowed_files": [],
}


def test(name: str, condition: bool, info: str = "") -> tuple[str, bool, str]:
    return (name, condition, info)


def run() -> int:
    results: list[tuple[str, bool, str]] = []

    # 1. CSS 파일 hex 위반 잡힘
    css_path = FIXTURES / "fail_css_hex.css"
    text = css_path.read_text(encoding="utf-8")
    hits, _ = check_css_hex(css_path, text, EMPTY_RULES)
    results.append(test(
        "CSS hex 위반 검출 (#2C7AFC, #fff)",
        len(hits) >= 1,
        f"실제 {len(hits)}건 잡힘",
    ))

    # 2. HTML inline style hex / 인라인 패턴 / SVG 잡힘
    html_path = FIXTURES / "fail_html_inline.html"
    text = html_path.read_text(encoding="utf-8")
    hex_hits, _ = check_html_hex(html_path, text, EMPTY_RULES)
    results.append(test(
        "HTML inline/style 블록 hex 위반 검출",
        len(hex_hits) >= 3,  # inline #FF0000 + style 블록 #1234AB + #ABCDEF
        f"실제 {len(hex_hits)}건 잡힘",
    ))
    inline_hits = find_inline_styles(text)
    # `style="--bar-w:75%"`는 허용. 나머지 2건(color/padding) 잡혀야
    results.append(test(
        "inline style 위반 검출 (CSS 변수 setter 제외)",
        len(inline_hits) >= 2,
        f"실제 {len(inline_hits)}건 잡힘",
    ))
    svg_hits, allowed_brand = find_non_iconify_icons(html_path, text)
    results.append(test(
        "iconify 외 작은 SVG 검출 (viewBox 24 24 fluent path)",
        len(svg_hits) >= 1,
        f"위반 {len(svg_hits)} / 허용 brand {allowed_brand}",
    ))
    results.append(test(
        "shift-ring SVG는 BRAND_KEYWORDS로 허용",
        allowed_brand >= 1,
        f"허용 {allowed_brand}건",
    ))

    # 3. 등록되지 않은 토큰 정의 파일은 hex가 잡혀야 (회귀)
    tokens_path = FIXTURES / "pass_tokens.css"
    text = tokens_path.read_text(encoding="utf-8")
    hits_unregistered, _ = check_css_hex(tokens_path, text, EMPTY_RULES)
    results.append(test(
        "허용 목록 외 파일은 :root --var:#hex도 위반으로 검출",
        len(hits_unregistered) >= 2,
        f"실제 {len(hits_unregistered)}건 잡힘 (목록 미등록)",
    ))

    # NEW: keyframes 닫힘 손상 검출 (c02-checklist 회귀 방지)
    broken_path = FIXTURES / "fail_broken_keyframes.html"
    text = broken_path.read_text(encoding="utf-8")
    at_hits = find_broken_at_rules(text)
    results.append(test(
        "@keyframes 닫는 } 누락 검출 (c02 회귀 방지)",
        len(at_hits) >= 1,
        f"실제 {len(at_hits)}건 잡힘",
    ))

    # 4. 등록하면 통과
    allowed_rules = dict(EMPTY_RULES)
    allowed_rules["allowed_token_definition_files"] = [
        str(tokens_path.relative_to(Path(__file__).resolve().parents[3]))
    ]
    hits_registered, _ = check_css_hex(tokens_path, text, allowed_rules)
    results.append(test(
        "허용 목록에 등록한 파일의 --var:#hex 토큰 정의는 통과",
        len(hits_registered) == 0,
        f"실제 {len(hits_registered)}건 잡힘 (목록 등록 후)",
    ))

    # 결과 출력
    print("\n== audit fixture 회귀 테스트 ==\n")
    passed = sum(1 for _, ok, _ in results if ok)
    for name, ok, info in results:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}  ({info})")
    print(f"\n결과: {passed}/{len(results)} 통과")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(run())
