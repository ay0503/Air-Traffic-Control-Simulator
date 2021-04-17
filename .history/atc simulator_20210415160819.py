from cmu_112_graphics import *
from objects import *
#from airports import *


def appStarted(app):
    # graphics
    app.color = "white"
    app.airport = 'KLAX'
    app.timerDelay = 1000
    app.wind = [123, 12]
    app.selected = None
    app.boardWidth, app.boardHeight = app.width - 250, app.height
    # app states

    # aircrafts
    A1 = Aircraft("DAL123", [450, 330], 133, 300, 7000, 0)
    A2 = Aircraft("BAW321", [800, 600], 233, 250, 4000, 0)
    A3 = Aircraft("KAL434", [0, 700], 87, 250, 9000, -1000)

    # airports
    KLAX = Airport("KLAX", [[0, -6, 83], [0, -11, 83], [0, +6, 83], [0, +11, 83]])

    # inital parameters
    app.airports = [KLAX]
    app.aircrafts = [A1, A2, A3]

def keyPressed(app, event):
    if app.selected != None:
        if event.key == "Up":
            app.selected.hdg += 4
        elif event.key == "Down":
            app.selected.hdg -= 4
        elif event.key == "w":
            app.selected.wind[0] -= 4
        pass

def mousePressed(app, event):
    # detect mouse click on plane for selection
    for aircraft in app.aircrafts:
        if ((event.x - aircraft.pos[0]) ** 2 + (event.y - aircraft.pos[1]) ** 2) ** 0.5 < 20:
            app.selected = aircraft
    pass

def mouseScrolled(app, event):
    pass

def mouseDragged(app, event):
    #TODO drag airline info stick
    pass

def timerFired(app):
    for aircraft in app.aircrafts:
        aircraft.move()
    #TODO check for arrivals
    #aircraft.checkArrival()
    #TODO add departing and approaching flights

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    if app.selected != None:
        canvas.create_text(app.width - 20, app.height - 20, anchor = 'e', 
                            text = f"{app.selected.callsign}", font = "Arial 14 bold",
                            fill = 'white')
    pass

def drawAirport(app, canvas, airport):
    #TODO draw runways properly
    cx, cy = app.boardWidth / 2, app.height / 2
    for runway in airport.runways:
        dx, dy = hdgVector(runway[2], 30)
        # draw runway
        canvas.create_line(cx + runway[0], cy + runway[1], 
                        cx + runway[0] + dx, 
                        cy + runway[1] + dy, 
                        fill = app.color, width = 3)
        #TODO draw ILS wing
        #canvas.create_polygon(cx + runway[0], )

# draws aircraft and information
def drawAircraft(app, canvas, plane):
    info = f"{plane.callsign}, {plane.hdg}°, {plane.spd}kt, {int(plane.alt)}ft, {plane.vs}ft/m"
    x, y = plane.pos
    # aircraft
    canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, outline = app.color)
    # pointer
    canvas.create_line(x, y, x + hdgVector(plane.hdg, plane.spd / 6)[0],
                y - hdgVector(plane.hdg, plane.spd / 6)[1], fill = app.color)
    # aircraft information
    canvas.create_text(x + 10, y, text = info, 
                        anchor = "w", font = "Arial 8 bold", fill = 'white')

def drawSidebar(app, canvas):
    margin = 10
    canvas.create_rectangle(app.boardWidth, 0, app.width, app.height,
                            fill = app.color)
    for row in range(len(app.aircrafts)):
        flight = app.aircrafts[row]
        info = f"{flight.callsign}, {flight.hdg}°, {flight.spd}kt, \
                {int(flight.alt)}ft, {flight.vs}ft/m"
        canvas.create_rectangle(app.boardWidth + margin, margin + row * 80,
                                app.width - margin, margin + (row + 1) * 80,
                                outline = 'black', )
        canvas.create_text(app.boardWidth + margin, margin + row * 80,
                            anchor = 'nw', text = info, font = 'Arial 12 bold')
    pass

# wind circle direction indicator
def drawWind(app, canvas):
    r = 40
    hdg = app.wind[0]
    spd = app.wind[1]
    canvas.create_oval(app.width - 30, 30, app.width - 30 - r, 30 + r, 
                        outline = app.color)
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
    drawSidebar(app, canvas)
    #drawWind(app, canvas)

runApp(width=1280, height=720)