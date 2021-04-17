from cmu_112_graphics import *
from objects import *
from arrival_generator import *
import time


def appStarted(app):
    # graphics
    app.color = "white"
    app.airport = 'KLAX'
    app.timerDelay = 100
    app.wind = [123, 12]
    app.selected = None
    app.boardWidth, app.boardHeight = app.width - 250, app.height
    app.startTime = time.time()
    # app states


    # airports
    #TODO runway generator from data
    KLAX = Airport("KLAX", [[0, -6, 83], [0, -11, 83], [0, +6, 83], [0, +11, 83]])

    # inital parameters
    app.airport = KLAX
    # aircrafts
    #TODO random aircraft generator
    A1 = Aircraft("DAL123", [450, 330], 133, 300, 7000, 0, 'KSEA', "KLAX")
    A2 = Aircraft("BAW321", [800, 600], 233, 250, 4000, 0, 'EGLL', "KLAX")
    A3 = Aircraft("KAL434", [0, 700], 87, 250, 9000, -1000, 'RKSI', "KLAX") 
    app.aircrafts = [A1, A2, A3]

def keyPressed(app, event):
    if app.selected != None:
        if event.key == "Up":
            app.selected.hdg += 4
        elif event.key == "Down":
            app.selected.hdg -= 4
        elif event.key == "w":
            app.selected.wind[0] -= 4
    if event.x > app.boardWidth and 0 < event.y < app.boardHeight < 355:
        

def mousePressed(app, event):
    # detect mouse click on plane for selection
    for aircraft in app.aircrafts:
        if ((event.x - aircraft.pos[0]) ** 2 + (event.y - aircraft.pos[1]) ** 2) ** 0.5 < 20:
            app.selected = aircraft
    pass

def mouseScrolled(app, event):
    pass

def sizeChanged(app):
    app.boardWidth, app.boardHeight = app.width - 250, app.height

def mouseDragged(app, event):
    #TODO drag airline info stick
    pass

def timerFired(app):
    for aircraft in app.aircrafts:
        aircraft.move()
    # create arrivals every 30 seconds
    print(int(time.time() - app.startTime))
    print(app.aircrafts)
    if int(time.time() - app.startTime) % 5 == 0:
        app.aircrafts.append(createArrival(app.width, app.height, app.airport))
    #TODO check for arrivals
    #aircraft.checkArrival()
    #TODO add departingflights

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.boardWidth, app.boardHeight, fill = 'black')
    if app.selected != None:
        canvas.create_text(app.boardWidth - 20, app.height - 20, anchor = 'e', 
                            text = f"{app.selected.callsign}", font = "Arial 14 bold",
                            fill = 'white')

def drawAirport(app, canvas):
    #TODO draw runways properly
    cx, cy = app.boardWidth / 2, app.boardHeight / 2
    for runway in app.airport.runways:
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
    # change anchor opposite to pointer
    if plane.hdg < 180: anchor, offset = "e", -10
    else: anchor, offset = "w", 10
    # aircraft information
    canvas.create_text(x + offset, y, text = info, 
                        anchor = anchor, font = "Arial 8 bold", fill = 'white')

def drawSidebar(app, canvas):
    margin = 5
    # white background
    canvas.create_rectangle(app.boardWidth, 0, app.width, app.height,
                            fill = app.color)
    # titles
    canvas.create_text((app.boardWidth + app.width) / 2, 15, text = 'Flights',
                        font = "Arial 14 bold")
    # draw flight sticks
    for row in range(min(len(app.aircrafts), 5)):
        flight = app.aircrafts[row]
        info = f"{flight.callsign}, {flight.hdg}°, {flight.spd}kt,\n{int(flight.alt)}ft, {flight.vs}ft/m, {flight.start} - {flight.end}"
        canvas.create_rectangle(app.boardWidth + margin, 30 + row * (50 + margin),
                                app.width - margin, 30 + row * margin + (row + 1) * 50,
                                outline = 'black', width = 2)
        canvas.create_text(app.boardWidth + 3 * margin, 30 + row * margin + (row + 0.5) * 50,
                            anchor = 'w', text = info, font = 'Arial 12 bold')

# wind circle direction indicator
def drawWind(app, canvas):
    r = 40
    hdg = app.wind[0]
    spd = app.wind[1]
    canvas.create_oval(app.boardWidth - 30, 30, app.boardWidth - 30 - r, 30 + r, 
                        outline = app.color, width = 2)
    canvas.create_line(app.boardWidth - 30 - r / 2, 
                        30 + r / 2, 
                        app.boardWidth - 30 - r / 2 + hdgVector(hdg, 1.5 * spd)[0], 
                        30 + r / 2 - hdgVector(hdg, 1.5 * spd)[1], 
                        fill = app.color, width = 2)
    canvas.create_text(app.boardWidth - 40 - r, 30 + r / 2, anchor = 'e',
                        font = 'Arial 8', fill = app.color,
                        text = f'{app.wind[0]} at {app.wind[1]} kts')


def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawAirport(app, canvas)
    for aircraft in app.aircrafts:
        drawAircraft(app, canvas, aircraft)
    drawSidebar(app, canvas)
    drawWind(app, canvas)

runApp(width = 1920, height = 1080)