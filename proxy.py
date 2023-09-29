from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import requests


class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_GET(self, body=True):
        try:
            target_domain = "https://target_domain.com"
            res = requests.get(f"{target_domain}{self.path}", headers=self.headers)
            self.send_response(res.status_code)
            for key, value in res.headers.items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(res.content)
        except Exception as e:
            self.send_error(500, str(e))

    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET


if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 8443), ProxyHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='path/to/cert.pem', keyfile='path/to/privkey.pem',
                                   server_side=True)
    print('Starting proxy...')
    httpd.serve_forever()
