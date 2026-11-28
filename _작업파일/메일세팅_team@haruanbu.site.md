# team@haruanbu.site 만들기 — Zoho Mail 무료 + 가비아 DNS

확정 2026-08-09. 명함·인쇄물·제안서 PDF의 연락처는 **이미 이 주소로 교체됐다.**
**메일함이 실제로 열리기 전에는 인쇄·발송하지 않는다.**

## 사전 확인 (2026-08-09 기준, 이미 확인함)

| 항목 | 상태 |
|---|---|
| 네임서버 | `ns1.gabia.co.kr` 등 — **DNS는 My가비아에서 관리** |
| 기존 MX | 없음 — 충돌 없이 추가 가능 |
| 기존 TXT/SPF | 없음 |
| `A @` | `76.76.21.21` (Vercel) — **건드리지 않는다** |
| `CNAME www` | `cname.vercel-dns.com` — **건드리지 않는다** |

메일 레코드(MX·TXT)를 추가해도 홈페이지에는 영향이 없다. 서로 다른 레코드다.

## 순서

1. **Zoho 가입** — `zoho.com/mail` → **"Sign up with a domain I already own"** → `haruanbu.site`
   → 요금제 **Forever Free** (안 보이면 `zoho.com/mail/zohomail-pricing` 맨 아래)
   로그인 계정은 기존 개인 gmail 그대로 써도 된다. 새 구글 계정은 필요 없다.
2. **도메인 인증** — Zoho가 주는 TXT 값을 My가비아 → DNS 관리툴 → `haruanbu.site` → 레코드 추가
   → Zoho에서 Verify
3. **메일 계정 생성** — `team` → `team@haruanbu.site`
4. **아래 레코드 추가**

| 종류 | 호스트 | 값 | 우선순위 |
|---|---|---|---|
| MX | @ | mx.zoho.com | 10 |
| MX | @ | mx2.zoho.com | 20 |
| MX | @ | mx3.zoho.com | 50 |
| TXT (SPF) | @ | `v=spf1 include:zoho.com ~all` | — |
| TXT (DKIM) | zmail._domainkey | Zoho 관리자 → Email Config → DKIM에서 생성되는 `v=DKIM1; k=rsa; p=...` | — |
| TXT (DMARC) | _dmarc | `v=DMARC1; p=none; rua=mailto:team@haruanbu.site` | — |

> 가입 시 데이터센터가 유럽(zoho.eu)으로 잡히면 MX가 `mx.zoho.eu` 계열로 다르다.
> **Zoho 화면에 뜨는 값이 최종 기준이다.** TTL은 기본값 그대로 둔다.

5. **검증**

```bash
bash _작업파일/메일DNS확인.sh
```

전부 `[OK]`가 되면 `mail.zoho.com` 로그인 → 개인 메일에서 `team@haruanbu.site`로 테스트 발송.
도착하면 끝. 반영에 수분~수시간 걸리므로 `[ ]`가 남아 있으면 시간을 두고 다시 돌린다.

## 알아둘 제약

- **Zoho 무료는 IMAP/POP/SMTP를 열어주지 않는다.** Gmail 앱에 계정으로 추가하는 방식은 안 된다.
- **자동 전달(Email Forwarding)도 무료 플랜에서는 막혀 있다** — 유료 전용이다.
  즉 개인 Gmail 한 곳에서 몰아보는 방법은 없다.
- 따라서 team@ 메일을 보는 방법은 둘뿐이다:
  **① Zoho Mail 모바일 앱**(푸시 알림 옴, 권장) ② `mail.zoho.com` 웹
- Gmail 한 곳에서 다 보려면 Mail Lite($1.25/user/월, 연 약 2만원)로 올려야 한다.
  그러면 전달·IMAP이 열린다.
- 무료 한도: 5명 / 1도메인 / 5GB.

## 아직 안 정해진 것

- **대표 전화번호** — 인쇄물·의향확인서·데이터파기확인서에 공란으로 남아 있다.
  정해지면 명함 뒷면과 함께 채우고 PDF를 다시 뽑는다.
- **NFC 명함 여부**
