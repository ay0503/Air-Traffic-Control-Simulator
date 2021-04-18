import string, math, time
from airline_data import airlines, airlineHubs
from airport_data import airports
import decimal, random
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
    #! BUG rechecks same aircraft and changes safety status
    for fl1 in aircrafts:
        for fl2 in aircrafts:
            if fl1.pos != fl2.pos:
                d = distance(fl1.pos, fl2.pos)
                altDiff = abs(fl1.alt - fl2.alt)
                if d < 80 and altDiff < 500:
                    fl1.safe = fl2.safe = False
                    break
                elif d < 30 and altDiff < 60:
                    fl1.safe = fl2.safe = False
                    fl1.crash = fl2.crash = True
                else: 
                    fl1.safe = fl2.safe = True

def vectorHdg(p1, p2):
    d = (p2[0] - p1[0], -p2[1] - p1[1])
    if d[0] == 0:
        if d[1] > 0:
            return 0
        elif d[1] < 0:
            return 180
    angle = math.degrees(math.atan2(d[1], d[0]))
    hdg = 360 - ((angle + 270) % 360)
    return int(hdg)

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return [spd * math.cos(angle), spd * math.sin(angle)]

def normalVector(vector):
    vector[0], vector[1] = -vector[1], vector[0]
    return vector

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
    
testCheckDirection()

# classes
###### TODO POSITIONS MUST END UP BEING RELATIVE TO WINDOW WITH LAT, LONG ######
# TODO add autopilot state for direct, hdg line predictions
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
        self.direct = None
        self.acc = 0
        self.bank = 0
        self.altCon = -1
        self.hdgCon = -1
        self.spdCon = -1
        self.safe = True
        self.crash = False

    def airline_code(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return code

    def airline_name(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return airlines[code]

    def airline_hubs(self):
        return airlineHubs[self.airline_code()]

    def flt_no(self):
        airline = no = ''
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
        if self.direct != None:
            self.direct_waypoint(self.direct)

    def change_hdg(self, hdg):
        if (self.hdg % 360) != hdg:
            if checkDirection(self.hdg, hdg):
                self.bank = 3
                self.hdgCon = hdg
            else: 
                self.bank = -3
                self.hdgCon = hdg
        else: self.bank = 0

    def change_spd(self, spd):
        if self.spd != spd:
            sign = int((spd - self.spd) / abs((spd - self.spd)))
            self.acc = sign * 3
            self.spdCon = spd

    def change_alt(self, alt):
        if self.alt != alt:
            sign = int((alt - self.alt) / abs((alt - self.alt)))
            self.vs = sign * 2000
            self.altCon = alt
        else: 
            self.vs = 0
            self.altCon = alt

    def check_on_grid(self, width, height):
        if (0 <= self.pos[0] < width and 0 <= self.pos[1] < height):
            return True
        return False

    def check_constraints(self):
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
    def direct_waypoint(self, waypoint):
        req_hdg = vectorHdg(self.pos, waypoint.pos)
        if self.hdg != req_hdg:
            self.direct = self.waypoint
            self.change_hdg(req_hdg)
        

class Departure(Flight):

    def __init__(self):
        pass

    # TODO create takeoff
    def takeoff(self, runway):
        pass

class Arrival(Flight):
    
    def __init__(self):
        pass

    # TODO check for ILS landings
    def check_arrival(self, runway):
        pass

    # TODO create ILS and ILS capture system
    def intercept_ILS(self, runway):
        if abs(self.hdg - runway.hdg) < 30:
            self.change_hdg(runway.hdg)

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

# TODO create time, size based traffic
class Airport(object):

    def __init__(self, code, pos, runways, size):
        self.pos = pos
        self.code = code
        self.runways = runways
        self.size =  self.traffic = size
        self.waypoints = []

    def name(self):
        return airports[self.code]

    # TODO create purpose for this condition
    def check_size_limits(self, aircraft):
        if ord(aircraft.size) > ord(self.size):
            return False
        return True

    def create_waypoints(self, width, height):
        letters = list(string.ascii_uppercase)
        # TODO modify frequency of random name lengths
        for i in range(15 * (ord(self.size) - ord("A") + 1)):
            x, y = random.randrange(100, width - 100), random.randrange(50, height - 50)
            name = ''
            length = random.randrange(3,6)
            for i in range(length):
                name += random.choice(letters)
            self.waypoints.append(Waypoint(name, [x, y]))

class Runway(object):
    
    def __init__(self, rwy, pos, hdg, length, airport):
        self.pos = list(map(lambda x, y : x + y, pos, airport.pos))
        self.hdg = hdg
        self.rwy = rwy
        self.num = roundHalfUp(hdg / 10)
        self.length = length
        self.plength = self.length / 500
        self.beacon = list(map(lambda x,y:x+y, self.pos, hdgVector(self.hdg, 12 * self.plength)))

    def range_ILS(self):
        norm = normalVector(list(map(lambda x,y: x-y, self.beacon, self.pos)))
        p2 = list(map(lambda x,y: x - y / 15, self.beacon, norm))
        p3 = list(map(lambda x,y: x + y / 15, self.beacon, norm))
        p1 = self.pos
        return p1, p2, p3
