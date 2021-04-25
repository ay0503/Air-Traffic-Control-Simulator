from cmu_112_graphics import *
from objects import *
from flight_generator import *
from airport_generation import *
from commands import *
from draw_functions import *
import time, string, random

# TODO create timer
# TODO create fuel restriction
# TODO flight time, limits, fuel
#* AI FOR WEATHER AVOIDANCE
#* WEATHER EVENTS THAT AFFECT AIRPORT AND AIRCRAFT
#* WINDS, STORMS
#* PROBABILITY OF LANDINGS
#* EXTRA CONTROL MODES
#* CONSTRAINTS THAT END THE GAME(SAFETY VIOLATION)
#* SAFETY: Proximity, Fuel, 
#* GOAL STATES: Scores (motivation)

def appStarted(app):
    # graphics
    app.color = "white"
    app.sidebarWidth = 260
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 50
    app.input = []
    app.command = ""
    app.detailHeight = 240
    app.controlHeight = 460
    app.margin = 5
    
    # app states
    app.crash = False
    app.selected = None
    app.selected_waypoint = None
    app.startTime = time.time()
    app.type = False
    app.draw = []
    app.pro = False
    
    # airports
    #* GAMEMODES: Real World Data, Random Generated Data, Maybe? Custom building
    # TODO runway generator from data
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
    #pprint(f"Airport: {vars(app.airport)}")

    # inital parameters
    app.timerDelay = 1000
    app.index = 0
    app.timer = 0
    
    # aircrafts
    app.flights = []
    for count in range(2):
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
    app.flights.append(createDeparture(app.airport))
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

def mousePressed(app, event):
    if 0 < event.x < app.mapWidth and app.mapHeight < event.y < app.height:
        app.type = True
    # detect mouse click on plane for selection
    if 0 < event.x < app.mapWidth and 0 < event.y < app.mapHeight:
        for aircraft in app.flights:
            if distance(aircraft.pos, (event.x, event.y)) < 20:
                app.selected = aircraft
        for waypoint in app.airport.waypoints:
            if distance(waypoint.pos, (event.x, event.y)) < 20:
                app.selected_waypoint = waypoint
        #app.selected = None

# changes map size
def sizeChanged(app):
    app.mapWidth, app.mapHeight = app.width - app.sidebarWidth, app.height - 50

# dragging flights for debugging
def mouseDragged(app, event):
    if app.selected != None:
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
    checkSafety(app.flights)
    # create arrivals every 30 seconds
    if app.timer % 10 == 0 and app.timer > 0 and len(app.flights) < 10:
        app.flights.append(createArrival(app.mapWidth, app.mapHeight, app.airport))
        """ if not flight.check_on_grid(app.mapWidth, app.mapHeight):
            app.flights.remove(aircraft) """

def redrawAll(app, canvas):
    if app.crash:
        drawGameOver(app, canvas)
    drawBackground(app, canvas)
    drawAirport(app, canvas)
    for flight in app.flights:
        if type(flight) == Departure:
            drawDeparture(app, canvas, flight)
        else: drawArrival(app, canvas, flight)
    drawWaypoints(app, canvas)
    drawCommandInput(app, canvas)
    drawSidebar(app, canvas)
    drawWind(app, canvas)

runApp(width = 1920, height = 1080)