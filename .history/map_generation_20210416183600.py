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

moves = [[1, 0], [-1, 0], [0, 1]]

def moveIsLegal(board, x, y, start):
    if (0 <= x < len(board[0]) and 0 <= y < len(board) and )

def findRoute(board, x, y, start):
    if (x, y) == (end, len(board)):
        return board
    for move in moves:
        x += move[0]
        y += move[1]
        if 
    