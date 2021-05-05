from cmu_112_graphics import *
from objects import *
from flight_generator import *
from airport_generation import *
from commands import *
from perlin_noise import imageScale, octave
from weather import wind, stormCloud, changeRange
from draw_functions import *
import time, string

#!!! BUG ON MACOS WHERE AIRCRAFT SPAWNS UNDER COMMMAND PROMPT (not on Windows)
# TODO START SCREEN


def appStarted(app):

    # graphics
    app.color = "white"
    app.sidebarWidth = 260
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 60
    app.command = ""
    app.detailHeight = 240
    app.controlHeight = 460
    app.margin = 5
    app.pauseColor = "white"
    app.onexColor = "white"
    app.fourxColor = "white"
    app.startColor = "white"
    
    # app states
    app.crash = False
    app.selected_waypoint = None
    app.startTime = time.time()
    app.type = False
    app.pro = False
    app.score = 0
    app.debug = False
    app.timerDelay = 200
    app.index = 0
    app.timer = 0
    app.difficulty = 0
    app.rows = app.mapHeight // 10
    app.cols = app.mapWidth // 10
    app.cause = None
    app.not_draw = False
    app.count = 0
    app.start = False
    app.paused = False

    # weather
    app.imageScale = 5

    # random generation
    app.airport = generateAirport([app.mapWidth / 2, app.mapHeight / 2])
    app.airport.create_waypoints(app.mapWidth, app.mapHeight)
    newWeather(app)
    app.image = Image.new(mode='RGB', size=(len(app.airport.storm[0]), len(app.airport.storm)))
    saveImage(app)
    
    # flights
    app.flights = [createArrival(app.mapWidth, app.mapHeight, app.airport),
                    createDeparture(app.airport)]
    for i in range(app.difficulty):
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
    app.selected = app.flights[0]
    app.sticks = 5
    app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]

def newWeather(app):
    imageScale = 5
    width, height = 1660 // imageScale, 1020 // imageScale
    result = octave([[0] * (width) for y in range(height)], 0.4, 1, 2, random.randint(10,20))
    winds = wind(changeRange(result))
    storm = stormCloud(changeRange(result))
    app.airport.weather = Weather(app.airport, winds, storm)

def saveImage(app):
    for y in range(len(app.airport.storm)):
        for x in range(len(app.airport.storm[0])):
            r, g, b = 0, 0, 0
            if app.airport.storm[y][x] == "black":
                r, g, b = 0, 0, 0
            elif app.airport.storm[y][x] == "green3":
                r, g, b, = 10, 155, 10
            elif app.airport.storm[y][x] == "yellow3":
                r, g, b = 205, 205, 0
            elif app.airport.storm[y][x] == "firebrick1":
                r, g, b = 255, 48, 48
            app.image.putpixel((x,y),(r, g, b))
    app.image = app.scaleImage(app.image, imageScale)

def commandControl(app, event):
    if event.key in string.printable:
        app.command += event.key
    elif event.key == "Space":
        app.command += (" ")
    elif event.key in ["Backspace", "Delete"]:
        app.command = app.command[:-1]
    elif event.key == "Enter":
        print("Command:", app.command)
        if debugCommand(app.command):
            debugExecuteCommand(app.flights, app.airport, app.command)
        else: executeCommand(app.flights, app.airport, app.command)
        app.command = ""

def keyPressed(app, event):
    if app.type:
        commandControl(app, event)
    else:
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
        elif event.key == "p":
            app.paused = not app.paused
        elif event.key == "r":
            appStarted(app)

def mousePressed(app, event):
    # play again button detection
    if app.start:
        if app.crash:
            if (app.mapWidth / 2 - 110 < event.x < app.mapWidth / 2 + 110 
                and app.mapHeight / 2 + 120 < event.y < app.mapHeight / 2 + 180):
                appStarted(app)
        else:
            # command input click
            if 0 < event.x < app.mapWidth and app.mapHeight < event.y < app.height:
                app.type = True
            else:
                app.type = False
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
    base = 280 + 6 * app.margin + app.detailHeight
    r = 55
    x0, y0, x1, y1 = app.mapWidth + app.margin, base, app.width - app.margin, base + app.controlHeight
    if (x0 + app.margin < event.x < x0 + app.margin + 2 * r and 
        y0 + app.margin + 2.5 * r < event.y < y0 + app.margin + 3.5 * r):
        app.start = True
        app.startColor = "light green"
    elif (x1 - app.margin - 2 * r < event.x < x1 - app.margin and 
        y0 + app.margin + 2.5 * r < event.y < y0 + app.margin + 3.5 * r):
        app.paused = not app.paused
        if app.paused:
            app.pauseColor = "light green"
        else: app.pauseColor = "white"
    elif (x0 + app.margin < event.x < x0 + app.margin + 2 * r and
        y0 + app.margin + 4 * r < event.y < y0 + app.margin + 5 * r):
        if app.timerDelay != 1000:
            app.timerDelay = 1000
            app.onexColor = "light green"
            app.fourxColor = "white"
        else:
            app.timerDelay = 500
            app.onexColor = "white"
    elif (x1 - app.margin - 2 * r < event.x < x1 - app.margin and
        y0 + app.margin + 4 * r < event.y < y0 + app.margin + 5 * r):
        if app.timerDelay != 250:
            app.timerDelay = 250
            app.fourxColor = "light green"
            app.onexColor = "white"
        else:
            app.timerDelay = 500
            app.fourxColor = "white"

# changes map size
def sizeChanged(app):
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 50

# dragging flights for debugging
def mouseDragged(app, event):
    if app.selected != None and app.debug:
        app.selected.pos = [event.x, event.y]

def timerFired(app):
    if not (app.crash or app.paused) and app.start:
        app.count += 1
        app.display = app.flights[app.index:min(len(app.flights), app.index + app.sticks)]
        app.timer = (time.time() - app.startTime) // 2
        # moves aircraft, checks for crashes and constraint violations
        for flight in app.flights:
            if not flight.safe:
                if int(app.count) % 2 == 0:
                    flight.color = "light green"
                else: flight.color = "red"
            else: flight.color = "light green"
            if flight.crash:
                app.crash = True
            flight.check_constraints()
            flight.move()
            checkSafety(app)
            if type(flight) == Arrival:
                flight.check_ILS(app.airport.runways)
                if flight.landed:
                    app.score += 10
                    app.display.remove(flight)
                    app.flights.remove(flight)
            elif type(flight) == Departure:
                if flight.sent:
                    app.score += 5
                    app.display.remove(flight)
                    app.flights.remove(flight)
        # create arrivals every 120 seconds
        if int(app.timer % 120 * 5) == 0 and int(app.count) > 0 and len(app.flights) < 6:
            app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
            if not flight.check_on_grid(app.mapWidth, app.mapHeight):
                app.flights.remove(flight)

def redrawAll(app, canvas):
    if app.start:
        drawBackground(app, canvas)
        drawAirport(app, canvas)
        drawCommandInput(app, canvas)
        for flight in app.flights:
            if type(flight) == Departure:
                drawDeparture(app, canvas, flight)
            else: drawArrival(app, canvas, flight)
        drawWaypoints(app, canvas)
        drawWarning(app, canvas)
        drawSidebar(app, canvas)
        drawWind(app, canvas)
        if app.crash:
            drawGameOver(app, canvas)
    else:
        drawStartScreen(app, canvas)
        drawSidebarControls(app, canvas)

runApp(width = 1920, height = 1080)