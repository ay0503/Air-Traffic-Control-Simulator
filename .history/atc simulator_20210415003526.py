from cmu_112_graphics import *
from objects import *
#from airports import *


def appStarted(app):
    # graphics
    app.color = "white"
    app.airport = 'KLAX'
    app.x, app.y = 500, 418
    app.hdg = 35
    app.timerDelay = 600
    app.wind = 30, 12
    # app states

    # inital parameters
    pass

def hdgVector(hdg, spd):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return spd * math.cos(angle), spd * math.sin(angle)

def keyPressed(app, event):
    if event.key == "Up":
        app.hdg += 4
    elif event.key == "Down":
        app.hdg -= 4
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

def drawAircraft(app, canvas):
    #for aircraft in aircrafts:
    canvas.create_rectangle(app.x - 5, app.y - 5, 
                            app.x + 5, app.y + 5, outline = app.color,
                            )
    canvas.create_line(app.x, app.y, 
                        app.x + 30 * hdgVector(app.hdg)[0],
                        app.y + 30 * hdgVector(app.hdg)[1], 
                        fill = app.color)
    pass

def drawWind(app, canvas):
    r = 40
    hdg, spd = app.wind
    canvas.create_circle(app.width - 10, 10, app.width - 10 - r, 10 + r)
    canvas.create_line(app.width - 10 - r / 2, 10 + r / 2, 
                        app.width - 10 - r + r * hdgVector(hdg, spd)[0], 
                        10 + r / 2 +  r * hdgVector(hdg, spd)[1])

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    #drawAirport(app, canvas)
    #drawAircraft(app, canvas)
    drawWind(app, canvas)

runApp(width=1280, height=720)