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

def findCommand(cmd):
    wordlist = cmd.split(" ")
    if cmd.contains("climb"):
        altComm = wordlist[wordlist.find("climb") + 1:]
        alt = findAltitude(altComm)
    pass

def findAltitude(cmd, wordlist):
    numbers = []
    for word in cmd.split(" "):
        if word.isdigit():
            numbers.append(word)
    for number in numbers:
        if int(number) % 500 == 0:
            return number

def divideCommand(cmd):
    callsign = findCallsign(cmd)

def testDivideCommand():
    c1 = "DAL123 fly heading 230 climb to 3000"
    c2 = "DAL123 descend to 2000"
    c3 = "Delta 3232 "
    assert(divideCommand(c1))
    assert(divideCommand(c2))
    assert(divideCommand(c3))
    print("Passed")