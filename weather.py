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
            # if pressure difference is not zero
            if (dx and dy) != 0:
                diff = L[y + dy][x + dx] - L[y][x]
                # direction based pressure differences
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

# returns list scaled to a range of -1, 1
def changeRange(L):
    right, left = -1, 1
    for row in L:
        if max(row) > right:
            right = max(row)
        elif min(row) < left:
            left = min(row)
    result = copy.deepcopy(L)
    scale = 1 / (right - left)
    for y in range(len(result)):
        for x in range(len(result[0])):
            result[y][x] = (result[y][x] - left) * scale - 1
    return result

# returns color map of weather map
def stormCloud(L):
    result = L
    #! scale to control storm probability
    scale = random.uniform(-0.05, 0)
    for y in range(len(L)):
        for x in range(len(L[0])):
            # regular
            a, b, c, d = -1.1, -1.03, -1, -0.93
            if a <= L[y][x] + scale <= b:
                result[y][x] = "firebrick1"
            elif b < L[y][x] + scale <= c:
                result[y][x] = "yellow3"
            elif c < L[y][x] + scale <= d:
                result[y][x] = "green3"
            elif d < L[y][x] + scale:
                result[y][x] = "black" 
    return result

# removes zeros from first and last rows and cols 
# (pressure map starts from 1st row and ends before last row)
def removeZeros(L):
    for row in L:
        row.remove(0)
    L.pop()

noiseMap = result
#print2dList(noiseMap)
winds = wind(changeRange(noiseMap))

#print(stormCloud(noiseMap))