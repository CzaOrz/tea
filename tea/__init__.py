# coding: utf-8
import loggus

from tea.mw import Mw
from tea.ctx import NewCtx
from tea.route import Route
from wsgiref import simple_server
from tea.wsgi.handler import RequestHandler


class App(Route):

    def Application(self, environ, start_response):
        ctx = NewCtx(environ)
        route = ctx.Method + ctx.Path
        if route not in self.routeMap:
            start_response("404 forbidden", [])
            return [f"not defined route[{route}]".encode("utf-8")]
        mws, handler = self.routeMap[route]
        Mw(ctx, handler, *mws)
        start_response("200 ok", ctx.ResponseHeaders)
        return ctx.ResponseBody

    def Run(self, host="0.0.0.0", port=8080):
        loggus.withFields({"host": host, "port": port}).info("server start")
        self.GatherParty()
        simple_server.make_server(host, port, self.Application, handler_class=RequestHandler).serve_forever()


def hello(ctx):
    ctx.writeStr("hello world")


def mw1(ctx):
    import time, loggus
    start = int(time.time())
    yield
    loggus.info(int(time.time()) - start)


def mw2(ctx):
    import time, loggus
    loggus.info("mw2")
    yield


if __name__ == '__main__':
    app = App()
    app.Use(mw1)
    app.Get("/hello", hello)
    party = app.Party("/api/v1", mw2)
    party.Get("/hello", hello)

    app.Run()
