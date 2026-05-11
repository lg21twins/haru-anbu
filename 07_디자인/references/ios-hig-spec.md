# iOS 26 Human Interface Guidelines — Developer-Ready Spec

> 하루안부 보호자앱 HTML/CSS 목업 작업을 위한 iOS 디자인 레퍼런스
> 최종 업데이트: 2026-04-16

---

## 1. Typography

### Text Styles

| Style | Size | Weight | Line Height | 용도 |
|-------|------|--------|-------------|------|
| Large Title | 34px | 400 (Regular) | 1.2 | 최상위 페이지 헤더 |
| Title 1 | 28px | 400 | 1.2 | 화면 타이틀 |
| Title 2 | 22px | 400 | 1.3 | 섹션 헤더 |
| Title 3 | 20px | 400 | 1.3 | 서브섹션 헤더 |
| Headline | 17px | 600 (Semibold) | 1.4 | 행 레이블, 강조 본문 |
| Body | 17px | 400 | 1.4 | 기본 본문 |
| Callout | 16px | 400 | 1.4 | 보조 텍스트 |
| Subheadline | 15px | 400 | 1.4 | 부제, 설명 |
| Footnote | 13px | 400 | 1.4 | 작은 텍스트 |
| Caption 1 | 12px | 400 | 1.3 | 캡션 |
| Caption 2 | 11px | 400 | 1.3 | 최소 가독 사이즈 |

### Font Stack (웹 구현용)

```css
font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

---

## 2. Color System

### System Colors

| Name | Light | Dark | 용도 |
|------|-------|------|------|
| Blue | `#007AFF` | `#0A84FF` | 기본 액션, 링크, CTA |
| Green | `#34C759` | `#30D158` | 성공, 완료, 정상 |
| Red | `#FF3B30` | `#FF453A` | 삭제, 에러, 위험 |
| Orange | `#FF9500` | `#FF9F0A` | 경고 |
| Yellow | `#FFCC00` | `#FFD60A` | 알림, 주의 |
| Pink | `#FF2D55` | `#FF375F` | 강조 |
| Purple | `#5856D6` | `#5E5CE6` | 보조 강조 |
| Teal | `#5AC8FA` | `#64D2FF` | 정보 |
| Indigo | `#5856D6` | `#5E5CE6` | 정보(보조) |

### Semantic Colors

| Role | Light | Dark |
|------|-------|------|
| **Label** | `#000000` | `#FFFFFF` |
| **Secondary Label** | `rgba(60,60,67,0.60)` | `rgba(235,235,245,0.60)` |
| **Tertiary Label** | `rgba(60,60,67,0.30)` | `rgba(235,235,245,0.30)` |
| **Quaternary Label** | `rgba(60,60,67,0.18)` | `rgba(235,235,245,0.18)` |
| **System Background** | `#FFFFFF` | `#000000` |
| **Secondary Background** | `#F2F2F7` | `#1C1C1E` |
| **Tertiary Background** | `#FFFFFF` | `#2C2C2E` |
| **Grouped Background** | `#F2F2F7` | `#000000` |
| **Secondary Grouped** | `#FFFFFF` | `#1C1C1E` |
| **Tertiary Grouped** | `#F2F2F7` | `#2C2C2E` |
| **Separator** | `rgba(60,60,67,0.29)` | `rgba(84,84,88,0.65)` |
| **Opaque Separator** | `#C6C6C8` | `#38383A` |
| **System Fill** | `rgba(120,120,128,0.20)` | `rgba(120,120,128,0.36)` |
| **Secondary Fill** | `rgba(120,120,128,0.16)` | `rgba(120,120,128,0.32)` |
| **Tertiary Fill** | `rgba(118,118,128,0.12)` | `rgba(118,118,128,0.24)` |

---

## 3. Layout & Spacing

### 구조적 높이

| Element | Height |
|---------|--------|
| Status Bar (Dynamic Island) | 54px |
| Navigation Bar (standard) | 44px |
| Navigation Bar (with status bar) | 64px |
| Large Title Nav (expanded) | 116px |
| Tab Bar | 49px |
| Home Indicator safe area | 34px |
| Tab Bar + safe area 총합 | 83px |

### 간격 시스템 (8pt Grid)

```css
--space-1: 4px;    /* 예외적 미세 간격 */
--space-2: 8px;    /* 기본 단위 */
--space-3: 12px;   /* 보조 간격 */
--space-4: 16px;   /* 표준 마진/패딩 */
--space-5: 20px;   /* 큰 화면 마진 */
--space-6: 24px;   /* 섹션 간격 */
--space-8: 32px;   /* 대형 간격 */
--space-10: 40px;  /* 블록 간격 */
--space-12: 48px;  /* 최대 블록 간격 */
```

### 콘텐츠 영역

| 항목 | 값 |
|------|-----|
| 좌우 콘텐츠 마진 | 16px (기본), 20px (큰 화면) |
| 카드 내부 패딩 | 16px |
| 리스트 셀 내부 패딩 | 16px (좌우), 12px (상하) |
| 최소 터치 타겟 | 44 x 44px |
| 섹션 간 간격 | 8-16px |

---

## 4. Corner Radius

| Element | Radius | CSS |
|---------|--------|-----|
| 작은 요소 (뱃지, 칩) | 8px | `border-radius: 8px` |
| 카드, Inset Grouped 셀 | 12px | `border-radius: 12px` |
| 큰 카드, 모달 | 16px | `border-radius: 16px` |
| 캡슐/필 버튼 | height/2 | `border-radius: 999px` |
| Bottom Sheet 상단 | 12-16px | `border-radius: 16px 16px 0 0` |

### Concentric Corner (iOS 26)
자식 요소의 radius = 부모 radius - padding

```css
/* 예: 부모 카드 radius 16px, 내부 padding 12px */
.parent { border-radius: 16px; padding: 12px; }
.child  { border-radius: 4px; } /* 16 - 12 = 4 */
```

---

## 5. Shadow & Elevation

| Level | CSS box-shadow |
|-------|----------------|
| Subtle | `0 1px 4px rgba(0,0,0,0.06), 0 0 1px rgba(0,0,0,0.04)` |
| Card | `0 2px 8px rgba(0,0,0,0.12)` |
| Elevated | `0 4px 16px rgba(0,0,0,0.14)` |
| Modal | `0 8px 28px rgba(0,0,0,0.16)` |

---

## 6. Materials & Liquid Glass (iOS 26)

### Blur Levels

| Material | backdrop-filter |
|----------|-----------------|
| Ultra Thin | `blur(4px) saturate(120%)` |
| Thin | `blur(8px) saturate(130%)` |
| Regular | `blur(16px) saturate(150%)` |
| Thick | `blur(24px) saturate(180%)` |
| Ultra Thick | `blur(40px) saturate(200%)` |

### Liquid Glass 구현

```css
.liquid-glass {
    background: rgba(255, 255, 255, 0.26);
    backdrop-filter: blur(20px) saturate(160%) brightness(1.04);
    -webkit-backdrop-filter: blur(20px) saturate(160%) brightness(1.04);
    border: 0.5px solid rgba(255, 255, 255, 0.55);
    box-shadow:
        inset 0 1px 1px rgba(255, 255, 255, 0.6),
        0 2px 8px rgba(0, 0, 0, 0.08);
}

.liquid-glass-strong {
    background: rgba(255, 255, 255, 0.42);
    backdrop-filter: blur(32px) saturate(180%) brightness(1.06);
    -webkit-backdrop-filter: blur(32px) saturate(180%) brightness(1.06);
    border: 0.5px solid rgba(255, 255, 255, 0.70);
    box-shadow:
        inset 0 1px 1px rgba(255, 255, 255, 0.6),
        0 4px 16px rgba(0, 0, 0, 0.10);
}
```

---

## 7. Component Specs

### Navigation Bar

```
높이: 44px (콘텐츠), 98px (status bar + nav bar)
타이틀: 17px Semibold, 중앙 정렬
Large Title: 34px Regular, 좌측 정렬, 확장시 +52px
Back 버튼: chevron 18px, 터치 타겟 44x44px
Bar Button: 터치 타겟 44x44px
```

### Tab Bar

```
높이: 49px (+34px home indicator)
아이콘: 25x25px
레이블: 10px Medium (500)
선택: 풀컬러 (100%)
비선택: 60% opacity
아이콘-레이블 간격: 2px
iOS 26: 캡슐형 플로팅 + Liquid Glass
```

### List / Table View

```
셀 최소 높이: 44px
표준 셀 높이: 44-56px
Inset Grouped 좌우 마진: 16px
Inset Grouped 코너: 12px
구분선: 1px, 좌측 16px inset
섹션 헤더: 13px, 대문자, Secondary Label 색상
```

### Button

```
최소 높이: 44px (터치 타겟)
표준 높이: 50px
패딩: 0 24px
코너: Small 8px / Medium 10px / Large 12px / Capsule height/2
Active: scale(0.98), opacity 0.8, 120ms
Disabled: opacity 0.5
```

### Toggle Switch

```
크기: 51 x 31px (고정)
Thumb: 27 x 27px
코너: 999px (캡슐)
On: System Green (#34C759)
Off: System Fill
애니메이션: 0.3s ease
```

### Search Bar

```
높이: 56px (컨테이너), 44px (텍스트필드)
코너: 10px
배경: Tertiary Fill
플레이스홀더: Secondary Label 색상
아이콘: 16px, Tertiary Label 색상
```

### Bottom Sheet

```
Medium detent: 화면 50%
Large detent: 전체 화면
코너: 16px (상단만)
핸들 바: 44 x 5px, 캡슐형, systemGray3
핸들 위치: 상단 중앙, 8px 마진
배경 딤: rgba(0,0,0,0.30)
```

### Alert / Action Sheet

```
코너: 14px
배경: System Background
제목: 17px Semibold
메시지: 13px Regular
버튼 높이: 44px
구분선: Separator 색상
Destructive: System Red
Cancel: 별도 분리, Bold
```

---

## 8. Motion & Animation

| Type | Duration | Easing |
|------|----------|--------|
| 빠른 피드백 (탭, 토글) | 150ms | ease |
| 표준 전환 (페이지, 모달) | 300ms | ease-in-out |
| 스프링 (iOS 기본) | 400ms | cubic-bezier(0.25, 0.46, 0.45, 0.94) |
| 느린 전환 (복잡한 레이아웃) | 600ms | ease-in-out |
| 버튼 눌림 | 120ms | ease |

### CSS Spring 근사값

```css
/* iOS 기본 스프링 */
transition-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);

/* 부드러운 바운스 */
transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1);

/* 감쇠 스프링 */
transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
```

---

## 9. 하루안부 적용 매핑

### 현재 → iOS HIG 조정 사항

| 변수 | 현재값 | iOS 표준 | 조치 |
|------|--------|----------|------|
| `--radius-md` | 14px | 12px | 조정 |
| `--text-body` | 16px | 17px | 조정 |
| `--text-headline` | 17px | 17px Semibold | 확인 (일치) |
| `--space-xs` | 4px | 4px | 유지 |
| `--space-sm` | 8px | 8px | 유지 |
| `--space-md` | 12px | 12px | 유지 |
| `--space-lg` | 16px | 16px | 유지 |
| `--shadow-sm` | 현재값 | `0 1px 4px rgba(0,0,0,0.06)` | 비교 확인 |
| 탭바 높이 | 68px | 83px (49+34) | 검토 |
| 셀 높이 | 56px | 44-56px | 유지 (범위 내) |

### 유지할 하루안부 고유 요소

- Pretendard Variable (한글 최적화 폰트)
- 역할 기반 컬러 체계 (보호자 #2C7AFC / 간호사 #059669 / 환자 #FB923C)
- 블롭 배경 애니메이션
- 벤토 그리드 대시보드 레이아웃
