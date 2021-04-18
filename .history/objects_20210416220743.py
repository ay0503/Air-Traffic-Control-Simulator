import string, math, time
from airline_data import airlines, airlineHubs
from airport_data import airports

time = time.time()

# helper functions

def keepDistance(aircrafts):
    for fl1 in aircrafts:
        for fl2 in aircrafts:
            if fl1.pos != fl2.pos:
                distance = ((fl1.pos[0] - fl2.pos[0]) ** 2 + (fl1.pos[1] - fl2.pos[1]) ** 2) ** 0.5
                if distance < 40:
                    return False
    return True

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle), spd * math.sin(angle)

def runwayILS(pos, hdg):
    x0 = pos
    x1, x2 = hdgVector(hdg, 100)
    
# classes
###### TODO POSITIONS MUST END UP BEING RELATIVE TO WINDOW WITH LAT, LONG ######
class Aircraft(object):
    
    def __init__(self, callsign, pos, hdg, spd, alt, vs, start, end):
        self.callsign = callsign
        self.pos = pos
        self.hdg = hdg
        self.spd = spd
        self.alt = alt
        self.vs = vs
        self.start = start
        self.end = end
        self.acc = 0
        self.bank = 0

    def airlineCode(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return code

    def airlineName(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return airlines[code]

    def airlineHubs(self):
        return airlineHubs[self.airlineCode()]

    def fltno(self):
        airline = ''
        no = ''
        for letter in self.callsign:
            if letter.isalpha():
                airline += letter
            elif letter.isdigit():
                no += letter
        return f"{airlines[airline]} {no}"

    def move(self):
        self.pos[0] += hdgVector(self.hdg, self.spd / 100)[0]
        self.pos[1] -= hdgVector(self.hdg, self.spd / 100)[1]
        self.alt += self.vs / 60
        self.hdg += self.bank
        self.spd += self.acc

    def changeHeading(self, hdg):
        if self.hdg != hdg:
            if hdg > self.hdg:
                self.bank = 2
            else: self.bank = -2
        else: self.bank = 0

    def changeSpd(self, spd):
        if self.spd != spd:
            self.acc = 10
        else: self.acc = 0

    def changeAlt(self, alt):
        if self.alt < alt:
            sign = int((alt - self.alt) / abs((alt - self.alt)))
            self.vs = sign * 50
        else: self.vs = 0

    def directWaypoint(self, waypoint):
        self.hdg = waypoint - self.pos

    def followILS(self, runway):
        if abs(self.hdg - runway.hdg) < 30:
            self.changeHeading(runway.hdg)

    def checkArrival(self, runway):
        pass

class Airline(object):

    def __init__(self, code, name, hubs):
        self.code = code
        self.name = name
        self.hubs = hubs

    def createFlno(self, no):
        return f"{self.code}{no}"

#TODO create converter for Earth coordinates to canvas coordinates

class Airport(object):

    def __init__(self, code, runways):
        self.code = code
        self.runways = runways
        #self.size = size

    def name(self):
        return airports[self.code]

class runways(object):
    
    def __init__(self, pos, hdg, length):
        self.pos = pos
        self.hdg = hdg
        self.length = length

    
