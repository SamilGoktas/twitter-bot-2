from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
print("Server is running on port 8000...")
server.serve_forever()