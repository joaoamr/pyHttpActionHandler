from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
import traceback
from traceback import format_exc

class HttpActionServer(BaseHTTPRequestHandler):
    GET = {} #Global dictionary for get params
    POST = {} #Global dictionary for post params
    url = '' #Requested url
    data_echo = '' #Data send from server

    def echo(self, data):
        self.data_echo += data

    def _exceptionreport(self, action):
        """
        Reports the exception at application terminal and client response
        """
        res = '<h1>An exception occurred while processing ' + action + ' request.</h1><br>' 
        print('An excepetion occurred while processing ' + action + ' request.\n')
        tb = format_exc()
        tb = tb.split('\n')
        print(tb[0])
        res = res + tb[0] + '<br>'
        for i in range(5, len(tb)):
            res = res + tb[i] + '<br>'
            
        return res.encode('utf-8')
          
    def _loadrequest(self, action):
        """
        Run the requested action.
        If the target is a pyhtml file, it runs the code and returns the response.
        Otherwise, it returns the requested file.
        """
        echo = self.echo
        self.data_echo = ''
        POST = self.POST
        GET = self.GET
        PATH = self.path
        if action.endswith('.pyhtml') == False:
            try:
                file = open(action, 'rb')
                response = file.read()
                file.close()
                return response
            except:
                return False
        
        try:
            file = open(action, 'r')
        except:
            return False
        
        response = file.read()
        file.close()
        serverCmd = ''
        #Catch and run server commands 
        st_i = response.find('<.py\n')
        while st_i > -1:
            fn_i = response.find('\n.>')
            serverCmd += response[st_i + 5:fn_i] + '\n'
            response = response[:st_i] + response[fn_i + 3:]
            st_i = response.find('<.py\n')
        
        #serverCmd += '\nlocals.update(locals())' 
        
        vars=locals().copy()
        exec(serverCmd, locals=vars)

        #Bind variables to response
        st_i = response.find('.py(')
        while st_i > -1:
            fn_i = response.find(')', st_i)
            var = response[st_i + 4:fn_i]
            try:
                value = vars[var]
            except Exception as e:
                traceback.print_exc()
                print('vars:')
                print(vars)
                value = '.py(' + var + ')'

            response = response[:st_i] + str(value) + response[fn_i + 1:]
            st_i = response.find('.py(', st_i + 1)

        response = self.data_echo + response
        return response.encode('utf-8')

    #set http headers to response 
    def _writeheaders(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _processUrl(self):
        """
        Process the requested URL and add the params to the GET dictionary
        """
        req = self.path.split('?')
        self.GET.clear()
        if len(req) > 1:
            params = req[1].split('&')
            for i in range (0, len(params)):
                try:
                    self.GET[params[i].split('=')[0]] = unquote_plus(params[i].split('=')[1])
                except:
                    pass
        if req[0].endswith('/'):
            req[0] = req[0] + 'index.pyhtml'
            
        self.url = req[0]

    def _processPostBody(self, post):
        """
        Process the post body and add the params to the POST dictionary
        """
        self.POST.clear()
        post = unquote_plus(post)
        params = post.split('&')
        for i in range (0, len(params)):
            try:
                self.POST[params[i].split('=')[0]] = params[i].split('=')[1]
            except:
                pass

    #Process GET requests
    def do_GET(self):
        print(self.path)
        self._processUrl()
        self._writeresponse()

    #Process POST requests    
    def do_POST(self):
        self._processUrl()     
        content_len = int(self.headers.get('content-length', 0))
        post = self.rfile.read(content_len)
        self._processPostBody(post.decode('utf-8'))
        self._writeresponse()

    #Write the response to client
    def _writeresponse(self):
        res = b''
        try:
            res = self._loadrequest('web\\' + self.url[1:])
        except:
            res = self._exceptionreport(self.url)
            
        if res == False:
            try:
                self.url = self.url + '/index.pyhtml'
                res = self._loadrequest('web\\' + self.url[1:])
            except:
                res = self._exceptionreport(self.url)
        
            if res == False:
                res = self._loadrequest('sys\\404_notfound.pyhtml')
                self.url = '404_notfound.pyhtml'
                        
        if self.url.endswith('.pyhtml') or self.url.endswith('.html'):
            self._writeheaders()

        self.wfile.write(res)

    def do_PUT(self):
        self.do_POST()
