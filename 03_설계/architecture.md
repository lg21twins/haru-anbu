# 케어 플랫폼 — 시스템 아키텍처 설계서

**v1.0 | 2026.03**

---

## 1. 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                        클라이언트 계층                            │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  보호자 (모바일) │  │  환자 (태블릿)  │  │  의료진 (PC 데스크톱)   │   │
│  │  React Web    │  │  React Web    │  │  React Web           │   │
│  │  반응형 모바일  │  │  큰글자 UI     │  │  데스크톱 최적화       │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘   │
│         │                  │                      │               │
└─────────┼──────────────────┼──────────────────────┼───────────────┘
          │                  │                      │
          ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Vercel (호스팅 + Edge)                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  React SPA (TypeScript + Tailwind CSS)                   │    │
│  │  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │    │
│  │  │ React   │ │ Zustand  │ │ React    │ │ Tailwind   │  │    │
│  │  │ Router  │ │ (상태관리) │ │ Query   │ │ CSS        │  │    │
│  │  └─────────┘ └──────────┘ └──────────┘ └────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Vercel Serverless Functions (Edge Runtime)              │    │
│  │  - Claude API 프록시 (API 키 보호)                        │    │
│  │  - FCM 푸시 알림 발송                                     │    │
│  │  - AI 일일 리포트 Cron Job                                │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
          │                  │                      │
          ▼                  ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Supabase (BaaS)                              │
│                                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │ Auth     │ │ Database │ │ Realtime │ │ Storage          │   │
│  │ (인증)    │ │(PostgreSQL)│ │ (실시간)  │ │ (파일 저장)       │   │
│  │          │ │ + RLS    │ │          │ │                  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
          │                                         │
          ▼                                         ▼
┌──────────────────┐                    ┌──────────────────┐
│ Claude API       │                    │ Firebase (FCM)   │
│ (Anthropic)      │                    │ 푸시 알림          │
│ - 케어 가이드     │                    │                  │
│ - 일일 리포트     │                    │                  │
└──────────────────┘                    └──────────────────┘
```

---

## 2. 기술 스택 상세

### 2.1 프론트엔드

| 기술 | 버전 | 용도 | 선택 이유 |
|------|------|------|-----------|
| **React** | 19.x | UI 프레임워크 | 컴포넌트 재사용, 단일 코드베이스로 3역할 분기 |
| **TypeScript** | 5.x | 타입 안전성 | 3인 협업 시 타입 에러 조기 발견 |
| **Tailwind CSS** | 4.x | 스타일링 | 유틸리티 퍼스트, Claude 코드 생성에 최적화 |
| **React Router** | 7.x | 라우팅 | 역할 기반 라우트 가드, 중첩 레이아웃 |
| **Zustand** | 5.x | 전역 상태 관리 | 가벼움, 보일러플레이트 최소, 학습 곡선 낮음 |
| **TanStack Query** | 5.x | 서버 상태 관리 | 캐싱, 리페칭, Supabase 연동 최적화 |
| **date-fns** | 4.x | 날짜 처리 | 시간표, 타임라인, 타임스탬프 포맷팅 |

### 2.2 백엔드 (BaaS)

| 기술 | 용도 | 선택 이유 |
|------|------|-----------|
| **Supabase** | DB + Auth + Realtime + Storage | 올인원 BaaS, 백엔드 코드 최소화 |
| **PostgreSQL** | 메인 데이터베이스 | Supabase 내장, 관계형 데이터 처리 |
| **Row-Level Security** | 역할별 데이터 접근 제어 | DB 레벨 보안, 클라이언트 직접 접근 안전 |
| **Supabase Realtime** | 실시간 데이터 동기화 | 체크리스트 → 대시보드, 채팅 메시지 |
| **Supabase Storage** | 파일 저장 (채팅 이미지) | 버킷 기반 접근 제어, CDN |
| **Supabase Auth** | 사용자 인증 | 소셜 로그인(카카오/구글) 내장 지원 |

### 2.3 서버리스 / 외부 서비스

| 기술 | 용도 | 선택 이유 |
|------|------|-----------|
| **Vercel** | 호스팅 + Serverless Functions | GitHub 연동 자동 배포, Edge 성능 |
| **Claude API** (Anthropic) | AI 케어 가이드, 일일 리포트 | 프로젝트 AI 스택 통일, 한국어 품질 우수 |
| **Firebase Cloud Messaging** | 푸시 알림 | 크로스 플랫폼 무료 푸시 |

---

## 3. 데이터베이스 설계

### 3.1 ER 다이어그램

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   users       │     │   patients    │     │  care_records     │
├──────────────┤     ├──────────────┤     ├──────────────────┤
│ id (PK)       │──┐  │ id (PK)       │──┐  │ id (PK)           │
│ role           │  │  │ name          │  │  │ patient_id (FK)   │
│ name           │  │  │ age           │  │  │ type              │
│ email          │  │  │ type          │  │  │ status            │
│ facility_id    │  │  │ grade         │  │  │ note              │
│ avatar_url     │  │  │ medical_staff │  │  │ timestamp         │
│ created_at     │  │  │ room_no       │  │  │ staff_id (FK)     │
└──────────────┘  │  │ facility_id   │  │  └──────────────────┘
                   │  └──────────────┘  │
                   │         │           │
                   │         ▼           │
                   │  ┌──────────────┐  │  ┌──────────────────┐
                   │  │   alerts      │  │  │  messages         │
                   │  ├──────────────┤  │  ├──────────────────┤
                   │  │ id (PK)       │  │  │ id (PK)           │
                   │  │ type          │  │  │ sender_id (FK)    │
                   │  │ message       │  │  │ receiver_id (FK)  │
                   │  │ patient_id    │  │  │ content           │
                   │  │ sent_by (FK)  │  │  │ media_url         │
                   │  │ sent_to (FK)  │  │  │ read_at           │
                   │  │ responded_at  │  │  │ created_at        │
                   │  │ status        │  │  └──────────────────┘
                   │  └──────────────┘  │
                   │                     │
┌──────────────┐  │  ┌──────────────┐  │  ┌──────────────────┐
│daily_reports  │  │  │ai_chat_      │  │  │  schedules        │
├──────────────┤  │  │sessions      │  │  ├──────────────────┤
│ id (PK)       │  │  ├──────────────┤  │  │ id (PK)           │
│ patient_id    │  │  │ id (PK)       │  │  │ patient_id (FK)   │
│ date          │  │  │ user_id (FK)  │  │  │ type              │
│ care_summary  │  │  │ type          │  │  │ title             │
│ ai_text       │  │  │ messages_json │  │  │ start_time        │
│ sent_at       │  │  │ topic         │  │  │ end_time          │
└──────────────┘  │  │ created_at    │  │  │ repeat_rule       │
                   │  └──────────────┘  │  │ staff_id (FK)     │
                   │                     │  │ facility_id       │
                   │                     │  └──────────────────┘
                   │                     │
┌──────────────┐  │  ┌──────────────┐  │  ┌──────────────────┐
│prescriptions  │  │  │medical_      │  │  │medical_timeline  │
├──────────────┤  │  │records       │  │  │_events           │
│ id (PK)       │  │  ├──────────────┤  │  ├──────────────────┤
│ patient_id    │◄─┘  │ id (PK)       │◄─┘  │ id (PK)           │
│ doctor_id     │     │ patient_id    │     │ patient_id (FK)   │
│ drug_name     │     │ doctor_id     │     │ event_type        │
│ dosage        │     │ diagnosis     │     │ title             │
│ frequency     │     │ opinion       │     │ summary           │
│ start_date    │     │ follow_up     │     │ related_record_id │
│ end_date      │     │ record_date   │     │ event_date        │
│ notes         │     │ visibility    │     │ created_by (FK)   │
│ created_at    │     │ created_at    │     │ facility_id       │
└──────────────┘     └──────────────┘     └──────────────────┘
```

### 3.2 테이블 상세 스키마

```sql
-- ================================================
-- 1. users (사용자)
-- ================================================
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  role TEXT NOT NULL CHECK (role IN ('family', 'medical', 'patient')),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  facility_id UUID,
  avatar_url TEXT,
  fcm_token TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 2. patients (환자)
-- ================================================
CREATE TABLE patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  age INTEGER,
  type TEXT CHECK (type IN ('elderly', 'child', 'adult')),
  grade TEXT,
  medical_staff_id UUID REFERENCES users(id),
  room_no TEXT,
  facility_id UUID,
  family_id UUID REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 3. care_records (케어 기록)
-- ================================================
CREATE TABLE care_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  type TEXT NOT NULL CHECK (type IN ('meal', 'medication', 'hygiene', 'activity')),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'skipped')),
  note TEXT,
  timestamp TIMESTAMPTZ DEFAULT now(),
  staff_id UUID REFERENCES users(id)
);

-- ================================================
-- 4. alerts (알림)
-- ================================================
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type TEXT NOT NULL CHECK (type IN ('sos', 'fall', 'health')),
  message TEXT,
  patient_id UUID NOT NULL REFERENCES patients(id),
  sent_by UUID REFERENCES users(id),
  sent_to UUID REFERENCES users(id),
  responded_at TIMESTAMPTZ,
  status TEXT DEFAULT 'sent' CHECK (status IN ('sent', 'delivered', 'read', 'responded', 'resolved')),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 5. messages (채팅 메시지)
-- ================================================
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id UUID NOT NULL REFERENCES users(id),
  receiver_id UUID NOT NULL REFERENCES users(id),
  content TEXT,
  media_url TEXT,
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 6. daily_reports (AI 일일 리포트)
-- ================================================
CREATE TABLE daily_reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  date DATE NOT NULL,
  care_summary JSONB,
  ai_generated_text TEXT,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 7. ai_chat_sessions (AI 채팅 세션)
-- ================================================
CREATE TABLE ai_chat_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  type TEXT CHECK (type IN ('care_guide', 'emotion_support')),
  messages_json JSONB DEFAULT '[]'::jsonb,
  topic TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 8. schedules (시간표)
-- ================================================
CREATE TABLE schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  type TEXT CHECK (type IN ('daily_routine', 'care_task')),
  title TEXT NOT NULL,
  start_time TIMESTAMPTZ NOT NULL,
  end_time TIMESTAMPTZ,
  repeat_rule TEXT,
  staff_id UUID REFERENCES users(id),
  facility_id UUID,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 9. prescriptions (처방전)
-- ================================================
CREATE TABLE prescriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  doctor_id UUID NOT NULL REFERENCES users(id),
  drug_name TEXT NOT NULL,
  dosage TEXT,
  frequency TEXT,
  start_date DATE,
  end_date DATE,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 10. medical_records (진료기록)
-- ================================================
CREATE TABLE medical_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  doctor_id UUID NOT NULL REFERENCES users(id),
  diagnosis TEXT,
  opinion TEXT,
  follow_up_plan TEXT,
  record_date DATE NOT NULL,
  visibility TEXT DEFAULT 'summary' CHECK (visibility IN ('full', 'summary', 'restricted')),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ================================================
-- 11. medical_timeline_events (의료 타임라인)
-- ================================================
CREATE TABLE medical_timeline_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  event_type TEXT NOT NULL CHECK (event_type IN ('diagnosis', 'prescription', 'examination')),
  title TEXT NOT NULL,
  summary TEXT,
  related_record_id UUID,
  event_date DATE NOT NULL,
  created_by UUID REFERENCES users(id),
  facility_id UUID,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### 3.3 RLS (Row-Level Security) 정책

```sql
-- ================================================
-- users: 본인 정보만 수정, 같은 시설 사용자 조회 가능
-- ================================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_select_same_facility" ON users
  FOR SELECT USING (facility_id = (SELECT facility_id FROM users WHERE id = auth.uid()));

CREATE POLICY "users_update_own" ON users
  FOR UPDATE USING (id = auth.uid());

-- ================================================
-- care_records: 의료진만 작성, 보호자는 연결된 환자만 열람
-- ================================================
ALTER TABLE care_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "care_records_insert_medical" ON care_records
  FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'medical')
  );

CREATE POLICY "care_records_select_family" ON care_records
  FOR SELECT USING (
    -- 의료진: 담당 환자
    EXISTS (
      SELECT 1 FROM patients p
      WHERE p.id = care_records.patient_id
      AND p.medical_staff_id = auth.uid()
    )
    OR
    -- 보호자: 연결된 환자
    EXISTS (
      SELECT 1 FROM patients p
      WHERE p.id = care_records.patient_id
      AND p.family_id = auth.uid()
    )
  );

-- ================================================
-- alerts: 발신자(의료진) 또는 수신자(보호자)만 접근
-- ================================================
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "alerts_access" ON alerts
  FOR ALL USING (sent_by = auth.uid() OR sent_to = auth.uid());

-- ================================================
-- messages: 송신자 또는 수신자만 접근
-- ================================================
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "messages_access" ON messages
  FOR ALL USING (sender_id = auth.uid() OR receiver_id = auth.uid());

-- ================================================
-- prescriptions: 의료진 전체, 보호자 요약, 환자 본인만
-- ================================================
ALTER TABLE prescriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "prescriptions_medical_full" ON prescriptions
  FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'medical')
  );

CREATE POLICY "prescriptions_family_read" ON prescriptions
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM patients p
      WHERE p.id = prescriptions.patient_id
      AND p.family_id = auth.uid()
    )
  );

CREATE POLICY "prescriptions_patient_own" ON prescriptions
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM patients p
      WHERE p.id = prescriptions.patient_id
      AND EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'patient')
    )
  );

-- ================================================
-- medical_records: 의료진 전체, 보호자 요약만, 환자 제한적
-- ================================================
ALTER TABLE medical_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "medical_records_medical" ON medical_records
  FOR ALL USING (
    EXISTS (SELECT 1 FROM users WHERE id = auth.uid() AND role = 'medical')
  );

CREATE POLICY "medical_records_family" ON medical_records
  FOR SELECT USING (
    visibility IN ('full', 'summary')
    AND EXISTS (
      SELECT 1 FROM patients p
      WHERE p.id = medical_records.patient_id
      AND p.family_id = auth.uid()
    )
  );
```

---

## 4. 프론트엔드 아키텍처

### 4.1 폴더 구조

```
src/
├── app/                          # 앱 진입점
│   ├── App.tsx                   # 라우터 + 프로바이더
│   ├── router.tsx                # 라우트 정의 + 가드
│   └── providers.tsx             # QueryClient, Auth 등
│
├── features/                     # 기능 단위 모듈
│   ├── auth/                     # F-07 인증 + 역할 분기
│   │   ├── components/
│   │   ├── hooks/
│   │   └── pages/
│   │       ├── LoginPage.tsx
│   │       └── OnboardingPage.tsx
│   │
│   ├── checklist/                # F-01 케어 체크리스트
│   │   ├── components/
│   │   │   ├── ChecklistCard.tsx
│   │   │   └── ChecklistItem.tsx
│   │   ├── hooks/
│   │   │   └── useChecklist.ts
│   │   └── pages/
│   │       └── ChecklistPage.tsx
│   │
│   ├── dashboard/                # F-02 보호자 대시보드
│   │   ├── components/
│   │   │   ├── CareStatusCard.tsx
│   │   │   └── CompletionRate.tsx
│   │   └── pages/
│   │       └── DashboardPage.tsx
│   │
│   ├── sos/                      # F-03 SOS 긴급 알림
│   │   ├── components/
│   │   │   ├── SOSButton.tsx
│   │   │   ├── SOSModal.tsx
│   │   │   └── SOSTimeline.tsx
│   │   └── pages/
│   │       └── SOSPage.tsx
│   │
│   ├── chat/                     # F-04 1:1 채팅
│   │   ├── components/
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ImageUpload.tsx
│   │   └── pages/
│   │       └── ChatPage.tsx
│   │
│   ├── report/                   # F-05 AI 일일 리포트
│   │   ├── components/
│   │   │   └── ReportCard.tsx
│   │   └── pages/
│   │       └── ReportPage.tsx
│   │
│   ├── ai-guide/                 # F-06 AI 케어 가이드
│   │   ├── components/
│   │   │   ├── GuideChat.tsx
│   │   │   └── ModeToggle.tsx
│   │   ├── hooks/
│   │   │   └── useAIGuide.ts
│   │   └── pages/
│   │       └── AIGuidePage.tsx
│   │
│   ├── schedule/                 # F-08 시간표
│   │   ├── components/
│   │   │   ├── DailySchedule.tsx
│   │   │   └── CareTimeline.tsx
│   │   └── pages/
│   │       └── SchedulePage.tsx
│   │
│   └── medical/                  # F-09 처방전·진료기록
│       ├── components/
│       │   ├── PrescriptionForm.tsx
│       │   ├── PrescriptionView.tsx
│       │   ├── MedicalRecordForm.tsx
│       │   └── MedicalTimeline.tsx
│       └── pages/
│           ├── PrescriptionPage.tsx
│           └── MedicalTimelinePage.tsx
│
├── layouts/                      # 역할별 레이아웃
│   ├── FamilyLayout.tsx          # 보호자 (모바일 탭바)
│   ├── MedicalLayout.tsx         # 의료진 (PC 사이드바)
│   └── PatientLayout.tsx         # 환자 (큰글자 단순)
│
├── shared/                       # 공통 모듈
│   ├── components/               # 공통 UI 컴포넌트
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── Input.tsx
│   │   ├── Badge.tsx
│   │   ├── Toast.tsx
│   │   ├── Skeleton.tsx
│   │   └── EmptyState.tsx
│   ├── hooks/                    # 공통 훅
│   │   ├── useAuth.ts
│   │   ├── useRealtime.ts
│   │   └── useNotification.ts
│   ├── lib/                      # 유틸리티
│   │   ├── supabase.ts           # Supabase 클라이언트
│   │   ├── claude.ts             # Claude API 호출
│   │   └── fcm.ts                # FCM 설정
│   └── types/                    # TypeScript 타입
│       ├── database.ts           # DB 스키마 타입
│       └── api.ts                # API 응답 타입
│
└── styles/
    └── globals.css               # Tailwind 기본 스타일
```

### 4.2 역할 기반 라우팅

```typescript
// src/app/router.tsx (개념)

const routes = {
  // 공통
  '/login':           LoginPage,
  '/onboarding':      OnboardingPage,

  // 보호자 (family)
  '/family/dashboard':     DashboardPage,        // F-02
  '/family/chat':          ChatPage,             // F-04
  '/family/chat/:id':      ChatRoomPage,
  '/family/ai-guide':      AIGuidePage,          // F-06
  '/family/reports':       ReportPage,           // F-05
  '/family/schedule':      SchedulePage,         // F-08
  '/family/medical':       MedicalTimelinePage,  // F-09
  '/family/prescriptions': PrescriptionPage,     // F-09
  '/family/sos':           SOSAlertPage,         // F-03 (수신)

  // 의료진 (medical)
  '/medical/checklist':     ChecklistPage,       // F-01
  '/medical/patients':      PatientListPage,
  '/medical/patients/:id':  PatientDetailPage,
  '/medical/sos':           SOSPage,             // F-03 (발신)
  '/medical/chat':          ChatPage,            // F-04
  '/medical/schedule':      SchedulePage,        // F-08
  '/medical/prescriptions': PrescriptionFormPage,// F-09
  '/medical/records':       MedicalRecordPage,   // F-09

  // 환자 (patient)
  '/patient/home':          PatientHomePage,
  '/patient/schedule':      SchedulePage,        // F-08
  '/patient/prescriptions': PrescriptionPage,    // F-09 (큰글자)
};
```

### 4.3 상태 관리 전략

```
┌─────────────────────────────────────────┐
│              상태 관리 계층               │
├─────────────────────────────────────────┤
│                                          │
│  서버 상태 (TanStack Query)              │
│  ├── 케어 기록, 알림, 메시지, 처방전      │
│  ├── Supabase → Query 캐싱               │
│  └── Realtime → 캐시 무효화              │
│                                          │
│  전역 상태 (Zustand)                     │
│  ├── 인증 상태 (user, role)              │
│  ├── 알림 상태 (unread count)            │
│  └── UI 상태 (사이드바, 모달)            │
│                                          │
│  로컬 상태 (React useState)              │
│  ├── 폼 입력값                           │
│  ├── 토글, 드롭다운                      │
│  └── 임시 UI 상태                        │
│                                          │
└─────────────────────────────────────────┘
```

---

## 5. 주요 데이터 플로우

### 5.1 케어 체크리스트 → 대시보드 실시간 반영

```
의료진 (PC)                    Supabase                    보호자 (모바일)
    │                            │                              │
    │  1. 체크 입력               │                              │
    ├──────────────────────────► │                              │
    │     INSERT care_records    │                              │
    │                            │  2. Realtime broadcast       │
    │                            ├─────────────────────────────►│
    │                            │     { type: 'INSERT',        │
    │                            │       table: 'care_records'} │
    │                            │                              │
    │                            │                     3. UI 업데이트
    │                            │                     (대시보드 카드 갱신)
    │                            │                              │
    │                     목표: 3초 이내                         │
```

### 5.2 SOS 긴급 알림 플로우

```
의료진 (PC)          Vercel Function        FCM           보호자 (모바일)
    │                     │                  │                  │
    │ 1. SOS 버튼 클릭    │                  │                  │
    │    + 상황 메모       │                  │                  │
    ├────────────────────►│                  │                  │
    │  INSERT alerts      │                  │                  │
    │                     │ 2. FCM 발송      │                  │
    │                     ├─────────────────►│                  │
    │                     │                  │ 3. 푸시 알림     │
    │                     │                  ├─────────────────►│
    │                     │                  │                  │
    │                     │                  │    4. 알림 확인   │
    │                     │◄─────────────────┼──────────────────┤
    │                     │  UPDATE alerts   │                  │
    │                     │  (responded_at)  │                  │
    │                     │                  │                  │
    │  [5분 미응답 시]     │                  │                  │
    │                     │ 5. 자동 재알림   │                  │
    │                     ├─────────────────►│                  │
    │                     │                  ├─────────────────►│
```

### 5.3 AI 케어 가이드 대화 플로우

```
보호자 (모바일)       Vercel Function        Claude API
    │                     │                     │
    │ 1. 질문 입력         │                     │
    │ "장기요양등급        │                     │
    │  신청은 어떻게?"     │                     │
    ├────────────────────►│                     │
    │                     │ 2. API 호출          │
    │                     │ + System Prompt      │
    │                     │ + 대화 히스토리       │
    │                     ├────────────────────►│
    │                     │                     │
    │                     │ 3. 응답 스트리밍      │
    │                     │◄────────────────────┤
    │ 4. 스트리밍 표시     │                     │
    │◄────────────────────┤                     │
    │                     │                     │
    │ [감정 신호 감지 시]  │                     │
    │ "너무 힘들어요..."   │                     │
    ├────────────────────►│                     │
    │                     │ 5. 모드 전환          │
    │                     │ System Prompt 변경   │
    │                     │ → 감정 지원 모드     │
    │                     ├────────────────────►│
    │                     │◄────────────────────┤
    │◄────────────────────┤                     │
    │ "많이 힘드셨겠어요.  │                     │
    │  잠시 이야기         │                     │
    │  나눠볼까요?"        │                     │
```

### 5.4 AI 일일 리포트 생성 플로우

```
Vercel Cron (매일 저녁)     Supabase          Claude API         FCM
    │                         │                  │                │
    │ 1. 오늘 케어 데이터 조회 │                  │                │
    ├────────────────────────►│                  │                │
    │◄────────────────────────┤                  │                │
    │  care_records (오늘)     │                  │                │
    │                         │                  │                │
    │ 2. AI 요약 요청          │                  │                │
    ├─────────────────────────┼─────────────────►│                │
    │                         │                  │                │
    │ 3. 요약 텍스트 수신      │                  │                │
    │◄─────────────────────────────────────────────┤                │
    │                         │                  │                │
    │ 4. 리포트 저장           │                  │                │
    ├────────────────────────►│                  │                │
    │  INSERT daily_reports   │                  │                │
    │                         │                  │                │
    │ 5. 푸시 알림 발송        │                  │                │
    ├─────────────────────────┼──────────────────┼───────────────►│
    │                         │                  │    → 보호자     │
```

---

## 6. AI 시스템 설계

### 6.1 AI 케어 가이드 System Prompt 구조 (5개 모드)

```
┌──────────────────────────────────────────────────┐
│              AI 케어 가이드 프롬프트 구조           │
├──────────────────────────────────────────────────┤
│                                                   │
│  [Base System Prompt]                             │
│  - 역할: 전문적이지만 따뜻한 요양 상담사            │
│  - 지식 범위: 요양원 정보, 건강 정보, 복지 제도      │
│  - 제한: 의료 진단 X, 처방 X, 법적 자문 X          │
│  - 면책: "최종 판단은 의료진이 합니다" 포함          │
│                                                   │
│  [Mode 1: 백과사전] (기본)                         │
│  - 객관적 정보 제공                                │
│  - 절차, 서류, 비용 등 구체적 안내                  │
│  - 출처 기반 답변                                  │
│                                                   │
│  [Mode 2: 감정 지원] (감정 신호 감지 시 전환)       │
│  - 공감 + 위로 톤                                 │
│  - 피로도 높을 시 전문 상담 기관 안내               │
│  - 법적 프레이밍: "감정 체크인 서비스"              │
│                                                   │
│  [Mode 3: 요양원 찾기] ★ NEW                      │
│  - 대화로 조건 수집 (지역, 등급, 유형, 예산)        │
│  - 공공 데이터 기반 검색 결과 카드 제공             │
│  - 데이터: 국민건강보험공단 장기요양기관 정보        │
│                                                   │
│  [Mode 4: 요양보호사 안내] ★ NEW                   │
│  - 재가: 방문요양센터 배정 / 매칭 앱 안내           │
│  - 시설: 담당 요양보호사 프로필 조회                │
│  - 외부 딥링크: 케어닥, 케어네이션 연결             │
│                                                   │
│  [Mode 5: 요양비 계산] ★ NEW                      │
│  - 등급별 급여 한도액 / 본인부담률 계산             │
│  - 시설 vs 재가 비용 비교                          │
│  - 감경(기초수급/차상위) + 비급여 반영              │
│  - 데이터: 국민건강보험공단 고시 (매년 갱신)        │
│                                                   │
│  [전환 트리거]                                     │
│  - 감정 지원: 키워드(힘들다, 지친다 등) + 문맥      │
│  - 요양원 찾기: "요양원 찾아줘", "시설 추천" 등     │
│  - 요양보호사: "요양보호사", "간병인" 등            │
│  - 요양비 계산: "비용", "얼마", "본인부담금" 등     │
│                                                   │
└──────────────────────────────────────────────────┘
```

### 6.2 Claude API 호출 설정

```typescript
// 개념적 API 호출 구조

// 케어 가이드 — 백과사전 모드
{
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  system: CARE_GUIDE_SYSTEM_PROMPT,
  messages: conversationHistory,
  stream: true
}

// 일일 리포트 생성
{
  model: "claude-haiku-4-5-20251001",  // 비용 절감
  max_tokens: 512,
  system: DAILY_REPORT_SYSTEM_PROMPT,
  messages: [
    { role: "user", content: todayCareDataSummary }
  ]
}
```

### 6.3 AI 비용 관리 전략

| 전략 | 적용 대상 | 예상 절감 |
|------|-----------|-----------|
| Haiku 모델 사용 | 일일 리포트 (정형화된 요약) | 토큰 비용 90% 절감 |
| Sonnet 모델 사용 | 케어 가이드 (복잡한 대화) | 품질-비용 균형 |
| 응답 캐싱 | FAQ성 질문 (등급 신청 절차 등) | 반복 호출 50% 절감 |
| max_tokens 제한 | 전체 | 불필요한 장문 방지 |
| 대화 히스토리 제한 | 케어 가이드 | 최근 10턴만 포함 |

---

## 7. 보안 아키텍처

### 7.1 인증 플로우

```
사용자                  앱               Supabase Auth        카카오/구글
  │                    │                     │                    │
  │ 1. 소셜 로그인 클릭 │                     │                    │
  ├───────────────────►│                     │                    │
  │                    │ 2. OAuth 리다이렉트  │                    │
  │                    ├────────────────────►│                    │
  │                    │                     │ 3. OAuth 인증      │
  │                    │                     ├───────────────────►│
  │                    │                     │◄───────────────────┤
  │                    │                     │ 4. JWT 발급        │
  │                    │◄────────────────────┤                    │
  │                    │                     │                    │
  │                    │ 5. users 테이블에서 role 조회              │
  │                    │ 6. 역할별 화면 라우팅                      │
  │◄───────────────────┤                                          │
```

### 7.2 데이터 보안 계층

```
┌─────────────────────────────────────┐
│ Layer 1: 전송 암호화 (HTTPS/TLS)     │
├─────────────────────────────────────┤
│ Layer 2: 인증 (Supabase Auth + JWT) │
├─────────────────────────────────────┤
│ Layer 3: 인가 (RLS 정책)            │
│  - family → 연결된 환자만            │
│  - medical → 담당 환자만             │
│  - patient → 본인 기록만             │
├─────────────────────────────────────┤
│ Layer 4: 의료 데이터 암호화           │
│  - 처방전·진료기록 AES-256           │
├─────────────────────────────────────┤
│ Layer 5: API 키 보호                 │
│  - Claude API 키 → Vercel 환경변수   │
│  - Supabase 키 → 환경변수            │
└─────────────────────────────────────┘
```

---

## 8. 배포 아키텍처

```
GitHub Repository
    │
    │ push / PR merge
    ▼
Vercel (자동 배포)
    │
    ├── Production ──── main 브랜치 ──── care-platform.vercel.app
    ├── Preview ─────── PR 브랜치 ────── pr-123.vercel.app
    └── Development ─── dev 브랜치 ───── dev.care-platform.vercel.app

환경변수 (Vercel Dashboard):
    ├── NEXT_PUBLIC_SUPABASE_URL
    ├── NEXT_PUBLIC_SUPABASE_ANON_KEY
    ├── SUPABASE_SERVICE_ROLE_KEY (서버 전용)
    ├── ANTHROPIC_API_KEY (서버 전용)
    └── FCM_SERVER_KEY (서버 전용)
```

### 8.1 브랜치 전략

```
main ─────────────────────────────────────── 프로덕션
  │
  ├── dev ────────────────────────────────── 개발 통합
  │     │
  │     ├── feature/F-01-checklist ────────── 기능 브랜치
  │     ├── feature/F-02-dashboard
  │     ├── feature/F-03-sos
  │     ├── feature/F-06-ai-guide
  │     └── fix/realtime-connection
  │
  └── hotfix/critical-bug ────────────────── 긴급 수정
```

---

## 9. 성능 목표 및 모니터링

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| 페이지 초기 로드 (LCP) | < 2초 | Vercel Analytics |
| 체크리스트 → 대시보드 반영 | < 3초 | Supabase Realtime 타임스탬프 |
| SOS 알림 발송 | < 30초 | FCM 발송 로그 |
| AI 가이드 첫 응답 (TTFB) | < 2초 | 스트리밍 시작 시간 |
| AI 가이드 응답 성공률 | > 95% | API 에러율 모니터링 |
| 번들 사이즈 | < 300KB (gzip) | Vercel 빌드 로그 |

---

*케어 플랫폼 프로젝트 팀 | 시스템 아키텍처 설계서 v1.0 | 2026.03*
