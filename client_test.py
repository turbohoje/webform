#!/usr/bin/env python3

import ssl
import sys
import http.client

HOST = '34.134.131.179'
PORT = 8443

server_certificate_pem = """-----BEGIN CERTIFICATE-----
MIIDZzCCAk+gAwIBAgIUSWvO+etC/f2ljFt+LlYfN8UxtdEwDQYJKoZIhvcNAQEL
BQAwQzELMAkGA1UEBhMCdXMxCzAJBgNVBAgMAmNvMQ8wDQYDVQQHDAZkZW52ZXIx
FjAUBgNVBAoMDXJvY2tldHNjaWVuY2UwHhcNMjUwMTI5MDEzNTE3WhcNMjYwMTI5
MDEzNTE3WjBDMQswCQYDVQQGEwJ1czELMAkGA1UECAwCY28xDzANBgNVBAcMBmRl
bnZlcjEWMBQGA1UECgwNcm9ja2V0c2NpZW5jZTCCASIwDQYJKoZIhvcNAQEBBQAD
ggEPADCCAQoCggEBAMFCJ1tkDL0F05N8JZNaoX2o6ZHaWJSbi/WUAUcNPL9qv+jY
nDYGJPpKItb0aZWYMlop4PuN0QfRlrRoXP+I8bbAyRHw0nH7mwORaYcrS893BBca
ptIEecOUcO+G3NLR/t/sbWL3muKDCh3e9lap8EX2uPqctIxcr2osruKta/VH9MVG
uViEptDFk7W80T4svtugIA+iUx4m9OPEJBviFr8kVALGVrmu7D6X9rYp+EAZyeNt
EfoCD0+SWU1BL2o4/Lqqe59YTmd34wPmjNmNSFngIFDjtgRCu1dmkdhfa4NMoqJP
ueaqVbp/oOgx7IVTi1VpOGVVxPVnpQu99as/Eg8CAwEAAaNTMFEwHQYDVR0OBBYE
FBxvkSSz0tt+UVinwDGaSKmwVZjvMB8GA1UdIwQYMBaAFBxvkSSz0tt+UVinwDGa
SKmwVZjvMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBADc2B0z3
AAnRqeMnNWZiRW33EWR4Uzz4m8wTGzQCodXfpk4Lhpdq2zYmabtGZzBFpGgWeqcA
7UUqQdDR+YCf7MaStrJM4iuL/9mMT69Zfo7DGnVdLQ7z/w+41AMNeFVX+Glwq9Z2
iR+TDwgQX2ivzO6Jn+GhvKGq/Agymu6waQx6tJtqA5Xc9ZXiPjO+cCFyPN41MEz1
7eMwXxTmlyVKKMfwlYkjBXa9a0HdzAq5L1gouS8CkXJB0i1zwvJNoQtn/sVbtsMw
FVSD5N/LIupZS4EhfkeKdG2Pj8j23ckw6emMDFAlwY0Oi9NPpYYlIEiWvhITfqYv
ab9n8jLbL1JA8Zk=
-----END CERTIFICATE-----
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: client.py [hello | getfile | getlog | prepend] [optional payload]")
        sys.exit(1)

    command = sys.argv[1]

    # Create an SSLContext in client mode.
    # We trust our self-signed 'server.crt'.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cadata=server_certificate_pem)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

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
    elif command == "getlog":
        # Send GET /download-file
        conn.request("GET", "/download-log")
        resp = conn.getresponse()

        #print(f"Response status: {resp.status} {resp.reason}")
        if resp.status == 200:
            file_contents = resp.read()
            #print("File contents:")
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