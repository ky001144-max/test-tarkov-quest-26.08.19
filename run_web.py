import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format%args}\n")

def find_available_port(start_port=8080):
    import socket
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1
    return start_port

if __name__ == "__main__":
    port = find_available_port(PORT)
    url = f"http://localhost:{port}"
    print(f"==================================================")
    print(f"  타르코프 퀘스트 가이드 (Tarkov Quest Guide) 웹 서버")
    print(f"  서버 주소: {url}")
    print(f"  디렉터리: {DIRECTORY}")
    print(f"  종료하려면 Ctrl+C 를 누르세요.")
    print(f"==================================================")

    # Open browser automatically
    webbrowser.open(url)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
