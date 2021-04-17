import random

width, height = 1920, 1080
board = [[0] * width for row in range(height)]
half = [0.5, 1]

start = random.randrange(random.randrange(0, width))
end = start

avg = (start + width) / 2

def getCellBounds(app, row, col):
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col + 1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row + 1) / app.rows
    return (x0, y0, x1, y1)

def findRoute(board, x, y):
    if height == 