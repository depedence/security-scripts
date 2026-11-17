from http.server import BaseHTTPRequestHandler, HTTPServer

PAGES = {
    "/secure": {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "no-referrer",
    },
    "/weak": {
        "X-Content-Type-Options": "nosniff",
    },
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in PAGES:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        for name, value in PAGES[self.path].items():
            self.send_header(name, value)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"hello")


HTTPServer(("127.0.0.1", 8005), Handler).serve_forever()
