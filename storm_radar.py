from objects import *
from cmu_112_graphics import *
from perlin_noise import result
from weather import stormCloud

# draw storm cloud
def appStarted(app):
    app.margin = 5
    app.rows = 100
    app.cols = 100
    app.storm = stormCloud(result)

def getCellBounds(app, row, col):
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col + 1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

# draw wind board
def drawBoard(app, canvas):
    for row in range(len(app.storm)):
        for col in range(len(app.storm[0])):
            color = app.storm[row][col]
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = color)

def redrawAll(app, canvas):
    drawBoard(app, canvas)

runApp(width = len(result[0]) * 10, height = len(result) * 10)