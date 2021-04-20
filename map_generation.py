import random, math
from cmu_112_graphics import *

width, height = 360, 360
board = [([0] * width) for row in range(height)]

def f(x, y):
    x, y = math.radians(x), math.radians(y)
    return math.sin(x) ** 10 + math.cos(10 + y * x) * math.cos(x)

for y in range(height):
    for x in range(width):
        board[y][x] = f(x, y)


# returns cell bounds of a cell of the row and column
def getCellBounds(app, row, col):
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col + 1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

print(board)

def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def appStarted(app):
    app.board = board
    app.rows = len(app.board)
    app.cols = len(app.board[0])
    app.margin = 5

def drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = color,
                                    width = 3)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            color = abs(int(board[row][col] * 255))
            drawCell(app, canvas, row, col, rgbString(color, color, color))

def redrawAll(app, canvas):
    drawBoard(app, canvas)

for row in range(len(board)):
    for col in  range(len(board[0])):
        if board[row][col] < 0.5:
            board[row][col] = 0

runApp(width = 1920, height = 1080)