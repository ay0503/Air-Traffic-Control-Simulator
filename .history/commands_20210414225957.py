def findCallsign(cmd):
    #TODO check for call sign in verbal or code form
    for word in cmd.split(" "):
        if word.startswith(""):
            pass

def divideCommand(cmd):
    callsign = findCallsign

def testDivideCommand():
    c1 = "DAL123 fly heading 230 climb to 3000"
    c2 = "DAL123 descend to 2000"
    c3 = "Delta 3232 "
    assert(divideCommand(c1))
    assert(divideCommand(c2))
    assert(divideCommand(c3))
    print("Passed")