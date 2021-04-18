from cmu_112_graphics import *
from objects import *
#from airports import *


def appStarted(app):
    # graphics
    app.color = "light green"
    app.airport = 'KLAX'
    app.x, app.y = 500, 418
    app.hdg = 35
    app.timerDelay = 1000
    
    # app states

    # inital parameters
    pass

def hdgVector(hdg):
    angle = math.radians((360 - (hdg + 270) % 360) % 360)
    return math.cos(angle), math.sin(angle)

def keyPressed(app, event):
    pass

def keyReleased(app, event):
    if event.key == "Up":
        app.hdg += 1
    elif event.key == "Down":
        app.hdg -= 1
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
    app.x += 30 * hdgVector(app.hdg)[0]
    app.y += 30 * hdgVector(app.hdg)[1]

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

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawAirport(app, canvas)
    drawAircraft(app, canvas)

runApp(width=1280, height=720)