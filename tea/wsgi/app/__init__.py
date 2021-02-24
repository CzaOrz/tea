# coding: utf-8

def Application(environ, start_response):
    start_response("200 ok")
    return [b"test"]
