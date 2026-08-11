from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import threading

import os, sys
# ensure workspace root is on path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import Main

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/routes' or parsed.path == '/api/routes':
            try:
                results = Main._build_api_payload()
                self._set_headers(200)
                self.wfile.write(json.dumps(results, default=str).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Handler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving API on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down')
        httpd.server_close()

if __name__ == '__main__':
    run()
