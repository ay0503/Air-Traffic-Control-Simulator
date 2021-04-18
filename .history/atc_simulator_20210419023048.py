from cmu_112_graphics import *
from objects import *
from arrival_generator import *
from airport_generation import *
from commands import *
import time, string, random

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
    app.type = False
    
    # airports
    # TODO runway generator from data
    # pre generation of
    """ app.airport = Airport("KLAX", [app.mapWidth / 2, app.mapHeight / 2], [], 'F')
    app.airport.runways += [Runway('25L', [0, -6], 251, 12000, app.airport), 
                            Runway('24R', [0, +11], 251, 12000, app.airport),
                            Runway('25R', [0, -11], 251, 12000, app.airport),
                            Runway('24L', [0, +6], 251, 12000, app.airport)] """
    # random generation
    app.airport = generateAirport([app.mapWidth / 2, app.mapHeight / 2])
    app.airport.create_waypoints(app.mapWidth, app.mapHeight)
    print(app.airport.size)
    #pprint(f"Airport: {vars(app.airport)}")

    # inital parameters
    app.wind = [random.randrange(0, 360), random.randrange(2,15)]
    app.timerDelay = 1000
    app.index = 0
    app.timer = 0
    
    # aircrafts
    app.flights = []
    for count in range(2):
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
    app.sticks = 5
    app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]

def keyPressed(app, event):
    if app.type:
        if event.key in string.printable:
            app.input.append(event.key)
        elif event.key == "Space":
            app.input.append(" ")
        elif event.key in ["Backspace", "Delete"]:
            app.input = app.input[:-1]
        elif event.key == "Enter":
            app.command = "".join(app.input)
            print(app.command)
            executeCommand(app.flights, app.airport, app.command)
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
    if 0 < event.x < app.mapWidth and app.mapHeight < event.y < app.height:
        app.type = True
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
    app.timer = (time.time() - app.startTime)
    # moves aircraft
    for aircraft in app.flights:
        aircraft.move()
    checkSafety(app.flights)
    # create arrivals every 30 seconds
    if app.timer % 10 == 0 and app.timer > 0:
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
    # checks for crashes and constraint violations
    for flight in app.flights:
        if flight.crash:
            app.crash = True
        flight.check_constraints()
        """ if not flight.check_on_grid(app.mapWidth, app.mapHeight):
            app.flights.remove(aircraft) """
    # TODO check for arrivals
    #aircraft.checkArrival()

def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.mapWidth, app.mapHeight, fill = 'black')
    increment = 200
    for dist in range(0, app.width, increment):
        canvas.create_oval(app.airport.pos[0] - dist, app.airport.pos[1] - dist,
                            app.airport.pos[0] + dist, app.airport.pos[1] + dist,
                            outline = app.color, dash = (1, 1))
        #canvas.create_text()
    if app.selected != None:
        canvas.create_text(app.mapWidth - 20, app.mapHeight - 20, anchor = 'e', 
                        text = f"{app.selected.callsign} - {app.selected.flt_no()}", 
                        font = "Arial 14 bold", fill = 'white')

def drawAirport(app, canvas):
    # TODO draw runways properly
    cx, cy = app.mapWidth / 2, app.mapHeight / 2
    for runway in app.airport.runways:
        rx, ry = runway.pos
        dx, dy = hdgVector(runway.hdg, runway.plength)
        p1, p2, p3, = runway.range_ILS()
        # draw ILS range
        canvas.create_line(p1, p2, fill = app.color, dash = (1, 1))
        canvas.create_line(p1, p3, fill = app.color, dash = (1, 1))
        canvas.create_line(p3, p2, fill = app.color, dash = (1, 1))
        canvas.create_line(runway.pos, runway.beacon, fill = app.color, dash = (1, 1))
        # draw runway
        canvas.create_line(rx, ry, rx + dx, ry + dy, fill = "light green", width = 3)
        # max beacon position
        canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill = app.color)

def drawWaypoints(app, canvas):
    for waypoint in app.airport.waypoints:
        cx, cy = waypoint.pos
        # TODO change circles to equilateral triangles
        canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill = app.color)
        canvas.create_text(cx - 5, cy - 5, text = waypoint.name, 
                        font = "Arial 9", fill = app.color, anchor = 'e')

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
    # trajectory
    if app.selected != None:
        if app.selected.direct == None:
            canvas.create_line(x, y, x + hdgVector(app.selected.hdg, 5 * app.selected.spd)[0],
                        y - hdgVector(app.selected.hdg, 5 * app.selected.spd)[1], fill = app.color,
                        dash = (1, 1))
        else:
            canvas.create_line(x, y, app.selected.direct.pos[0], app.selected.direct.pos[1], 
                                fill = app.color, dash = (1, 1))
    # change anchor opposite to pointer
    if plane.hdg < 180: anchor, offset = "e", -10
    else: anchor, offset = "w", 10
    # aircraft information
    canvas.create_text(x + offset, y, text = info, 
                        anchor = anchor, font = "Arial 8 bold", fill = 'white')
    # safety ring
    canvas.create_oval(x - r, y - r, x + r, y + r, outline = safetyColor, dash = (1, 1))

# draws sidebar with flight stick information
def drawSidebar(app, canvas):
    margin = 5
    # white background
    canvas.create_rectangle(app.mapWidth, 0, app.width, app.height,
                            fill = app.color)
    # titles
    canvas.create_text((app.mapWidth + app.width) / 2, 15, text = 'Flights',
                        font = "Arial 14 bold")
    # timer
    canvas.create_text((app.mapWidth + app.width) / 2, app.mapHeight, 
                    text = f'Timer: {int(app.timer // 60)}:{int((app.timer % 60))}', font = "Arial 21 bold")
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
    for flight in app.flights:
        drawAircraft(app, canvas, flight)
    drawCommandInput(app, canvas)
    drawSidebar(app, canvas)
    drawWind(app, canvas)
    drawWaypoints(app, canvas)

runApp(width = 1920, height = 1080)