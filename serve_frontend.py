#!/usr/bin/env python3
"""
Simple HTTP server for TechStep frontend
"""
import http.server
import socketserver
import os
import sys

PORT = 3000
DIRECTORY = "/home/user/webapp"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def log_message(self, format, *args):
        sys.stdout.write(f"{self.log_date_time_string()} - {format%args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"TechStep Frontend Server running at http://0.0.0.0:{PORT}")
        print(f"Serving directory: {DIRECTORY}")
        sys.stdout.flush()
        httpd.serve_forever()