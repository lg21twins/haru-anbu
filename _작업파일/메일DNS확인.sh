#!/usr/bin/env bash
# team@haruanbu.site (Zoho Mail) DNS 설정 확인기
#
#   bash _작업파일/메일DNS확인.sh
#
# 가비아 DNS에 레코드를 넣은 뒤 이걸 돌린다.
# 전부 [OK]가 되면 Zoho 관리자 화면에서도 초록불이 뜬다.
# 반영에는 수분~수시간이 걸린다 — [ ]가 있으면 시간을 두고 다시 돌린다.

DOMAIN="haruanbu.site"
MAIL="team@${DOMAIN}"
ok=0; miss=0

# 로컬 리졸버는 오래된 응답을 캐시해 방금 넣은 레코드를 "없음"으로 잘못 보고한다.
# 공용 리졸버에 직접 묻는다. 그것도 안 잡히면 가비아 권한 서버로 한 번 더 확인한다.
R="@1.1.1.1"
AUTH="@ns.gabia.co.kr"
lookup () { # $1=타입 $2=이름
  local v
  v=$(dig +short "$1" "$2" $R | tr -d '"')
  [ -z "$v" ] && v=$(dig +short "$1" "$2" $AUTH | tr -d '"')
  echo "$v"
}

say () { # $1=상태 $2=이름 $3=설명
  if [ "$1" = "ok" ]; then printf "  [OK]  %-22s %s\n" "$2" "$3"; ok=$((ok+1))
  else                     printf "  [  ]  %-22s %s\n" "$2" "$3"; miss=$((miss+1)); fi
}

echo "== ${DOMAIN} 메일 DNS 확인 =="
echo

echo "1. 홈페이지 레코드 (건드리면 안 되는 것)"
A=$(lookup A "$DOMAIN" | head -1)
W=$(lookup CNAME "www.$DOMAIN" | head -1)
[ -n "$A" ] && say ok "A(@)" "$A" || say no "A(@)" "없음 — 홈페이지가 죽는다. 확인 필요"
[ -n "$W" ] && say ok "CNAME(www)" "$W" || say no "CNAME(www)" "없음"
echo

echo "2. 수신 (MX) — 없으면 메일이 아예 안 온다"
MX=$(lookup MX "$DOMAIN")
if [ -z "$MX" ]; then
  say no "MX" "레코드 없음"
else
  echo "$MX" | while read -r pri host; do say ok "MX $pri" "$host"; done
  echo "$MX" | grep -qi "zoho" || echo "         주의: zoho 계열이 아닌 MX가 있다"
fi
echo

echo "3. 발신 신뢰 (SPF / DKIM / DMARC) — 없으면 스팸함으로 간다"
SPF=$(lookup TXT "$DOMAIN" | grep -i "v=spf1")
DKIM=$(lookup TXT "zmail._domainkey.$DOMAIN" | grep -i "v=DKIM1")
DMARC=$(lookup TXT "_dmarc.$DOMAIN" | grep -i "v=DMARC1")
[ -n "$SPF" ]   && say ok "TXT SPF"   "$SPF"                  || say no "TXT SPF"   "없음 (@ / v=spf1 include:zoho.com ~all)"
[ -n "$DKIM" ]  && say ok "TXT DKIM"  "$(echo "$DKIM" | cut -c1-40)..." || say no "TXT DKIM"  "없음 (zmail._domainkey / Zoho가 생성해주는 값)"
[ -n "$DMARC" ] && say ok "TXT DMARC" "$DMARC"                || say no "TXT DMARC" "없음 (_dmarc / v=DMARC1; p=none; rua=mailto:${MAIL})"
echo

echo "4. 소유권 인증 TXT (Zoho verify 단계에서만 필요, 끝나면 지워도 됨)"
lookup TXT "$DOMAIN" | grep -i "zoho-verification" | sed 's/^/       /' || true
lookup TXT "$DOMAIN" | grep -qi "zoho-verification" || echo "       (없음 — 이미 인증을 마쳤다면 정상)"
echo

echo "-- 결과: ${ok}개 확인 / ${miss}개 미설정"
if [ "$miss" -eq 0 ]; then
  echo "   전부 잡혔다. mail.zoho.com 로그인 후 개인 메일에서 ${MAIL} 로 테스트 발송해볼 것."
else
  echo "   미설정 항목은 My가비아 > DNS 관리툴 > ${DOMAIN} 에서 추가한다."
  echo "   방금 넣었다면 반영 대기중일 수 있다 (수분~수시간)."
fi
