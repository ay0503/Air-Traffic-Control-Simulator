import string, math
from airline_data import airlines


class Aircraft(object):
    
    def __init__(self, callsign, pos, hdg, spd, alt, vs):
        self.callsign = callsign
        self.pos = pos
        self.hdg = hdg
        self.spd = spd
        self.alt = alt
        self.vs = vs

    def airline(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return airlines[code]

    def fltno(self):
        return self.callsign

    def changeHeading(self, hdg):
        self.hdg = hdg

    def changeSpd(self, spd):
        self.spd = spd

    def changeAlt(self, vs, alt):
        self.vs = vs
        self.alt = alt

    def directWaypoint(self, waypoint):
        self.hdg = waypoint - self.pos
    
class Airport(object):

    def __init__(self, code, pos, runways):
        self.code = code
        self.pos = pos
        self.runways = runways

    def getName(self, code):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return airports[code]