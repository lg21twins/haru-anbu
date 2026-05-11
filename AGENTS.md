# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 디자인 규칙 (필수)

- **이모지 절대 금지**: 모든 UI(HTML/CSS/JS, 문서 포함)에서 이모지(😊, 🙂, 💊 등) 사용 금지. 아이콘이 필요하면 `iconify-icon`(fluent:* 등)로 통일.
- 적용 범위: v9.5_보호자앱, v10_의료진웹, v11_요양보호사앱, v12_환자앱, v13_온보딩, v14_쇼케이스 전체
- 기존 파일에 이모지가 있으면 수정 시 iconify 아이콘으로 교체할 것

## Project Overview

Antigravity Kit is an AI-powered design intelligence toolkit providing searchable databases of UI styles, color palettes, font pairings, chart types, and UX guidelines. It works as a skill/workflow for AI coding assistants (Codex, Windsurf, Cursor, etc.).

## Search Command

```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

**Domain search:**
- `product` - Product type recommendations (SaaS, e-commerce, portfolio)
- `style` - UI styles (glassmorphism, minimalism, brutalism) + AI prompts and CSS keywords
- `typography` - Font pairings with Google Fonts imports
- `color` - Color palettes by product type
- `landing` - Page structure and CTA strategies
- `chart` - Chart types and library recommendations
- `ux` - Best practices and anti-patterns

**Stack search:**
```bash
python3 src/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>
```
Available stacks: `html-tailwind` (default), `react`, `nextjs`, `astro`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

## Architecture

```
src/ui-ux-pro-max/                # Source of Truth
├── data/                         # Canonical CSV databases
│   ├── products.csv, styles.csv, colors.csv, typography.csv, ...
│   └── stacks/                   # Stack-specific guidelines
├── scripts/
│   ├── search.py                 # CLI entry point
│   ├── core.py                   # BM25 + regex hybrid search engine
│   └── design_system.py          # Design system generation
└── templates/
    ├── base/                     # Base templates (skill-content.md, quick-reference.md)
    └── platforms/                # Platform configs (Codex.json, cursor.json, ...)

cli/                              # CLI installer (uipro-cli on npm)
├── src/
│   ├── commands/init.ts          # Install command with template generation
│   └── utils/template.ts         # Template rendering engine
└── assets/                       # Bundled assets (~564KB)
    ├── data/                     # Copy of src/ui-ux-pro-max/data/
    ├── scripts/                  # Copy of src/ui-ux-pro-max/scripts/
    └── templates/                # Copy of src/ui-ux-pro-max/templates/

.Codex/skills/ui-ux-pro-max/     # Codex skill (symlinks to src/)
.factory/skills/ui-ux-pro-max/   # Droid (Factory) skill (symlinks to src/)
.shared/ui-ux-pro-max/            # Symlink to src/ui-ux-pro-max/
.Codex-plugin/                   # Codex Marketplace publishing
```

The search engine uses BM25 ranking combined with regex matching. Domain auto-detection is available when `--domain` is omitted.

## Sync Rules

**Source of Truth:** `src/ui-ux-pro-max/`

When modifying files:

1. **Data & Scripts** - Edit in `src/ui-ux-pro-max/`:
   - `data/*.csv` and `data/stacks/*.csv`
   - `scripts/*.py`
   - Changes automatically available via symlinks in `.Codex/`, `.factory/`, `.shared/`

2. **Templates** - Edit in `src/ui-ux-pro-max/templates/`:
   - `base/skill-content.md` - Common SKILL.md content
   - `base/quick-reference.md` - Quick reference section (Codex only)
   - `platforms/*.json` - Platform-specific configs

3. **CLI Assets** - Run sync before publishing:
   ```bash
   cp -r src/ui-ux-pro-max/data/* cli/assets/data/
   cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/
   cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/
   ```

4. **Reference Folders** - No manual sync needed. The CLI generates these from templates during `uipro init`.

## Prerequisites

Python 3.x (no external dependencies required)

## Git Workflow

Never push directly to `main`. Always:

1. Create a new branch: `git checkout -b feat/...` or `fix/...`
2. Commit changes
3. Push branch: `git push -u origin <branch>`
4. Create PR: `gh pr create`
