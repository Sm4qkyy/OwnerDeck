# Local preview.
#
#   python _serve.py          -> http://localhost:8000
#
# Vercel serves this site with cleanUrls on, so /terms is a real URL and
# /terms.html is not. A plain http.server would 404 every internal link, so
# this resolves extensionless paths the same way Vercel does. It also honours
# the redirects in vercel.json, so the preview matches production.
#
# It does NOT run api/*.js — the live chat will fail locally, which is
# expected. Everything else (layout, type, colour, the deck) is real.
import http.server
import json
import os
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, 'vercel.json'), encoding='utf-8') as f:
    CFG = json.load(f)
REDIRECTS = {r['source'].rstrip('/'): r['destination'] for r in CFG.get('redirects', [])}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        path = self.path.split('?', 1)[0].split('#', 1)[0]

        dest = REDIRECTS.get(path.rstrip('/') or '/')
        if dest:
            self.send_response(308)
            self.send_header('Location', dest)
            self.end_headers()
            return

        if path.startswith('/api/'):
            self.send_response(501)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error":"api routes do not run under _serve.py"}')
            return

        # cleanUrls: /terms -> terms.html
        if path not in ('/', '') and not os.path.splitext(path)[1]:
            candidate = os.path.join(ROOT, path.lstrip('/') + '.html')
            if os.path.isfile(candidate):
                self.path = path + '.html'

        return super().do_GET()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        code = args[1] if len(args) > 1 else ''
        if str(code).startswith(('4', '5')):
            sys.stderr.write('  %s %s\n' % (code, args[0]))


class Server(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    print('Ownerdeck preview  ->  http://localhost:%d' % PORT)
    print('cleanUrls and redirects emulated. api/ routes are not available.')
    print('Ctrl+C to stop.\n')
    with Server(('', PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nstopped')
