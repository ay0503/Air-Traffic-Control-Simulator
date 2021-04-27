import numpy as np
from objects import *

# external code
# https://www.kite.com/python/answers/how-to-add-noise-to-a-signal-using-numpy-in-python
def noise():
    # used as air pressure map
    L = np.random.normal(0, 0.3, (53,85))
    for y in range(len(L)):
        for x in range(len(L[0])):
            L[y][x] = '%.3f' % L[y][x]
    return L

# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows, cols = len(a), len(a[0])
    fieldWidth = len(a[0])
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

# calculate wind from average air pressure differences
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
    return [hdg, spd * 3]

# removes zeros from first and last rows and cols
def removeZeros(L):
    for row in L:
        row.remove(0)
    L.pop()

noiseMap = noise()
#print2dList(noiseMap)
winds = wind(noiseMap)