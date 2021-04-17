import string, math, time
from airline_data import airlines
from airport_data import airports
from cmu_112_graphics import *


def findCallsign(app, cmd):
    #TODO check for call sign in verbal or code form
    # code
    for word in cmd.split(" "):
        if word.startswith(""):
            for aircraft in app.aircrafts:
                if word == aircraft.callsign:
                    return word
                no = aircraft.fltno.split(" ")[1]
                callsign = f"{airlines[aircraft.airline]} {no}"
                if callsign in cmd:
                    return aircraft.callsign

print(findCallsign(app, "Delta 123"))

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