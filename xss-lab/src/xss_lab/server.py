import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def render_search(query):
    return f"<h1>Search</h1><p>You searched for: {html.escape(query)}</p>"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/search":
            self.send_response(404)
            self.end_headers()
            return
        query = parse_qs(parsed.query).get("q", [""])[0]
        body = render_search(query)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Set-Cookie", "session=abc1234; HttpOnly")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


HTTPServer(("127.0.0.1", 8008), Handler).serve_forever()
