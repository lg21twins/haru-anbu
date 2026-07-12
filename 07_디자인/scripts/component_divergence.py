#!/usr/bin/env python3
"""
같은 클래스명이 여러 화면에서 서로 다른 사양으로 정의되는 케이스를 찾는다.

사용:
    python3 07_디자인/scripts/component_divergence.py

산출:
    07_디자인/review-reports/component_divergence_<YYYYMMDD>.md
"""
from __future__ import annotations
import datetime as dt
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = REPO_ROOT / "07_디자인" / "review-reports"

FOLDERS = [
    "v10_의료진웹",
    "v11_보호자앱",
    "v11_요양보호사앱",
    "v12_환자앱",
    "v13_온보딩",
    "v15_의료진앱",
]
EXCLUDE_PARTS = {"_archive", "_history"}

# 점검 제외할 화면 단순/맥락 클래스 (.app-shell 같이 wrapper만)
SKIP_CLASSES = {
    "app-shell", "bg", "app", "stack",
    "msg-list",  # 다양한 컬렉션
}

# 진짜 단독 정의만 카운트 — 셀렉터 시작 또는 콤마 직후가 정확히 `.class[:pseudo]` 이고
# 그 뒤에 공백+다른 셀렉터가 없을 때만 매칭.
CLASS_RULE_RE = re.compile(
    r'(?:^|,)\s*'                          # 룰 시작 또는 콤마 다음
    r'\.([A-Za-z_][\w-]*)'                 # .class-name
    r'(?:::?[\w-]+)*'                      # 선택적 :pseudo / ::pseudo (조합 OK)
    r'\s*\{([^{}]*)\}', re.DOTALL | re.MULTILINE
)

def normalize(decl: str) -> str:
    """선언부를 정규화 (공백·줄바꿈·순서 무시 — 동일성만 판단)"""
    parts = []
    for prop in decl.split(";"):
        p = prop.strip()
        if not p:
            continue
        # 값 정규화: 공백 1개로
        p = re.sub(r"\s+", " ", p)
        # CSS 변수 fallback 무시 (var(--x, #yyy) → var(--x))
        p = re.sub(r"var\(\s*(--[\w-]+)\s*,[^)]+\)", r"var(\1)", p)
        parts.append(p)
    return "|".join(sorted(parts))


def collect_class_defs():
    """클래스명 → [(파일, 정규화된 선언, 원본 선언 첫 80자)] 매핑."""
    table: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for folder in FOLDERS:
        files = list((REPO_ROOT / folder).rglob("*.html"))
        files.extend((REPO_ROOT / folder).rglob("*.css"))
        for p in files:
            if any(x in p.parts for x in EXCLUDE_PARTS):
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            rel = str(p.relative_to(REPO_ROOT))
            contents = (
                [text]
                if p.suffix == ".css"
                else [sm.group(1) for sm in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.DOTALL)]
            )
            for content in contents:
                for m in CLASS_RULE_RE.finditer(content):
                    cls = m.group(1)
                    if cls in SKIP_CLASSES:
                        continue
                    body = m.group(2)
                    norm = normalize(body)
                    snippet = re.sub(r"\s+", " ", body.strip())[:80]
                    table[cls].append((rel, norm, snippet))
    return table


def find_divergences(table: dict[str, list[tuple[str, str, str]]]):
    """클래스가 여러 파일에서 다른 정규화 결과를 가지면 divergence."""
    diverged = []
    for cls, defs in table.items():
        if len(defs) < 2:
            continue
        normalized_set = {d[1] for d in defs}
        if len(normalized_set) <= 1:
            continue
        # 파일별 그룹화
        by_norm: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for f, n, s in defs:
            by_norm[n].append((f, s))
        diverged.append((cls, len(defs), len(normalized_set), by_norm))
    diverged.sort(key=lambda x: (-x[1], -x[2]))
    return diverged


def write_report(diverged):
    today = dt.date.today().strftime("%Y%m%d")
    out = REPORT_DIR / f"component_divergence_{today}.md"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 컴포넌트 정의 다이버전스 리포트",
        "",
        f"실행 일시: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 의미",
        "",
        "같은 CSS 클래스명이 여러 화면에서 **서로 다른 사양**으로 정의된 경우.",
        "디자인 시스템 원칙상 컴포넌트는 한 곳(system/components.css)에서 정의되어야 한다.",
        "화면별 로컬 정의는 의도된 변형이 아닌 한 통일 대상.",
        "",
        f"## 총 발견: {len(diverged)}개 클래스",
        "",
        "정규화: 공백·순서·var() 폴백 hex 무시. 그래도 다른 값이면 다이버전스로 판단.",
        "",
    ]
    if not diverged:
        lines.append("위반 없음.")
    else:
        lines.append("| 클래스 | 정의 파일 수 | 다른 사양 수 |")
        lines.append("|---|---:|---:|")
        for cls, total, n_distinct, _ in diverged:
            lines.append(f"| `.{cls}` | {total} | {n_distinct} |")
        lines.append("")
        lines.append("## 상세 (상위 30개)")
        lines.append("")
        for cls, total, n_distinct, by_norm in diverged[:30]:
            lines.append(f"### `.{cls}` — {total}개 파일, {n_distinct}개 다른 사양")
            lines.append("")
            for i, (norm, files) in enumerate(by_norm.items(), 1):
                lines.append(f"**버전 {i}** ({len(files)}개 파일):")
                for f, snippet in files[:5]:
                    lines.append(f"- `{f}`: `{snippet}`")
                if len(files) > 5:
                    lines.append(f"- … 외 {len(files) - 5}개")
                lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main():
    table = collect_class_defs()
    diverged = find_divergences(table)
    report = write_report(diverged)

    print(f"\n== 컴포넌트 다이버전스 리포트 ==")
    print(f"클래스 전체: {len(table)}")
    print(f"다이버전스 발견: {len(diverged)}개 클래스")
    print(f"\n상위 15개 (정의 파일 많은 순):")
    for cls, total, n_distinct, _ in diverged[:15]:
        print(f"  .{cls:30s}  {total:3d}개 파일 / {n_distinct}개 다른 사양")
    print(f"\n리포트: {report.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
