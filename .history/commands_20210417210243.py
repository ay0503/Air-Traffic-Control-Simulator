import string, math, time
from objects import *
from airline_data import airlines
from airport_data import airports
from arrival_generator import *


flights = [Flight('DAL123', [0, 0], 234, 230, 9000, 0, 'KLAX', 'RKSI')]

def findCallsign(cmd, aircrafts):
    for word in cmd.split(" "):
        for aircraft in aircrafts:
            # verbal case (no spaces)
            if word == aircraft.callsign:
                return word
            no = aircraft.fltno().split(" ")[1]
            callsign = f"{airlines[aircraft.airlineCode()]} {no}"
            # non-verbal code case (no spaces)
            if callsign in cmd:
                return aircraft.callsign
            # TODO non-verbal code case (spaces)

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

def findSpdCommand(cmd):
    words = cmd.split(" ")
    keywords = ["accelerate", "decelerate", "speed"]
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

def executeCommand(flights, cmd):
    (callsign, alt, hdg, spd) = divideCommand(cmd, flights)
    aircraft = None
    for flight in flights:
        if flight.callsign == callsign:
            aircraft = flight
    if aircraft == None: return None
    if alt != None:
        aircraft.changeAlt(int(alt))
    if hdg != None:
        aircraft.changeHeading(int(hdg))
    if spd != None:
        aircraft.changeSpd(int(spd))

cmd = "Delta123 turn right heading 350"
print(divideCommand(cmd, flights))

def testDivideCommand():
    c1 = "DAL123 fly heading 230 climb to 3000"
    c2 = "DAL123 descend to 2000"
    c3 = "Delta 3232 "
    assert(divideCommand(c1))
    assert(divideCommand(c2))
    assert(divideCommand(c3))
    print("Passed")