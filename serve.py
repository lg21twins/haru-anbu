#!/usr/bin/env python3
"""하루안부 로컬 정적 서버 — 캐시 완전 비활성(no-store).
브라우저가 옛 버전을 들고 있는 문제 방지용. 그냥 링크만 열면 항상 최신본.

실행:  python3 "/Users/yechanshon/Desktop/Haru Anbu/serve.py"
링크:  http://localhost:8910/haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html
"""
import http.server
import os
import socket

PORT = 8910
ROOT = os.path.dirname(os.path.abspath(__file__))


def lan_ip():
    """폰에서 열 때 쓸 주소. 실제로 나가는 인터페이스의 IP 를 고른다."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))      # 패킷은 보내지 않는다 — 경로만 물어본다
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 모든 응답에 캐시 금지 헤더 — 브라우저가 매번 새로 받아옴
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    os.chdir(ROOT)
    # TCPServer 는 한 번에 요청 하나만 처리한다. 브라우저가 연결을 붙들고 있으면
    # (탭을 열어둔 채 두면 흔하다) 서버 전체가 멎어 폰에서는 아예 열리지 않았다.
    # ThreadingHTTPServer 는 연결마다 스레드를 띄워 서로를 막지 않는다.
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    http.server.ThreadingHTTPServer.daemon_threads = True
    with http.server.ThreadingHTTPServer(("", PORT), NoCacheHandler) as httpd:
        print(f"하루안부 no-cache 서버")
        print(f"  맥   : http://localhost:{PORT}/haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html")
        print(f"  폰   : http://{lan_ip()}:{PORT}/haru-anbu-showcase-v8-bundle/haru-anbu-showcase-v8.html")
        print(f"  root : {ROOT}")
        httpd.serve_forever()
