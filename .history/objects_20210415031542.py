import string, math, time
from airline_data import airlines
from airport_data import airports

time = time.time()

# helper functions

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle), spd * math.sin(angle)

def runwayILS(pos, hdg):
    x0 = pos
    x1, x2 = hdgVector(hdg, 100)
    

# classes

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
        if self.hdg != hdg:
            if hdg > self.hdg:
                self.hdg += 2
            else: self.hdg -= 2

    def move(self):
        self.pos[0] += hdgVector(self.hdg, self.spd / 100)[0]
        self.pos[1] -= hdgVector(self.hdg, self.spd / 100)[1]
        self.alt += self.vs

    def changeSpd(self, spd):
        self.spd = spd

    def changeAlt(self, vs, alt):
        self.vs = vs
        self.alt = alt

    def directWaypoint(self, waypoint):
        self.hdg = waypoint - self.pos

    def followILS(self, runway):
        if abs(self.hdg - runway.hdg) < 30:
            self.changeHeading(runway.hdg)

class Airport(object):

    def __init__(self, code, runways):
        self.code = code
        self.runways = runways

    def name(self):
        return airports[self.code]

    class runways(object):
        
        def __init__(self, pos, hdg):
            self.pos = pos
            self.hdg = hdg

