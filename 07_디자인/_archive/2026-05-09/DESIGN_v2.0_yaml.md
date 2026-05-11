---
version: v2.0
name: 하루안부 (Haru Anbu)
description: A care-coordination design language for elderly home care. Three role themes (Guardian Blue, Medical Green, Patient Orange) ride on top of one shared glass-morphism chassis — translucent white cards, frosted floating pill tabbar, soft 4-stop role gradients, and Pretendard typography. UI chrome is warm and calm, never clinical; the system reads as "messaging + journal + dashboard," not "hospital chart."

colors:
  guardian: "#2C7AFC"
  guardian-light: "#5B9BFF"
  guardian-dark: "#1E5FD6"
  guardian-soft: "#DBEAFE"
  medical: "#22C55E"
  medical-light: "#4ADE80"
  medical-dark: "#16A34A"
  medical-soft: "#DCFCE7"
  patient: "#FB923C"
  patient-light: "#FDBA74"
  patient-dark: "#EA580C"
  patient-soft: "#FFEDD5"
  point-yellow: "#F5D310"
  success: "#16A34A"
  success-soft: "#DCFCE7"
  warning: "#F59E0B"
  warning-soft: "#FEF3C7"
  danger: "#DC2626"
  danger-soft: "#FEE2E2"
  info: "#2C7AFC"
  info-soft: "#DBEAFE"
  canvas: "#F0F4F8"
  surface: "#FFFFFF"
  surface-muted: "#FAFAFA"
  surface-glass: "rgba(255,255,255,0.80)"
  surface-glass-light: "rgba(255,255,255,0.45)"
  surface-tabbar: "rgba(210,225,250,0.55)"
  overlay-dim: "rgba(0,0,0,0.40)"
  border-subtle: "#E5E5EA"
  border-strong: "#D4D4D8"
  border-glass: "rgba(255,255,255,0.55)"
  border-glass-soft: "rgba(255,255,255,0.45)"
  border-accent-tint: "rgba(44,122,252,0.12)"
  ink: "#1C1C1E"
  ink-secondary: "#8E8E93"
  ink-tertiary: "#9E9E9E"
  ink-disabled: "#D4D4D8"
  on-accent: "#FFFFFF"
  on-dark: "#FFFFFF"

gradients:
  guardian-bg: "linear-gradient(180deg, #d4e4ff 0%, #e8f0fe 40%, #f2f6ff 70%, #EEF3FB 100%)"
  guardian-glow: "radial-gradient(circle, rgba(44,122,252,0.14) 0%, transparent 65%)"
  medical-bg: "linear-gradient(180deg, #DCFCE7 0%, #F0F4F8 120px)"
  patient-bg: "linear-gradient(180deg, #FFEDD5 0%, #F0F4F8 120px)"
  hero-guardian: "linear-gradient(135deg, #2C7AFC 0%, #1E5FD6 100%)"
  hero-medical: "linear-gradient(135deg, #22C55E 0%, #16A34A 100%)"
  hero-patient: "linear-gradient(135deg, #FB923C 0%, #EA580C 100%)"

typography:
  display:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  title:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 22px
    fontWeight: 600
    lineHeight: 1.2
  headline:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 17px
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.4
  body-large:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  callout:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
  caption:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
  mini:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.2
  tabbar-label:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 11px
    fontWeight: 700
    lineHeight: 1.0
  patient-body:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  patient-headline:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.4

rounded:
  none: 0px
  xs: 4px
  sm: 8px
  md: 12px
  card: 14px
  lg: 18px
  xl: 24px
  modal: 28px
  pill: 9999px
  full: 9999px

spacing:
  none: 0px
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 20px
  xxl: 24px
  section: 32px
  block: 48px
  hero: 64px
  page-margin-mobile: 16px
  page-margin-web: 24px

shadows:
  card: "0 1px 4px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.04)"
  card-md: "0 4px 16px rgba(0,0,0,0.08), 0 0 1px rgba(0,0,0,0.04)"
  card-lg: "0 8px 28px rgba(0,0,0,0.12), 0 0 1px rgba(0,0,0,0.04)"
  glass: "0 4px 20px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.35)"
  hero-guardian: "0 8px 28px rgba(44,122,252,0.25)"
  modal-bottom: "0 -4px 30px rgba(0,0,0,0.10)"

blur:
  card: 16px
  tabbar: 20px
  modal: 40px
  header: 12px

motion:
  fast: 150ms
  normal: 250ms
  slow: 350ms
  ease-standard: "cubic-bezier(0.2, 0, 0, 1)"
  ease-emphasize: "cubic-bezier(0.2, 0, 0, 1.2)"

sizes:
  touch-target: 44px
  touch-target-patient: 56px
  button-default: 48px
  button-compact: 44px
  button-large: 56px
  input: 48px
  row: 56px
  row-compact: 44px
  row-patient: 64px
  header: 44px
  header-web: 64px
  tabbar: 56px
  sidebar-web: 240px
  content-max-web: 1280px
  icon-sm: 20px
  icon-md: 24px
  icon-lg: 28px
  icon-xl: 32px
  avatar-sm: 32px
  avatar-md: 40px
  avatar-lg: 56px
  avatar-xl: 72px

components:
  btn-primary:
    backgroundColor: "{colors.guardian}"
    textColor: "{colors.on-accent}"
    typography: "{typography.headline}"
    rounded: "{rounded.card}"
    height: 48px
    padding: 0 20px
  btn-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.headline}"
    rounded: "{rounded.card}"
    border: "1px solid {colors.border-subtle}"
    height: 48px
  btn-destructive:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-accent}"
    typography: "{typography.headline}"
    rounded: "{rounded.card}"
    height: 48px
  btn-ghost:
    backgroundColor: transparent
    textColor: "{colors.guardian}"
    typography: "{typography.headline}"
    rounded: "{rounded.card}"
  btn-pill-mode:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.callout}"
    rounded: "{rounded.pill}"
    border: "1px solid {colors.border-subtle}"
    padding: 6px 16px
  btn-pill-mode-active:
    backgroundColor: "{colors.guardian}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.pill}"
    padding: 6px 16px
  card-glass:
    backgroundColor: "{colors.surface-glass}"
    backdropBlur: "{blur.card}"
    border: "1px solid {colors.border-glass}"
    rounded: "{rounded.lg}"
    shadow: "{shadows.glass}"
    padding: 18px
  card-flat:
    backgroundColor: "{colors.surface}"
    border: "1px solid {colors.border-subtle}"
    rounded: "{rounded.card}"
    shadow: "{shadows.card}"
    padding: 16px
  card-row:
    backgroundColor: "{colors.surface-glass}"
    backdropBlur: "{blur.card}"
    border: "1px solid {colors.border-glass}"
    rounded: "{rounded.card}"
    height: 56px
  card-hero-guardian:
    backgroundColor: "{gradients.hero-guardian}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.xl}"
    shadow: "{shadows.hero-guardian}"
    padding: 24px
  card-emphasis-accent:
    backgroundColor: "{colors.surface-glass}"
    backdropBlur: "{blur.card}"
    border: "1px solid {colors.border-accent-tint}"
    rounded: "{rounded.lg}"
    shadow: "{shadows.glass}"
    padding: 18px
  bottom-sheet:
    backgroundColor: "rgba(255,255,255,0.97)"
    backdropBlur: "{blur.modal}"
    rounded: "28px 28px 0 0"
    shadow: "{shadows.modal-bottom}"
    padding: 24px
  modal-overlay:
    backgroundColor: "{colors.overlay-dim}"
  header-mobile:
    backgroundColor: transparent
    backdropBlur: "{blur.header}"
    height: 44px
    padding: 0 16px
  header-web:
    backgroundColor: "{colors.surface}"
    height: 64px
    padding: 0 24px
    border: "1px solid {colors.border-subtle}"
  tabbar-floating-pill:
    backgroundColor: "{colors.surface-tabbar}"
    backdropBlur: "{blur.tabbar}"
    border: "1px solid {colors.border-glass-soft}"
    rounded: "{rounded.pill}"
    shadow: "{shadows.glass}"
    height: 56px
    sideInset: 16px
    bottomOffset: "calc(16px + env(safe-area-inset-bottom))"
    iconSize: 24px
    labelTypography: "{typography.tabbar-label}"
    activeColor: "{colors.guardian}"
    inactiveColor: "rgba(28,28,30,0.45)"
  fab-ai:
    backgroundColor: "{gradients.hero-guardian}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.full}"
    shadow: "{shadows.hero-guardian}"
    size: 56px
  badge-status:
    rounded: "{rounded.pill}"
    typography: "{typography.mini}"
    padding: 2px 8px
  badge-success:
    backgroundColor: "{colors.success-soft}"
    textColor: "#15803D"
  badge-warning:
    backgroundColor: "{colors.warning-soft}"
    textColor: "#B45309"
  badge-danger:
    backgroundColor: "{colors.danger-soft}"
    textColor: "{colors.danger}"
  badge-info:
    backgroundColor: "{colors.info-soft}"
    textColor: "{colors.info}"
  input-text:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.callout}"
    rounded: "{rounded.sm}"
    border: "1px solid {colors.border-subtle}"
    height: 48px
    padding: 0 16px
  input-text-focus:
    border: "1px solid {colors.guardian}"
    rounded: "{rounded.sm}"
  toast:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.callout}"
    rounded: "{rounded.pill}"
    padding: 12px 20px
  sos-banner:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-dark}"
    rounded: "{rounded.card}"
    padding: 16px
  timeline-dot:
    backgroundColor: "{colors.guardian}"
    rounded: "{rounded.full}"
    size: 10px
  timeline-line:
    backgroundColor: "{colors.border-subtle}"
    width: 2px
---

## Overview

하루안부 is a multi-role care-coordination platform — guardians track an elderly parent's day, medical staff oversee patients in a clinical workspace, caregivers run a field-mobile checklist, and patients themselves get a simplified, large-text companion. The design language is built around **one chassis, three role themes**.

The chassis is glass-morphism over a soft role gradient: translucent white cards (`rgba(255,255,255,0.80)` with `backdrop-filter: blur(16px)`) sit on a 4-stop role-tinted background, separated by a frosted-glass hairline rather than a hard border. The signature surface is the **floating pill tabbar** — a 56px-tall pill that floats 16px above the safe area, never edge-to-edge, with five icon+label tabs and the AI FAB perched as a separate circular button to the side.

Color is role-driven through a single `--color-accent` semantic anchor. The same component definitions render Guardian Blue (`#2C7AFC`), Medical Green (`#22C55E`), or Patient Orange (`#FB923C`) depending on `data-role` on the `<html>` root. There is no second brand color per role — every CTA, every active tab, every focus ring is the role's accent. A single warm yellow (`#F5D310`) plays the rare "point" role for stars and important badges.

Typography is **Pretendard Variable** at every size, with a quiet 8-step ladder. Body sits at 16px, headlines at 17px / 600, display at 32px / 600. The patient role automatically upshifts to 18px body / 56px touch targets for senior-friendly readability — this is a token override, not a separate stylesheet.

**Key Characteristics:**
- Three-theme one-chassis model — `data-role` swaps `{colors.guardian}` ↔ `{colors.medical}` ↔ `{colors.patient}` while components stay structurally identical.
- Glass-morphism cards as the dominant surface — translucent white, blur, frosted hairline border. Hard white cards are the exception, not the rule.
- Floating pill tabbar — never full-bleed; always 16px from screen edges, with the AI FAB as a separate orbital satellite.
- 4-stop role gradient page background with a soft radial glow overlay (Guardian only).
- Single role accent for every interactive element — no secondary brand color per role.
- Pretendard Variable across all sizes; weight ladder is 400 / 500 / 600 / 700 (no 300, no 800).
- Filled Fluent icons only (`fluent:*-{16,20,24,28}-filled`) — line/outline mixing is forbidden.
- Patient role auto-upshifts type sizes and touch targets via token override — no separate component code.
- 4px spacing grid; structural padding snaps to 8/12/16/20/24.
- Soft, warm shadows only — `rgba(0,0,0,0.06–0.12)`. Never the harsh elevation of a clinical chart.

## Colors

> **Source files analyzed:** `07_디자인/tokens/tokens.css`, `v11_보호자앱/common.css`, `v11_보호자앱/g-guardian-live.html`, `v10_의료진웹/의료진_대시보드_v9.5.html`, `v12_환자앱/patient.css`. Color is identical in structure across all roles; only the accent layer changes.

### Role Accent (the one anchor)

The semantic token `--color-accent` is the single anchor that the role theme overrides. Every role-specific surface — primary button, active tab, focus ring, hero-card gradient, info badge — reads from this anchor.

- **Guardian Blue** (`{colors.guardian}` — #2C7AFC): The Haru Anbu logo color and the default. iOS-style deep blue, used on the boyhood/familial side of the product (보호자앱). Light variant `{colors.guardian-light}` (#5B9BFF) for hover-equivalent emphasis, dark `{colors.guardian-dark}` (#1E5FD6) for press, soft `{colors.guardian-soft}` (#DBEAFE) for info-badge fills and gradient bg starts.
- **Medical Green** (`{colors.medical}` — #22C55E): Tailwind green-500. Shared across doctor, nurse, and caregiver roles (`data-role="doctor"|"nurse"|"caregiver"|"medical"` all resolve here). Reads as "care/clinical-clean" without the harshness of teal or pure cyan. Strong variant `{colors.medical-dark}` (#16A34A) is also the success semantic.
- **Patient Orange** (`{colors.patient}` — #FB923C): Warm orange (Tailwind orange-400). Chosen specifically to feel "warm and welcoming" rather than alarming — patients are elderly, and the role aims for a companion-not-clinic feel.
- **Point Yellow** (`{colors.point-yellow}` — #F5D310): The single role-independent "point" color. Reserved for star ratings, achievement badges, and the rare moment when a non-accent emphasis is required.

### Semantic Status

- **Success** (`{colors.success}` — #16A34A on `{colors.success-soft}` rgba(34,197,94,0.12)): Checklist completion, "정상" status, completed medication.
- **Warning** (`{colors.warning}` — #F59E0B on `{colors.warning-soft}`): Pending action, "주의" needed, not-yet-done items.
- **Danger** (`{colors.danger}` — #DC2626 on `{colors.danger-soft}`): SOS, emergency banners, destructive button fills.
- **Info** (`{colors.info}` — #2C7AFC on `{colors.info-soft}`): Aliased to the Guardian Blue accent. Even on Medical or Patient screens, info status reads in the role's accent — the alias swaps automatically.

### Surface

- **Canvas** (`{colors.canvas}` — #F0F4F8): The cool blue-gray app background. Sits behind the role gradient on most screens; appears alone on inputs and muted utility surfaces.
- **Surface** (`{colors.surface}` — #FFFFFF): Pure white. Used for hard-card variants and as a fallback when glass blur isn't available.
- **Surface Muted** (`{colors.surface-muted}` — #FAFAFA): Lower-emphasis card fill, off-white but still cleaner than the canvas.
- **Surface Glass** (`{colors.surface-glass}` — rgba(255,255,255,0.80)): The signature card fill. Always paired with `backdrop-filter: blur(16px)` and the frosted-hairline border.
- **Surface Tabbar** (`{colors.surface-tabbar}` — rgba(210,225,250,0.55)): The deep-blue-tinted glass specifically for the floating pill tabbar. Subtly different from the card glass — the tab bar reads as a distinct floating surface, not just another card.
- **Overlay Dim** (`{colors.overlay-dim}` — rgba(0,0,0,0.40)): Modal backdrop fill.

### Text

- **Ink** (`{colors.ink}` — #1C1C1E): Primary text. Near-black, not pure black — keeps the warm tone consistent with the soft glass surfaces. Used on every body line, every headline, every list-row title.
- **Ink Secondary** (`{colors.ink-secondary}` — #8E8E93): Captions, timestamps, supporting metadata.
- **Ink Tertiary** (`{colors.ink-tertiary}` — #9E9E9E): Disabled text, placeholder hints.
- **On-Accent** (`{colors.on-accent}` — #FFFFFF): Text on Guardian Blue, Medical Green, Patient Orange surfaces — and on the danger/SOS banner. Always pure white.

### Borders & Hairlines

- **Border Subtle** (`{colors.border-subtle}` — #E5E5EA): The default 1px hairline — input fields, flat cards, list dividers.
- **Border Strong** (`{colors.border-strong}` — #D4D4D8): Used sparingly when a card needs more definition (rare; the system prefers shadow + glass over hard borders).
- **Border Glass** (`{colors.border-glass}` — rgba(255,255,255,0.55)): The signature frosted-highlight border on glass cards — a 1px line that catches light at the top edge and dissolves at the bottom.
- **Border Glass Soft** (`{colors.border-glass-soft}` — rgba(255,255,255,0.45)): A slightly weaker version used on the tabbar and FAB so they sit just behind the cards in the optical hierarchy.
- **Border Accent Tint** (`{colors.border-accent-tint}` — rgba(44,122,252,0.12)): The "this card is special" border — applied to AI cards, SOS preview cards, and emphasis surfaces. The tint hue is the role accent, not always blue.

### Role Gradients

Each role page background is a 4-stop linear gradient (Guardian) or 2-stop linear (Medical, Patient) that fades from the soft-tinted top down into the canvas.

| Role | Gradient |
|---|---|
| Guardian | `{gradients.guardian-bg}` — `linear-gradient(180deg, #d4e4ff 0%, #e8f0fe 40%, #f2f6ff 70%, #EEF3FB 100%)` |
| Medical | `{gradients.medical-bg}` — `linear-gradient(180deg, #DCFCE7 0%, #F0F4F8 120px)` |
| Patient | `{gradients.patient-bg}` — `linear-gradient(180deg, #FFEDD5 0%, #F0F4F8 120px)` |

The Guardian gradient additionally carries a soft radial glow (`{gradients.guardian-glow}`) at `blur(30px)` over the upper region — this is the only role with a depth glow, and it's what gives the Guardian app its distinct "atmospheric" feel relative to the flatter Medical and Patient surfaces.

### Hero Surfaces

When a card needs to read as a feature/CTA hero (today's care summary, AI report cover, SOS banner emphasis), it shifts to a 135° accent gradient.

| Role | Hero gradient |
|---|---|
| Guardian | `{gradients.hero-guardian}` — `linear-gradient(135deg, #2C7AFC, #1E5FD6)` |
| Medical | `{gradients.hero-medical}` — `linear-gradient(135deg, #22C55E, #16A34A)` |
| Patient | `{gradients.hero-patient}` — `linear-gradient(135deg, #FB923C, #EA580C)` |

These are paired with `{shadows.hero-guardian}` (or the role equivalent) — a colored drop shadow at 25% opacity that gives the hero card visible weight against the page gradient.

## Typography

### Font Family

- **Base**: `Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'Segoe UI', Roboto, sans-serif`. Pretendard is the entire UI — display, body, captions, button labels. Loaded via the orioncactus CDN as a variable font; weight is selected per token, not per file.
- **Mono**: `ui-monospace, 'SF Mono', Menlo, Consolas, monospace` — only for code blocks and timestamp grids in dev/debug surfaces.

### Hierarchy

| Token | Size | Weight | Line Height | Use |
|---|---|---|---|---|
| `{typography.display}` | 32px | 600 | 1.2 | Screen-level hero ("오늘 어머님은…", big numbers) |
| `{typography.title}` | 22px | 600 | 1.2 | Section headers, modal headers |
| `{typography.headline}` | 17px | 600 | 1.4 | Card titles, list-row titles, button labels |
| `{typography.body}` | 16px | 400 | 1.4 | Default paragraph and form body |
| `{typography.body-large}` | 18px | 400 | 1.6 | Patient app body (1.6 leading for senior readability) |
| `{typography.callout}` | 14px | 400 | 1.4 | Subtitles, supporting copy, input-field text |
| `{typography.caption}` | 13px | 400 | 1.4 | Timestamps, metadata captions |
| `{typography.mini}` | 11px | 400 | 1.2 | Status badges, micro-labels |
| `{typography.tabbar-label}` | 11px | 700 | 1.0 | Floating pill tabbar labels (the rare 700 weight) |
| `{typography.patient-body}` | 18px | 400 | 1.6 | Patient role override of `{typography.body}` |
| `{typography.patient-headline}` | 20px | 600 | 1.4 | Patient role override of `{typography.headline}` |

### Principles

- **Pretendard at every size, no exceptions.** No display/text variant split — the Pretendard variable file handles the full ladder, and the line-height scale (1.2 / 1.4 / 1.6) is what shapes the reading rhythm.
- **Weight ladder: 400 / 500 / 600 / 700.** Body is 400. Mid-emphasis is 500 (rare; used for sub-headings inside dense lists). Headlines are 600. The tabbar label is 700 — a deliberate burst of weight at the smallest tappable label, so the active state can carry color contrast even at 11px.
- **Patient role overrides body up.** When `data-role="patient"`, `--text-body` resolves to 18px and `--text-headline` to 20px automatically. Component code never branches on role; it just reads the semantic token.
- **Line-height carries the role.** Guardian and Medical: 1.4 body. Patient: 1.6 body. The looser leading on Patient is part of the senior-readability budget alongside the size bump.
- **No display-tight tracking.** Unlike Apple's negative letter-spacing convention, Pretendard is rendered at default tracking. Korean glyph balance suffers under negative tracking, and the brand voice is "warm reading," not "cinematic statement."
- **Weight 300 is forbidden.** The variable font supports it, but the system does not. Korean characters at weight 300 read as ghosted on glass surfaces; the floor is 400.

### Note on Font Substitutes

Pretendard is open-source and CDN-delivered (the variable subset is ~150KB gzipped). When unavailable:

- The fallback chain (`-apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'Segoe UI'`) renders the system Korean face on most platforms — Apple SD Gothic Neo on iOS/macOS, Yu Gothic / Malgun Gothic on Windows. These are visually close to Pretendard but slightly heavier at 600.
- Pretendard's distinguishing trait is its **Korean numeral balance** at body sizes — Apple SD Gothic Neo runs slightly narrower numerals. When using the fallback, reduce `letter-spacing` on display sizes by `-0.005em` to match Pretendard's default cadence.
- For non-Korean contexts (English-only UI like the developer console), `Inter` is a reasonable Latin-only substitute, but the production app is Korean-first and Pretendard is the canonical voice.

## Layout

### Spacing System

- **Base unit:** 4px. The full ladder snaps to 4-multiples; 2px (`{spacing.xxs}`) exists only for inline icon padding adjustments.
- **Tokens:** `{spacing.xxs}` 2px · `{spacing.xs}` 4px · `{spacing.sm}` 8px · `{spacing.md}` 12px · `{spacing.lg}` 16px · `{spacing.xl}` 20px · `{spacing.xxl}` 24px · `{spacing.section}` 32px · `{spacing.block}` 48px · `{spacing.hero}` 64px.
- **Page margin:** `{spacing.page-margin-mobile}` (16px) on mobile, `{spacing.page-margin-web}` (24px) on web. The token resolves automatically through `data-platform`.
- **Card inset:** Default 16px (`{spacing.lg}`), loose 24px (`{spacing.xxl}`) for hero cards, compact 8px (`{spacing.sm}`) for chip-style mini-cards.
- **Stack rhythm:** 12px between sibling list rows, 24px between cards, 32px between sections, 48px between major blocks.

### Grid & Container

- **Mobile (Guardian/Patient/Caregiver):** Single-column. Page margin 16px each side. Cards are full-width minus margins. Tabbar floats with 16px side inset, 16px + safe-area bottom offset.
- **Web (Medical):** 240px sidebar + flexible content area. Content max-width 1280px. Cards arrange in 2–3 column grids on dashboard surfaces with 20px gutters.
- **Floating pill geometry:** The tabbar is **never edge-to-edge**. Side inset is 16px on both sides; the pill rounds at `{rounded.pill}`. This is the most identifiable layout signature.

### Whitespace Philosophy

Whitespace breathes between glass cards rather than around them. Cards sit close to each other (12px stack) so the page reads as a "messaging timeline of care events," but each card has internal generous padding (16–24px) to give content room. The floating pill tabbar enforces a 56px+ no-content zone at the bottom of every screen — content scrolls beneath the pill, blurred by the tabbar's backdrop-filter.

The Patient role expands the spacing scale silently: row heights become 64px (vs 56px), button heights become 56px (vs 48px), touch targets become 56px (vs 44px). Component code is unchanged; the platform/role tokens override the size scale.

## Elevation & Depth

| Level | Treatment | Use |
|---|---|---|
| Flat | No shadow, no border | Inline copy, body text, hairline-divided list rows |
| Card | `{shadows.card}` — `0 1px 4px rgba(0,0,0,0.06)` | Default flat-white cards |
| Card MD | `{shadows.card-md}` — `0 4px 16px rgba(0,0,0,0.08)` | Important cards, button groups |
| Card LG | `{shadows.card-lg}` — `0 8px 28px rgba(0,0,0,0.12)` | Hero/feature cards, modals |
| Glass | `{shadows.glass}` — `0 4px 20px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.35)` | Tabbar, FAB, glass-style hero buttons (the inset highlight is the frosted-glass shimmer) |
| Hero accent | `{shadows.hero-guardian}` — `0 8px 28px rgba(44,122,252,0.25)` | Hero gradient cards (color-tinted at 25% alpha) |
| Modal-bottom | `{shadows.modal-bottom}` — `0 -4px 30px rgba(0,0,0,0.10)` | Bottom sheets (shadow points up) |

**Shadow philosophy.** Shadows are warm and subtle — `rgba(0,0,0,0.06–0.12)`, never `0.20+`. The system deliberately avoids the hard, multi-layer shadows of a clinical EMR or a finance app, because the brand voice is "family messaging," not "hospital chart." The one bold shadow is the **hero accent shadow** (`{shadows.hero-guardian}` and role variants) — a tinted shadow that gives the gradient hero card visible color-bloom on the page.

### Decorative Depth

- **Backdrop-filter blur** on glass cards (16px), tabbar (20px), modal sheets (40px), and headers (12px) creates layered depth without shadow weight.
- **Inset highlight** on glass shadow (`inset 0 1px 0 rgba(255,255,255,0.35)`) catches light at the top edge of pills and FABs — a 1px frosted shimmer that signals "this is glass, not paint."
- **Role gradient + radial glow** (Guardian only) supplies atmospheric depth at the page level — the rest is built up from the cards.
- **No decorative gradients on cards.** Card fills are flat translucent white. Gradient is reserved for hero CTAs and the page background.

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.none}` | 0px | Full-bleed images, dividers |
| `{rounded.xs}` | 4px | Small tags, micro-badges |
| `{rounded.sm}` | 8px | Inputs, chips, small badges |
| `{rounded.md}` | 12px | Inline cards, secondary surfaces |
| `{rounded.card}` | 14px | Default card, default button — the brand's primary radius |
| `{rounded.lg}` | 18px | Glass cards, modals |
| `{rounded.xl}` | 24px | Hero cards, feature surfaces |
| `{rounded.modal}` | 28px | Bottom sheets (top corners only) |
| `{rounded.pill}` | 9999px | Floating tabbar, status badges, mode chips, FAB |

### Photography & Illustration Geometry

- **Avatar imagery**: Circular (`{rounded.full}`) at 32 / 40 / 56 / 72px scales. Used for family chat senders, patient profile, caregiver avatar.
- **Brand character (`하루안부캐릭터.png`)**: A friendly mascot illustration. Always presented on a clean white or canvas surface, never inside a glass card — the character carries its own color story.
- **No rounded photography on hero cards** — hero cards are gradient-fill, no imagery.
- **Iconography only, no stock photography.** The brand voice is illustrative and warm; raster photography would clash with the glass-flat-tone visual register.

## Components

### Top Navigation

**`header-mobile`** — Sticky, transparent header with `backdrop-filter: blur(12px)` over the role gradient. Height 44px. Three-region layout: left action (back arrow or icon), centered title in `{typography.headline}`, right action (notifications, search). The transparent fill means the page gradient bleeds through, keeping the header optically connected to the rest of the screen.

**`header-web`** — 64px tall, white surface, 1px hairline bottom. Used on the medical desktop dashboard. Holds the role logo, search input, notification bell, and user avatar dropdown right-aligned. Pairs with the `{component.sidebar-web}` 240px navigation.

**`tabbar-floating-pill`** — The signature surface. A pill-shaped floating bar that sits 16px above the safe-area bottom and 16px in from each side. Background `{colors.surface-tabbar}` (deep-blue-tinted glass at 55% alpha) with `backdrop-filter: blur(20px)`. Border `{colors.border-glass-soft}`, shadow `{shadows.glass}` (with the inset-top highlight). Five tabs: 홈 / 가이드 / 소통 / 기록 / 마이. Each tab is a column-stack: `fluent:*-24-filled` icon at 24px above an 11px / 700 label. Active tab uses the role accent color; inactive is `rgba(28,28,30,0.45)`. The AI FAB sits as a separate 56px circular button to the right of the tabbar — physically detached, optically related.

### Buttons

**`btn-primary`** — The primary CTA. Background `{colors.guardian}` (or role accent), text `{colors.on-accent}`, typography `{typography.headline}` (17px / 600), rounded `{rounded.card}` (14px), height 48px, padding 0 20px.
- Active state: `transform: scale(0.98)` + `opacity: 0.8` over 150ms.
- Disabled state: `opacity: 0.4`, no transform.

**`btn-secondary`** — Companion to primary when two CTAs sit together. Background `{colors.surface}`, text `{colors.ink}`, 1px solid `{colors.border-subtle}`, same height and radius as primary.

**`btn-destructive`** — Background `{colors.danger}` (#DC2626), text white. Reserved for delete, remove, "위험 액션." Used sparingly — never as a default CTA.

**`btn-ghost`** — Background transparent, text `{colors.guardian}` (or role accent), no border. Inline link-style action embedded in body copy.

**`btn-pill-mode`** — Filter / mode chip. Background `{colors.surface}` + 1px border, text `{colors.ink}` in `{typography.callout}`, rounded `{rounded.pill}`, padding 6px × 16px. Selected state (`{component.btn-pill-mode-active}`) flips to `{colors.guardian}` background with white text.

### Cards & Containers

**`card-glass`** — The default card. Background `{colors.surface-glass}` (rgba(255,255,255,0.80)) with `backdrop-filter: blur(16px)`, 1px solid `{colors.border-glass}` (the frosted highlight border), rounded `{rounded.lg}` (18px), shadow `{shadows.glass}`, padding 18px. This is what most cards look like in the system — every guardian dashboard card, every list row container, every settings group.

**`card-flat`** — Hard-card variant. Background `{colors.surface}` (pure white), 1px solid `{colors.border-subtle}`, rounded `{rounded.card}` (14px), shadow `{shadows.card}`, padding 16px. Used when the card sits over a busy background image, or when the screen needs a "documents-on-paper" feel rather than the floating glass register.

**`card-row`** — A glass card sized as a list row. Same fill and border as `{component.card-glass}` but `{rounded.card}` (14px) and 56px height. Stacks tightly with 12px spacing between rows to create a card-list rhythm.

**`card-hero-guardian`** — The accent-gradient hero card. Background `{gradients.hero-guardian}` (135° blue gradient), text white, rounded `{rounded.xl}` (24px), shadow `{shadows.hero-guardian}` (color-tinted 25% drop). Used on home screens for the day's primary care summary and on AI-report covers. Role variants `card-hero-medical` and `card-hero-patient` swap the gradient and shadow tint.

**`card-emphasis-accent`** — A glass card with the role-tinted border instead of the default frosted-white border. Used for AI-suggestion cards, the SOS preview, and other "this card is special" moments. Same fill, blur, shadow, and radius as `{component.card-glass}`; only the border tint changes.

**`bottom-sheet`** — Modal sheet anchored to the bottom edge. Background `rgba(255,255,255,0.97)` with `backdrop-filter: blur(40px)`, rounded 28px on top corners only, shadow `{shadows.modal-bottom}` (points up: `0 -4px 30px`), padding 24px. Slides up from below over a `{component.modal-overlay}` dim.

**`sos-banner`** — Background `{colors.danger}`, text white, rounded `{rounded.card}`, padding 16px. Always lives at the top of the screen when triggered, never inside another card. Uses `fluent:siren-24-filled` as the leading icon.

### Inputs & Forms

**`input-text`** — Background `{colors.canvas}` (the page-canvas color, slightly cooler than white), text `{colors.ink}` in `{typography.callout}` (14px), 1px solid `{colors.border-subtle}`, rounded `{rounded.sm}` (8px), height 48px, padding 0 16px.
- Focus state: border switches to `{colors.guardian}` (or role accent). No box-shadow; the border color change carries the focus signal.
- Error state: border switches to `{colors.danger}`; helper text below in `{typography.caption}` `{colors.danger}`.
- Disabled state: `opacity: 0.5`, cursor not-allowed.

**Search input variant** — Same as `{component.input-text}` but with a leading `fluent:search-24-filled` icon at 20px and `{rounded.pill}` corner radius. Used in the medical patient-list search and the chat search.

### Badges, Chips & Labels

**`badge-status`** — Pill-shaped status indicator. `{rounded.pill}`, padding 2px × 8px, typography `{typography.mini}` (11px / 400). Four flavors:

| Flavor | Background | Text |
|---|---|---|
| Success | `{colors.success-soft}` (#DCFCE7) | #15803D |
| Warning | `{colors.warning-soft}` (#FEF3C7) | #B45309 |
| Danger | `{colors.danger-soft}` (#FEE2E2) | #DC2626 |
| Info | `{colors.info-soft}` (#DBEAFE) | #2C7AFC |

**Mode chip** — Filter selector. See `{component.btn-pill-mode}` and `{component.btn-pill-mode-active}` above. Used in record-filter rows, message-mode toggles, and care-category pickers.

### Toast & Alerts

**`toast`** — Background `{colors.ink}` (dark, #1C1C1E), text white in `{typography.callout}`, rounded `{rounded.pill}`, padding 12px × 20px. Position: `fixed`, bottom 100px (above the floating tabbar). Animation: `translateY(20px) → 0` over 250ms; auto-dismiss after 2.5s.

### Floating Action Button

**`fab-ai`** — The orbital AI button next to the floating tabbar. 56 × 56px circular, background `{gradients.hero-guardian}` (or role gradient), shadow `{shadows.hero-guardian}` (tinted), icon `fluent:sparkle-24-filled` in white at 24px. Tap opens the AI assistant chat as a `{component.bottom-sheet}`.

### Timeline

**`timeline-dot`** + **`timeline-line`** — A vertical event-stream pattern used on the day-record screens. A 2px solid `{colors.border-subtle}` vertical line runs the height of the timeline; 10px circular dots in the role accent color punctuate each event. Each event card sits to the right of its dot, separated by 12px.

### Footer

The mobile apps have **no footer** — the floating pill tabbar is the only persistent bottom chrome. The web (medical) dashboard has a minimal legal footer: 32px tall, `{colors.canvas}` fill, `{typography.caption}` text in `{colors.ink-secondary}`, copyright + privacy + terms links separated by 12px middle dots.

## Iconography

### Library

- **Microsoft Fluent Icons (Filled)** via Iconify CDN. Format: `<iconify-icon icon="fluent:{name}-{size}-filled">`.
- **Single style only.** Filled, never line/outline. Mixing line and filled is forbidden — the visual rhythm depends on consistent icon weight.
- **Variant size families:** `-16-filled`, `-20-filled`, `-24-filled`, `-28-filled`. The variant choice affects optical detail; the rendered size is controlled separately via CSS `font-size`.

### Size Rules

| Context | Variant | Render |
|---|---|---|
| Tabbar (mobile) | `-24-filled` | 24px |
| Header / primary buttons | `-24-filled` | 24px |
| Web sidebar | `-24-filled` | 24px |
| Inline list-row | `-20-filled` or `-24-filled` | 20px |
| Status chips, micro badges | `-16-filled` | 16px |
| Hero / empty-state | `-28-filled` or larger | 28–48px |

### Reference Set

| Use | Icon |
|---|---|
| Home (tab) | `fluent:home-24-filled` |
| Care guide (tab) | `fluent:clipboard-task-list-ltr-24-filled` |
| Chat / messaging (tab) | `fluent:chat-24-filled` |
| Records (tab) | `fluent:document-text-24-filled` |
| Profile (tab) | `fluent:person-24-filled` |
| Notification | `fluent:alert-24-filled` |
| Medication | `fluent:pill-24-filled` |
| Meal | `fluent:food-24-filled` |
| Heart / vitals | `fluent:heart-pulse-24-filled` |
| Activity | `fluent:accessibility-24-filled` |
| AI / sparkle | `fluent:sparkle-24-filled` |
| Send | `fluent:send-24-filled` |
| Emergency / SOS | `fluent:siren-24-filled` |

## Do's and Don'ts

### Do

- Use `--color-accent` (resolved through `data-role`) for every interactive element — primary CTA, active tab, focus ring, info badge, link text. Don't hardcode `#2C7AFC` in component code.
- Set glass cards as the default surface (`{component.card-glass}`). Use the flat `{component.card-flat}` only when blur isn't supported or the card sits over a busy image.
- Reserve the floating pill tabbar geometry (16px side inset, 56px height, `{rounded.pill}`) — never let the tabbar go edge-to-edge or full-bleed.
- Apply the AI FAB as a **separate** circular button beside the tabbar. The pill stays a 5-tab pill; the FAB is its own orbital satellite.
- Run body copy at 16px on Guardian/Medical and 18px on Patient — but read this from `--text-body`, never hardcode.
- Use `transform: scale(0.98)` + `opacity: 0.8` over 150ms as the universal button press feedback.
- Pair Fluent filled icons at the size mapped to context (24px tab/header, 20px inline, 16px chip).
- Soft warm shadows only (`rgba(0,0,0,0.06–0.12)`). The brand reads as "family messaging," not "clinical chart."
- Use the role accent's hero gradient (`{gradients.hero-guardian}` and friends) for hero CTA cards; pair with the role's tinted shadow.

### Don't

- Don't introduce a second brand color per role. Each role has exactly one accent — every "click me" goes through it.
- Don't mix Fluent filled with line/outline icons (`fluent:*-regular`, `ph:*`, `tabler:*`, `material-symbols:*`). Filled-only is non-negotiable.
- Don't use weight 300 on Korean text — the floor is 400. The variable font supports it; the system does not.
- Don't apply harsh shadows (`rgba(0,0,0,0.20)` or above). The brand voice is warm; clinical-chart elevation breaks the register.
- Don't put the floating tabbar edge-to-edge. The 16px side inset and pill rounding are the most identifiable signature.
- Don't wrap the brand mascot inside a glass card — it lives on a clean white or canvas surface.
- Don't branch component code on `data-role`. All role variation flows through token override (`--color-accent`, `--text-body`, `--size-touch-target`).
- Don't override patient text sizes back down inside Patient screens — the upshift is the role's accessibility budget. If a screen feels cramped, reduce content density, not the type scale.
- Don't add gradients to card fills. Gradient is reserved for the page background and hero cards.

## Responsive Behavior

### Breakpoints

| Name | Width | Key Changes |
|---|---|---|
| Phone (Patient) | ≤ 414px | Single-column; tabbar 16px inset; type at `{typography.patient-body}` (18px) |
| Phone (Guardian/Caregiver) | ≤ 414px | Single-column; tabbar 16px inset; type at `{typography.body}` (16px) |
| Phablet | 415–767px | Same as phone; cards may run 2-column on rare wide layouts |
| Tablet | 768–1023px | Mobile apps render as-is (centered with side gutters); web dashboard collapses sidebar |
| Small desktop (Web) | 1024–1279px | Medical web sidebar at 240px; content area flexible up to 1280px max |
| Desktop (Web) | ≥ 1280px | Content locks at 1280px; extra width becomes margin |

The mobile apps (Guardian, Patient, Caregiver) are **PWA-first** — they install to the home screen and target single-portrait phone layouts. The web app (Medical) is **desktop-first** — its layouts assume mouse precision, sidebar navigation, and dashboard density.

### Touch Targets

- **Mobile default:** 44 × 44px minimum (iOS HIG).
- **Patient role:** 56 × 56px minimum. Buttons render at `{sizes.button-large}` (56px) and rows at `{sizes.row-patient}` (64px) automatically through the `[data-role="patient"]` token override.
- **Web (mouse):** 36 × 36px minimum — `{sizes.touch-target}` resolves down to 36 under `[data-platform="web"]`.

### Collapsing Strategy

- **Tabbar (mobile):** Stays floating-pill across all phone widths. Side inset stays 16px; tabs compress label spacing rather than dropping labels.
- **Web sidebar:** 240px expanded → 64px icon-only at < 1024px → drawer-overlay at < 768px.
- **Cards:** Single-column on mobile; 2–3 column grid on web ≥ 1024px with 20px gutters.
- **Type scale:** Patient role overrides body and headline sizes globally; no further breakpoint scaling. Guardian/Medical/Caregiver keep one size scale across all widths.

### Image Behavior

- Product app uses no stock photography. The mascot illustration scales fluidly via `max-width: 100%`.
- Avatar images use `srcset` with 1x/2x/3x for retina; lazy-loaded except for the above-fold profile.
- Icon assets are SVG via Iconify — fully resolution-independent.

## Iteration Guide

1. Focus on ONE component at a time. Reference its YAML key directly (`{component.card-glass}`, `{component.tabbar-floating-pill}`).
2. Variants of an existing component (`-active`, `-focus`, role gradients) live as separate entries in `components:`.
3. Use `{token.refs}` everywhere — never inline hex. Role accent in particular: always `{colors.guardian}` etc, never `#2C7AFC`.
4. Never document hover. Default and Active/Pressed states only — these are touch-first products.
5. The radius ladder is `{rounded.sm}` 8px (chips/inputs), `{rounded.card}` 14px (default), `{rounded.lg}` 18px (glass cards), `{rounded.xl}` 24px (hero), `{rounded.modal}` 28px (sheets), `{rounded.pill}` (tabbar/badges/FAB). Don't mix in-between values.
6. The floating pill tabbar geometry is unbreakable: 16px side inset, 56px height, `{rounded.pill}`, AI FAB orbital.
7. Glass surfaces always carry the inset-top highlight in their shadow (`{shadows.glass}`) — that 1px frosted shimmer is what makes the glass register read.
8. Role variation flows through `data-role` token override. Component code stays role-agnostic.
9. When in doubt about emphasis: lift to `{component.card-emphasis-accent}` (role-tinted border) before reaching for a hero gradient.

## Known Gaps

- **Dark mode** is not yet defined. The system is daytime-light only; a dark-mode counterpart for glass surfaces (translucent black? deep navy?) is an open design question.
- **Form validation states** are partially documented (focus, error) but multi-error states, inline help patterns, and async-validation spinners are not surfaced.
- **Empty states** are described in UX writing principles but lack a structural component spec — illustration size, copy length, CTA placement.
- **Onboarding (`v13_온보딩`)** has only one screen built and may introduce a hero/illustration register that supersedes the current `card-hero-*` family.
- **Caregiver field-mobile (`v11_요양보호사앱`)** shares the medical green theme but operates outdoors — sunlight contrast and one-handed reach patterns may require platform-specific overrides not yet captured.
- **Notification system** (in-app, push, banner) needs unified treatment — currently `{component.toast}` and `{component.sos-banner}` cover only two of the four channels.
- **Backdrop-filter blur values** (16/20/40px) are formalized as tokens but Safari fallback rendering when blur is disabled (low-power mode) is not specified.
- **Role gradient on darker upper canvases** (e.g., evening-mode app skin, hypothetical dim variant) was not analyzed.

---

*하루안부 — Design System v2.0 — based on `07_디자인/tokens/tokens.css` (Source of Truth) and the v9.5/v10/v11/v12 implementation set.*
