# 디자인 감사 리포트 — mobile-apps (v0.2)

실행 일시: 2026-05-23 11:28:09
규칙 파일: `07_디자인/review-rules/mobile-apps.json`
검사 대상: `mobile-apps`

## 종합 결과 — audit v0.2 기준 FAIL

- 통과: 2건 / 실패: 5건

## 실패 항목

- [FAIL] 폴더 · v11_보호자앱 — 기대 PASS / 실제 FAIL
    - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 15
- [FAIL] 폴더 · v11_요양보호사앱 — 기대 PASS / 실제 FAIL
    - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 10
- [FAIL] 폴더 · v15_의료진앱 — 기대 PASS / 실제 FAIL
    - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 6
- [FAIL] 폴더 · v12_환자앱 — 기대 PASS / 실제 FAIL
    - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 1
- [FAIL] 폴더 · v10_의료진웹 — 기대 PASS / 실제 FAIL
    - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 43

## 통과 항목

- [PASS] 폴더 · v13_온보딩 — 기대 PASS / 실제 PASS
- [PASS] 대표 화면 존재 — 기대 전부 존재 / 실제 전부 존재

## 수정 권장안

### 폴더 · v11_보호자앱
- 기대값: PASS
- 실제값: FAIL
- 위반 위치:
  - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 15

### 폴더 · v11_요양보호사앱
- 기대값: PASS
- 실제값: FAIL
- 위반 위치:
  - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 10

### 폴더 · v15_의료진앱
- 기대값: PASS
- 실제값: FAIL
- 위반 위치:
  - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 6

### 폴더 · v12_환자앱
- 기대값: PASS
- 실제값: FAIL
- 위반 위치:
  - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 1

### 폴더 · v10_의료진웹
- 기대값: PASS
- 실제값: FAIL
- 위반 위치:
  - - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 43


## 클로드에게 보낼 요약 지시문

```text
mobile-apps 디자인 감사(v0.2)에서 다음 위반이 발견됐다.
- 폴더 · v11_보호자앱: 기대 PASS / 실제 FAIL
  · - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 15
- 폴더 · v11_요양보호사앱: 기대 PASS / 실제 FAIL
  · - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 10
- 폴더 · v15_의료진앱: 기대 PASS / 실제 FAIL
  · - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 6
- 폴더 · v12_환자앱: 기대 PASS / 실제 FAIL
  · - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 1
- 폴더 · v10_의료진웹: 기대 PASS / 실제 FAIL
  · - [FAIL] 아이콘 · iconify-icon 외 사용 — 기대 0 / 실제 43
수정 후 다시 design_audit.py를 실행해서 PASS로 만들어줘.
```
