#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import threading
import time
import mimetypes
import base64
from urllib.parse import unquote

WATCH_EXTS = {'.html', '.htm', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.json'}
HOST = '127.0.0.1'
PORT = 8000

clients_lock = threading.Lock()
clients = set()

BASIC_USER = os.getenv('BASIC_AUTH_USER', '')
BASIC_PASS = os.getenv('BASIC_AUTH_PASS', '')

class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    server_version = "LiveHTTP/1.0"

    def _auth_ok(self):
        if not BASIC_USER and not BASIC_PASS:
            return True
        auth = self.headers.get('Authorization')
        if not auth or not auth.startswith('Basic '):
            self._send_401()
            return False
        try:
            dec = base64.b64decode(auth.split(' ', 1)[1].strip()).decode('utf-8')
        except Exception:
            self._send_401()
            return False
        if ':' not in dec:
            self._send_401()
            return False
        u, p = dec.split(':', 1)
        if u == BASIC_USER and p == BASIC_PASS:
            return True
        self._send_401()
        return False

    def _send_401(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Preview"')
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Authentication required')

    def translate_path(self, path):
        path = unquote(path.split('?',1)[0].split('#',1)[0])
        cwd = os.getcwd()
        trailing_slash = path.rstrip('/').endswith('/') or path.endswith('/')
        path = os.path.normpath(path)
        words = [w for w in path.split('/') if w and w not in ('.', '..')]
        full = cwd
        for w in words:
            full = os.path.join(full, w)
        if os.path.isdir(full) and trailing_slash:
            return full + '/'
        return full

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_HEAD(self):
        if not self._auth_ok():
            return
        return super().do_HEAD()

    def do_GET(self):
        if not self._auth_ok():
            return
        if self.path.startswith('/__lr.js'):
            self._serve_lr_js()
            return
        if self.path.startswith('/__livereload'):
            self._serve_sse()
            return
        return super().do_GET()

    def _serve_lr_js(self):
        code = (
            "(function(){\n" \
            "  if (!('EventSource' in window)) return;\n" \
            "  var es = new EventSource('/__livereload');\n" \
            "  var reload = function(){ console.log('[livereload] reload'); window.location.reload(); };\n" \
            "  es.onmessage = function(e){ if(e && e.data === 'reload'){ reload(); } };\n" \
            "  es.onerror = function(){ console.warn('[livereload] connection lost, retrying...'); };\n" \
            "})();\n"
        ).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/javascript; charset=utf-8')
        self.send_header('Content-Length', str(len(code)))
        self.end_headers()
        self.wfile.write(code)

    def _serve_sse(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()
        with clients_lock:
            clients.add(self.wfile)
        try:
            self.wfile.write(b": ping\n\n")
            self.wfile.flush()
            while True:
                time.sleep(15)
                try:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
                except Exception:
                    break
        finally:
            with clients_lock:
                clients.discard(self.wfile)

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for index in ("index.html", "index.htm"):
                index_path = os.path.join(path, index)
                if os.path.exists(index_path):
                    path = index_path
                    break
        if os.path.isfile(path) and path.lower().endswith(('.html', '.htm')):
            try:
                with open(path, 'rb') as f:
                    content = f.read()
                inject = b"\n<script src=\"/__lr.js\"></script>\n"
                lower = content.lower()
                pos = lower.rfind(b"</body>")
                if pos != -1:
                    newc = content[:pos] + inject + content[pos:]
                else:
                    newc = content + inject
                self.send_response(200)
                ctype = mimetypes.guess_type(path)[0] or 'text/html'
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(newc)))
                self.end_headers()
                self.wfile.write(newc)
                return None
            except OSError:
                self.send_error(404, "File not found")
                return None
        return super().send_head()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

last_sig = None

def compute_sig(root):
    max_mtime = 0
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fn in files:
            if fn.startswith('.'):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if WATCH_EXTS and ext not in WATCH_EXTS:
                continue
            try:
                m = os.path.getmtime(os.path.join(base, fn))
                if m > max_mtime:
                    max_mtime = m
            except OSError:
                pass
    return max_mtime


def broadcaster(root):
    global last_sig
    last_sig = compute_sig(root)
    while True:
        time.sleep(0.5)
        sig = compute_sig(root)
        if sig > last_sig:
            last_sig = sig
            data = b"data: reload\n\n"
            stale = []
            with clients_lock:
                for w in list(clients):
                    try:
                        w.write(data)
                        w.flush()
                    except Exception:
                        stale.append(w)
                for w in stale:
                    clients.discard(w)


def main():
    root = os.getcwd()
    srv = ThreadingHTTPServer((HOST, PORT), LiveReloadHandler)
    t = threading.Thread(target=broadcaster, args=(root,), daemon=True)
    t.start()
    print(f"Serving {root} at http://{HOST}:{PORT} (live reload, basic auth={'on' if (BASIC_USER or BASIC_PASS) else 'off'})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
