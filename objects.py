import string, math, time
from airline_data import airlines, airlineHubs
from airport_data import airports
import decimal, random, copy
time = time.time()

# helper functions
imageScale = 5

# returns pixel distance between two points
def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

# https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# checks if aircraft is close to a line vector used in localizer guidance
def checkLineDistance(beaconpos, runwaypos, pos, d = 20):
    start = copy.deepcopy(beaconpos)
    end = copy.deepcopy(runwaypos)
    vector = list(map(lambda x,y: y-x, start, end))
    interval = list(map(lambda x: x / distance(start, end), vector))
    while distance(start, end) > 2 ** 1.5:
        if distance(pos, start) < d:
            return True
        start = list(map(lambda x,y: x+y, start, interval))
    return False

# changes safety status of aircraft based on proximity and fuel limits
def checkSafety(app):
    # TODO create storm proximity constraint
    for fl1 in app.flights:
        if 0 < fl1.pos[0] < len(app.airport.storm[0]) and 0 < fl1.pos[1] < len(app.airport.storm[1]):
            if app.airport.storm[int(fl1.pos[1] // imageScale)][int(fl1.pos[0] // imageScale)] == "firebrick1":
                fl1.safe = False
                app.cause = "Storm"
                break
        if fl1.fuel / fl1.fuelRate < 5:
            fl1.crash = True
            app.cause = "Fuel"
        elif fl1.fuel / fl1.fuelRate < 30:
            fl1.safe = False
            app.cause = "Fuel"
            break
        for fl2 in app.flights:
            if fl1 != fl2:
                d = distance(fl1.pos, fl2.pos)
                altDiff = abs(fl1.alt - fl2.alt)
                if d < 40 and altDiff < 500 and (fl1.alt and fl2.alt) > 500:
                    fl1.safe = fl2.safe = False
                    fl1.crash = fl2.crash = True
                    app.cause = "Proximity"
                if d < 80 and altDiff < 1500:
                    fl1.safe = fl2.safe = False
                    app.cause = "Proximity"
                    break
                else:
                    fl1.safe = fl2.safe = True
                    app.cause = None

# returns a heading from a 2d cartesian vector
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

def hdgAngle(hdg):
    return (360 - (hdg + 270) % 360) % 360

# returns a 2d cartesian vector from a magnetic heading value
def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return [spd * math.cos(angle), spd * math.sin(angle)]

# returns a normal vector of the given vector
def normalVector(vector):
    vector[0], vector[1] = -vector[1], vector[0]
    return vector

# checks the most efficient direction to turn (left or right) to get to heading
def checkDirection(currHdg, hdg):
    if hdg == 0: hdg = 360
    if hdg - currHdg >= 180 or -180 <= hdg - currHdg <= 0:
        return False
    else: return True

# test to check direction of turn when given select headings
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
    
# game classes
class Flight(object):
    
    def __init__(self, callsign, type, pos, hdg, spd, alt, vs, start, end, fuel):
        self.callsign = callsign
        self.type = type
        self.pos = pos
        self.hdg = hdg
        self.spd = spd
        self.alt = alt
        self.vs = vs
        self.fuelRate = int(fuel / 500) + 0.01
        self.start = start
        self.end = end
        self.direct = None
        self.acc = 0
        self.color = 'light green'
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

    # returns ICAO airline code
    def airline_code(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return code

    # returns airline name
    def airline_name(self):
        code = ''
        for letter in self.callsign:
            if letter.isalpha():
                code += letter
        return airlines[code]

    # returns a list of all the airline's main airports and hubs
    def airline_hubs(self):
        return airlineHubs[self.airline_code()]

    # returns the flight number of the flight
    def flt_no(self):
        airline = no = ''
        for letter in self.callsign:
            if letter.isalpha():
                airline += letter
            elif letter.isdigit():
                no += letter
        return f"{airlines[airline]} {no}"

    # moves aircraft with current parameters
    def move(self):
        #self.path.append(self.pos)
        self.pos[0] += hdgVector(self.hdg, self.spd / 100)[0]
        self.pos[1] -= hdgVector(self.hdg, self.spd / 100)[1]
        self.alt += self.vs / 25
        self.hdg += self.bank
        self.spd += self.acc
        self.fuel -= self.fuelRate
        if self.direct != None:
            if type(self) == Arrival and not self.ILS:
                self.direct_waypoint(self.direct)

    # aircraft banks at a 3 degree angle to change heading to "heading mode"
    def change_hdg(self, hdg):
        if (self.hdg % 360) != hdg:
            if checkDirection(self.hdg, hdg):
                self.bank = 3
                self.hdgCon = hdg
            else: 
                self.bank = -3
                self.hdgCon = hdg
        else: self.bank = 0

    # aircraft changes speed with a 3kt/s acceleration
    def change_spd(self, spd):
        if self.spd != spd:
            sign = int((spd - self.spd) / abs((spd - self.spd)))
            self.acc = sign * 3
            self.spdCon = spd

    # aircraft changes altitude with 2000 ft/min vertical speed
    def change_alt(self, alt):
        if self.alt != alt:
            sign = int((alt - self.alt) / abs((alt - self.alt)))
            self.vs = sign * 2000
            self.altCon = alt
        else: 
            self.vs = 0
            self.altCon = alt

    # checks if aircraft is on the map (within map boundaries)
    def check_on_grid(self, width, height):
        if (0 <= self.pos[0] < width and 0 <= self.pos[1] < height):
            return True
        return False

    # checks for the parameter constraints set when changing alt, hdg, spd, etc.
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

    # aircraft directs to the waypoint and changes to "direct mode"
    def direct_waypoint(self, waypoint):
        req_hdg = vectorHdg(self.pos, waypoint.pos)
        if self.hdg != req_hdg:
            self.direct = waypoint
            self.change_hdg(req_hdg)
        elif distance(self.pos, waypoint.pos) < 50:
            self.hdg = req_hdg
            self.direct = None
        
    def altitude_range(self):
        time = 25 * (self.altCon - self.alt) / self.vs
        distance = self.spd / 100 * time
        return distance

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

    # aircraft is cleared for takeoff
    def clear_takeoff(self):
        self.cleared = True

    # TODO replace with vspeed 
    # aircraft takesoff (accelerates to speed when it will increase in altitude)
    def takeoff(self):
        if self.spd < self.type.vspeed:
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
        #! Landing probability
        self.ga = random.choice([True] * 1 + [False] * 6)
        #self.ga = True
        self.landed = False
        self.ga_state = self.ga
    
    # aircraft checks for any ILS beacons
    def check_ILS(self, runways):
        for runway in runways:
            #print(distance(self.pos, runway.beacon), self.hdg, runway.hdg)
            if checkLineDistance(runway.beacon, runway.pos, self.pos) and abs(self.hdg - runway.hdg) < 40:
                self.ILS = True
                self.runway = runway
                self.intercept_ILS(runway)
                self.direct = runway
            if self.ILS:
                self.capture_gs(self.runway)
                self.land(self.runway)

    # aircraft decreases in speed during final approach (glideslope)
    def gs_change_spd(self, spd):
        if self.spd != spd:
            sign = int((spd - self.spd) / abs((spd - self.spd)))
            self.acc = sign * 2
            self.spdCon = spd

    # aircraft captures localizer of ILS system which horizontally guides aircraft
    def intercept_ILS(self, runway):
        if checkLineDistance(runway.beacon, runway.pos, self.pos, 8):
            self.direct_waypoint(runway)

    # aircraft captures glideslope that vertically guides aircraft to ground
    def capture_gs(self, runway):
        if 0 < self.alt < 4000 and distance(self.pos, runway.pos) < 200:
            time = (distance(self.pos, runway.pos) - 5) / (self.spd / 100)
            self.vs = - int(self.spd * 4.8)
            self.gs_change_spd(140)

    # aircraft lands on runway if speed, altitude are 
    # appropriate and no go around is declared
    def land(self, runway):
        if self.alt < 100 and distance(self.pos, runway.pos) < 15:
            if not self.ga:
                self.landed = True
            else: 
                self.go_around()
                self.ga = False
    
    # aircraft perform go around procedures
    def go_around(self):
        self.alt = 120
        self.vs = 2500
        self.change_alt(3500)
        self.change_spd(210)
        self.hdg = self.runway.hdg
        self.ILS = False

class Aircraft(object):
    
    def __init__(self, name, code, size, freq):
        self.name = name
        self.code = code
        self.size = size
        self.freq = freq
        if self.size == "A":
            self.vspeed = 60
        else: self.vspeed = (ord(self.size) - ord("A")) * 10 + 100

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

    def __init__(self, code, pos, runways, size):
        self.pos = pos
        self.code = code
        self.runways = runways
        self.size =  self.traffic = size
        self.waypoints = []

    # returns official aircraft name (real world mode)
    def name(self):
        return airports[self.code]

    # aircraft that are larger than the airport size will not be generated
    # TODO create purpose for this condition
    def check_size_limits(self, aircraft):
        if ord(aircraft.size) > ord(self.size):
            return False
        return True

    # generates a size dependent number of random waypoint object
    # and adds it to the airport's waypoint list
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
        self.open = True
        if airport.size not in ["A", "B"]:
            if list(map(lambda x: x.open, airport.runways)).count(True) > 0:
                self.wind = airport.weather.winds[int(self.pos[1] // 5)][int(self.pos[0] // 5)]
                self.open = self.check_winds(airport.winds)
        else: self.open = True
        #print(list(map(lambda x: x.open, filter(lambda x: x.open == True, airport.runways))))
        self.num = roundHalfUp(hdg / 10)
        self.length = length
        self.plength = self.length / 400
        self.beacon = [self.pos[0] - hdgVector(self.hdg, 275)[0], 
                        self.pos[1] + hdgVector(self.hdg, 275)[1]]
        #self.wind = airport.winds[self.pos[1] // 20, self.pos[0] // 20]

    # if wind heading and spd is greater than legal crosswind limits, the runway is closed
    def check_winds(self, winds):
        x, y = int(self.pos[0] // imageScale), int(self.pos[1] // imageScale)
        if ((abs(winds[y][x][0] - self.hdg) < 80 or abs(winds[y][x][0] - self.hdg + 180) % 360 < 80) and winds[y][x][1] < 10):
            return True
        return False

    # returns the three points of isosceles triangle with the 
    # beacon as the mid point of the base and the runway as the upper point
    def range_ILS(self):
        norm = normalVector(list(map(lambda x,y: x-y, self.beacon, self.pos)))
        p2 = list(map(lambda x,y: x - y / 15, self.beacon, norm))
        p3 = list(map(lambda x,y: x + y / 15, self.beacon, norm))
        p1 = self.pos
        return p1, p2, p3

class Weather(object):

    def __init__(self, airport, winds, storm):
        airport.storm = storm
        self.stormLevel = random.randrange(0,3)
        self.winds = airport.winds = winds
        self.visibility = self.stormLevel

    def createStorms(self, pos, airport, level):
        self.stormLevel = level
        self.winds = self.createWinds()

    def createWinds(self, airport):
        pass

testCheckDirection()