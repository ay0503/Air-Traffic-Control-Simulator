from objects import *
from cmu_112_graphics import *
import numpy as np

# external code
def noise():
    # used as air pressure map
    # https://www.kite.com/python/answers/how-to-add-noise-to-a-signal-using-numpy-in-python
    L = np.random.normal(0, 0.5, (51,83))
    for y in range(len(L)):
        for x in range(len(L[0])):
            L[y][x] = '%.3f' % L[y][x]
    return L

# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = maxItemLength(a)
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).rjust(fieldWidth), end='')
        print(' ]')
    print(']')

# wind map generation
def wind(L):
    result = [[0] * (len(L[0]) - 1) for y in range(len(L) - 1)]
    for x in range(1, len(L[0]) - 1):
        for y in range(1, len(L) - 1):
            wind = createWind(L, x, y)
            result[y - 1][x - 1] = wind
    removeZeros(result)
    return result

def createWind(L, x, y):
    result = []
    for dx in [-1, 0, +1]:
        for dy in [-1, 0, +1]:
            if (dx and dy) != 0:
                diff = L[y + dy][x + dx] - L[y][x]
                if diff > 0:
                    wind = [[-dx, -dy], 10 * abs(diff)]
                elif diff < 0: 
                    wind = [[dx, dy], 10 * abs(diff)]
                else: 
                    wind = [[0,0],0]
                result.append(wind)
    start = [0,0]
    for wind in result:
        vector = list(map(lambda x: x * wind[1], wind[0]))
        start = list(map(lambda x,y: x+y, start, vector))
    hdg = vectorHdg([0,0], start)
    spd = distance([0,0], start) / 7
    return [hdg, spd]

def removeZeros(L):
    for row in L:
        row.remove(0)
    L.pop()

noiseMap = noise()
#print2dList(noiseMap)
winds = wind(noiseMap)

# draw windmap
def appStarted(app):
    app.margin = 5
    app.rows = 18
    app.cols = 32
    app.winds = winds

def getCellBounds(app, row, col):
    # aka 'modelToView'
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawBoard(app, canvas):
    for row in range(len(app.winds)):
        for col in range(len(app.winds[0])):
            wind = app.winds[row][col]
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            midx, midy = (x0 + x1) * 0.5, (y0 + y1) * 0.5
            canvas.create_rectangle(x0, y0, x1, y1, fill='white')
            canvas.create_line(midx, midy, 
                    midx + hdgVector(wind[0], 10 * wind[1])[0],
                    midy + hdgVector(wind[0], 10 * wind[1])[1],
                    width = 1)

def redrawAll(app, canvas):
    drawBoard(app, canvas)

runApp(width=1660, height=1020)