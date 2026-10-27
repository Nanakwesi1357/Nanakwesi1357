#!/usr/bin/env python3
"""
mock_ollama.py — a tiny fake of the parts of the Ollama HTTP API used by
app/chat.py and app/one_shot.py. It lets the client code be tested on a
machine with no Ollama and no model download.

Implements:
    POST /api/chat   -> streaming NDJSON, same shape as real Ollama
    GET  /api/tags   -> {"models": []}

Run:
    python3 tests/mock_ollama.py            # listens on 127.0.0.1:11499
    OLLAMA_HOST=http://127.0.0.1:11499 python3 app/chat.py
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 11499
REPLY = "Hello from the mock model. I am running entirely on localhost."


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # quiet
        pass

    def do_GET(self):
        if self.path == "/api/tags":
            body = json.dumps({"models": []}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0"))
        json.loads(self.rfile.read(length) or b"{}")  # validate it parses

        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.end_headers()

        words = REPLY.split(" ")
        for i, word in enumerate(words):
            chunk = {
                "model": "mock-model",
                "message": {"role": "assistant", "content": word + " "},
                "done": False,
            }
            self.wfile.write((json.dumps(chunk) + "\n").encode())
            self.wfile.flush()
        self.wfile.write((json.dumps({"model": "mock-model", "done": True}) + "\n").encode())
        self.wfile.flush()


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"mock Ollama listening on http://127.0.0.1:{PORT}")
    server.serve_forever()
