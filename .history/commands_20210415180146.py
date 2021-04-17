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
        if 130 <= int(number) < 250:
            return number

def findSpdCommand(cmd):
    words = cmd.split(" ")
    keywords = ["accelerate", "decelerate", "speed"]
    for keyword in keywords:
        if keyword in words:
            hdgComm = words[words.index(keyword):]
            return findSpeed(hdgComm)
    return None


def divideCommand(cmd):
    callsign = findCallsign(cmd)
    alt = findAltCommand(cmd)
    hdg = findHdgCommand(cmd)
    spd = findSpdCommand(cmd)
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