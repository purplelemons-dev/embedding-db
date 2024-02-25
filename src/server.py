from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from json import dumps
from database import DB

db = DB()

class Handler(BaseHTTPRequestHandler):

    protocol_version = "HTTP/1.1"

    def send(self, status: int, data: str, content_type: str = "text/plain"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data.encode())

    def send_json(self, status: int, data: dict):
        self.send(status, dumps(data), "application/json")

    def do_POST(self):
        if not self.path.startswith("/api"):
            self.send_response(404)
            self.end_headers()
            return

        if self.path == "/api/table":
            self.send_json(200, db.database)


server = ThreadingHTTPServer(("0.0.0.0", 80), Handler)

def run_server():
    server.serve_forever()
