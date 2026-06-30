import socket
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import cast


def open_auth_url(auth_url: str):

    class _ReusingHTTPServer(HTTPServer):
        allow_reuse_address = True
        auth_code: str

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if "code" in params:
                cast(_ReusingHTTPServer, self.server).auth_code = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(
                    b"Authorization successful. You can close this window."
                )
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing authorization code.")

    httpd = _ReusingHTTPServer(("localhost", 5173), CallbackHandler)
    try:
        httpd.handle_request()
        return httpd.auth_code
    finally:
        httpd.socket.shutdown(socket.SHUT_RDWR)
        httpd.server_close()
