# coding: utf-8
from collections import defaultdict

__all__ = "NewCtx",


def NewCtx(environ):
    return Ctx(environ)


class Ctx:

    def __init__(self, environ):
        self.environ = environ
        self.__responseHeaders = []
        self.__responseBody = []
        # extract
        self.__contentLength = int(environ.get("CONTENT_LENGTH", 0))
        self.__contentType = environ.get("CONTENT_TYPE", "")
        self.__remoteAddr = environ.get("REMOTE_ADDR", "")
        self.__path = environ["PATH_INFO"]
        self.__method = environ["REQUEST_METHOD"]
        self.__body = environ["wsgi.input"].read(self.__contentLength) if self.__contentLength else ""
        # extract query
        self.__urlParams = defaultdict(list)
        for query in environ.get("QUERY_STRING", "").split("&"):
            queries = query.split("=", 1)
            if len(queries) != 2:
                continue
            self.__urlParams[queries[0]].append(queries[1])
        # extract path params
        self.__pathParams = {}
        # extract headers
        self.__headers = {}
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                self.__headers[key.replace("HTTP_", "")] = value

    @property
    def ContentLength(self):
        return self.__contentLength

    @property
    def ContentType(self):
        return self.__contentType

    @property
    def RemoteAddr(self):
        return self.__remoteAddr

    @property
    def Path(self):
        return self.__path

    @property
    def Body(self):
        return self.__body

    @property
    def UrlParams(self):
        return self.__urlParams

    @property
    def PathParams(self):
        return self.__pathParams

    @property
    def Method(self):
        return self.__method

    @property
    def Headers(self):
        return self.__headers

    @property
    def ResponseHeaders(self):
        return self.__responseHeaders

    @property
    def ResponseBody(self):
        return self.__responseBody

    def writeStr(self, body: str):
        self.__responseBody.append(body.encode("utf-8"))

    def writeBytes(self, body: bytes):
        self.__responseBody.append(body)
