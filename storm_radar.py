from objects import *
from cmu_112_graphics import *
from perlin_noise import result
from weather import stormCloud, changeRange

#* STORM CLOUD VISUALIZER

# draw storm cloud
def appStarted(app):
    app.margin = 5
    app.rows = 90
    app.cols = 160
    app.storm = stormCloud(changeRange(result))
    app.image = Image.new(mode='RGB', size=(len(app.storm[0]), len(app.storm)))
    for y in range(len(app.storm)):
        for x in range(len(app.storm[0])):
            r, g, b = 0, 0, 0
            if app.storm[y][x] == "black":
                r, g, b = 0, 0, 0
            elif app.storm[y][x] == "green3":
                r, g, b, = 0, 205, 0
            elif app.storm[y][x] == "yellow3":
                r, g, b = 205, 205, 0
            elif app.storm[y][x] == "firebrick1":
                r, g, b = 255, 48, 48
            app.image.putpixel((x,y),(r, g, b))
    app.image = app.scaleImage(app.image, 10)

def getCellBounds(app, row, col):
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col + 1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

# draw wind board
def drawClouds(app, canvas):
    for row in range(len(app.storm)):
        for col in range(len(app.storm[0])):
            color = app.storm[row][col]
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = color)

def redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image))

#runApp(width = len(result[0]) * 10, height = len(result) * 10)