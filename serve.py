#!/usr/bin/env python3
"""하루안부 로컬 정적 서버 — 캐시 완전 비활성(no-store).
브라우저가 옛 버전을 들고 있는 문제 방지용. 그냥 링크만 열면 항상 최신본.

실행:  python3 "/Users/yechanshon/Desktop/Haru Anbu/serve.py"
링크:  http://localhost:8910/haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html
"""
import http.server
import socketserver
import os

PORT = 8910
ROOT = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 모든 응답에 캐시 금지 헤더 — 브라우저가 매번 새로 받아옴
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
        print(f"하루안부 no-cache 서버: http://localhost:{PORT}/  (root: {ROOT})")
        httpd.serve_forever()
