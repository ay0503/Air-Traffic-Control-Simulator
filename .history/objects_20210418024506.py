import string, math, time
from airline_data import airlines, airlineHubs
from airport_data import airports
import decimal
time = time.time()

# helper functions

def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def checkSafety(aircrafts):
    # !BUG rechecks same aircraft and changes safety status
    for fl1 in aircrafts:
        for fl2 in aircrafts:
            if fl1.pos != fl2.pos:
                d = distance(fl1.pos, fl2.pos)
                altDiff = abs(fl1.alt - fl2.alt)
                if d < 80 and altDiff < 500:
                    fl1.safe = fl2.safe = False
                elif d < 30 and altDiff < 60:
                    fl1.safe = fl2.safe = False
                    fl1.crash = fl2.crash = True
                else: 
                    fl1.safe = fl2.safe = True

def vectorHdg(p1, p2):
    d = (int(p2[0] - p1[0]), int(p2[1] - p1[1]))
    if d[0] == 0:
        if d[1] > 0:
            return 0
        elif d[1] < 0:
            return 180
    angle = math.degrees(math.atan(d[1] / d[0]))
    hdg = 360 - (angle + 270) % 360
    return int(hdg)

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return [spd * math.cos(angle), spd * math.sin(angle)]

def normalVector(vector):
    vector[0], vector[1] = -vector[1], vector[0]
    return vector

def addVector(v1, v2):
    return list(map(lambda x,y:x+y, v1, v2))

def subtractVector(v1, v2):
    return list(map(lambda x,y:x-y, v1, v2))

def checkDirection(currHdg, hdg):
    if hdg == 0: hdg = 360
    if hdg > currHdg:
        if hdg - currHdg > 180:
            return False
        return True
    else: 
        if hdg - currHdg < -180:
            return True
        return False

def testCheckDirection():
    print('Testing checkDirection()')
    assert(checkDirection(124, 90) == False)
    assert(checkDirection(160, 92) == False)
    assert(checkDirection(20, 340) == False)
    assert(checkDirection(20, 200) in [True, False])
    assert(checkDirection(75, 60) == False)
    assert(checkDirection(20, 210) == False)
    assert(checkDirection(314, 22) == True)
    assert(checkDirection(20, 190) == True)
    print("Passed")

def runwayILS(pos, hdg):
    x0 = pos
    x1, x2 = hdgVector(hdg, 100)
    
#testCheckDirection()

# classes
###### TODO POSITIONS MUST END UP BEING RELATIVE TO WINDOW WITH LAT, LONG ######
class Flight(object):
    
    def __init__(self, callsign, type, pos, hdg, spd, alt, vs, start, end):
        self.callsign = callsign
        self.type = type
        self.pos = pos
        self.hdg = hdg
        self.spd = spd
        self.alt = alt
        self.vs = vs
        self.start = start
        self.end = end
        # TODO create type of aircraft (new class)
        #self.type = type
        self.acc = 0
        self.bank = 0
        self.altCon = -1
        self.hdgCon = -1
        self.spdCon = -1
        self.safe = True
        self.crash = False

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
        self.alt += self.vs / 25
        self.hdg += self.bank
        self.spd += self.acc

    def changeHeading(self, hdg):
        if (self.hdg % 360) != hdg:
            if checkDirection(self.hdg, hdg):
                self.bank = 1
                self.hdgCon = hdg
            else: 
                self.bank = -1
                self.hdgCon = hdg
        else: self.bank = 0

    def changeSpd(self, spd):
        if self.spd != spd:
            sign = int((spd - self.spd) / abs((spd - self.spd)))
            self.acc = sign * 2
            self.spdCon = spd
        else: 
            self.acc = 0
            self.spdCon = spd

    def changeAlt(self, alt):
        if self.alt != alt:
            sign = int((alt - self.alt) / abs((alt - self.alt)))
            self.vs = sign * 2000
            self.altCon = alt
        else: 
            self.vs = 0
            self.altCon = alt

    def checkOnGrid(self, width, height):
        if (0 <= self.pos[0] < width and 0 <= self.pos[1] < height):
            return True
        return False

    def checkConstraints(self):
        self.hdg %= 360
        if self.vs > 0:
            if self.alt >= self.altCon:
                self.vs = 0
                self.altCon = -1
        elif self.vs < 0:
            if self.alt <= self.altCon:
                self.vs = 0
                self.altCon = -1
        if self.acc > 0:
            if self.spd >= self.spdCon:
                self.acc = 0
                self.spdCon = -1
        elif self.acc < 0:
            if self.spd <= self.spdCon:
                self.acc = 0
                self.spdCon = -1
        if self.bank > 0:
            if self.hdg >= self.hdgCon:
                self.bank = 0
                self.hdgCon = -1
        elif self.bank < 0:
            if self.hdg <= self.hdgCon:
                self.bank = 0
                self.hdgCon = -1

    # TODO need to account for drift 
    def directWaypoint(self, waypoint):
        hdg = vectorHdg(self.pos, waypoint.pos)
        self.changeHeading(hdg)

    # TODO create takeoff
    def takeoff(self, runway):
        pass

    # TODO create ILS and ILS capture system
    def interceptILS(self, runway):
        if abs(self.hdg - runway.hdg) < 30:
            self.changeHeading(runway.hdg)

    # TODO check for ILS landings
    def checkArrival(self, runway):
        pass

class Aircraft(object):
    
    def __init__(self, name, code, size, freq):
        self.name = name
        self.code = code
        self.size = size
        self.freq = freq

class Waypoint(object):

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

class Airline(object):

    def __init__(self, code, name, hubs):
        self.code = code
        self.name = name
        self.hubs = hubs

    def createFlno(self, no):
        return f"{self.code}{no}"

# TODO create converter for Earth coordinates to canvas coordinates

class Airport(object):

    def __init__(self, code, runways, size):
        self.code = code
        self.runways = runways
        self.limit = size

    def name(self):
        return airports[self.code]

    # TODO create purpose for this condition
    def checkSizeLimits(self, aircraft):
        if ord(aircraft.size) > ord(self.size):
            return False
        return True

class Runway(object):
    
    def __init__(self, rwy, pos, hdg, length):
        self.pos = pos
        self.hdg = hdg
        self.rwy = rwy
        self.num = roundHalfUp(hdg / 10)
        self.length = length / 1000
        self.beacon = list(map(lambda x,y:x+y, self.pos, hdgVector(self.hdg, self.length / 1000)))

    def rangeILS(self):
        vector = list(map(lambda x,y:x-y, self.beacon, self.pos))
        base = list(map(lambda x: x / 8, addVector(self.beacon, normalVector(vector))))
        p1, p2, p3 = subtractVector(self.beacon, base), addVector(self.beacon, base), self.pos
        return p1, p2, p3

L = Runway('25L', [0,0], 251, 12000)
print(L.beacon)
print(L.rangeILS())