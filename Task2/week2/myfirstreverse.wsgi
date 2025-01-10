from myfirstwebapp import app as application

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"WSGI script is working"]

