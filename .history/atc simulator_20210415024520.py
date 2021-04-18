from cmu_112_graphics import *
from objects import *
#from airports import *


def appStarted(app):
    # graphics
    app.color = "white"
    app.airport = 'KLAX'
    app.timerDelay = 400
    app.wind = [123, 12]

    # app states

    # aircrafts
    A1 = Aircraft("DAL123", [450, 330], 133, 300, 7000, 0)
    A2 = Aircraft("BAW321", [800, 600], 233, 250, 4000, 0)

    # airports
    KLAX = Airport("KLAX", [[0, -2, 25], [0, -4, 25], [0, +2, 25], [0, +4, 25]])

    # inital parameters
    app.airports = [KLAX]
    app.aircrafts = [A1, A2]

def keyPressed(app, event):
    if event.key == "Up":
        app.hdg += 4
    elif event.key == "Down":
        app.hdg -= 4
    elif event.key == "w":
        app.wind[0] -= 4
    pass

def keyReleased(app, event):
    pass

def mousePressed(app, event):
    pass

def mouseReleased(app, event):
    pass

def mouseMoved(app, event):
    pass

def mouseDragged(app, event):
    pass

def timerFired(app):
    for aircraft in app.aircrafts:
        aircraft.move()

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    pass

def drawAirport(app, canvas, airport):
    #TODO draw runways'
    length = 12
    for runway in airport.runways:
        canvas.create_line(runway[0], runway[1], runway[0] + length, 
                        runway[1] +  length, fill = app.color, width = 4)

# draws aircraft and information
def drawAircraft(app, canvas, plane):
    info = f"{plane.callsign}, {plane.hdg}, {plane.spd}, {plane.alt}, {plane.vs}"
    x, y = plane.pos
    # aircraft
    canvas.create_rectangle(x - 5, y - 5, 
                            x + 5, y + 5, outline = app.color)
    # pointer
    canvas.create_line(x, y, 
                        x + hdgVector(plane.hdg, plane.spd / 6)[0],
                        y - hdgVector(plane.hdg, plane.spd / 6)[1], 
                        fill = app.color)
    # aircraft information
    canvas.create_text(x + 10, y, text = info, 
                        anchor = "w", font = "Arial 8 bold", fill = 'white')

# wind circle direction indicator
def drawWind(app, canvas):
    r = 40
    hdg = app.wind[0]
    spd = app.wind[1]
    canvas.create_oval(app.width - 30, 30, app.width - 30 - r, 30 + r, 
                        outline = app.color, width = 2)
    canvas.create_line(app.width - 30 - r / 2, 
                        30 + r / 2, 
                        app.width - 30 - r / 2 + hdgVector(hdg, spd / 20)[0], 
                        30 + r / 2 +  hdgVector(hdg, spd / 20)[1], 
                        fill = app.color)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    for airport in app.airports:
        drawAirport(app, canvas, airport)
    for aircraft in app.aircrafts:
        drawAircraft(app, canvas, aircraft)
    #drawWind(app, canvas)

runApp(width=1280, height=720)