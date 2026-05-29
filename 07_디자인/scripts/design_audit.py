#!/usr/bin/env python3
"""
하루안부 디자인 시스템 정적 감사 도구 (v0.2)

사용:
    python3 07_디자인/scripts/design_audit.py --target role-component-board
    python3 07_디자인/scripts/design_audit.py --target mobile-apps
    python3 07_디자인/scripts/design_audit.py --target app-folder --folder v11_보호자앱

산출:
    07_디자인/review-reports/<target>_audit_<YYYYMMDD>.md
    + 콘솔 요약

v0.2 변경점:
    - hex 검사를 파일 확장자별로 분리 (.html / .css / .js)
    - `:root` 안 `--var: #hex` 토큰 정의는 `allowed_token_definition_files`
      목록 안의 파일에서만 허용 (앱 화면은 기본 금지)
    - app-folder 타깃도 iconify 외 아이콘 검사 수행
    - 허용된 예외(meta theme-color / tokens.css 토큰 / CSS var setter / brand 로고)
      를 별도 카운트로 분리해 리포트
    - utility 클래스(.u-*) 개수를 정보성 카운트로 출력
    - mobile-apps 타깃 실제 구현 (대표 3앱 폴더 합산)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RULE_DIR = REPO_ROOT / "07_디자인" / "review-rules"
REPORT_DIR = REPO_ROOT / "07_디자인" / "review-reports"

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U0001F000-\U0001F2FF"
    "\U00002600-\U000027BF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "]"
)
HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}\b")
TOKEN_DEF_HEX_RE = re.compile(r"--[\w-]+\s*:\s*[^;]*#[0-9A-Fa-f]{3,8}")
INLINE_STYLE_RE = re.compile(r'\sstyle="[^"]*"')
INLINE_CSS_VAR_ONLY_RE = re.compile(r'^\s*(--[\w-]+\s*:\s*[^;]+;?\s*)+$')
META_THEME_COLOR_RE = re.compile(r'<meta[^>]+name="theme-color"[^>]+content="(#[0-9A-Fa-f]{3,8})"')
SECTION_RE = re.compile(r'<section class="section')
ROLE_COL_RE = re.compile(r'<div class="col" data-role=')


@dataclass
class CheckResult:
    name: str
    passed: bool
    expected: str = ""
    actual: str = ""
    detail: list[str] = field(default_factory=list)

    def line(self) -> str:
        mark = "PASS" if self.passed else "FAIL"
        head = f"- [{mark}] {self.name}"
        if self.expected or self.actual:
            head += f" — 기대 {self.expected} / 실제 {self.actual}"
        return head


@dataclass
class AllowedCount:
    """허용된 예외 카운트 — 위반 아니지만 가시화해서 '검사를 안 해서 0건'을 방지."""
    name: str
    count: int
    sample: list[str] = field(default_factory=list)


# =============================================================================
# 1. 파일 확장자별 검사 함수
# =============================================================================

def is_allowed_token_def_file(rel_path: str, rules: dict) -> bool:
    """이 파일이 token 정의 파일로 허용된 목록에 있는지."""
    allowed = rules.get("allowed_token_definition_files", [])
    return rel_path in allowed


def check_html_hex(path: Path, text: str, rules: dict) -> tuple[list[tuple[int, str]], dict]:
    """HTML 파일의 hex 검사.

    검사 대상:
      - <style> 블록 안 hex (단, `--var: #hex` 토큰 정의는 별도 처리)
      - inline style attr 안 hex
      - JS 문자열 안 hex (간이 — html 안 <script>)
    허용:
      - <meta name="theme-color" content="#...">
      - 토큰 정의 파일(allowed_token_definition_files) 내 토큰 정의
      - `:root`/`[data-*]` 블록 안 `--var: #hex` (허용 파일에서만)
    """
    violations: list[tuple[int, str]] = []
    allowed_counts = {"meta_theme_color": [], "local_token_def": [], "tokens_css_def": []}
    is_tokens_file = is_allowed_token_def_file(str(path.relative_to(REPO_ROOT)), rules)

    # 1) meta theme-color 허용 (text 전체에서 사전 식별)
    theme_color_lines: set[int] = set()
    for m in META_THEME_COLOR_RE.finditer(text):
        ln = text[: m.start()].count("\n") + 1
        theme_color_lines.add(ln)
        allowed_counts["meta_theme_color"].append(f"{path.name}:L{ln} {m.group(1)}")

    # 2) style 블록(들) 검사
    for sm in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.DOTALL):
        block_content = sm.group(1)
        base = text[: sm.start()].count("\n") + 1
        # :root / [data-*] 토큰 정의 라인 식별
        token_lines: set[int] = set()
        for bm in re.finditer(r"(:root|\[data-[\w-]+(?:=\"[\w-]+\")?\])\s*\{([^{}]*)\}", block_content, re.DOTALL):
            block_offset = block_content[: bm.start()].count("\n")
            block_text = bm.group(0)
            for off, line in enumerate(block_text.splitlines()):
                if TOKEN_DEF_HEX_RE.search(line):
                    ln = base + block_offset + off
                    token_lines.add(ln)
                    if is_tokens_file:
                        allowed_counts["tokens_css_def"].append(f"{path.name}:L{ln}")
                    else:
                        allowed_counts["local_token_def"].append(f"{path.name}:L{ln}")
        # 라인 단위 hex 검사
        for off, line in enumerate(block_content.splitlines()):
            ln = base + off
            if not HEX_RE.search(line):
                continue
            if ln in token_lines:
                # tokens.css 허용 파일이면 OK, 아니면 화면 파일의 로컬 토큰 정의는 위반
                if is_tokens_file:
                    continue
                # 허용 패턴(allowed_local_token_patterns) 검사
                if _matches_allowed_local_pattern(line, rules):
                    continue
                violations.append((ln, line.strip()))
                continue
            # 일반 hex 라인
            violations.append((ln, line.strip()))

    # 3) inline style attr 안 hex
    for m in re.finditer(r'\sstyle="([^"]*)"', text):
        if HEX_RE.search(m.group(1)):
            ln = text[: m.start()].count("\n") + 1
            if ln in theme_color_lines:
                continue
            violations.append((ln, m.group(0).strip()[:120]))

    # 4) <script> 블록 안 hex (간이) — js_hex_allowed_files면 chart_fallback으로 분류
    rel = str(path.relative_to(REPO_ROOT))
    js_allowed = rel in set(rules.get("js_hex_allowed_files", []))
    for sm in re.finditer(r"<script[^>]*>(.*?)</script>", text, re.DOTALL):
        block_content = sm.group(1)
        base = text[: sm.start()].count("\n") + 1
        for off, line in enumerate(block_content.splitlines()):
            if re.search(r'["\']#[0-9A-Fa-f]{3,8}["\']', line):
                if js_allowed:
                    allowed_counts.setdefault("chart_fallback", []).append(f"{path.name}:L{base+off}")
                    continue
                violations.append((base + off, line.strip()[:120]))

    return violations, allowed_counts


def _matches_allowed_local_pattern(line: str, rules: dict) -> bool:
    """allowed_local_token_patterns에 매칭되는 변수명 정의인지."""
    patterns = rules.get("allowed_local_token_patterns", [])
    if not patterns:
        return False
    for pat in patterns:
        # `--chart-*` 같은 glob 패턴을 정규식으로
        regex = "^" + re.escape(pat).replace(r"\*", r"[\w-]*") + r"\s*:"
        # 라인에서 `--var:` 부분만 떼서 매칭
        var_match = re.search(r"(--[\w-]+)\s*:", line)
        if not var_match:
            continue
        if re.match(regex, var_match.group(0)):
            return True
    return False


def check_css_hex(path: Path, text: str, rules: dict) -> tuple[list[tuple[int, str]], dict]:
    """CSS 파일 hex 검사.

    허용 파일(`allowed_token_definition_files`)이면 모든 `--var: #hex` 정의 허용,
    그 외 위치의 hex는 위반.
    그 외 파일이면 모든 hex가 위반(단 allowed_local_token_patterns 예외).
    """
    violations: list[tuple[int, str]] = []
    allowed_counts = {"tokens_css_def": [], "local_token_def": []}
    rel = str(path.relative_to(REPO_ROOT))
    is_tokens_file = is_allowed_token_def_file(rel, rules)

    for i, line in enumerate(text.splitlines(), 1):
        if not HEX_RE.search(line):
            continue
        if TOKEN_DEF_HEX_RE.search(line):
            if is_tokens_file:
                allowed_counts["tokens_css_def"].append(f"{path.name}:L{i}")
                continue
            if _matches_allowed_local_pattern(line, rules):
                allowed_counts["local_token_def"].append(f"{path.name}:L{i} (pattern)")
                continue
            # 화면 CSS의 로컬 토큰 정의는 위반
            violations.append((i, line.strip()))
            continue
        # 토큰 정의가 아닌 일반 hex
        if is_tokens_file:
            # tokens.css 안에서도 토큰 정의 라인이 아니면 잡음
            violations.append((i, line.strip()))
        else:
            violations.append((i, line.strip()))
    return violations, allowed_counts


def check_js_hex(path: Path, text: str, rules: dict) -> tuple[list[tuple[int, str]], dict]:
    """JS/MJS 파일의 hex 문자열 검사."""
    violations: list[tuple[int, str]] = []
    allowed_counts = {"chart_fallback": []}
    chart_allow = set(rules.get("js_hex_allowed_files", []))
    rel = str(path.relative_to(REPO_ROOT))
    for i, line in enumerate(text.splitlines(), 1):
        if not re.search(r'["\']#[0-9A-Fa-f]{3,8}["\']', line):
            continue
        if rel in chart_allow:
            allowed_counts["chart_fallback"].append(f"{path.name}:L{i}")
            continue
        violations.append((i, line.strip()[:120]))
    return violations, allowed_counts


def find_hex_violations(path: Path, text: str, rules: dict) -> tuple[list[tuple[int, str]], dict]:
    """확장자 dispatcher."""
    suffix = path.suffix.lower()
    if suffix == ".html":
        return check_html_hex(path, text, rules)
    if suffix == ".css":
        return check_css_hex(path, text, rules)
    if suffix in (".js", ".mjs"):
        return check_js_hex(path, text, rules)
    return [], {}


# =============================================================================
# 2. 기존 검사 — inline style / emoji / forbidden class / non-iconify icons
# =============================================================================

def find_inline_styles(text: str) -> list[tuple[int, str]]:
    """CSS 변수 setter만 들어있는 inline style은 허용, 그 외 위반."""
    hits: list[tuple[int, str]] = []
    style_attr_re = re.compile(r'\sstyle="([^"]*)"')
    for i, line in enumerate(text.splitlines(), 1):
        for m in style_attr_re.finditer(line):
            body = m.group(1)
            if INLINE_CSS_VAR_ONLY_RE.match(body):
                continue
            hits.append((i, line.strip()))
            break
    return hits


def count_allowed_inline_css_vars(text: str) -> int:
    """허용된 CSS 변수 setter inline style 개수."""
    count = 0
    for m in re.finditer(r'\sstyle="([^"]*)"', text):
        if INLINE_CSS_VAR_ONLY_RE.match(m.group(1)):
            count += 1
    return count


def find_broken_at_rules(text: str) -> list[tuple[int, str]]:
    """`<style>` 블록 안 `@keyframes` / `@media` 등 at-rule이 정상 닫혔는지 검사.
    또한 keyframes 안의 selector가 %/from/to 외 다른 클래스이면 손상으로 판정 — c02-checklist
    같은 사고 (keyframes 닫는 `}` 누락 → 다음 룰이 keyframes로 빨려 들어감) 회귀 방지.
    """
    violations: list[tuple[int, str]] = []
    for sm in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.DOTALL):
        content = sm.group(1)
        base = text[: sm.start()].count("\n") + 1
        for km in re.finditer(r"@(\w+)\s+[\w-]*\s*\{", content):
            at_name = km.group(1)
            start = km.end()
            depth = 1
            i = start
            while i < len(content) and depth > 0:
                ch = content[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                i += 1
            if depth != 0:
                ln = base + content[: km.start()].count("\n")
                violations.append((ln, f"@{at_name} 블록이 닫히지 않음"))
                continue
            if at_name == "keyframes":
                body = content[start : i - 1]
                for rm in re.finditer(
                    r"(?:^|;|\})\s*([.\w][\w.\s\-]*?)\s*\{", body, re.MULTILINE
                ):
                    sel = rm.group(1).strip()
                    if not re.match(r"^(\d+%(\s*,\s*\d+%)*|from|to)$", sel):
                        ln = base + content[: start + rm.start()].count("\n")
                        violations.append(
                            (ln, f"@keyframes 안 비정상 selector: '{sel[:50]}'")
                        )
                        break
    return violations


def find_emojis(text: str) -> list[tuple[int, str]]:
    return [
        (i, line.strip())
        for i, line in enumerate(text.splitlines(), 1)
        if EMOJI_RE.search(line)
    ]


def find_forbidden_classes(text: str, classes: list[str]) -> list[tuple[int, str, str]]:
    hits = []
    for cls in classes:
        pat = re.compile(rf"\b{re.escape(cls)}\b")
        for i, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                hits.append((i, cls, line.strip()))
    return hits


def find_non_iconify_icons(path: Path, text: str) -> tuple[list[tuple[int, str]], int]:
    """HTML 안의 SVG / .svg 이미지 사용을 검사.
    허용:
      - 브랜드 심볼 (viewBox="0 0 2526 2526") — 하루안부 로고
      - 클래스/id에 'brand', 'haru-mark', 'bg-logo', 'intro-ring', 'pulse', 'wave', 'spinner' 포함
      - viewBox가 256 이상 (큰 일러스트)
      - <img src=...brand-system/...> 또는 /logo/ 경로
    위반:
      - 작은 fluent 대체 가능 SVG (viewBox 24 24 등 일반 아이콘 크기)
    """
    if path.suffix.lower() != ".html":
        return [], 0
    hits = []
    allowed_brand = 0
    BRAND_KEYWORDS = (
        'brand-', 'haru-mark', 'bg-logo', 'intro-ring', 'shift-svg',
        'pulse', 'wave', 'spinner', 'ring-progress', 'sos__ring',
        # v0.3: 의도된 시각화 SVG는 유지 — 모바일 탭바 시그니처, 스파크라인, SOS ring,
        # 차트 인디케이터 등 (svg_inventory_v0.3 분류 참조)
        'tab-svg', 'ov-spark', 'sos-ring', 'ai-score-ring',
        'chart-marker', 'gauge-ring', 'mood-dot',
        'shift-ring', 'progress-fill', 'progress-stroke', 'spark-line',
        # v0.4: viewBox 자동 허용 좁힌 후 명시 클래스 필요
        'countdown-ring',
    )

    def is_allowed_svg(snippet: str) -> bool:
        if any(k in snippet for k in BRAND_KEYWORDS):
            return True
        # 하루안부 브랜드 심볼 viewBox
        if 'viewBox="0 0 2526 2526"' in snippet:
            return True
        # 큰 viewBox (256+) — 일러스트로 판단 (자동 허용, 클래스 무관)
        vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', snippet)
        if vb_match:
            w, h = int(vb_match.group(1)), int(vb_match.group(2))
            if min(w, h) >= 256:
                return True
        # v0.4 좁힘: 시각화 ring 전용 viewBox는 BRAND_KEYWORDS 클래스가 있을 때만 허용.
        # (60,60)/(84,84)/(140,140)/(44,44) 만으로는 일반 아이콘도 통과해 버려 audit 구멍.
        # → ring/spark/progress/sos 같은 시그니처 클래스를 함께 요구.
        return False

    for m in re.finditer(r"<svg\b[^>]*>", text):
        snippet = m.group(0)
        ln = text[: m.start()].count("\n") + 1
        if is_allowed_svg(snippet):
            allowed_brand += 1
            continue
        hits.append((ln, snippet[:90]))

    for m in re.finditer(r'<img[^>]+src="([^"]+\.svg)"[^>]*>', text):
        ln = text[: m.start()].count("\n") + 1
        src = m.group(1)
        if "brand-system" in src or "/logo/" in src or "심볼단독" in src or "01_심볼" in src:
            allowed_brand += 1
            continue
        hits.append((ln, m.group(0)[:90]))
    return hits, allowed_brand


def count_meta_theme_color(text: str) -> int:
    return len(META_THEME_COLOR_RE.findall(text))


def count_u_classes(text: str, custom_prefixes: tuple[str, ...] = ("u-",)) -> int:
    """style 블록 안의 `.u-*` 클래스 정의 카운트."""
    style_block = re.search(r"<style[^>]*>(.*?)</style>", text, re.DOTALL)
    if not style_block:
        return 0
    content = style_block.group(1)
    count = 0
    for prefix in custom_prefixes:
        count += len(re.findall(rf"\.{re.escape(prefix)}[\w-]+\s*\{{", content))
    return count


# =============================================================================
# 3. 타깃 checker
# =============================================================================

def check_role_component_board(rules: dict) -> tuple[list[CheckResult], dict]:
    results: list[CheckResult] = []
    details: dict = {"allowed": []}

    primary_file = REPO_ROOT / rules["files"][0]
    text = primary_file.read_text(encoding="utf-8")
    details["primary_file"] = str(primary_file.relative_to(REPO_ROOT))

    s_rules = rules["rules"]["structure"]
    sections = len(SECTION_RE.findall(text))
    role_cols = len(ROLE_COL_RE.findall(text))
    col_role_counts = {"guardian": 0, "caregiver": 0, "medical": 0}
    for m in re.finditer(r'<div class="col" data-role="([a-z]+)"', text):
        role = m.group(1)
        if role in col_role_counts:
            col_role_counts[role] += 1

    results.append(CheckResult("구조 · 섹션 수", sections == s_rules["sections"],
                               str(s_rules["sections"]), str(sections)))
    results.append(CheckResult("구조 · role 컬럼 총수", role_cols == s_rules["role_columns_total"],
                               str(s_rules["role_columns_total"]), str(role_cols)))
    for role_name, expected_key in [("guardian", "guardian_columns"),
                                     ("caregiver", "caregiver_columns"),
                                     ("medical", "medical_columns")]:
        results.append(CheckResult(f"구조 · {role_name} 컬럼",
                                   col_role_counts[role_name] == s_rules[expected_key],
                                   str(s_rules[expected_key]), str(col_role_counts[role_name])))

    f_rules = rules["rules"]["forbidden"]
    inline_hits = find_inline_styles(text)
    results.append(CheckResult("금지 · inline style",
                               len(inline_hits) == f_rules["inline_style_count"],
                               str(f_rules["inline_style_count"]), str(len(inline_hits)),
                               detail=[f"L{ln}: {ls[:100]}" for ln, ls in inline_hits[:10]]))
    hex_hits, allowed = find_hex_violations(primary_file, text, rules)
    results.append(CheckResult("금지 · 직접 hex",
                               len(hex_hits) == f_rules["direct_hex_in_body_count"],
                               str(f_rules["direct_hex_in_body_count"]), str(len(hex_hits)),
                               detail=[f"L{ln}: {ls[:100]}" for ln, ls in hex_hits[:10]]))
    details["allowed"].append(AllowedCount("허용 · CSS 변수 setter inline style",
                                            count_allowed_inline_css_vars(text)))
    details["allowed"].append(AllowedCount("허용 · meta theme-color",
                                            count_meta_theme_color(text)))
    for k, v in allowed.items():
        if v:
            details["allowed"].append(AllowedCount(f"허용 · hex({k})", len(v), v[:5]))

    emoji_hits = find_emojis(text)
    results.append(CheckResult("금지 · 이모지",
                               len(emoji_hits) == f_rules["emoji_count"],
                               str(f_rules["emoji_count"]), str(len(emoji_hits)),
                               detail=[f"L{ln}: {ls[:100]}" for ln, ls in emoji_hits[:10]]))
    forbidden_cls = f_rules.get("forbidden_classes", [])
    fc_hits = find_forbidden_classes(text, forbidden_cls)
    results.append(CheckResult(f"금지 · 폐기 클래스명({', '.join(forbidden_cls)})",
                               len(fc_hits) == 0, "0", str(len(fc_hits)),
                               detail=[f"L{ln}: ({cls}) {ls[:100]}" for ln, cls, ls in fc_hits[:10]]))

    icon_hits, brand_ok = find_non_iconify_icons(primary_file, text)
    results.append(CheckResult("아이콘 · iconify-icon 외 사용",
                               len(icon_hits) == 0, "0", str(len(icon_hits)),
                               detail=[f"L{ln}: {ls}" for ln, ls in icon_hits[:5]]))

    at_hits = find_broken_at_rules(text)
    results.append(CheckResult("CSS · @keyframes/@media at-rule 닫힘",
                               len(at_hits) == 0, "0", str(len(at_hits)),
                               detail=[f"L{ln}: {msg}" for ln, msg in at_hits[:5]]))
    if brand_ok:
        details["allowed"].append(AllowedCount("허용 · 브랜드 로고 SVG", brand_ok))

    # utility 카운트 (정보성)
    u_count = count_u_classes(text)
    details["allowed"].append(AllowedCount(f"정보 · {primary_file.name} 유틸리티 클래스(.u-*)", u_count))

    tokens_path = rules["rules"]["tokens_import"]["must_link_stylesheet"]
    has_link = f'href="{tokens_path}"' in text or tokens_path in text
    results.append(CheckResult(f"임포트 · {tokens_path} 링크",
                               has_link, "있음", "있음" if has_link else "없음"))

    v_rules = rules["rules"]["version_match"]
    expected_v = v_rules["expected_substring"]
    version_issues: list[str] = []
    for cls in v_rules["patterns"]:
        cls_re = re.compile(rf'class="[^"]*{re.escape(cls)}[^"]*"[^>]*>([^<]+)<')
        m = cls_re.search(text)
        if not m:
            version_issues.append(f"{cls} 요소를 찾지 못함")
            continue
        body = m.group(1).strip()
        if expected_v not in body:
            version_issues.append(f"{cls} 본문 '{body}'에 '{expected_v}' 없음")
    results.append(CheckResult(f"버전 · {expected_v} 통일",
                               len(version_issues) == 0,
                               "통일", "통일" if not version_issues else "불일치",
                               detail=version_issues))

    lc = rules.get("link_check", {})
    link_file = REPO_ROOT / lc.get("file", "")
    if link_file.exists():
        link_text = link_file.read_text(encoding="utf-8")
        missing = [s for s in lc.get("must_contain", []) if s not in link_text]
        results.append(CheckResult(f"링크 · {lc['file']} 안 보드 진입점",
                                   len(missing) == 0, "있음",
                                   "있음" if not missing else f"누락: {missing}"))
    return results, details


def check_app_folder(rules: dict, folder: str) -> tuple[list[CheckResult], dict]:
    base = REPO_ROOT / folder
    if not base.exists():
        return [CheckResult(f"폴더 없음: {folder}", False)], {}

    exts = set(rules.get("include_extensions", [".html", ".css", ".md", ".js"]))
    excludes = rules.get("exclude", [])

    files: list[Path] = []
    for p in base.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        if any(ex.rstrip("/") in p.parts for ex in excludes):
            continue
        files.append(p)

    inline_total = 0
    hex_total = 0
    emoji_total = 0
    forbidden_total = 0
    icon_total = 0
    at_total = 0
    inline_files: dict[str, int] = {}
    hex_files: dict[str, int] = {}
    emoji_files: dict[str, int] = {}
    forbidden_files: dict[str, int] = {}
    icon_files: dict[str, int] = {}
    at_files: dict[str, int] = {}
    allowed_summary: dict[str, int] = {}
    forbidden_classes = rules["rules"].get("forbidden_classes", [])
    u_total = 0

    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(p.relative_to(REPO_ROOT))
        if p.suffix.lower() == ".html":
            inline_c = len(find_inline_styles(text))
            if inline_c:
                inline_total += inline_c
                inline_files[rel] = inline_c
            allowed_summary["CSS 변수 setter inline"] = allowed_summary.get("CSS 변수 setter inline", 0) + count_allowed_inline_css_vars(text)
            allowed_summary["meta theme-color"] = allowed_summary.get("meta theme-color", 0) + count_meta_theme_color(text)
            u_total += count_u_classes(text)
            icon_hits, brand_ok = find_non_iconify_icons(p, text)
            if icon_hits:
                icon_total += len(icon_hits)
                icon_files[rel] = len(icon_hits)
            allowed_summary["브랜드 로고 SVG"] = allowed_summary.get("브랜드 로고 SVG", 0) + brand_ok
            at_hits = find_broken_at_rules(text)
            if at_hits:
                at_total += len(at_hits)
                at_files[rel] = len(at_hits)
        hex_hits, allowed = find_hex_violations(p, text, rules)
        if hex_hits:
            hex_total += len(hex_hits)
            hex_files[rel] = len(hex_hits)
        for k, v in allowed.items():
            allowed_summary[f"hex/{k}"] = allowed_summary.get(f"hex/{k}", 0) + len(v)
        emoji_c = len(find_emojis(text))
        if emoji_c:
            emoji_total += emoji_c
            emoji_files[rel] = emoji_c
        fc_c = sum(text.count(cls) for cls in forbidden_classes)
        if fc_c:
            forbidden_total += fc_c
            forbidden_files[rel] = fc_c

    results = []
    results.append(CheckResult(f"폴더 · {folder} 파일 수", True, "-", str(len(files))))
    results.append(CheckResult("금지 · inline style",
                               inline_total <= rules["rules"]["max_inline_style"],
                               str(rules["rules"]["max_inline_style"]), str(inline_total),
                               detail=[f"{f}: {c}건" for f, c in sorted(inline_files.items(), key=lambda x: -x[1])[:15]]))
    results.append(CheckResult("금지 · 직접 hex(HTML/CSS/JS)",
                               hex_total <= rules["rules"]["max_direct_hex_in_body"],
                               str(rules["rules"]["max_direct_hex_in_body"]), str(hex_total),
                               detail=[f"{f}: {c}건" for f, c in sorted(hex_files.items(), key=lambda x: -x[1])[:15]]))
    results.append(CheckResult("금지 · 이모지",
                               emoji_total <= rules["rules"]["max_emoji"],
                               str(rules["rules"]["max_emoji"]), str(emoji_total),
                               detail=[f"{f}: {c}건" for f, c in sorted(emoji_files.items(), key=lambda x: -x[1])[:15]]))
    results.append(CheckResult(f"금지 · 폐기 클래스명({', '.join(forbidden_classes)})",
                               forbidden_total == 0, "0", str(forbidden_total),
                               detail=[f"{f}: {c}건" for f, c in sorted(forbidden_files.items(), key=lambda x: -x[1])[:15]]))
    results.append(CheckResult("아이콘 · iconify-icon 외 사용",
                               icon_total == 0, "0", str(icon_total),
                               detail=[f"{f}: {c}건" for f, c in sorted(icon_files.items(), key=lambda x: -x[1])[:15]]))
    results.append(CheckResult("CSS · @keyframes/@media at-rule 닫힘",
                               at_total == 0, "0", str(at_total),
                               detail=[f"{f}: {c}건" for f, c in sorted(at_files.items(), key=lambda x: -x[1])[:15]]))

    details = {"primary_file": folder, "file_count": len(files),
               "allowed": [AllowedCount(k, v) for k, v in allowed_summary.items() if v],
               "u_class_total": u_total}
    details["allowed"].append(AllowedCount(f"정보 · 유틸리티 클래스(.u-*) 총합", u_total))
    return results, details


def check_mobile_apps(rules: dict) -> tuple[list[CheckResult], dict]:
    """대표 모바일 3앱 + 환자/온보딩/웹 합산 감사."""
    folders = rules.get("folders", [])
    if not folders:
        return [CheckResult("mobile-apps · folders 정의 없음", False)], {}
    all_results: list[CheckResult] = []
    overall_summary: dict[str, int] = {}
    for folder in folders:
        sub_results, sub_details = check_app_folder(rules, folder)
        # sub_results의 카운트만 추출해 합산
        for r in sub_results:
            try:
                overall_summary[r.name] = overall_summary.get(r.name, 0) + int(r.actual)
            except (TypeError, ValueError):
                pass
        passed = all(r.passed for r in sub_results)
        all_results.append(CheckResult(f"폴더 · {folder}",
                                       passed, "PASS", "PASS" if passed else "FAIL",
                                       detail=[r.line() for r in sub_results if not r.passed]))
    # 대표 화면 존재 체크
    rep_screens = rules.get("representative_screens", [])
    missing = [s for s in rep_screens if not (REPO_ROOT / s).exists()]
    all_results.append(CheckResult("대표 화면 존재", len(missing) == 0,
                                   "전부 존재", "전부 존재" if not missing else f"누락: {missing}"))
    details = {"primary_file": "mobile-apps", "allowed": []}
    return all_results, details


TARGETS = {
    "role-component-board": check_role_component_board,
    "mobile-apps": check_mobile_apps,
    "app-folder": "_dynamic_app_folder_",
}


# =============================================================================
# 4. 리포트 작성
# =============================================================================

def write_report(target: str, rules: dict, results: list[CheckResult], details: dict) -> Path:
    today = dt.date.today().strftime("%Y%m%d")
    suffix = ""
    if target == "app-folder" and details.get("primary_file"):
        suffix = "_" + details["primary_file"].replace("/", "_")
    out = REPORT_DIR / f"{target}{suffix}_audit_{today}.md"

    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]
    overall_pass = len(failed) == 0

    lines: list[str] = []
    lines.append(f"# 디자인 감사 리포트 — {target} (v0.2)")
    lines.append("")
    lines.append(f"실행 일시: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"규칙 파일: `07_디자인/review-rules/{target}.json`")
    if details.get("primary_file"):
        lines.append(f"검사 대상: `{details['primary_file']}`")
    lines.append("")
    lines.append(f"## 종합 결과 — audit v0.2 기준 {'PASS' if overall_pass else 'FAIL'}")
    lines.append("")
    lines.append(f"- 통과: {len(passed)}건 / 실패: {len(failed)}건")
    lines.append("")

    if failed:
        lines.append("## 실패 항목")
        lines.append("")
        for r in failed:
            lines.append(r.line())
            for d in r.detail:
                lines.append(f"    - {d}")
        lines.append("")

    lines.append("## 통과 항목")
    lines.append("")
    for r in passed:
        lines.append(r.line())
    lines.append("")

    allowed_list = details.get("allowed", [])
    if allowed_list:
        lines.append("## 허용된 예외 / 정보성 카운트")
        lines.append("")
        lines.append("아래는 검사가 정상 작동한 결과 _정책적으로 허용_ 된 항목과 정보성 카운트입니다.")
        lines.append("'검사를 안 해서 0건'이 아님을 보여주기 위해 분리 표시합니다.")
        lines.append("")
        for a in allowed_list:
            lines.append(f"- {a.name}: {a.count}건")
            for s in a.sample[:3]:
                lines.append(f"    - {s}")
        lines.append("")

    lines.append("## 수정 권장안")
    lines.append("")
    if not failed:
        lines.append("- 위반 사항 없음. 현재 상태를 기준으로 유지하면 됨.")
    else:
        for r in failed:
            lines.append(f"### {r.name}")
            lines.append(f"- 기대값: {r.expected}")
            lines.append(f"- 실제값: {r.actual}")
            if r.detail:
                lines.append("- 위반 위치:")
                for d in r.detail:
                    lines.append(f"  - {d}")
            lines.append("")
    lines.append("")

    lines.append("## 클로드에게 보낼 요약 지시문")
    lines.append("")
    if not failed:
        lines.append("```text")
        lines.append(f"{target} audit v0.2 기준 PASS. 변경 없음.")
        lines.append("```")
    else:
        lines.append("```text")
        lines.append(f"{target} 디자인 감사(v0.2)에서 다음 위반이 발견됐다.")
        for r in failed:
            lines.append(f"- {r.name}: 기대 {r.expected} / 실제 {r.actual}")
            for d in r.detail[:3]:
                lines.append(f"  · {d}")
        lines.append("수정 후 다시 design_audit.py를 실행해서 PASS로 만들어줘.")
        lines.append("```")
    lines.append("")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="하루안부 디자인 감사 도구 (v0.2)")
    parser.add_argument("--target", required=True, choices=sorted(TARGETS.keys()),
                        help="감사 대상")
    parser.add_argument("--folder", help="app-folder 타깃일 때 폴더 경로")
    parser.add_argument("--no-report", action="store_true", help="MD 리포트 생략")
    args = parser.parse_args()

    rules = load_rules(args.target)
    if args.target == "app-folder":
        if not args.folder:
            sys.exit("app-folder 타깃은 --folder <path>를 함께 지정해야 합니다.")
        results, details = check_app_folder(rules, args.folder)
    elif args.target == "mobile-apps":
        results, details = check_mobile_apps(rules)
    else:
        checker = TARGETS[args.target]
        results, details = checker(rules)

    print(f"\n== 감사 (v0.2) — {args.target} ==\n")
    for r in results:
        print(r.line())
        for d in r.detail[:5]:
            print(f"    {d}")
    allowed_list = details.get("allowed", [])
    if allowed_list:
        print("\n허용 / 정보:")
        for a in allowed_list:
            print(f"  · {a.name}: {a.count}건")

    failed = [r for r in results if not r.passed]
    print(f"\n결과: {'PASS' if not failed else 'FAIL'} ({len(results) - len(failed)}/{len(results)} 통과)")

    if not args.no_report:
        report_path = write_report(args.target, rules, results, details)
        print(f"리포트: {report_path.relative_to(REPO_ROOT)}")

    return 0 if not failed else 1


def load_rules(target: str) -> dict:
    path = RULE_DIR / f"{target}.json"
    if not path.exists():
        sys.exit(f"규칙 파일을 찾을 수 없습니다: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
