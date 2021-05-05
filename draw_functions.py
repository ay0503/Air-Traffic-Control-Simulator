from cmu_112_graphics import *
from objects import *
from weather import noiseMap
import threading
from storm_radar import drawClouds

# draws weather, range rings (200nm)
def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.mapWidth, app.mapHeight, fill = 'black')
    increment = 200
    if not app.not_draw:
        drawClouds(app, canvas)
    for dist in range(0, app.width, increment):
        canvas.create_oval(app.airport.pos[0] - dist, app.airport.pos[1] - dist,
                            app.airport.pos[0] + dist, app.airport.pos[1] + dist,
                            outline = app.color, dash = (1, 1), width = 2.5)
    if app.selected != None:
        canvas.create_text(app.mapWidth - 20, app.mapHeight - 20, anchor = 'e', 
                        text = f"{app.selected.callsign} - {app.selected.flt_no()}", 
                        font = "Arial 14 bold", fill = app.color)
    canvas.create_text(2 * app.margin, app.mapHeight - 20, anchor = "w", text = f"{1000 // app.timerDelay}x Speed",
                        font = "Arial 14 bold", fill = app.color)

def drawClouds(app, canvas):
    canvas.create_image(app.mapWidth / 2, app.mapHeight / 2, image=ImageTk.PhotoImage(app.image))

def drawWarning(app, canvas):
    if app.cause != None:
        if int(app.count) % 2 == 0:
            color = "white"
            rect_color = "red"
        else: 
            color = "red"
            rect_color = "white"
        canvas.create_rectangle(app.mapWidth / 2 - 150, app.mapHeight - 90, 
                                app.mapWidth / 2 + 150, app.mapHeight - 50,
                                fill = color)
        canvas.create_text(app.mapWidth / 2, app.mapHeight - 70, text = f"{app.cause} Warning",
                            font = "Arial 25 bold", fill = rect_color)

# draws runways, ils vectors
def drawAirport(app, canvas):
    cx, cy = app.mapWidth / 2, app.mapHeight / 2
    for runway in app.airport.runways:
        rx, ry = runway.pos
        dx, dy = hdgVector(runway.hdg, runway.plength)
        p1, p2, p3, = runway.range_ILS()
        color = 'red'
        if runway.open:
            color = 'light green'
            # draw ILS range
            canvas.create_line(p1, p2, fill = app.color, dash = (1, 1), width = 1.5)
            canvas.create_line(p1, p3, fill = app.color, dash = (1, 1), width = 1.5)
            canvas.create_line(p3, p2, fill = app.color, dash = (1, 1), width = 1.5)
            canvas.create_line(runway.pos, runway.beacon, fill = app.color, 
                                dash = (1, 1), width = 1.5)
            # max beacon position
            canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill = app.color)
        # draw runway
        canvas.create_line(rx, ry, rx + dx, ry - dy, fill = color, width = 3)

# draws waypoints and names
def drawWaypoints(app, canvas):
    for waypoint in app.airport.waypoints:
        cx, cy = waypoint.pos
        p1 = (cx, cy - 4)
        p2 = (cx + 6 / 3 ** 0.5, cy + 2)
        p3 = (cx - 6 / 3 ** 0.5, cy + 2)
        canvas.create_polygon(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], fill = app.color)
        canvas.create_text(cx - 5, cy - 5, text = waypoint.name, 
                        font = "Arial 9 bold", fill = app.color, anchor = 'e')

# draws aircraft and information
def drawAircraft(app, canvas, plane, color):
    info = f"{plane.callsign}, {plane.hdg}°, {plane.spd}kt, {int(plane.alt)}ft, {plane.vs}ft/m"
    x, y = plane.pos
    r = 40
    # aircraft
    canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, outline = color, width = 2)
    # pointer
    canvas.create_line(x, y, x + hdgVector(plane.hdg, plane.spd / 6)[0],
                y - hdgVector(plane.hdg, plane.spd / 6)[1], fill = color, width = 2)
    # trajectory
    if app.selected == plane:
        if app.selected.direct == None:
            canvas.create_line(x, y, x + hdgVector(app.selected.hdg, 5 * app.selected.spd)[0],
                        y - hdgVector(app.selected.hdg, 5 * app.selected.spd)[1], fill = color,
                        dash = (1, 1), width = 2)
        elif type(app.selected) == Arrival and app.selected.ILS == True:
            canvas.create_line(app.selected.pos[0], app.selected.pos[1], app.selected.runway.pos[0], app.selected.runway.pos[1], 
                                fill = color, dash = (1, 1), width = 2)
        else:
            canvas.create_line(app.selected.pos[0], app.selected.pos[1], app.selected.direct.pos[0], app.selected.direct.pos[1], 
                                fill = color, dash = (1, 1), width = 2)
    # change anchor opposite to pointer
    if plane.hdg < 180: anchor, offset = "e", -10
    else: anchor, offset = "w", 10
    # aircraft information
    canvas.create_text(x + offset, y, text = info, 
                        anchor = anchor, font = "Arial 8 bold", fill = 'white')
    # safety ring
    canvas.create_oval(x - r, y - r, x + r, y + r, outline = plane.color, dash = (1, 1), width = 2)
    # altitude range
    if plane.altCon != -100 and plane.vs != 0:
        ar = plane.altitude_range()
        canvas.create_arc(plane.pos[0] - ar, plane.pos[1] - ar, 
                        plane.pos[0] + ar, plane.pos[1] + ar,
                        style = ARC, start = hdgAngle(plane.hdg) - 30, 
                        extent = 60, outline = app.color, width = 2.5)
    # path drawing feature
    """ if app.selected == plane:
        for i in range(len(plane.path) - 1):
            x0, y0 = plane.path[i]
            x1, y1 = plane.path[i + 1]
            canvas.create_line(x0, y0, x1, y1, fill = 'light green', width = 2) """

def drawDeparture(app, canvas, plane):
    if not plane.sent:
        drawAircraft(app, canvas, plane, "white")

def drawArrival(app, canvas, plane):
    if not plane.landed:
        drawAircraft(app, canvas, plane, "white")

# draws sidebar with flight stick information
def drawSidebar(app, canvas):
    # white background
    canvas.create_rectangle(app.mapWidth, 0, app.width, app.height, fill = app.color)
    # titles
    canvas.create_text((app.mapWidth + app.width) / 2, 15, text = 'Flights', font = "Arial 14 bold")
    # timer
    canvas.create_rectangle(app.mapWidth + app.margin, app.height - (60 + app.margin),
                                    app.width - app.margin, app.height - app.margin,
                                    outline = 'black', width = 2, fill = app.color)
    # game info
    canvas.create_text(app.mapWidth + app.margin + 10, app.height - app.margin - 30, 
                text = f'Airport: {app.airport.code}, Class {app.airport.size} \nTimer: {int(app.timer // 60)}:{int((app.timer % 60))}      Score: {int(app.score)}', 
                font = "Arial 15 bold", anchor = 'w')
    # other elements
    drawSidebarFlights(app, canvas)
    drawSidebarDetails(app, canvas)
    if not app.pro:
        drawSidebarControls(app, canvas,)
    
def drawSidebarDetails(app, canvas):
    if app.selected != None:
        x0, y0, x1, y1 = app.mapWidth + app.margin, 280 + 5 * app.margin, app.width - app.margin, 280 + app.detailHeight + 5 * app.margin
        canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', width = 2, fill = app.color)
        for row in range(len(app.selected.details)):
            key = app.selected.details[row]
            if key == 'type':
                data = vars(app.selected)[key].name
            else: 
                data = vars(app.selected)[key]
                if isinstance(data, float):
                    data = int(data)
            canvas.create_text(app.mapWidth + 3 * app.margin, y0 + (row + 1) * app.margin + (row + 0.5) * 20, 
                            text = f"{key.capitalize()}: {data}",  font = 'Arial 12 bold', anchor = 'w')

# TODO beginner control panel
def drawSidebarControls(app, canvas):
    base = 280 + 6 * app.margin + app.detailHeight
    r = 55
    x0, y0, x1, y1 = app.mapWidth + app.margin, base, app.width - app.margin, base + app.controlHeight
    canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', width = 2, fill = app.color)
    # left circle
    canvas.create_oval(x0 + app.margin, y0 + app.margin, x0 + app.margin + 2 * r, 
                        y0 + app.margin + 2 * r, outline = 'black', width = 2, fill = app.color)
    canvas.create_text(x0 + app.margin + r, y0 + app.margin + 10, text = "0", fill = "black", font = 'Arial 12 bold')
    canvas.create_text(x0 + app.margin + 2 * r - 10, y0 + app.margin + r, text = "90", fill = "black", font = 'Arial 12 bold')
    canvas.create_text(x0 + app.margin + 15, y0 + app.margin + r, text = "270", fill = "black", font = 'Arial 12 bold')
    canvas.create_text(x0 + app.margin + r, y0 + app.margin + 2 * r - 10, text = "180", fill = "black", font = 'Arial 12 bold')
    # start
    canvas.create_rectangle(x0 + app.margin, y0 + app.margin + 2.5 * r, x0 + app.margin + 2 * r, 
                        y0 + app.margin + 3.5 * r, outline = 'black', width = 2, fill = app.startColor)
    canvas.create_text(x0 + app.margin + r, y0 + app.margin + 3 * r, text = "Start", 
                        fill = "black", font = 'Arial 12 bold')
    # pause
    canvas.create_rectangle(x1 - app.margin, y0 + app.margin + 2.5 * r, x1 - app.margin - 2 * r, 
                        y0 + app.margin + 3.5 * r, outline = 'black', width = 2, fill = app.pauseColor)
    canvas.create_text(x1 - app.margin - r, y0 + app.margin + 3 * r, text = "Pause", 
                        fill = "black", font = 'Arial 12 bold')
    # 1x Speed
    canvas.create_rectangle(x0 + app.margin, y0 + app.margin + 4 * r, x0 + app.margin + 2 * r, 
                        y0 + app.margin + 5 * r, outline = 'black', width = 2, fill = app.onexColor)
    canvas.create_text(x0 + app.margin + r, y0 + app.margin + 4.5 * r, text = "1x Speed", 
                        fill = "black", font = 'Arial 12 bold')
    # 4x Speed
    canvas.create_rectangle(x1 - app.margin, y0 + app.margin + 4 * r, x1 - app.margin - 2 * r, 
                        y0 + app.margin + 5 * r, outline = 'black', width = 2, fill = app.fourxColor)
    canvas.create_text(x1 - app.margin - r, y0 + app.margin + 4.5 * r, text = "4x Speed", 
                        fill = "black", font = 'Arial 12 bold')
    if app.selected_waypoint != None:
        canvas.create_text(x1 - app.margin - r, y0 + app.margin + 4.5 * r, 
                        text = f"{app.selected_waypoint.name}" , font = 'Arial 12 bold')

def drawSidebarFlights(app, canvas):
    # draw flight sticks
    if len(app.flights) > 0:
        for row in range(len(app.display)):
            flight = app.display[row]
            if not flight.safe:
                if int(app.count) % 2 == 0:
                    color = "light green"
                else: color = "red"
            else: color = "light green"
            # object recognition not working on macOS 11.2.3 (slow calculation speed)
            info = f"{app.flights.index(flight) + 1}. {flight.callsign}, {flight.type.code}, {flight.hdg}°, {flight.spd}kt, \n{int(flight.alt)}ft,  {flight.vs}ft/m,  {flight.start} - {flight.end}"
            canvas.create_rectangle(app.mapWidth + app.margin, 30 + row * (50 + app.margin),
                                    app.width - app.margin, 30 + row * app.margin + (row + 1) * 50,
                                    outline = 'black', width = 2, fill = color)
            canvas.create_text(app.mapWidth + 3 * app.margin, 30 + row * app.margin + (row + 0.5) * 50,
                                anchor = 'w', text = info, font = 'Arial 12 bold')

# draws command prompt at the bottom of the screen
def drawCommandInput(app, canvas):
    text = app.command
    lastLetter = 9 * len(text) + 95
    canvas.create_rectangle(0, app.mapHeight, app.mapWidth, app.height, 
                            fill = 'gray', outline = app.color, width = 2)
    canvas.create_text(5, (app.mapHeight + app.height) / 2, anchor = 'w', 
                        text = f"Command: {text} |", font = 'Arial 12 bold')

# wind circle direction indicator
def drawWind(app, canvas):
    r = 40
    x, y = int(app.airport.pos[0] // 20), int(app.airport.pos[1] // 20)
    hdg = app.airport.weather.winds[y][x][0]
    spd = app.airport.weather.winds[y][x][1]
    canvas.create_oval(app.mapWidth - 30, 30, app.mapWidth - 30 - r, 30 + r, 
                        outline = app.color, width = 2)
    canvas.create_line(app.mapWidth - 30 - r / 2, 
                        30 + r / 2, 
                        app.mapWidth - 30 - r / 2 + hdgVector(hdg, 15)[0], 
                        30 + r / 2 - hdgVector(hdg, 15)[1], 
                        fill = app.color, width = 2)
    canvas.create_text(app.mapWidth - 40 - r, 30 + r / 2, anchor = 'e',
                        font = 'Arial 8', fill = app.color,
                        text = f'{int(hdg)} at {int(spd)} kts')

def drawGameOver(app, canvas):
    width, height = 110, 30
    canvas.create_rectangle(0, 0, app.mapWidth, app.mapHeight, fill = 'black')
    canvas.create_rectangle(app.mapWidth / 2 - width, app.mapHeight / 2 - height + 150,
                        app.mapWidth / 2 + width, app.mapHeight / 2 + height + 150,
                        fill = app.color, outline = "light green", width = 4)
    # text
    canvas.create_text(app.mapWidth / 2, app.mapHeight / 2 + 150, text = "Play Again",
                        font = "Arial 30 bold", fill = 'black')    
    canvas.create_text(app.mapWidth / 2, app.mapHeight / 2 - 70, text = "GAME OVER", 
                        font = "Arial 45 bold", fill = app.color)
    canvas.create_text(app.mapWidth / 2, app.mapHeight / 2, fill = app.color, font = "Arial 30 bold",
                        text = f"Game Ended Because of {app.cause} violation")
    canvas.create_text(app.mapWidth / 2, app.mapHeight / 2 + 70, text = f"Score: {app.score}", 
                        font = "Arial 30 bold", fill = app.color)   

def drawStartScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.mapWidth, app.mapHeight, fill = 'black')
    canvas.create_text(app.mapWidth / 2, app.mapHeight / 2, text = "Air Traffic Control Simulator",
                        font = "Arial 45 bold", fill = app.color)
    canvas.create_text(app.mapWidth / 2, app.mapHeight / 2 + 80, text = "Press the Start Button",
                        font = "Arial 25 bold", fill = app.color)
    canvas.create_rectangle(app.mapWidth, 0, app.width, app.height, fill = app.color)
    canvas.create_rectangle(0, app.mapHeight, app.mapWidth, app.height, 
                            fill = 'gray', outline = app.color, width = 2)
