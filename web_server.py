import http.server
import socketserver
import sys
import os

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stdout.write(f"{self.log_date_time_string()} - {format%args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    PORT = 5000
    Handler = CustomHTTPRequestHandler
    os.chdir('/home/user/webapp')
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://0.0.0.0:{PORT}/")
        sys.stdout.flush()
        httpd.serve_forever()
