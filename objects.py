import string, math, time
from airline_data import airlines, airlineHubs
from airport_data import airports
import decimal, random, copy
time = time.time()

# helper functions

def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def checkLineDistance(beaconpos, runwaypos, pos):
    start = copy.deepcopy(beaconpos)
    end = copy.deepcopy(runwaypos)
    vector = list(map(lambda x,y: y-x, start, end))
    interval = list(map(lambda x: x / distance(start, end), vector))
    while distance(start, end) > 2 ** 1.5:
        if distance(pos, start) < 20:
            return True
        start = list(map(lambda x,y: x+y, start, interval))
    return False

def checkSafety(aircrafts):
    #! BUG rechecks same aircraft and changes safety status
    for fl1 in aircrafts:
        if fl1.fuel / fl1.fuelRate < 5:
            fl1.crash = True
        elif fl1.fuel / fl1.fuelRate < 30:
            fl1.safe = False
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
    d = (p2[0] - p1[0], p2[1] - p1[1])
    if d[0] == 0:
        if d[1] > 0:
            return 0
        elif d[1] < 0:
            return 180
    angle = -math.degrees(math.atan2(d[1], d[0]))
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
    if hdg - currHdg >= 180 or -180 <= hdg - currHdg <= 0:
        return False
    else: return True

def testCheckDirection():
    print('Testing Heading Direction Algorithm...', end = "")
    assert(checkDirection(124, 90) == False)
    assert(checkDirection(160, 92) == False)
    assert(checkDirection(20, 340) == False)
    assert(checkDirection(20, 200) in [True, False])
    assert(checkDirection(75, 60) == False)
    assert(checkDirection(20, 210) == False)
    assert(checkDirection(314, 22) == True)
    assert(checkDirection(20, 190) == True)
    assert(checkDirection(120, 80) == False)
    assert(checkDirection(188, 291) == True)
    print("Passed")
    
testCheckDirection()

# classes
###### TODO POSITIONS MUST END UP BEING RELATIVE TO WINDOW WITH LAT, LONG ######
class Flight(object):
    
    def __init__(self, callsign, type, pos, hdg, spd, alt, vs, start, end, fuel):
        self.callsign = callsign
        self.type = type
        self.pos = pos
        self.hdg = hdg
        self.spd = spd
        self.alt = alt
        self.vs = vs
        self.fuelRate = int(fuel / 300) + 1
        self.start = start
        self.end = end
        self.direct = None
        self.acc = 0
        self.bank = 0
        self.altCon = -100
        self.hdgCon = -100
        self.spdCon = -100
        self.path = []
        self.draw = []
        self.safe = True
        self.crash = False
        self.details = ['callsign', 'type', 'hdg', 'spd', 
                        'alt', 'vs', 'fuel', 'start', 'end']

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
        self.path.append(self.pos)
        self.pos[0] += hdgVector(self.hdg, self.spd / 100)[0]
        self.pos[1] -= hdgVector(self.hdg, self.spd / 100)[1]
        self.alt += self.vs / 25
        self.hdg += self.bank
        self.spd += self.acc
        self.fuel -= self.fuelRate
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
        if abs(self.alt - self.altCon) <= 80:
            self.vs = 0
            self.alt = self.altCon
            self.altCon = -100
        if abs(self.spd - self.spdCon) <= 2:
            self.acc = 0
            self.spd = self.spdCon
            self.spdCon = -100
        if abs(self.hdg - self.hdgCon) <= 2:
            self.bank = 0
            self.hdg = self.hdgCon
            self.hdgCon = -100

    def direct_waypoint(self, waypoint):
        req_hdg = vectorHdg(self.pos, waypoint.pos)
        if self.hdg != req_hdg:
            self.direct = waypoint
            self.change_hdg(req_hdg)
        elif distance(self.pos, waypoint.pos) < 50:
            self.hdg = req_hdg
            self.direct = None
        
class Departure(Flight):

    def __init__(self, callsign, type, pos, hdg, spd, alt, vs, start, end, runway, fuel):
        super().__init__(callsign, type, pos, hdg, spd, alt, vs, start, end, fuel)
        self.alt = 0
        self.spd = 0
        self.fuel = fuel
        self.cleared = False
        self.departed = False
        self.end = end.name
        self.runway = runway
        self.sent = False
        self.endWaypoint = end

    def move(self):
        if self.cleared:
            self.takeoff()
        self.pos[0] += hdgVector(self.hdg, self.spd / 100)[0]
        self.pos[1] -= hdgVector(self.hdg, self.spd / 100)[1]
        self.alt += self.vs / 25
        self.hdg += self.bank
        self.spd += self.acc
        if self.departed:
            self.fuel -= self.fuelRate
        if self.direct != None:
            self.direct_waypoint(self.direct)
        if distance(self.pos, self.endWaypoint.pos) < 30:
            self.sent = True

    def clear_takeoff(self):
        self.cleared = True

    # TODO replace with vspeed
    def takeoff(self):
        if self.spd < 145:
            self.acc = 5
        else:
            self.vs = 3000
            self.acc = 5
            if self.alt > 1000:
                self.vs = 2000
                self.acc = 0
                self.departed = True

class Arrival(Flight):

    def __init__(self, callsign, type, pos, hdg, spd, alt, vs, start, end, fuel):
        super().__init__(callsign, type, pos, hdg, spd, alt, vs, start, end, fuel)
        self.fuel = fuel
        self.ILS = False
        self.landed = False
    
    def check_ILS(self, runways):
        for runway in runways:
            #print(distance(self.pos, runway.beacon), self.hdg, runway.hdg)
            if (checkLineDistance(runway.beacon, runway.pos, self.pos) 
                and abs(self.hdg - runway.hdg) < 30):
                self.ILS = True
                self.runway = runway
                self.intercept_ILS(runway)
            if self.ILS:
                self.capture_gs(self.runway)
                self.land(self.runway)

    def gs_change_spd(self, spd):
        if self.spd != spd:
            sign = int((spd - self.spd) / abs((spd - self.spd)))
            self.acc = sign * 2
            self.spdCon = spd

    # TODO follow localizer
    def intercept_ILS(self, runway):
        self.direct_waypoint(runway)

    def capture_gs(self, runway):
        if self.alt < 4000 and distance(self.pos, runway.pos) < 200:
            time = (distance(self.pos, runway.pos) - 5) / (self.spd / 100)
            self.vs = - int(self.spd * 5)
            self.gs_change_spd(140)

    def land(self, runway):
        if self.alt < 100 and distance(self.pos, runway.pos) < 15:
            self.landed = True

# self.vs = int(-self.alt * 60 / 125)

class Aircraft(object):
    
    def __init__(self, name, code, size, freq):
        self.name = name
        self.code = code
        self.size = size
        self.freq = freq

# TODO maybe add waypoints to ILS line
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
# TODO create weather based states
class Airport(object):

    def __init__(self, code, pos, runways, size, winds):
        self.pos = pos
        self.code = code
        self.weather = Weather(self, winds)
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
        # TODO modify frequency of random name lengths
        for i in range(15 * (ord(self.size) - ord("A") + 1)):
            x, y = random.randrange(100, width - 100), random.randrange(50, height - 50)
            name = ''
            length = random.randrange(2,5)
            for i in range(length):
                letters = list(string.ascii_uppercase)
                if i == 0:
                    letters.remove(self.code[0])
                    name += random.choice(letters)
                name += random.choice(letters)
            self.waypoints.append(Waypoint(name, [x, y]))

# TODO divide into depart and arrive (easier to account for wind)
class Runway(object):
    
    def __init__(self, rwy, pos, hdg, length, airport):
        self.pos = list(map(lambda x, y : x + y, pos, airport.pos))
        self.hdg = hdg
        self.rwy = rwy
        # TODO WIP average is extreme
        if airport.size not in ["A", "B"]:
            self.open = self.check_winds(airport.winds)
        else: self.open = True
        self.num = roundHalfUp(hdg / 10)
        self.length = length
        self.plength = self.length / 400
        self.beacon = [self.pos[0] - hdgVector(self.hdg, 10 * self.plength)[0], 
                        self.pos[1] + hdgVector(self.hdg, 10 * self.plength)[1]]

    def check_winds(self, winds):
        x, y = int(self.pos[0] // 20), int(self.pos[1] // 20)
        if ((abs(winds[y][x][0] - self.hdg) < 80 or abs(winds[y][x][0] - self.hdg + 180) % 360 < 80) and winds[y][x][1] < 10):
            return True
        return False

    def range_ILS(self):
        norm = normalVector(list(map(lambda x,y: x-y, self.beacon, self.pos)))
        p2 = list(map(lambda x,y: x - y / 15, self.beacon, norm))
        p3 = list(map(lambda x,y: x + y / 15, self.beacon, norm))
        p1 = self.pos
        return p1, p2, p3

        #abs(self.hdg - airport.wind) < 30 or abs((self.hdg + 180) % 360 - airport.wind) < 30

class Weather(object):

    def __init__(self, airport, winds):
        self.storm = []
        self.stormLevel = random.randrange(0,3)
        self.winds = airport.winds = winds
        self.visibility = self.stormLevel

    def createStorms(self, pos, airport, level):
        self.stormLevel = level
        self.winds = self.createWinds()

    def createWinds(self, airport):
        pass

    def landing_success(self, airport):
        pass
