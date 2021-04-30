import random

width = height = 1

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

def unitVector(x, y):
    k = (x ** 2 + y ** 2) ** -0.5
    return (k * x, k * y)

def gradient():
    x, y = random.uniform(-1, 1), random.uniform(-1, 1)
    return unitVector(x, y)

def fade(x):
    return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def interpolate(d, a, b):
    return (1 - d) * a + d * b

def noise(x, y, scale):
    # corners
    p1 = int(x), int(y)
    p2 = p1[0] + 1, p1[1]
    p3 = p1[0], p1[1] + 1
    p4 = p1[0] + 1, p1[1] + 1
    # gradient vectors
    g1, g2, g3, g4 = gradient(), gradient(), gradient(), gradient()
    # smooth step
    dx, dy = fade(x - p1[0]), fade(y - p1[1])
    # dot product
    d1, d2 = (x - p1[0], y - p1[1]), (x - p2[0], y - p2[1])
    d3, d4 = (x - p3[0], y - p3[1]), (x - p4[0], y - p4[1])
    # linear interpolation
    top = interpolate(dx, dot(g1, d1), dot(g2, d2))
    bottom = interpolate(dx, dot(g3, d3), dot(g4, d4))
    return interpolate(dy, top, bottom) * scale

result = [[0] * (width * 100) for y in range(height * 100)]

octaves = 2

def octave(result, per, lac):
    for y in range(len(result)):
        for x in range(len(result[0])):
            amp = 4
            freq = 1
            noiseH = 0
            for i in range(octaves):
                noiseH += noise(x * freq / 10, y * freq / 10, 0.1) * amp +  + f(x, y, len(result[0]), len(result))
                amp *= per
                freq *= lac
            result[y][x] = noiseH
    return result

def f(x, y, width, height):
    return - ((x - width / 2) / width) ** 2 - ((y - height / 2) / height )** 2

def Noise2D(L):
    for y in range(len(L)):
        for x in range(len(L[0])):
            L[y][x] = noise(x / 10, y / 10, 2)
    return L 

result = octave(result, 4, 16)
#print2dList(result)
#result = octave(result, 10, 4000)