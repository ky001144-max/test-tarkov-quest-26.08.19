import os
import sys
import threading
import time
import subprocess
import http.server
import socketserver

PORT = 8085
APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=APP_DIR, **kwargs)

    def log_message(self, format, *args):
        pass

def start_server(port):
    with socketserver.TCPServer(("127.0.0.1", port), QuietHandler) as httpd:
        httpd.serve_forever()

def find_available_port(start_port=8085):
    import socket
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            port += 1
    return start_port

def run_desktop():
    port = find_available_port(PORT)
    url = f"http://127.0.0.1:{port}/index.html"

    # Start background local web server
    server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(0.5)

    print(f"==================================================")
    print(f"  타르코프 퀘스트 가이드 데스크톱 프로그램 실행 중...")
    print(f"  로컬 주소: {url}")
    print(f"==================================================")

    # 1. Try pywebview if installed
    try:
        import webview
        print("네이티브 Webview 엔진으로 실행합니다.")
        window = webview.create_window(
            title="타르코프 퀘스트 가이드 & 인터랙티브 맵",
            url=url,
            width=1400,
            height=900,
            resizable=True,
            on_top=False
        )
        webview.start()
        return
    except ImportError:
        pass

    # 2. Try Edge/Chrome App Mode on Windows (Clean frameless app window)
    if sys.platform == "win32":
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
        target_browser = None
        if os.path.exists(edge_path):
            target_browser = edge_path
        elif os.path.exists(chrome_path):
            target_browser = chrome_path

        if target_browser:
            print("전용 데스크톱 앱 윈도우 모드로 실행합니다.")
            subprocess.run([target_browser, f"--app={url}", "--window-size=1400,900"])
            return

    # 3. Fallback to default browser
    import webbrowser
    webbrowser.open(url)
    print("브라우저에서 실행되었습니다. 종료하려면 콘솔 창을 닫으세요.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run_desktop()
