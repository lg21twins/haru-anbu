#!/bin/bash
# making-of-v2 (7-Act 재구성된 새 버전) dev 서버 띄우기
# 원본(3000)과 동시에 띄울 수 있도록 PORT=3001 사용
# 이 파일 더블클릭하면 자동으로 실행됨

cd "$(dirname "$0")/making-of-v2" || exit 1

echo ""
echo "════════════════════════════════════════════════════════"
echo "  하루안부 — Making Of (v2 · 7-Act 재구성)"
echo "  http://localhost:3001"
echo "════════════════════════════════════════════════════════"
echo ""

# node_modules가 symlink로 setup되어 있으면 그대로 사용. 없으면 install.
if [ ! -e "node_modules" ]; then
  echo "▶ 의존성 설치 중 (최초 1회)..."
  npm install
fi

PORT=3001 npm run dev
