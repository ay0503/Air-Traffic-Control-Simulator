from cmu_112_graphics import *
from objects import *
#from airports import *


def appStarted(app):
    # graphics
    app.color = "white"
    app.airport = 'KLAX'
    app.timerDelay = 600
    app.wind = [123, 12]
    # app states

    # inital parameters
    aircrafts = []
    A1 = Aircraft("DAL123", (450, 330), 133, 300, 7000, 0)
    aircrafts.append(A1)

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle), spd * math.sin(angle)

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
    app.x += hdgVector(app.hdg, 30)[0]
    app.y += hdgVector(app.hdg, 30)[1]

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    pass

def drawAirport(app, canvas):
    #TODO draw runways
    pass

# draws aircraft and information
def drawAircraft(app, canvas, plane):
    info = f"{plane.callsign}, {plane.spd}, {plane.alt}, {plane.vs}"
    x, y = plane.pos
    #for aircraft in aircrafts:
    canvas.create_rectangle(x - 5, y - 5, 
                            x + 5, y + 5, outline = app.color)
    canvas.create_line(x, y, 
                        x + 30 * hdgVector(plane.hdg)[0],
                        y + 30 * hdgVector(plane.hdg)[1], 
                        fill = app.color)
    # aircraft information
    canvas.create_text(x, y, text = info, font = "Arial 20 bold")

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
    #drawAirport(app, canvas)
    for aircraft in aircrafts:
        drawAircraft(app, canvas, aircraft)
    #drawWind(app, canvas)

runApp(width=1280, height=720)