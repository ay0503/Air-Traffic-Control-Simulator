from cmu_112_graphics import *
from objects import *
from flight_generator import *
from airport_generation import *
from commands import *
from draw_functions import *
from weather import winds, stormCloud, changeRange
from perlin_noise import result
import time, string

#!!! IF THE GAME IS TOO SLOW, PRESS "X" TO DISABLE WEATHER VISUALIZATION

def appStarted(app):
    # graphics
    app.color = "white"
    app.sidebarWidth = 260
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 60
    app.input = []
    app.command = ""
    app.detailHeight = 240
    app.controlHeight = 460
    app.margin = 5
    
    # app states
    app.crash = False
    app.selected_waypoint = None
    app.startTime = time.time()
    app.type = False
    app.draw = []
    app.pro = True
    app.score = 0
    app.debug = False
    app.finished = set()
    app.pressure = noiseMap
    app.image1 = Image.new(mode='RGB', size=(app.mapWidth, app.mapHeight))
    app.timerDelay = 1000
    app.index = 0
    app.timer = 0
    app.rows = app.mapHeight // 10
    app.cols = app.mapWidth // 10
    app.cause = None
    app.not_draw = False

    #* FUTURE GAMEMODES: Real World Data, Random Generated Data, Maybe? Custom building
    # pre generation
    """ app.airport = Airport("KLAX", [app.mapWidth / 2, app.mapHeight / 2], [], 'F')
    app.airport.runways += [Runway('25L', [0, -6], 251, 12000, app.airport), 
                            Runway('24R', [0, +11], 251, 12000, app.airport),
                            Runway('25R', [0, -11], 251, 12000, app.airport),
                            Runway('24L', [0, +6], 251, 12000, app.airport)] """
    # random generation
    # TODO possibly make realism setting
    # TODO make size a difficulty setting
    app.airport = generateAirport([app.mapWidth / 2, app.mapHeight / 2])
    app.airport.create_waypoints(app.mapWidth, app.mapHeight)
    print("Size:", app.airport.size)
    # TODO implement storms as part of the weather object
    app.airport.weather = Weather(app.airport, winds, stormCloud(changeRange(result)))
    
    # flights
    app.flights = [createArrival(app.mapWidth, app.mapHeight, app.airport),
                    createDeparture(app.airport)]
    app.selected = app.flights[0]
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
            print("Command:", app.command)
            if debugCommand(app.command):
                debugExecuteCommand(app.flights, app.airport, app.command)
            else: executeCommand(app.flights, app.airport, app.command)
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
    elif event.key == "y":
        app.debug = not app.debug
    elif event.key == "x":
        app.not_draw = not app.not_draw

def mousePressed(app, event):
    # command input click
    if 0 < event.x < app.mapWidth and app.mapHeight < event.y < app.height:
        app.type = True
    # detect mouse click on plane for selection
    if 0 < event.x < app.mapWidth and 0 < event.y < app.mapHeight:
        for aircraft in app.flights:
            if distance(aircraft.pos, (event.x, event.y)) < 20:
                app.selected = aircraft
                break
            else: 
                app.selected = None
        for waypoint in app.airport.waypoints:
            if distance(waypoint.pos, (event.x, event.y)) < 20:
                app.selected_waypoint = waypoint
    # play again button detection
    if app.crash:
        if (app.mapWidth / 2 - 110 < event.x < app.mapWidth / 2 + 110 
            and app.mapHeight / 2 + 120 < event.y < app.mapHeight / 2 + 180):
            app.clickColor = 'green'
            appStarted(app)

# changes map size
def sizeChanged(app):
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 50

# dragging flights for debugging
def mouseDragged(app, event):
    if app.selected != None and app.debug:
        app.selected.pos = [event.x, event.y]
    app.draw.append((event.x, event.y))

def timerFired(app):
    """ print(list(map(lambda x: x.callsign, app.flights)))
    print(list(map(lambda x: x.callsign, app.display))) """
    app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]
    app.timer = (time.time() - app.startTime)
    # moves aircraft, checks for crashes and constraint violations
    for flight in app.flights:
        if flight.crash:
            app.crash = True
        flight.check_constraints()
        flight.move()
        if type(flight) == Arrival:
            flight.check_ILS(app.airport.runways)
            if flight.landed and flight not in app.finished:
                app.score += 10
                app.finished.add(flight)
        elif type(flight) == Departure:
            if flight.sent and flight not in app.finished:
                app.score += 5
                app.finished.add(flight)
    checkSafety(app.flights)
    # create arrivals every 30 seconds
    if int(app.timer % 120) == 0 and int(app.timer) > 0 and len(app.flights) < 6:
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
        if not flight.check_on_grid(app.mapWidth, app.mapHeight):
            app.flights.remove(flight)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawAirport(app, canvas)
    drawCommandInput(app, canvas)
    for flight in app.flights:
        if type(flight) == Departure:
            drawDeparture(app, canvas, flight)
        else: drawArrival(app, canvas, flight)
    drawWaypoints(app, canvas)
    drawSidebar(app, canvas)
    drawWind(app, canvas)
    if app.crash:
        drawGameOver(app, canvas)

runApp(width = 1920, height = 1080)