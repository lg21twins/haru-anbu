#!/usr/bin/env python3
"""사업계획서 원고(md) → rhwp 붙여넣기용 HTML 조각.

왜 있는가
---------
rhwp(HWP 편집 확장)는 클립보드 HTML 을 붙여넣으면 글자 크기 · 정렬 · 표 · 셀 배경까지 살린다.
평문으로 붙이면 양식 문단의 15pt · 넓은 자간을 물려받아 10쪽 제한을 넘는다.
그래서 원고를 항목(## 1. ~ ## 5.)별 HTML 로 바꿔 ego-browser 로 붙인다.

규칙 (원고 쪽)
- `## 1. ...` ~ `## 5. ...` : 항목 경계. 제목 줄 자체는 양식에 이미 있으므로 출력하지 않는다.
- `○ 소제목`               : 굵은 소제목 문단
- `- 본문`                 : 들여쓴 본문 문단 (앞에 '-' 유지)
- `| a | b |` 연속 줄       : 표. 첫 줄은 머리줄(배경색), `|---|` 줄은 무시
- `> ...`, 빈 줄, `[확인...]` 이 든 줄 : 출력하지 않는다(제출본에 메모가 새지 않게)

쓰는 법
    python3 tools/md_to_hwp_html.py 원고.md > out.json   # {"1": html, ..., "5": html}
"""
import html
import json
import re
import sys

BODY = "font-size:10pt;line-height:150%;text-align:justify;margin:0"
SUB = "font-size:10.5pt;font-weight:bold;text-align:left;margin:4pt 0 1pt 0"
CELL = "border:1px solid #000;font-size:9pt;padding:1pt 3pt;text-align:left"
HEAD = CELL + ";background:#E8EEF7;font-weight:bold"


def inline(s: str) -> str:
    s = html.escape(s, quote=False)  # rhwp 는 &#x27; 를 풀지 못한다
    return re.sub(r"\*\*(.+?)\*\*", r'<span style="font-weight:bold">\1</span>', s)


def table(rows):
    out = ['<table style="border-collapse:collapse;width:100%">']
    for i, r in enumerate(rows):
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        st = HEAD if i == 0 else CELL
        out.append("<tr>" + "".join(f'<td style="{st}">{inline(c)}</td>' for c in cells) + "</tr>")
    out.append("</table>")
    return "".join(out)


def convert(md: str):
    sections, cur, buf, rows = {}, None, [], []

    def flush_rows():
        if rows:
            buf.append(table(rows))
            rows.clear()

    for line in md.splitlines():
        m = re.match(r"^## ([1-5])\.", line)
        if m:
            flush_rows()
            if cur:
                sections[cur] = "".join(buf)
            cur, buf = m.group(1), []
            continue
        if cur is None:
            continue
        if line.startswith("## ") or line.startswith("---"):
            flush_rows()
            sections[cur] = "".join(buf)
            cur, buf = None, []
            continue
        s = line.strip()
        if s.startswith("|"):
            if not re.match(r"^\|[\s\-:|]+\|$", s):
                rows.append(s)
            continue
        flush_rows()
        if not s or s.startswith(">") or "[확인" in s:
            continue
        if s.startswith("○"):
            buf.append(f'<p style="{SUB}">{inline(s)}</p>')
        elif s.startswith("- "):
            buf.append(f'<p style="{BODY};margin-left:8pt">{inline(s)}</p>')
        else:
            buf.append(f'<p style="{BODY}">{inline(s)}</p>')
    flush_rows()
    if cur:
        sections[cur] = "".join(buf)
    return sections


if __name__ == "__main__":
    src = open(sys.argv[1], encoding="utf-8").read()
    json.dump(convert(src), sys.stdout, ensure_ascii=False)
