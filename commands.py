import string, math, time
from objects import *
from airline_data import airlines
from airport_data import airports
from airport_generation import *
from flight_generator import *

testAirport = generateAirport([800, 500])
testAirport.waypoints.append(Waypoint("BELLY", [0,0]))

testFlights = [Flight('DAL123', 'B738', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI', 535),
        Flight('KAL123', 'B738', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI', 535),
        Flight('DAL3232', 'B738', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI', 535),]


# typo recgnition

def letterCounts(word):
    result = dict()
    for letter in list(word):
        result[letter] = result.get(letter, 0) + 1
    return result

def closeEnough(typo, word, index):
    diff = 0
    typoData, wordData = letterCounts(typo), letterCounts(word)
    for key in wordData:
        if key not in typoData.keys():
            diff += 1
        else:
            diff += abs(typoData[key] - wordData[key])
    for i in range(min(len(word), len(typo))):
        if not ((typo[i:] in word[i:]) or (word[i:] in typo[i:])):
            diff += 1
    return diff / (2 * len(word)) < index

def findMatches(typo, words, index):
    for word in words:
        if closeEnough(typo, word, index):
            return word
    return None

# command recognition

def findCallsign(cmd, aircrafts):
    word = cmd.split(' ')
    for aircraft in aircrafts:
        no = aircraft.flt_no().split(" ")[1]
        # non-verbal case (no spaces)
        if word[0] == aircraft.callsign:
            return word[0]
        # non-verbal case (spaces)
        if word[0] + word[1] == aircraft.callsign:
            return aircraft.callsign
        # verbal case (spaces)
        if aircraft.flt_no() in cmd:
            return aircraft.callsign
        # number only case
        if word[0] == no:
            return aircraft.callsign
            
def findAltitude(words):
    numbers = []
    for word in words:
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        if int(number) % 50 == 0:
            return number

def findAltCommand(cmd):
    words = cmd.split(" ")
    keywords = ["climb", "descend"]
    for word in words:
        if findMatches(word, keywords, 0.5) != None:
            altComm = words[words.index(word):]
            return findAltitude(altComm)
    return None

def findHeading(words):
    numbers = []
    for word in words:
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        if 0 <= int(number) <= 360:
            return number

def findHdgCommand(cmd):
    words = cmd.split(" ")
    keywords = ["heading", "turn", "right", "left"]
    for word in words:
        if findMatches(word, keywords, 0.5) != None:
            hdgComm = words[words.index(word):]
            return findHeading(hdgComm)
    return None

def findSpeed(words):
    numbers = []
    for word in words:
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        # speed is under 250 kts below 10000 ft
        if 130 <= int(number) < 250 and int(number) % 5 == 0:
            return number

def findWaypoint(words, airport):
    names = []
    for word in words:
        if word.isalpha() and 2 < len(word) < 6:
            names.append(word)
    for name in names:
        for waypoint in airport.waypoints:
            if name == waypoint.name:
                return waypoint
    return None

def findDirectCommand(cmd, airport):
    words = cmd.split(" ")
    keywords = ["direct", "waypoint"]
    for word in words:
        if findMatches(word, keywords, 0.4) != None:
            wptComm = words[words.index(word):]
            return findWaypoint(wptComm, airport)
    return None

def findSpdCommand(cmd):
    words = cmd.split(" ")
    keywords = ["accelerate", "decelerate", "speed", "decel"]
    for word in words:
        if findMatches(word, keywords, 0.4) != None:
            spdComm = words[words.index(word):]
            return findSpeed(spdComm)
    return None

def findTakeoffClearance(cmd):
    words = cmd.split(" ")
    keywords = ["cleared", "takeoff"]
    for keyword in keywords:
        if keyword not in words:
            return False
    return True

def debugCommand(cmd):
    words = cmd.split(" ")
    return ("debug" in words)

# keyword based command recognition
def divideCommand(cmd, flights, airport):
    callsign = findCallsign(cmd, flights)
    alt = findAltCommand(cmd)
    wpt = findDirectCommand(cmd, airport)
    clr = findTakeoffClearance(cmd)
    hdg = findHdgCommand(cmd)
    spd = findSpdCommand(cmd)
    return (callsign, alt, wpt, hdg, spd, clr)

def debugExecuteCommand(flights, airport, cmd):
    if cmd == "crash":
        random.choice(flights).crash = True
        return
    fuel = None
    if "fuel" in cmd:
        fuel = 3000
    (callsign, alt, wpt, hdg, spd, clr) = divideCommand(cmd, flights, airport)
    flight = None
    for fl in flights:
        if fl.callsign == callsign:
            flight = fl
    if flight != None:
        if fuel != None: flight.fuel = fuel
        if alt != None: flight.alt = int(alt)
        if hdg != None: flight.hdg = int(hdg)
        if spd != None: flight.spd = int(spd)

def executeCommand(flights, airport, cmd):
    (callsign, alt, wpt, hdg, spd, clr) = divideCommand(cmd, flights, airport)
    flight = None
    for fl in flights:
        if fl.callsign == callsign:
            flight = fl
    if flight != None:
        if type(flight) == Departure:
            flight.clear_takeoff()
        if alt != None: flight.change_alt(int(alt))
        if wpt != None: flight.direct_waypoint(wpt)
        if hdg != None: flight.change_hdg(int(hdg))
        if spd != None: flight.change_spd(int(spd))

def testFindMatches():
    print("Testing Typo Recognition...", end = "")
    assert(findMatches("accalerte", ["accelerate", "decelerate"], 0.5) == "accelerate")
    assert(findMatches("accalerte", ["decelerate", "accelerate"], 0.5) == "accelerate")
    assert(findMatches("decsend", ["climb", "descend"], 0.4) == "descend")
    assert(findMatches("headng", ["accelerate", "heading"], 0.4) == "heading")
    assert(findMatches("drct", ["heading", "direct"], 0.5) == "direct")
    assert(findMatches("acclrate", ["heading", "direct"], 0.5) == None)
    print("Passed")

def testDivideCommand():
    print("Testing Command Recognition...", end = "")
    assert(divideCommand("DAL123 fly heading 230 climb to 3000", testFlights, testAirport) == ('DAL123', '3000', None, '230', None, False))
    """ assert(divideCommand("DAL 123 descend to 2000", testFlights, testAirport) == ('DAL123', '2000', None, None, None, False))
    assert(divideCommand("123 descend to 2000", testFlights, testAirport) == ('DAL123', '2000', None, None, None, False))
    assert(divideCommand("Delta 3232 decelerate to 210", testFlights, testAirport) == ('DAL3232', None, None, None, '210', False))
    assert(divideCommand("DAL 123 direct to BELLY", testFlights, testAirport) == ('DAL123', None, testAirport.waypoints[0], None, None, False))
    assert(divideCommand("Korean Air 123 turn right heading 350", testFlights, testAirport) == ('KAL123', None, None, '350', None, False))
    assert(divideCommand("DAL123 decelerate to 200", testFlights, testAirport) == ('DAL123', None, None, None, "200", False)) """
    print("Passed")

testFindMatches()
testDivideCommand()