

class Aircraft(object):
    
    def __init__(self, pos, hdg, spd, alt, vs):
        self.pos = pos
        self.hdg = hdg
        self.spd = spd
        self.alt = alt
        self.vs = vs

    def changeHeading(self, hdg):
        self.hdg = hdg

    def changeSpd(self, spd):
        self.spd = spd

    def changeAlt(self, alt):
        self.vs = 
        self.alt = alt

    def directWaypoint(self, waypoint):
        self.hdg = waypoint - self.pos

    def 

