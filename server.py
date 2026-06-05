#!/usr/bin/env python3
"""
HTTP server for STM32F103C8T6 Projects showcase.
Serves static files only (no auth needed).
"""
import os
import sys
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProjectHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()


def find_available_port(preferred=8083, max_try=10):
    for port in range(preferred, preferred + max_try):
        try:
            s = HTTPServer(('', port), ProjectHandler)
            s.server_close()
            return port
        except OSError:
            continue
    return preferred + max_try


if __name__ == '__main__':
    preferred = int(sys.argv[1]) if len(sys.argv) > 1 else 8083
    port = find_available_port(preferred)
    server = HTTPServer(('', port), ProjectHandler)
    print(f'╔══════════════════════════════════════════╗')
    print(f'║  STM32F103 项目合集 - 服务器已启动       ║')
    print(f'║  http://localhost:{port}/' + ' ' * (33 - len(str(port))) + '║')
    print(f'║                                          ║')
    print(f'║  智能家居 · 智能门锁 · 智能消防           ║')
    print(f'╚══════════════════════════════════════════╝')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
        server.server_close()
