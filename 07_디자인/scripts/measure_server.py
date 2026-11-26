#!/usr/bin/env python3
"""성능·점검 측정용 정적 서버 (저장소 루트를 서빙, 캐시 허용).

    python3 07_디자인/scripts/measure_server.py [포트=8000] &

기본 `python3 -m http.server` 는 접속 대기열이 5 라서 iframe 이 한꺼번에 자원을 부르면 `ERR_CONNECTION_RESET` 이 간헐로 난다
(페이지 결함이 아니다 — 실패 요청이 생기고 LCP 도 부풀어 보인다). 여기서는 대기열을 512 로 키우고 스레드로 처리한다.
`serve.py`(no-cache)는 쓰지 않는다 — 매번 폰트·CSS 를 다시 받아 수치가 부풀려진다.
"""
import http.server, os, socketserver, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    request_queue_size = 512
    daemon_threads = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"http://127.0.0.1:{port}  (root: {ROOT})")
    Server(("127.0.0.1", port), Handler).serve_forever()
