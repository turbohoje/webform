#!/usr/bin/env python3

#openssl genrsa -out server.key 2048
#openssl req -new -x509 -key server.key -out server.crt -days 365
#!/usr/bin/env python3

from datetime import datetime
import pytz
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = '0.0.0.0'
PORT = 8443
FILENAME = 'names.csv'  # The file we'll serve/download/prepend to
LOGFILE = "log.txt"

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/hello':
            # Endpoint 1: Return a "Hello World" message
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Hello from the TLS server!\n")

        elif self.path == '/download-file':
            # Endpoint 2: Serve the file
            try:
                with open(FILENAME, 'rb') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(data)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found.\n")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found\n")

    def do_POST(self):
        if self.path == '/prepend':
            # Endpoint 3: Read payload and prepend to file
            content_length = int(self.headers.get('Content-Length', 0))
            payload = self.rfile.read(content_length)

            denver_tz = pytz.timezone("America/Denver")
            now_denver = datetime.now(denver_tz)
            now = now_denver.isoformat()
            # Write back to the file
            with open(LOGFILE, 'ab') as f:
                f.write(now.encode("ascii") + ",".encode("ascii") + payload + "\n".encode("ascii"))

            # Respond to the client
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Successfully prepended data to file.\n")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found\n")

def main():
    # Create the HTTP server
    httpd = HTTPServer((HOST, PORT), MyHandler)
    
    # Create an SSL context with the proper protocol (TLS)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Load our server certificate and private key
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    
    # Wrap the HTTP server's underlying socket with this SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"Serving HTTPS on {HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    main()
#!/usr/bin/env python3

import ssl
import sys
import http.client

HOST = '127.0.0.1'
PORT = 8443

def main():
    if len(sys.argv) < 2:
        print("Usage: client.py [hello | getfile | prepend] [optional payload]")
        sys.exit(1)

    command = sys.argv[1]

    # Create an SSLContext in client mode.
    # We trust our self-signed 'server.crt'.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('server.crt')
    context.verify_mode = ssl.CERT_REQUIRED

    # Open an HTTPS connection to the server
    conn = http.client.HTTPSConnection(HOST, PORT, context=context)

    if command == "hello":
        # Send GET /hello
        conn.request("GET", "/hello")
        resp = conn.getresponse()

        print(f"Response status: {resp.status} {resp.reason}")
        print(resp.read().decode())

    elif command == "getfile":
        # Send GET /download-file
        conn.request("GET", "/download-file")
        resp = conn.getresponse()

        print(f"Response status: {resp.status} {resp.reason}")
        if resp.status == 200:
            file_contents = resp.read()
            print("File contents:")
            print(file_contents.decode())
        else:
            print(resp.read().decode())

    elif command == "prepend":
        # e.g. python client.py prepend "some data to prepend"
        if len(sys.argv) < 3:
            print("Usage: client.py prepend <payload>")
            sys.exit(1)
        payload = sys.argv[2]

        # Send POST /prepend with the payload
        headers = {"Content-Type": "text/plain"}
        conn.request("POST", "/prepend", body=payload, headers=headers)

        resp = conn.getresponse()
        print(f"Response status: {resp.status} {resp.reason}")
        print(resp.read().decode())

    else:
        print("Unknown command:", command)

    conn.close()

if __name__ == '__main__':
    main()