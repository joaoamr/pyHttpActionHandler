from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
from urldecode import decode

class HttpActionServer(BaseHTTPRequestHandler):
    GET = {}
    POST = {}
    url = ''
      
    def _loadrequest(self, action):
        POST = self.POST
        GET = self.GET
        if action.endswith('.pyhtml') == False:
            file = open(action, 'rb')
            response = file.read()
            file.close()
            return response
        
        file = open(action, 'r')
        response = file.read()
        file.close()
        serverCmd = ''
        #catch and run server commands 
        st_i = response.find('<.py\n')
        while st_i > -1:
            fn_i = response.find('\n.>')
            serverCmd += response[st_i + 5:fn_i] + '\n'
            response = response[:st_i] + response[fn_i + 3:]
            st_i = response.find('<.py\n')
            
        exec(serverCmd)

        #bind variables to response
        st_i = response.find('.py(')
        while st_i > -1:
            fn_i = response.find(')', st_i)
            var = response[st_i + 4:fn_i]
            try:
                var = locals()[var]
            except:
                var = '.py(' + var + ')'

            response = response[:st_i] + str(var) + response[fn_i + 1:]
            st_i = response.find('.py(', st_i + 1)
        return response.encode('utf-8')
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _processUrl(self):
        req = self.path.split('?')
        self.GET.clear()
        if len(req) > 1:
            params = req[1].split('&')
            for i in range (0, len(params)):
                try:
                    self.GET[params[i].split('=')[0]] = decode(params[i].split('=')[1])
                except:
                    pass
        self.url = req[0]

    def _processPostBody(self, post):
        post = decode(post)
        params = post.split('&')
        for i in range (0, len(params)):
            try:
                self.POST[params[i].split('=')[0]] = params[i].split('=')[1]
            except:
                pass

    
    def do_GET(self):
        print(self.path)
        self._processUrl()
        res = b''
        try:
            if self.url == '/':
                res = self._loadrequest('web\\index.pyhtml')
            else:
                res = self._loadrequest('web\\' + self.url[1:])
        except:
            res = self._loadrequest('sys\\404_notfound.pyhtml')
                        
        if self.url.endswith('.pyhtml') or self.url.endswith('.html'):
            self._set_headers()

        self.wfile.write(res)
        
    def do_POST(self):
        self._processUrl()     
        content_len = int(self.headers.get('content-length', 0))
        post = self.rfile.read(content_len)
        self._processPostBody(post.decode('utf-8'))
        
        res = b''
        try:
            if self.url == '/':
                res = self._loadrequest('web\\index.pyhtml')
            else:
                res = self._loadrequest('web\\' + self.url[1:])
        except:
            res = self._loadrequest('sys\\404_notfound.pyhtml')
            
        if self.url.endswith('.pyhtml') or self.url.endswith('.html'):
            self._set_headers()
            
        self.wfile.write(res)

    def do_PUT(self):
        self.do_POST()
