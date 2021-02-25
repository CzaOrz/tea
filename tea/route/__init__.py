# coding: utf-8
import loggus

from tea.mw import CheckMw, CheckArgs

__all__ = "Route",


class Route:

    def __init__(self, partyPref=""):
        self.partyPref = partyPref
        self.parties = []
        self.mws = []
        self.routeMap = {}  # mws, handler
        self.log = loggus.withFields({"module": "route", "partyPref": self.partyPref})

    def Use(self, *mws):
        CheckMw(*mws)
        self.mws += mws

    def Party(self, partyPref: str, *mws):
        if not partyPref.startswith("/") or partyPref.endswith("/"):
            self.log.panic(f"invalid route[{partyPref}]")
        party = Route(self.partyPref + partyPref)
        party.Use(*mws)
        self.parties.append(party)
        return party

    def GatherParty(self):
        for party in self.parties:
            party.GatherParty()
            if set(self.routeMap.keys()) & set(party.routeMap.keys()):
                self.log.withFields({
                    "routeMapKeys": self.routeMap.keys(),
                    "partyMapKeys": party.routeMap.keys(),
                }).panic("route conflict")
            self.routeMap.update(party.routeMap)
        if self.mws:
            for route, value in self.routeMap.items():
                self.routeMap[route] = (self.mws + value[0], value[1])

    def Register(self, method: str, route: str, *args):
        if not args:
            self.log.panic("not define handler")
        if not route.startswith("/"):
            self.log.panic(f"invalid route[{route}]")
        route = method.upper() + self.partyPref + route
        if route in self.routeMap:
            self.log.panic(f"conflict route[{route}]")
        mws, handler = args[:-1], args[-1]
        CheckMw(*mws)
        CheckArgs(handler)
        self.routeMap[route] = [list(mws), handler]

    def Get(self, route: str, *args):
        self.Register("GET", route, *args)

    def Post(self, route: str, *args):
        self.Register("POST", route, *args)

    def Put(self, route: str, *args):
        self.Register("PUT", route, *args)

    def Delete(self, route: str, *args):
        self.Register("DELETE", route, *args)
