# coding: utf-8
from wsgiref import simple_server
from tea.wsgi.app import Application
from tea.wsgi.handler import RequestHandler


def NewWSGIServer(host="0.0.0.0", port=8080):
    return simple_server.make_server(host, port, Application, handler_class=RequestHandler)


if __name__ == '__main__':
    NewWSGIServer().serve_forever()
