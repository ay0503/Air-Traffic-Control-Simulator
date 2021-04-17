from cmu_112_graphics import *
from objects import *
from arrival_generator import *
from commands import *
import time, string

def appStarted(app):
    # graphics
    app.color = "white"
    app.airport = 'KLAX'
    app.timerDelay = 200
    app.wind = [123, 12]
    app.selected = None
    app.boardWidth, app.boardHeight = app.width - 250, app.height - 50
    app.startTime = time.time()
    app.input = []
    app.command = ""

    # app states


    # airports
    #TODO runway generator from data
    KLAX = Airport("KLAX", [[0, -6, 83], [0, -11, 83], [0, +6, 83], [0, +11, 83]])

    # inital parameters
    app.airport = KLAX

    # aircrafts
    #TODO random aircraft generator
    app.aircrafts = [createArrival(app.boardWidth, app.boardHeight, app.airport)]

def keyPressed(app, event):
    if app.selected != None:
        if event.key == "Up":
            app.selected.hdg += 4
        elif event.key == "Down":
            app.selected.hdg -= 4
        elif event.key == "w":
            app.selected.wind[0] -= 4
    #if 0 < event.x < app.boardWidth and app.boardHeight < event.y < app.height:
    if event.key in string.printable:
        app.input.append(event.key)
    elif event.key == "Space":
        app.input.append(" ")
    elif event.key == "Backspace":
        app.input = app.input[:-1]
    elif event.key == "Enter":
        app.command = "".join(app.input)
        print(app.command)
        #TODO check for limits
        executeCommand(app.aircrafts, app.command)
        app.input = []

def mousePressed(app, event):
    # detect mouse click on plane for selection
    for aircraft in app.aircrafts:
        if ((event.x - aircraft.pos[0]) ** 2 + (event.y - aircraft.pos[1]) ** 2) ** 0.5 < 20:
            app.selected = aircraft

def sizeChanged(app):
    app.boardWidth, app.boardHeight = app.width - 250, app.height - 40

def mouseDragged(app, event):
    #TODO drag airline info stick
    pass

def timerFired(app):
    for aircraft in app.aircrafts:
        aircraft.move()
    # create arrivals every 30 seconds
    print(int(time.time() - app.startTime))
    ticker = int(time.time() - app.startTime)
    if ticker < 10:
        if ticker % 10 == 0 and ticker > 0:
            app.aircrafts.append(createArrival(app.width, app.height, app.airport))
    #TODO check distancing
    #keepDistance(app)
    #TODO check for arrivals
    #aircraft.checkArrival()

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
    for row in range(min(len(app.aircrafts), app.height // 180)):
        flight = app.aircrafts[row]
        info = f"{flight.callsign}, {flight.hdg}°, {flight.spd}kt,\n{int(flight.alt)}ft, {flight.vs}ft/m, {flight.start} - {flight.end}"
        canvas.create_rectangle(app.boardWidth + margin, 30 + row * (50 + margin),
                                app.width - margin, 30 + row * margin + (row + 1) * 50,
                                outline = 'black', width = 2)
        canvas.create_text(app.boardWidth + 3 * margin, 30 + row * margin + (row + 0.5) * 50,
                            anchor = 'w', text = info, font = 'Arial 12 bold')

def drawCommandInput(app, canvas):
    text = "".join(app.input)
    lastLetter = 9 * len(text) + 95
    ticker = time.time() - app.startTime
    canvas.create_rectangle(0, app.boardHeight, app.boardWidth, app.height, 
                            fill = 'gray', outline = app.color, width = 2)
    canvas.create_text(5, (app.boardHeight + app.height) / 2, anchor = 'w', 
                        text = f"Command: {text}", font = 'Arial 12 bold')
    if int(ticker) % 2 == 0:
        canvas.create_line(lastLetter, app.boardHeight + 9, lastLetter, app.height - 9,
                        width = 3)

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
    drawCommandInput(app, canvas)
    drawSidebar(app, canvas)
    drawWind(app, canvas)

runApp(width = 1920, height = 1080)