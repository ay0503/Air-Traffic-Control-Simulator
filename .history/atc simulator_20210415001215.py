from cmu_112_graphics import *
from objects import *
#from airports import *


def appStarted(app):
    # graphics
    app.color = "light green"
    app.airport = 'KLAX'
    app.x, app.y = 500, 418
    app.hdg = 35
    
    # app states

    # inital parameters
    pass

def hdgToAng(hdg):
    return (360 - (hdg + 270) % 360) % 360

def keyPressed(app, event):
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
    app.timerDelay = 100
    app.x += app.hdg * math.cos(hdgToAng(app.hdg))
    app.y += app.hdg * math.sin(hdgToAng(app.hdg))

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    pass

def drawAirport(app, canvas):
    #TODO draw runways
    pass

def drawAircraft(app, canvas):
    #for aircraft in aircrafts:
    app.hdg = 35
    canvas.create_rectangle(app.x - 5, app.y - 5, 
                            app.x + 5, app.y + 5, outline = app.color,
                            )
    canvas.create_line(app.x, app.y, 
                        app.x + app.hdg * math.cos(hdgToAng(app.hdg)),
                        app.y + app.hdg * math.sin(hdgToAng(app.hdg)), 
                        fill = app.color)
    pass

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawAirport(app, canvas)
    drawAircraft(app, canvas)

runApp(width=1280, height=720)