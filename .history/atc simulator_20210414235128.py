from cmu_112_graphics import *
from objects import *
from aiports import *


def appStarted(app):
    # graphics
    app.color = "light green"
    app.airport = KLAX
    
    # app states

    # inital parameters
    pass

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

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    pass

def drawAirport(app, canvas):
    #TODO draw runways
    pass

def drawAircraft(app, canvas):
    #for aircraft in aircrafts:
    x, y = 500, 418
        canvas.create_rectangle(aircraft.pos.x - 5, aircraft.pos.y - 5, 
                                aircraft.pos.x + 5, aircraft.pos.y + 5, )
    pass

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawAirport(app, canvas)
    drawAircraft(app, canvas)

runApp(width=1280, height=720)