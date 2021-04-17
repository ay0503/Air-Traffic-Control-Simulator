from cmu_112_graphics import *
from objects import *
from arrival_generator import *
from commands import *
import time, string

def appStarted(app):
    # graphics
    app.color = "white"
    app.boardWidth, app.boardHeight = app.width - 250, app.height - 50
    app.input = []
    app.command = ""
    
    # app states
    app.crash = False
    app.selected = None
    app.startTime = time.time()
    
    # airports
    # TODO runway generator from data
    KLAX = Airport("KLAX", [[0, -6, 83], [0, -11, 83], [0, +6, 83], [0, +11, 83]], 'F')

    # inital parameters
    app.airport = KLAX
    app.wind = [123, 12]
    app.timerDelay = 1000
    
    # aircrafts
    app.flights = []
    for count in range(2):
        app.flights.append(createArrival(app.boardWidth, app.boardHeight, app.airport))
    app.display = app.flights[:min(len(app.flights), app.height // 180)]

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
        # TODO check for limits
        executeCommand(app.flights, app.command)
        app.input = []
    elif event.key == "Up":
        if app.display != app.flights[:min(len(app.flights), app.height // 18)]:
            app.display = app.flights + app.flights[:-1]
    elif event.key == "Down":
        if app.display != app.flights[-min(len(app.flights), app.height // 18):]:
            
        pass

def mousePressed(app, event):
    # detect mouse click on plane for selection
    for aircraft in app.flights:
        if ((event.x - aircraft.pos[0]) ** 2 + (event.y - aircraft.pos[1]) ** 2) ** 0.5 < 20:
            app.selected = aircraft

def sizeChanged(app):
    app.boardWidth, app.boardHeight = app.width - 250, app.height - 40

def mouseDragged(app, event):
    if app.selected != None:
        app.selected.pos = [event.x, event.y]

def timerFired(app):
    # moves aircraft
    for aircraft in app.flights:
        aircraft.move()
    checkSafety(app.flights)
    # create arrivals every 30 seconds
    ticker = int(time.time() - app.startTime)
    if ticker % 10 == 0 and ticker > 0:
        app.flights.append(createArrival(app.width, app.height, app.airport))
    for aircraft in app.flights:
        if aircraft.crash:
            app.crash = True
        aircraft.checkConstraints()
        if not aircraft.checkOnGrid(app.boardWidth, app.boardHeight):
            app.flights.remove(aircraft)
    # TODO check for arrivals
    #aircraft.checkArrival()

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.boardWidth, app.boardHeight, fill = 'black')
    if app.selected != None:
        canvas.create_text(app.boardWidth - 20, app.boardHeight - 20, anchor = 'e', 
                        text = f"{app.selected.callsign} - {app.selected.fltno()}", 
                        font = "Arial 14 bold", fill = 'white')

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
        """ canvas.create_oval(runway.beacon[0] - 2, runway.beacon[1] - 2, 
                            runway.beacon[0] + 2, runway.beacon[1] + 2,
                            fill = "blue") """

# draws aircraft and information
def drawAircraft(app, canvas, plane):
    info = f"{plane.callsign}, {plane.hdg}°, {plane.spd}kt, {int(plane.alt)}ft, {plane.vs}ft/m"
    x, y = plane.pos
    r = 40
    if not plane.safe: safetyColor = 'red'
    else: safetyColor = 'light green'
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
    # safety ring
    canvas.create_oval(x - r, y - r, x + r, y + r, outline = safetyColor)

def drawSidebar(app, canvas):
    margin = 5
    # white background
    canvas.create_rectangle(app.boardWidth, 0, app.width, app.height,
                            fill = app.color)
    # titles
    canvas.create_text((app.boardWidth + app.width) / 2, 15, text = 'Flights',
                        font = "Arial 14 bold")
    # draw flight sticks
    for row in range(min(len(app.flights), app.height // 180)):
        flight = app.display[row]
        info = f"{flight.callsign},  {flight.type.code},  {flight.hdg}°,  {flight.spd}kt, \n{int(flight.alt)}ft,  {flight.vs}ft/m,  {flight.start} - {flight.end}"
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
    # command cursor
    """ if int(ticker) % 2 == 0:
        canvas.create_line(lastLetter, app.boardHeight + 9, lastLetter, app.height - 9,
                        width = 3) """

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
    for aircraft in app.flights:
        drawAircraft(app, canvas, aircraft)
    drawCommandInput(app, canvas)
    drawSidebar(app, canvas)
    drawWind(app, canvas)

runApp(width = 1920, height = 1080)