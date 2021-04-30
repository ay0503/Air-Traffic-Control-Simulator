import numpy as np
from objects import *
from perlin_noise import result

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

def stormCloud(L):
    result = L
    for y in range(len(L)):
        for x in range(len(L[0])):
            a, b, c, d = -2.5, -0.4, 0.1, 0.6
            if a < L[y][x] <= b:
                result[y][x] = "black"
            elif b < L[y][x] <= c:
                result[y][x] = "green"
            elif c < L[y][x] <= d:
                result[y][x] = "yellow"
            elif d < L[y][x]:
                result[y][x] = "red" 
    return result

# removes zeros from first and last rows and cols
def removeZeros(L):
    for row in L:
        row.remove(0)
    L.pop()

noiseMap = result
#print2dList(noiseMap)
winds = wind(noiseMap)

#print(stormCloud(noiseMap))