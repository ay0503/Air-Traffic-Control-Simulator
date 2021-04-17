import string, math, time
from objects import *
from airline_data import airlines
from airport_data import airports

A1 = Aircraft("DAL123", [450, 330], 133, 300, 7000, 0, 'KSEA', "KLAX")
A2 = Aircraft("BAW321", [800, 600], 233, 250, 4000, 0, 'EGLL', "KLAX")
A3 = Aircraft("KAL434", [0, 700], 87, 250, 9000, -1000, 'RKSI', "KLAX") 
aircrafts = [A1, A2, A3]

def findCallsign(cmd):
    #TODO check for call sign in verbal or code form
    # code
    for word in cmd.split(" "):
        if word.startswith(""):
            for aircraft in aircrafts:
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
    if  "climb" in words:
        altComm = words[words.index("climb") + 1:]
        return findAltitude(altComm)
    elif "descend" in words:
        altComm = words[words.index("descend") + 1:]
        return findAltitude(altComm)
    return None

def findHdgCommand(cmd):
    words = cmd.split(" ")
    if "heading" in words:
        hdgComm = words[words.index('heading') + 1:]
        return findHeading(hdgComm)
    elif "turn" in words:
        hdgComm = words[words.index('turn') + 1:]
        return findHeading(hdgComm)
    return None

def findHeading(words):
    numbers = []
    for word in words:
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        if 0 <= int(number) < 360 == 0:
            return number

def divideCommand(cmd):
    callsign = findCallsign(cmd)
    alt = findAltCommand(cmd)
    hdg = findHdgCommand(cmd)
    return callsign, alt, hdg

print(divideCommand("DAL123 fly heading 230 climb to 3000"))

def testDivideCommand():
    c1 = "DAL123 fly heading 230 climb to 3000"
    c2 = "DAL123 descend to 2000"
    c3 = "Delta 3232 "
    assert(divideCommand(c1))
    assert(divideCommand(c2))
    assert(divideCommand(c3))
    print("Passed")