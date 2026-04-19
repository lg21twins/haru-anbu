#!/bin/bash
# 더블클릭하면 로컬 서버 띄우고 Chrome에서 v10 보호자앱 홈 열기
# 포트: 9092 (이미 사용중이면 실패 → 터미널 메시지 확인)

cd "$(dirname "$0")"
echo ""
echo "========================================"
echo "  하루안부 v10 보호자앱 · 지욱"
echo "  포트 9092 에서 서버 띄웁니다."
echo "  종료: Ctrl+C 또는 이 창 닫기"
echo "========================================"
echo ""

# Chrome 자동 오픈 (서버 시동 대기 1초)
(sleep 1 && open -a "Google Chrome" "http://localhost:9092/g-guardian-live.html") &

# 서버 시동 (foreground — 종료 시 Ctrl+C)
python3 -m http.server 9092
