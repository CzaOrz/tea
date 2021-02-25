# coding: utf-8

def Application(environ, start_response):
    start_response("200 ok", [])
    from pprint import pprint
    pprint(environ)
    return [b"test"]


class App():
    pass
