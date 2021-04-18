import string, math, time
from objects import *
from airline_data import airlines
from airport_data import airports
from arrival_generator import *


testFlights = [Flight('DAL123', 'B738', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI'),
        Flight('KAL123', 'B738', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI'),
        Flight('DAL3232', 'B738', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI'),]

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
            
def findAltitude(words):
    numbers = []
    for word in words:
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        if int(number) % 500 == 0:
            return number

def findAltCommand(cmd):
    words = cmd.split(" ")
    keywords = ["climb", "descend"]
    for keyword in keywords:
        if keyword in words:
            altComm = words[words.index(keyword):]
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
    for keyword in keywords:
        if keyword in words:
            hdgComm = words[words.index(keyword):]
            return findHeading(hdgComm)
    return None

def findSpeed(words):
    numbers = []
    for word in words:
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        # speed is under 250 kts below 10000 ft
        if 130 <= int(number) < 250:
            return number

def findWaypoint(words, airport):
    numbers = []
    for word in words:
        if word.isalpha():
            numbers.append(word)
    for number in numbers:
    pass

def findDirectCommand(cmd):
    words = cmd.split(" ")
    keywords = ["direct", "waypoint"]
    for keyword in keywords:
        if keyword in words:
            wptComm = words[words.index(keyword):]
            return findWaypoint(wptComm)
    return None

def findSpdCommand(cmd):
    words = cmd.split(" ")
    keywords = ["accelerate", "decelerate", "speed", "decel"]
    for keyword in keywords:
        if keyword in words:
            spdComm = words[words.index(keyword):]
            return findSpeed(spdComm)
    return None

# keyword based command recognition
def divideCommand(cmd, flights):
    callsign = findCallsign(cmd, flights)
    alt = findAltCommand(cmd)
    hdg = findHdgCommand(cmd)
    spd = findSpdCommand(cmd)
    return (callsign, alt, hdg, spd)

def executeCommand(flights, airport, cmd):
    (callsign, alt, hdg, spd) = divideCommand(cmd, flights)
    flight = None
    for fl in flights:
        if fl.callsign == callsign:
            flight = fl
    if flight != None:
        if alt != None: flight.change_alt(int(alt))
        if wpt != None: flight.direct_waypoint(waypoint)
        if hdg != None: flight.change_heading(int(hdg))
        if spd != None: flight.change_spd(int(spd))

def testDivideCommand():
    print("Testing Command Recognition")
    assert(divideCommand("DAL123 fly heading 230 climb to 3000", testFlights) == ('DAL123', '3000', '230', None))
    assert(divideCommand("DAL 123 descend to 2000", testFlights) == ('DAL123', '2000', None, None))
    assert(divideCommand("Delta 3232 decelerate to 210", testFlights) == ('DAL3232', None, None, '210'))
    assert(divideCommand("Korean Air 123 turn right heading 350", testFlights) == ('KAL123', None, '350', None))
    assert(divideCommand("DAL123 decelerate to 200", testFlights) == ('DAL123', None, None, "200"))
    print("Passed")

testDivideCommand()