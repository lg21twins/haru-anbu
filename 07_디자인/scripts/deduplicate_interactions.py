#!/usr/bin/env python3
"""Replace repeated page-local toast helpers with the shared interaction module."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
APP_DIRS = ("v11_요양보호사앱", "v15_의료진앱")
SHARED_SCRIPT = '<script src="../07_디자인/system/interactions.js"></script>'
SHARED_STYLE = '<link rel="stylesheet" href="../07_디자인/system/interactions.css">'
TOAST_RE = re.compile(
    r"(?ms)^\s*function toast\((?:msg|m)\)\s*\{.*?^\s*\}\s*"
)
DURATION_RE = re.compile(r"setTimeout\(.*?,\s*(\d{4})\s*\)", re.DOTALL)
TOAST_STYLE_RE = re.compile(
    r"(?ms)^\s*\.toast\s*\{[^{}]*\}\s*"
    r"^\s*\.toast\.show\s*\{[^{}]*\}\s*"
)


def add_duration(html: str, duration: str) -> str:
    if duration == "1800" or "data-toast-duration=" in html:
        return html
    return re.sub(
        r"<html(\s[^>]*)?>",
        lambda match: match.group(0)[:-1] + f' data-toast-duration="{duration}">',
        html,
        count=1,
    )


def main() -> None:
    changed = 0
    for app_dir in APP_DIRS:
        for path in (ROOT / app_dir).glob("*.html"):
            html = path.read_text(encoding="utf-8")
            match = TOAST_RE.search(html)
            if not match and SHARED_SCRIPT not in html:
                continue
            if match:
                duration_match = DURATION_RE.search(match.group(0))
                duration = duration_match.group(1) if duration_match else "1800"
                html = TOAST_RE.sub("", html, count=1)
                html = add_duration(html, duration)
            if SHARED_SCRIPT not in html:
                html = html.replace("</head>", f"  {SHARED_SCRIPT}\n</head>", 1)
            if SHARED_STYLE not in html:
                html = html.replace(SHARED_SCRIPT, f"{SHARED_STYLE}\n  {SHARED_SCRIPT}", 1)
            html = re.sub(r"<script>\s*</script>", "", html)
            path.write_text(html, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))
        for pattern in ("*.css", "*.html"):
            for path in (ROOT / app_dir).rglob(pattern):
                if "_archive" in path.parts:
                    continue
                text = path.read_text(encoding="utf-8")
                cleaned = TOAST_STYLE_RE.sub("", text)
                if cleaned != text:
                    path.write_text(cleaned, encoding="utf-8")
    print(f"Replaced {changed} local toast helpers")


if __name__ == "__main__":
    main()
