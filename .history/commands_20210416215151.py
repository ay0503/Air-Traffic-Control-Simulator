import string, math, time
from objects import *
from airline_data import airlines
from airport_data import airports

def findCallsign(cmd, aircrafts):
    #TODO check for call sign in verbal or code form
    # code
    for word in cmd.split(" "):
        for aircraft in aircrafts:
            print(word, aircraft.callsign)
            if word == aircraft.callsign:
                return word
            no = aircraft.fltno().split(" ")[1]
            callsign = f"{airlines[aircraft.airlineCode()]} {no}"
            if callsign in cmd:
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
        if 0 <= int(number) < 360:
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
def divideCommand(cmd, aircrafts):
    callsign = findCallsign(cmd, aircrafts)
    alt = findAltCommand(cmd)
    hdg = findHdgCommand(cmd)
    spd = findSpdCommand(cmd)
    return (callsign, alt, hdg, spd)

def executeCommand(aircrafts, cmd):
    (callsign, alt, hdg, spd) = divideCommand(cmd, aircrafts)
    aircraft = None
    for flight in aircrafts:
        if flight.callsign == callsign:
            aircraft = flight
    if aircraft == None: return None
    if alt != None:
        aircraft.changeAlt()
    if hdg != None:
        aircraft.changeHeading(hdg)
    if spd != None:
        aircraft.changeSpd(spd)

cmd = "DLH19 turn right heading 350"
#print(divideCommand(cmd))

def testDivideCommand():
    c1 = "DAL123 fly heading 230 climb to 3000"
    c2 = "DAL123 descend to 2000"
    c3 = "Delta 3232 "
    assert(divideCommand(c1))
    assert(divideCommand(c2))
    assert(divideCommand(c3))
    print("Passed")