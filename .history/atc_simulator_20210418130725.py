from cmu_112_graphics import *
from objects import *
from arrival_generator import *
from commands import *
import time, string

def appStarted(app):
    # graphics
    app.color = "white"
    app.sidebarWidth = 260
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 50
    app.input = []
    app.command = ""
    
    # app states
    app.crash = False
    app.selected = None
    app.startTime = time.time()
    
    # airports
    # TODO runway generator from data
    app.airport = Airport("KLAX", [app.mapWidth / 2, app.mapHeight / 2], [], 'F')
    print(app.airport.pos)
    app.airport.runways += [Runway('25L', [0, -6], 251, 12000, app.airport), 
                            Runway('24R', [0, +11], 251, 12000, app.airport)]
    """ Runway('25R', [0, -11], 251, 12000, app.airport),
    Runway('24L', [0, +6], 251, 12000, app.airport), """
                           

    # inital parameters
    app.wind = [123, 12]
    app.timerDelay = 1000
    app.index = 0
    
    # aircrafts
    app.flights = []
    for count in range(2):
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
    app.sticks = 7
    app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]

def keyPressed(app, event):
    if 0 < event.x < app.mapWidth and app.mapHeight < event.y < app.height:
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
    if event.key == "Up":
        if app.display != app.flights[:app.sticks]:
            app.index -= 1
            app.display = app.flights[app.index:app.index + app.sticks]
    elif event.key == "Down":
        if app.display != app.flights[len(app.flights) - app.sticks:]:
            app.index += 1
            app.display = app.flights[app.index:app.index + app.sticks]
    elif event.key == "+":
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
        app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]

def mousePressed(app, event):
    # detect mouse click on plane for selection
    for aircraft in app.flights:
        if ((event.x - aircraft.pos[0]) ** 2 + (event.y - aircraft.pos[1]) ** 2) ** 0.5 < 20:
            app.selected = aircraft

# changes map size
def sizeChanged(app):
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 40

# dragging flights for debugging
def mouseDragged(app, event):
    if app.selected != None:
        app.selected.pos = [event.x, event.y]

def timerFired(app):
    """ print(list(map(lambda x: x.callsign, app.flights)))
    print(list(map(lambda x: x.callsign, app.display))) """
    app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]
    # moves aircraft
    for aircraft in app.flights:
        aircraft.move()
    checkSafety(app.flights)
    # create arrivals every 30 seconds
    ticker = int(time.time() - app.startTime)
    if ticker % 10 == 0 and ticker > 0:
        app.flights.append(createArrival(app.width, app.height, app.airport))
    # checks for crashes and constraint violations
    for aircraft in app.flights:
        if aircraft.crash:
            app.crash = True
        aircraft.checkConstraints()
        """ if not aircraft.checkOnGrid(app.mapWidth, app.mapHeight):
            app.flights.remove(aircraft) """
    # TODO check for arrivals
    #aircraft.checkArrival()

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.mapWidth, app.mapHeight, fill = 'black')
    if app.selected != None:
        canvas.create_text(app.mapWidth - 20, app.mapHeight - 20, anchor = 'e', 
                        text = f"{app.selected.callsign} - {app.selected.fltno()}", 
                        font = "Arial 14 bold", fill = 'white')

def drawAirport(app, canvas):
    # TODO draw runways properly
    cx, cy = app.mapWidth / 2, app.mapHeight / 2
    for runway in app.airport.runways:
        rx, ry = runway.pos
        dx, dy = hdgVector(runway.hdg, runway.plength)
        p1, p2, p3, = runway.rangeILS()
        # draw ILS range
        canvas.create_polygon(p1, p2, p3, outline = app.color)
        canvas.create_line(runway.pos, runway.beacon, fill = app.color)
        # draw runway
        canvas.create_line(rx, ry, rx + dx, ry + dy, fill = app.color, width = 3)
        # max beacon position
        canvas.create_oval(runway.beacon[0] - 1, runway.beacon[1] - 1, 
                            runway.beacon[0] + 1, runway.beacon[1] + 1,
                            fill = "white")

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

# draws sidebar with flight stick information
def drawSidebar(app, canvas):
    margin = 5
    # white background
    canvas.create_rectangle(app.mapWidth, 0, app.width, app.height,
                            fill = app.color)
    # titles
    canvas.create_text((app.mapWidth + app.width) / 2, 15, text = 'Flights',
                        font = "Arial 14 bold")
    # draw flight sticks
    if len(app.flights) > 0:
        for row in range(len(app.display)):
            flight = app.display[row]
            # object recognition not working on macOS 11.2.3 (slow calculation speed)
            info = f"{app.flights.index(flight) + 1}. {flight.callsign}, {flight.type.code}, {flight.hdg}°, {flight.spd}kt, \n{int(flight.alt)}ft,  {flight.vs}ft/m,  {flight.start} - {flight.end}"
            canvas.create_rectangle(app.mapWidth + margin, 30 + row * (50 + margin),
                                    app.width - margin, 30 + row * margin + (row + 1) * 50,
                                    outline = 'black', width = 2, fill = 'light green')
            canvas.create_text(app.mapWidth + 3 * margin, 30 + row * margin + (row + 0.5) * 50,
                                anchor = 'w', text = info, font = 'Arial 12 bold')

# draws command prompt at the bottom of the screen
def drawCommandInput(app, canvas):
    text = "".join(app.input)
    lastLetter = 9 * len(text) + 95
    ticker = time.time() - app.startTime
    canvas.create_rectangle(0, app.mapHeight, app.mapWidth, app.height, 
                            fill = 'gray', outline = app.color, width = 2)
    canvas.create_text(5, (app.mapHeight + app.height) / 2, anchor = 'w', 
                        text = f"Command: {text}", font = 'Arial 12 bold')
    # command cursor
    """ if int(ticker) % 2 == 0:
        canvas.create_line(lastLetter, app.mapHeight + 9, lastLetter, app.height - 9,
                        width = 3) """

# wind circle direction indicator
def drawWind(app, canvas):
    r = 40
    hdg = app.wind[0]
    spd = app.wind[1]
    canvas.create_oval(app.mapWidth - 30, 30, app.mapWidth - 30 - r, 30 + r, 
                        outline = app.color, width = 2)
    canvas.create_line(app.mapWidth - 30 - r / 2, 
                        30 + r / 2, 
                        app.mapWidth - 30 - r / 2 + hdgVector(hdg, 1.5 * spd)[0], 
                        30 + r / 2 - hdgVector(hdg, 1.5 * spd)[1], 
                        fill = app.color, width = 2)
    canvas.create_text(app.mapWidth - 40 - r, 30 + r / 2, anchor = 'e',
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