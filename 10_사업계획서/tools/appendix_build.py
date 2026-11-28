#!/usr/bin/env python3
"""하루안부 사업계획서 부록 — 세로(A4) · 가로(A4) 두 판을 같은 내용으로 굽는다.
    python3 tools/appendix_build.py
    → 부록/index.html · 부록/index_가로.html
      부록/하루안부_사업계획서_부록_세로.pdf · _가로.pdf (+ ~/Desktop/하루안부_달란트_부록_세로.pdf · _가로.pdf)
2026-11-26 사용자: "PARALLAX 부록처럼" · "15장 내외" · "디테일하게, 디자인 위계 신경 쓰고 깔끔하게"
· "배치 이게 최선이냐" · "(온보딩 쪽) 빼라" · "다른 쪽도 점검해서 최적 배치로, 세로 하나 가로 하나".
배치 규칙
- 폰 쪽: 같은 크기 폰을 한 줄(3대 또는 2대), 설명은 폰 아래 같은 폭. 남는 자리에 '자세히' 카드 2장(실제 화면을 약 2배로 자른 것).
  세로판은 카드가 아래 줄, 가로판은 오른쪽 단.
- 태블릿 · 전후 비교 · 개발 범위 · 배포 쪽도 방향마다 따로 짠다.
그림: tools/capture_mockup.py(화면) → tools/device_png.py(기기 목업) → 부록/그림/. 자세히 카드는 부록/그림/x_*.jpg(cap2 를 360×193 CSS px 로 자름).
넣지 않는 화면(계획서 "앱은 의료적 판단을 하지 않습니다"와 충돌하거나 틀림): 의료진 웹 대시보드, 의료진 수신함 · SBAR, 보호자 처방전, 결제(본인부담 금액 불일치).
"""
import pathlib, shutil
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "부록"
DESK = pathlib.Path.home() / "Desktop"
G = "그림/"
TOTAL = 13

FONT_CSS = "".join(f"@font-face {{ font-family: 'Haru Pretendard'; src: url('fonts/Pretendard-{n}.otf') format('opentype'); font-weight: {w}; }}\n"
                   for n, w in [('Regular', 400), ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800)])
BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { background: #e4e8ec; font-family: 'Haru Pretendard', 'Pretendard JP', 'Pretendard', 'Apple SD Gothic Neo', sans-serif; color: #0b1220; word-break: keep-all; }
.pg { position: relative; margin: 10mm auto; background: #fff; box-shadow: 0 2px 12px rgba(11,18,32,.16); overflow: hidden; display: flex; flex-direction: column; }
.top { display: flex; justify-content: space-between; font-size: 7.5pt; color: #7a8693; padding-bottom: 3mm; border-bottom: .25mm solid #e3e7ec; }
.ttl { display: flex; align-items: baseline; gap: 3.5mm; }
.ttl .no { font-size: 11pt; font-weight: 800; color: #2C7AFC; }
.ttl h2 { font-size: 19pt; font-weight: 700; letter-spacing: -.01em; }
.sub { font-size: 10pt; color: #4b5866; line-height: 1.5; }
figure { min-width: 0; }
figure img { display: block; }
.f8 { filter: drop-shadow(0 2mm 2.4mm rgba(11,18,32,.20)) drop-shadow(0 .4mm .6mm rgba(11,18,32,.12)); }
.scr { border: .25mm solid #dde3ea; border-radius: 1.2mm; width: 100%; }
.col { display: flex; flex-direction: column; align-items: center; }
figcaption { font-size: 8.3pt; line-height: 1.6; color: #4b5866; margin-top: 3mm; width: 100%; }
figcaption b { display: block; color: #0b1220; font-weight: 700; font-size: 10pt; letter-spacing: -.01em; margin-bottom: 1mm; }
figcaption b em { font-style: normal; color: #2C7AFC; font-weight: 800; margin-right: 1.8mm; }
.side { display: flex; gap: 5mm; align-items: center; }
.side figcaption { margin-top: 0; }
.foot { margin-top: auto; font-size: 7.3pt; line-height: 1.55; color: #7a8693; padding-top: 3mm; border-top: .25mm solid #e3e7ec; }
.dc { background: #f4f7fb; border-radius: 2mm; padding: 3.5mm 4mm 4mm; }
.dc .dl { font-size: 7.6pt; font-weight: 700; color: #2C7AFC; letter-spacing: .02em; margin-bottom: 2.2mm; }
.dc .dl span { color: #0b1220; margin-left: 1.5mm; }
.dc img { display: block; width: 100%; height: auto; border-radius: 1.4mm; border: .25mm solid #dde3ea; background: #fff; }
.g4 { display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 8mm; row-gap: 0; }
.g4 .gm { display: flex; justify-content: center; align-items: flex-start; }
.g4 .gc figcaption { margin-top: 4mm; }
.g4 .gk { display: flex; flex-direction: column; justify-content: space-between; height: 100%; }
.dc .dn { font-size: 8pt; line-height: 1.55; color: #4b5866; margin-top: 2.4mm; }
.box { background: #f4f7fb; border-radius: 1.6mm; padding: 4mm 5mm; font-size: 8.6pt; line-height: 1.6; color: #2b3542; }
.box h4 { font-size: 9.6pt; color: #0b1220; margin-bottom: 1.5mm; }
.box ul { padding-left: 4mm; }
.stats b { display: block; font-size: 22pt; font-weight: 800; letter-spacing: -.02em; color: #2C7AFC; line-height: 1.1; }
.stats span { display: block; font-size: 9.4pt; font-weight: 700; margin-top: 1.2mm; }
.stats em { display: block; font-style: normal; font-size: 7.8pt; color: #4b5866; margin-top: .6mm; line-height: 1.5; }
.arrow { text-align: center; font-size: 8pt; color: #2C7AFC; font-weight: 700; line-height: 1.5; }
.arrow .ln { font-size: 20pt; line-height: 1; }
.arrow .g { color: #7a8693; font-weight: 400; }
.tagb { display: inline-block; font-size: 7.4pt; font-weight: 700; padding: .7mm 2.2mm; border-radius: 3mm; margin-bottom: 2mm; }
.before { background: #fdecec; color: #b42318; } .after { background: #e7f6ec; color: #11743b; }
.logo { display: flex; align-items: center; gap: 3mm; }
.logo img { height: 10mm; }
.logo span { font-size: 17pt; font-weight: 800; letter-spacing: -.02em; }
.cover h1 { font-size: 28pt; line-height: 1.25; font-weight: 700; letter-spacing: -.015em; }
.cover .cv-sub { font-size: 11pt; color: #4b5866; margin-top: 4mm; }
.toc { list-style: none; border-top: .25mm solid #e3e7ec; }
.toc li { display: grid; grid-template-columns: 10mm 40mm 1fr 7mm; align-items: baseline; padding: 2.2mm 0; border-bottom: .25mm solid #e3e7ec; font-size: 9.4pt; }
.toc b { font-weight: 800; font-size: 9pt; color: #2C7AFC; }
.toc span { font-weight: 700; }
.toc em { font-style: normal; color: #4b5866; font-size: 8.4pt; }
.toc i { font-style: normal; color: #7a8693; font-size: 8pt; text-align: right; }
.cv-foot { font-size: 8pt; line-height: 1.6; color: #4b5866; }
.cv-foot p + p { margin-top: 2mm; color: #0b1220; }
@media print { body { background: #fff; } .pg { margin: 0; box-shadow: none; break-after: page; } }
"""
PORTRAIT_CSS = """@page { size: A4; margin: 0; }
.pg { width: 210mm; height: 297mm; padding: 13mm 15mm 12mm; }
.top { margin-bottom: 7mm; } .sub { margin: 2mm 0 7mm; }"""
LAND_CSS = """@page { size: A4 landscape; margin: 0; }
.pg { width: 297mm; height: 210mm; padding: 11mm 15mm 10mm; }
.top { margin-bottom: 5mm; } .sub { margin: 1.5mm 0 5mm; }"""

TOC = [('00', '서비스 한눈에', '기록 한 번 → 가족 · 의료진 · 어르신', 2),
       ('01', '요양보호사 앱', '오늘 · 케어 기록 · 소통 · 근무 일정 · 내 정보', 3),
       ('02', '외국인 요양보호사', '같은 기록 화면의 영어 · 중국어판', 5),
       ('03', '가족(보호자) 앱', '일일 리포트 · 알림 · 대화 · 의료 타임라인 · 확인 요청', 6),
       ('04', '의료진 앱', '요양보호사 보고 확인 · 회진 모드 · 긴급 호출', 8),
       ('05', '어르신 태블릿', '오늘 · 도움 요청 · 가족 연결 · 약 · 메시지', 9),
       ('06', '판단하지 않는 앱', '문구 수정 전후 — 의료기기(SaMD) 경계', 11),
       ('07', '첫 개발 범위 · 파일럿', '기록 → 가족 리포트 한 축', 12),
       ('08', '공개 배포 · 현장 검증', 'haruanbu.site · KHF 2026', 13)]

PHONE_PAGES = [
  dict(i=3, no='01', title='요양보호사 앱 ①', sub='모든 화면의 출발점. 근무 중 할 일 순서대로 기록하고, 그 기록이 가족 · 의료진 · 어르신 화면의 재료가 됩니다.',
       phones=[('c01', '오늘', '오전 근무 진행(5/9)과 다음 일(10:15 박영자 어르신 · 혈압 측정)을 크게. 「지금 기록 시작」 한 번으로 기록이 열립니다.'),
               ('c02', '케어 기록', '담당 4명의 오늘 기록 진행(3/8 · 5/8)을 보며, 손이 바쁘면 마이크로 말해서 남깁니다.'),
               ('c03', '소통 · 인수인계', '인수인계 항목을 확인하고, 간호사 · 보호자 메시지를 한 목록에서 답합니다.')],
       details=[('c02', '이유가 붙은 할 일', '할 일마다 왜 지금인지가 함께 뜹니다 — 박영자 · 혈당 재측정, 아침 혈당 142 주의.'),
                ('c03', '인수인계 체크', '낙상 위험 · 복약 · 통증 · 배회 · 폭력 · 가족 통보를 하나씩 확인합니다(4/5). 남은 항목은 노랗게.')],
       foot='요양보호사 앱 웹 시제품(v11) 화면을 iPhone 17 Pro 틀에 넣었습니다. 390 × 844 기준, 2026.11.26 캡처. 인수인계 요약 칸은 설계만 했고 파일럿에서는 AI 없이 돌립니다(계획서 3항).'),
  dict(i=4, no='01', title='요양보호사 앱 ②', sub='기록만이 아니라 근무 자체를 앱 안에서 — 일정 · 출퇴근 · 알림을 한곳에 둡니다.',
       phones=[('c04s', '근무 일정', '이번 주 주간 · 야간 · 휴무와 함께 근무하는 동료, 월간 근무표와 근무 교환 요청까지.'),
               ('c04m', '내 정보 · 출퇴근', '자격 · 담당 어르신 · 이번 달 기록지 제출(17/20) · 보수교육, 그리고 알림 설정.')],
       details=[('c04s', '주 근무 시간', '이번 주 40시간 · 5일 근무 · 2일 휴무. 주간 · 야간을 색으로 구분합니다.'),
                ('c04m', '출퇴근 · 긴급 알림', '시설 위치 확인으로 출퇴근을 남기고, 동료의 SOS를 받는 알림을 켭니다.')],
       foot='요양보호사 앱 웹 시제품(v11). 390 × 844 기준, 2026.11.26 캡처.'),
  dict(i=5, no='02', title='외국인 요양보호사', sub='현장의 요양보호사 중에는 한국어가 모국어가 아닌 분도 있습니다. 같은 기록 화면을 영어 · 중국어로 씁니다.',
       phones=[('c02en', 'Care Records', '케어 기록 화면의 영어판. 할 일 · 이유 · 진행이 같은 자리에 있어 일하는 순서가 같습니다.'),
               ('c02zh', '护理记录', '같은 화면의 중국어판. 이름 · 호실 · 수치는 그대로 두고 안내 문장만 바꿉니다.'),
               ('c03zh', '沟通', '소통 · 인수인계의 중국어판. 가족에게 가는 리포트는 한국어로 나갑니다.')],
       details=[('c02en', 'English', 'Due now · Ms. Park · Recheck blood sugar — 이유(morning glucose 142, watch)도 그대로 옮깁니다.'),
                ('c02zh', '中文', '当前待办 · 朴奶奶 · 复测血糖 — 같은 카드, 같은 순서, 같은 버튼.')],
       foot='영어 23개 · 중국어 5개 화면을 만들었습니다(계획서 1항). 이 쪽은 그중 요양보호사 앱 세 화면입니다. 2026.11.26 캡처.'),
  dict(i=6, no='03', title='가족(보호자) 앱 ①', sub='전화로 묻지 않아도 매일 오늘의 부모님을 압니다. 놀라게 하는 경고 대신, 있었던 일을 있는 그대로 전합니다.',
       phones=[('g01', '일일 리포트', '가장 먼저 안심할 한 줄, 그 아래 오늘의 사진과 한마디, 투약 · 맥박 요약. 첫 개발 범위의 도착점입니다(12쪽).'),
               ('g06', '알림', '측정 → 도착 → 재측정 시간을 보여 주고, 담당 간호사에게 바로 전화합니다.'),
               ('g03n', '간호사와 대화', '궁금한 것을 담당 간호사에게 직접 묻고, 답과 사진을 받습니다.')],
       details=[('g06', '판단 대신 사실', '「혈압 이상 감지」가 아니라 「혈압이 평소보다 높게 측정됐어요」. 150/95 · 5분 경과 · 2:35 재측정.'),
                ('g01', '돌본 사람의 한마디', '"오전 산책 때 햇빛이 좋아서 한참 머무르셨어요." — 누가 몇 시에 남겼는지까지(김서연 간호사 · 10:24).')],
       foot='보호자 앱 웹 시제품(v11). 390 × 844 기준, 2026.11.26 캡처.'),
  dict(i=7, no='03', title='가족(보호자) 앱 ②', sub='매일의 안부 너머 — 의료 기록 · 가족의 확인이 필요한 일 · 가족끼리의 대화까지.',
       phones=[('g10', '의료 타임라인', '처방 변경 · 검사 · 진료 · 긴급을 시간순으로. 의료진의 기록을 가족이 같은 순서로 봅니다.'),
               ('g03s', '소통 · 확인 요청', '처치 안내 · 투약 시간 변경처럼 가족의 확인이 필요한 일을 버튼 하나로 답합니다.'),
               ('g03f', '가족 그룹 채팅', '형제자매가 한 방에서 부모님 소식을 나눕니다. 각자 전화로 되묻지 않아도 됩니다.')],
       details=[('g10', '처방 변경도 가족에게', '도네페질 5mg → 10mg 증량(4월 1일). 인지기능 평가 결과와 다음 모니터링 계획까지.'),
                ('g03s', '확인 · 동의 버튼', '혈당 검사 처치 안내는 「확인」, 저녁 투약 18:00 → 18:30 변경은 「동의」로 답합니다.')],
       foot='보호자 앱 웹 시제품(v11). 390 × 844 기준, 2026.11.26 캡처.'),
  dict(i=8, no='04', title='의료진 앱', sub='앱은 판단하지 않습니다. 현장 기록을 시간순으로 모아 보여 주고, 확인과 판단은 의료진이 직접 합니다.',
       phones=[('d01', '요양보호사 보고 확인', '오늘 올라온 보고를 확인 전 · 확인함으로 나눠, 놓친 보고가 없게 합니다.'),
               ('d02', '회진 모드', '2차 라운드 8/15 진행 중. 다음 환자와 지난 라운드 이력을 보며 이어서 기록합니다.'),
               ('dsos', '긴급 호출', '요양보호사의 SOS를 한 화면에. 13초 안에 응답이 없으면 자동 통화, 보호자에게도 알립니다.')],
       details=[('d01', '사람이 남긴 보고', '최명자 어르신 · 혈압 180/110 · 13:50 요양보호사 기록, 메모 "혈압이 높아 재측정 부탁드립니다". 확인은 의료진이 누릅니다.'),
                ('dsos', '누가 · 어디서 · 언제', '최명자 어르신 · 2층 B-1호(스테이션에서 도보 40초) · 의식 저하 · 14:08:32 발생.')],
       foot='의료진 앱 웹 시제품(v15). 첫 화면은 판단 표현을 걷어 낸 문구 수정안을 적용해 찍었습니다(11쪽). 390 × 844 기준, 2026.11.26 캡처.'),
]

TAB1 = [('p01', '오늘', '가족 소식(딸이 보낸 사진 · 문자)과 고르기만 하면 되는 답장, 약 먹을 시간의 「먹었어요」, 가족에게 전화가 한 화면에. 맨 아래 가장 큰 두 버튼은 말로 하기와 도움 요청.'),
        ('p08', '도움 요청', '물 한 잔 · 화장실 · 식사 · 약 · 자세 · 온도, 그리고 아파요. 누르면 보호자에게 바로 알립니다.'),
        ('p03', '가족과 연결', '접속 중인 가족에게 바로 영상통화, 받은 사진 · 음성 메시지를 다시 봅니다.')]
TAB2 = [('p02', '오늘의 일정', '식사 · 약 · 측정 진행(4/7). 지금 할 일(점심 약)은 크게, 「다 먹었어요」 한 번이면 끝.'),
        ('p10', '약 잘 드셨어요', '먹은 약 세 가지와 다음 약 시간. 가족에게 「약 드셨어요」 소식이 자동으로 갑니다.'),
        ('p07', '가족 메시지', '딸의 사진과 메시지에 답장 버튼(예쁘구나 · 고맙다고 전해 줘)이나 음성으로 답합니다.'),
        ('p06', '사진 크게 보기', '받은 사진을 한 장씩 크게 넘겨 보고, 그 자리에서 답장하거나 전화합니다.')]
BEFORE = '「즉시 확인」 태그 · 「직전 162/96 대비 상승」 · 「권장: 재측정 · 담당의 보고 · 회진 우선순위 상향」 · 「AI 판단 · 오늘의 우선순위」 — 앱이 긴급도를 정하고 임상 권고를 내는 표현.'
AFTER = '「요양보호사 보고」 · 「13:50 요양보호사 기록」 · 메모 「혈압이 높아 재측정 부탁드립니다 — 이수진 요양보호사」 · 「오늘 올라온 보고」 · 「확인 전」 — 사람이 남긴 것을 전달만 합니다.'
SAME = '<h4>같은 원칙을 가족 화면에도</h4>알림 문구 「혈압 이상 감지」를 「혈압이 평소보다 높게 측정됐어요」로 바꾸고(6쪽), 판단은 간호 인력 확인 흐름으로 넘겼습니다. 개인정보보호법 · 의료법 · 노인장기요양보험법을 조문 단위로 대조해 화면 문구와 기능 범위를 정했습니다(계획서 1 · 3항).'
HAVE = '<h4>지금 있는 것</h4><ul><li>4역할 앱 · 웹 39개 화면(공개 배포)</li><li>개인정보 별도 동의 · 역할별 권한 설계</li><li>디자인 토큰 357개와 자동 검사 도구</li></ul>'
NOTYET = '<h4>아직 없는 것 → 첫 개발</h4><ul><li>서버 · 데이터베이스 · 로그인 · 푸시 알림</li><li>AI 요약(효용 확인 뒤 켬)</li><li>어르신 · 의료진 화면 연결은 다음 단계</li></ul>'
PILOT = '<h4>파일럿(2027.03 ~ 04)</h4>경기 남부 요양시설 1곳 · 8주 무상. 사전 · 사후로 <b>리포트 열람률</b>과 <b>가족 문의 전화 변화</b>를 잽니다. 1차 목표는 요양보호사의 기록 총량이 늘지 않는 것.'
WHO = '<h4>누가 무엇을 받나</h4><ul><li><b>요양보호사</b> — 하루 한 번 기록(목표 5분), 체크 항목 위주.</li><li><b>가족</b> — 매일 도착하는 일일 리포트.</li><li><b>의료진</b> — 측정값과 현장 메모를 시간순으로. 판단은 의료진이.</li><li><b>어르신</b> — 큰 글씨 · 큰 버튼 한 화면.</li></ul>'
WHY = '<h4>왜 한 번의 기록인가</h4><ul><li>가족의 같은 질문("오늘 어떠셨어요?")이 매일 전화로 요양팀에 몰립니다.</li><li>기록은 이미 남기고 있습니다. 가족에게 닿는 길이 비어 있을 뿐입니다.</li><li>새 일을 더하지 않고, 이미 하는 기록을 네 화면으로 나눠 보냅니다.</li></ul>'
STATS = [('4', '역할', '요양보호사 · 가족 · 의료진 · 어르신'), ('39', '화면', '앱 · 웹 고유 화면, 공개 배포'),
         ('357', '디자인 토큰', '자동 검사로 일관성 · 접근성 점검'), ('23 · 5', '영어 · 중국어 화면', '외국인 요양보호사 대응')]


def top(i, cover=False):
    left = "2026 계원예술대학교 달란트 창업경진대회" if cover else "하루안부 사업계획서 부록"
    return f'<header class="top"><span>{left}</span><span>{i:02d} / {TOTAL:02d}</span></header>'

def ph(n, h):  return f'<img class="f8" src="{G}{n}.png" style="height:{h}mm;width:auto" alt="">'
def tab(n, w): return f'<img class="f8" src="{G}{n}.png" style="width:{w}mm;height:auto" alt="">'

def cap(n, title, text):
    if not title: return f'<figcaption>{text}</figcaption>'
    num = f'<em>{n:02d}</em>' if isinstance(n, int) else ''
    return f'<figcaption><b>{num}{title}</b>{text}</figcaption>'

def dcard(n, title, note, w=None):
    st = f' style="width:{w}mm"' if w else ''
    return f'<div class="dc"{st}><p class="dl">자세히<span>{title}</span></p><img src="{G}x_{n}.jpg" alt=""><p class="dn">{note}</p></div>'

def page(i, no, title, sub, body, foot):
    return (f'\n\n<!-- ===== {i:02d}쪽 · {title} ===== -->\n<section class="pg">{top(i)}<div class="ttl"><span class="no">{no}</span><h2>{title}</h2></div>'
            f'<p class="sub">{sub}</p>{body}<p class="foot">{foot}</p></section>')

def stats_html(cols):
    cells = ''.join(f'<div><b>{a}</b><span>{b}</span><em>{c}</em></div>' for a, b, c in STATS)
    return f'<div class="stats" style="display:grid;grid-template-columns:repeat({cols},1fr);gap:4mm">{cells}</div>'


def build(land):
    P = []
    toc = ''.join(f'<li><b>{a}</b><span>{b}</span><em>{c}</em><i>{d:02d}</i></li>' for a, b, c, d in TOC)
    head = (f'<div class="logo"><img src="{G}logo.svg" alt=""><span>하루안부</span></div>'
            f'<h1 style="margin-top:{8 if land else 10}mm">사업계획서 부록<br>실제 화면</h1>'
            f'<p class="cv-sub">요양원 가족 소통 서비스 — 한 번의 기록이, 네 사람에게 각자의 언어로</p>')
    cfoot = ('<div class="cv-foot"><p>모든 화면은 같은 요양시설, 같은 입소자 네 명(박영자 78 · A-3 / 최명자 82 · B-1 / 김순자 79 · B-2 / 이정숙 85 · A-7)의 하루를 각자의 자리에서 본 것입니다. '
             '화면 속 시설 · 인물 · 기록은 시연용 가상 자료이고, 인물 사진은 AI 생성 이미지입니다.</p>'
             '<p><b>팀 노인과 바다</b> · 대표 손예찬 · 김지욱 · 고해은 · 계원예술대학교 디지털미디어디자인과</p></div>')
    if land:
        P.append(f'''<section class="pg cover">{top(1, True)}<div style="display:grid;grid-template-columns:132mm 1fr;gap:12mm;flex:1;margin-top:4mm">
<div style="display:flex;flex-direction:column">{head}<ol class="toc" style="margin-top:7mm">{toc}</ol><div style="margin-top:auto">{cfoot}</div></div>
<div class="col" style="justify-content:center;gap:6mm">{tab("p01", 118)}<div style="display:flex;gap:7mm">{ph("g01", 66)}{ph("c02", 66)}{ph("d01", 66)}</div></div></div></section>''')
    else:
        P.append(f'''<section class="pg cover">{top(1, True)}<div style="margin:8mm 0 8mm">{head}</div>
<div style="display:flex;align-items:flex-end;justify-content:center;gap:4mm;margin-bottom:8mm">{tab("p01", 92)}{ph("g01", 64)}{ph("c02", 64)}{ph("d01", 64)}</div>
<ol class="toc">{toc}</ol><div style="margin-top:auto">{cfoot}</div></section>''')

    if land:
        body = (f'<div class="col"><img src="{G}flow.jpg" style="width:236mm" alt=""></div>'
                f'<div class="g4" style="margin-top:6mm;align-items:stretch">'
                f'<div class="box">{WHO}</div><div class="box">{WHY}</div><div style="grid-column:span 2;padding:2mm 0 0 4mm;border-left:.25mm solid #e3e7ec">{stats_html(2)}</div></div>')
    else:
        body = (f'<div class="col"><img src="{G}flow.jpg" style="width:180mm" alt=""></div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm"><div class="box">{WHO}</div><div class="box">{WHY}</div></div>'
                f'<div style="margin-top:9mm;padding-top:6mm;border-top:.25mm solid #e3e7ec">{stats_html(4)}</div>')
    P.append(page(2, '00', '서비스 한눈에', '요양보호사가 한 번 남긴 기록이 받는 사람마다 다른 언어로 도착합니다. 입력하는 사람은 한 명, 받는 사람은 셋.', body,
                  '흐름도는 공개 시제품의 실제 화면으로 만들었습니다. 숫자는 사업계획서 1항과 같습니다(2026.11 기준).'))

    for d in PHONE_PAGES:
        n = len(d['phones'])
        if land:
            H = 118
            media = ''.join(f'<div class="gm" style="grid-column:{k + 1};grid-row:1">{ph(a, H)}</div>' for k, (a, _, _) in enumerate(d['phones']))
            caps = ''.join(f'<div class="gc" style="grid-column:{k + 1};grid-row:2">{cap(k + 1, b, c)}</div>' for k, (a, b, c) in enumerate(d['phones']))
            cards = ''.join(dcard(a if n == 3 else a + '_w', b, c) for a, b, c in d['details'])
            body = (f'<div class="g4" style="grid-template-rows:{H}mm auto">{media}'
                    f'<div class="gk" style="grid-column:{n + 1} / 5;grid-row:1">{cards}</div>{caps}</div>')
        else:
            h, cw = (108, 57) if n == 3 else (128, 86)
            figs = ''.join(f'<figure class="col" style="width:{cw}mm">{ph(a, h)}{cap(k + 1, b, c)}</figure>' for k, (a, b, c) in enumerate(d['phones']))
            cards = ''.join(dcard(a, b, c, 87) for a, b, c in d['details'])
            body = (f'<div style="display:flex;justify-content:space-between;gap:4mm">{figs}</div>'
                    f'<div style="display:flex;justify-content:space-between;margin-top:auto;margin-bottom:5mm">{cards}</div>')
        P.append(page(d['i'], d['no'], d['title'], d['sub'], body, d['foot']))

    (a1, t1, x1), (a2, t2, x2), (a3, t3, x3) = TAB1
    if land:
        body = (f'<div style="display:grid;grid-template-columns:1fr 84mm;column-gap:10mm;align-items:start"><figure>{tab(a1, 160)}{cap(1, t1, x1)}</figure>'
                f'<div style="display:flex;flex-direction:column;gap:5mm"><figure>{tab(a2, 84)}{cap(2, t2, x2)}</figure><figure>{tab(a3, 84)}{cap(3, t3, x3)}</figure></div></div>')
    else:
        body = (f'<figure>{tab(a1, 180)}{cap(1, t1, x1)}</figure>'
                f'<div style="display:flex;justify-content:space-between;margin-top:7mm"><figure style="width:87mm">{tab(a2, 87)}{cap(2, t2, x2)}</figure>'
                f'<figure style="width:87mm">{tab(a3, 87)}{cap(3, t3, x3)}</figure></div>')
    P.append(page(9, '05', '어르신 태블릿 ①', '큰 글씨, 큰 버튼, 메뉴는 넷(홈 · 할 일 · 가족 · 도움). 읽지 않아도 누를 수 있게 만들었습니다.', body,
                  '어르신 앱 웹 시제품(v12) 화면을 iPad Pro 11" 틀에 넣었습니다. 1210 × 834 기준, 2026.11.26 캡처.'))

    if land:
        cells = ''.join(f'<figure class="side" style="align-items:flex-start">{tab(a, 86)}<div style="padding-top:8mm">{cap(k + 1, b, c)}</div></figure>' for k, (a, b, c) in enumerate(TAB2))
        body = f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:9mm 10mm">{cells}</div>'
    else:
        cells = ''.join(f'<figure>{tab(a, 87)}{cap(k + 1, b, c)}</figure>' for k, (a, b, c) in enumerate(TAB2))
        body = f'<div style="display:grid;grid-template-columns:87mm 87mm;justify-content:space-between;gap:9mm 0">{cells}</div>'
    P.append(page(10, '05', '어르신 태블릿 ②', '하루의 할 일과 가족의 소식이, 누르는 한 번으로 끝나도록.', body, '어르신 앱 웹 시제품(v12). 1210 × 834 기준, 2026.11.26 캡처.'))

    if land:
        cell = lambda tag, cls, n, txt: (f'<figure class="side" style="width:128mm;align-items:flex-start">{ph(n, 118)}<div style="padding-top:10mm"><span class="tagb {cls}">{tag}</span>{cap("", "", txt)}</div></figure>')
        body = (f'<div style="display:flex;justify-content:space-between">{cell("수정 전", "before", "d01o", BEFORE)}{cell("수정 후", "after", "d01", AFTER)}</div>'
                f'<div class="box" style="margin-top:5mm">{SAME}</div>')
    else:
        cell = lambda tag, cls, n, txt: (f'<figure class="col" style="width:84mm"><span class="tagb {cls}">{tag}</span>{ph(n, 132)}{cap("", "", txt)}</figure>')
        body = (f'<div style="display:flex;justify-content:space-around">{cell("수정 전", "before", "d01o", BEFORE)}{cell("수정 후", "after", "d01", AFTER)}</div>'
                f'<div class="box" style="margin-top:auto;margin-bottom:5mm">{SAME}</div>')
    P.append(page(11, '06', '판단하지 않는 앱', '이상 감지 · 위험도 판정 · 복약 판단을 넣는 순간 의료기기(SaMD) 허가 대상이 됩니다. 그래서 판단의 주체를 앱에서 사람으로 되돌렸습니다.', body,
                  '수정 전은 공개 시제품(v15) 원본, 수정 후는 같은 화면에 문구 수정안을 적용해 찍었습니다. 수정안은 다음 배포에서 공개 사이트에 반영합니다.'))

    arrow = ('<div class="arrow" style="width:40mm"><div class="ln">→</div>서버 · 데이터베이스<br>로그인 · 푸시 알림<br>'
             '<span class="g">2026.12 ~ 2027.02 개발<br>관리형 백엔드 · AI 제외</span><div class="ln">→</div></div>')
    if land:
        flow = (f'<div style="display:flex;align-items:center;gap:3mm"><figure class="col" style="width:62mm">{ph("c02", 118)}{cap(1, "요양보호사 기록", "지금 있는 화면 그대로.")}</figure>'
                f'{arrow}<figure class="col" style="width:62mm">{ph("g01", 118)}{cap(2, "가족 일일 리포트", "매일 실제로 도착하게.")}</figure></div>')
        body = (f'<div style="display:flex;gap:10mm;align-items:center">{flow}'
                f'<div style="flex:1;display:flex;flex-direction:column;gap:4mm"><div class="box">{HAVE}</div><div class="box">{NOTYET}</div><div class="box">{PILOT}</div></div></div>')
    else:
        flow = (f'<div style="display:flex;align-items:center;justify-content:center;gap:4mm"><figure class="col" style="width:62mm">{ph("c02", 112)}{cap(1, "요양보호사 기록", "지금 있는 화면 그대로.")}</figure>'
                f'{arrow}<figure class="col" style="width:62mm">{ph("g01", 112)}{cap(2, "가족 일일 리포트", "매일 실제로 도착하게.")}</figure></div>')
        body = (f'{flow}<div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:7mm"><div class="box">{HAVE}</div><div class="box">{NOTYET}</div></div>'
                f'<div class="box" style="margin-top:5mm">{PILOT}</div>')
    P.append(page(12, '07', '첫 개발 범위 · 파일럿', '네 역할을 한 번에 만들면 검증이 늦어집니다. "매일 도착한다"를 먼저 증명합니다.', body,
                  '일정 · 범위는 사업계획서 5항(연도별 계획 · 시제품 현황과 제작 계획)과 같습니다.'))

    site = f'<figure><img class="scr" src="{G}site.jpg" alt="">{cap(1, "haruanbu.site", "4역할 39개 화면을 공개 배포했습니다. 첫 화면에서 역할별 앱으로 들어가 직접 눌러 볼 수 있습니다.")}</figure>'
    khf = f'<figure><img class="scr" src="{G}khf-team.jpg" alt="">{cap(2, "KHF 2026 현장", "2026년 8월 코엑스 병원 · 헬스케어 전시회(The Intelligent Hospital)에서 현업 종사자에게 시제품을 직접 시연하고 피드백을 받았습니다.")}</figure>'
    badge = f'<figure><img class="scr" src="{G}khf-badges.jpg" alt="">{cap(3, "참가 배지", "팀 3명.")}</figure>'
    qr = f'<figure style="text-align:center"><img src="{G}qr.svg" style="width:26mm;margin:0 auto" alt=""><figcaption style="text-align:center">휴대폰으로<br>바로 열기</figcaption></figure>'
    if land:
        qrcard = (f'<div class="box" style="display:flex;gap:5mm;align-items:center"><img src="{G}qr.svg" style="width:24mm;height:24mm" alt="">'
                  f'<div><h4>haruanbu.site</h4>휴대폰 카메라로 비추면 시제품이 바로 열립니다. 4역할 39개 화면.</div></div>')
        body = (f'<div style="display:grid;grid-template-columns:1fr 96mm;column-gap:10mm;align-items:start">{site}'
                f'<div style="display:flex;flex-direction:column;gap:5mm">{khf}{qrcard}</div></div>')
    else:
        body = f'{site}<div style="display:grid;grid-template-columns:104mm 44mm 26mm;gap:3mm;margin-top:6mm;align-items:start">{khf}{badge}{qr}</div>'
    P.append(page(13, '08', '공개 배포 · 현장 검증', '화면은 그림이 아니라 실제로 열리는 시제품입니다. 현장의 이야기도 직접 들었습니다.', body,
                  '사이트 화면은 공개 쇼케이스(haruanbu.site) 첫 화면을 2026.11.26 캡처했습니다. 현장 사진은 팀이 직접 찍었습니다.'))

    assert len(P) == TOTAL, len(P)
    css = FONT_CSS + BASE_CSS + (LAND_CSS if land else PORTRAIT_CSS)
    P[0] = '\n\n<!-- ===== 01쪽 · 표지 ===== -->\n' + P[0]
    note = ('<!-- 하루안부 사업계획서 부록. 글을 고치려면 아래에서 쪽 표시(===== 03쪽 ...)를 찾아 따옴표 밖의 한국어 문장만 고치고 저장한 뒤, '
            '크롬으로 열어 인쇄 → PDF로 저장(용지 A4 ' + ('가로' if land else '세로') + ', 여백 없음, 배경 그래픽 켬). 그림은 그림/ 폴더. -->\n')
    return f'<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>하루안부 사업계획서 부록 — 실제 화면({"가로" if land else "세로"})</title><style>{css}</style></head><body>\n' + note + f'{"".join(P).replace('<figure', chr(10) + '<figure').replace('<div class="dc"', chr(10) + '<div class="dc"').replace('<div class="box"', chr(10) + '<div class="box"')}\n</body></html>'


with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for land, html_name, pdf_name in [(False, "index.html", "하루안부_사업계획서_부록_세로.pdf"), (True, "index_가로.html", "하루안부_사업계획서_부록_가로.pdf")]:
        f = OUTDIR / html_name
        f.write_text(build(land), encoding="utf-8")
        pg = b.new_page(viewport={"width": 1200, "height": 1200})
        pg.goto(f.as_uri(), wait_until="networkidle"); pg.wait_for_timeout(800)
        over = pg.evaluate("""() => [...document.querySelectorAll('.pg')].map((s,i)=>{const r=s.getBoundingClientRect();
          const bad=[...s.querySelectorAll('figure,.box,.dc,.foot,.stats')].filter(e=>{const q=e.getBoundingClientRect();return q.bottom>r.bottom-2||q.right>r.right-2}).length;return bad?i+1:0}).filter(Boolean)""")
        pg.emulate_media(media="print")
        out = OUTDIR / pdf_name
        pg.pdf(path=str(out), print_background=True, prefer_css_page_size=True)
        pg.close()
        shutil.copy(out, DESK / pdf_name.replace("사업계획서_부록", "달란트_부록"))
        print(("가로" if land else "세로"), "넘치는 쪽:", over or "없음", round(out.stat().st_size / 1024), "KB")
    b.close()
