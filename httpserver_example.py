from httpactionhandler import HttpActionServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

port = 80
host = ''

for i in range(0, len(sys.argv)):
    if sys.argv[i] == '-p':
        port = sys.argv[i+1]
        continue

    if sys.argv[i] == '-h':
        host = sys.argv[i+1]
        continue


HTTPServer((host, port), HttpActionServer).serve_forever()
