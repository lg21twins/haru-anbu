# 하루안부 · 온보딩 v13

**상태**: 🚧 POC 1페이지 (ob01-welcome.html)
**역할 선택 전** 공통 화면 묶음

---

## 플랫폼 확정

- **모바일 PWA 기본** (9:16 세로). 태블릿·데스크톱 대응은 나중에 추가.
- `<html data-role="onboarding" data-platform="mobile">`
- `data-role="onboarding"` 은 tokens.css에 별도 오버라이드가 없으므로 **보호자 블루가 기본 테마**로 뜬다 (디폴트값 = `--brand-blue-500`).

---

## 왜 별도 폴더인가

v9에 이미 `onboarding/` 폴더가 있었지만, 이전 디자인 시스템(`common.css`) 기반이라 폐기. 새 tokens.css로 **처음부터 다시** 만든다. 재사용할 아이디어(splash/role pick/social)만 가져옴.

---

## 예상 화면 인벤토리

| ID | 화면 | 비고 |
|---|---|---|
| OB-01 | Welcome (히어로 로고 + 가입/로그인) | 첫 진입 |
| OB-02 | Role Picker (보호자/의료진/환자) | 역할 선택 → 이후 data-role 결정 |
| OB-03 | Social Sign-in (카카오/애플/전화) | 가입 분기 |
| OB-04 | Agreement (약관) | 법적 동의 |
| OB-05 | Profile (이름·전화·관계) | 최소 정보만 |
| OB-06 | Complete (환영 메시지 → 홈으로) | 첫 투어 |
