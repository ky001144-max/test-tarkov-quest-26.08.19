import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8090
DIRECTORY = "app_v10"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"=== [v1.10 Tarkov.dev Edition] Serving at http://localhost:{PORT} ===")
        threading.Thread(target=lambda: (time.sleep(0.5), webbrowser.open(f"http://localhost:{PORT}")), daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopped.")
