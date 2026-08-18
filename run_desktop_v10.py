import os
import sys
import threading
import time
import http.server
import socketserver
import webbrowser

PORT = 8090
DIRECTORY = "app_v10"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        pass

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(0.5)
    
    url = f"http://127.0.0.1:{PORT}/index.html"
    title = "[v1.10] 타르코프 퀘스트 가이드 - Market Quests Edition"
    
    try:
        import webview
        print(f"Starting Native Window for {title} on {url}...")
        webview.create_window(title, url, width=1440, height=900, min_size=(1024, 700))
        webview.start()
    except ImportError:
        print(f"pywebview not found. Opening in default web browser...")
        webbrowser.open(url)
        print(f"Running server on {url}. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped.")
