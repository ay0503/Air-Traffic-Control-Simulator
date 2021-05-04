import random, copy
from objects import distance

def minAndMax(L):
    right, left = -1, 1
    for row in L:
        if max(row) > right:
            right = max(row)
        elif min(row) < left:
            left = min(row)
    return left, right

# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
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

# returns unit vector between two points
def unitVector(x, y):
    k = (x ** 2 + y ** 2) ** -0.5
    return (k * x, k * y)

# returns random gradient vector
def gradient():
    x, y = random.uniform(-1, 1), random.uniform(-1, 1)
    return unitVector(x, y)

# smoothening function
def fade(x):
    return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3

# returns dot product of two vectors
def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

# linear interpolation formula
def interpolate(d, a, b):
    return (1 - d) * a + d * b

# elliptic parabaloid function to create cloud shape
def f(x, y, width, height, dx, dy, a, level):
    return ((a * (x - dx * width) / width) ** 2 + ((y - dy * height) / height) ** 2) * level

# creates noise for point x,y
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

# TODO scale parameter in storm object
# returns 2D list of noise with octave, persistance, lacunarity parameters
def octave(result, per, lac, octaves, level):
    width, height = len(result[0]), len(result)
    #! random eccentricity for elliptic base
    a = random.uniform(0.5, 2)
    #! position of cloud center
    dx, dy = random.random(), random.random()
    for y in range(height):
        for x in range(width):
            amp = 10
            freq = 0.1
            noiseH = 0
            for i in range(octaves):
                noiseH += (2 * noise(x * freq, y * freq, 1) + 1) * f(x, y, width, 
                            height, dx, dy, a, level)
                amp *= per
                freq *= lac
            result[y][x] = float("{:.2f}".format(noiseH))
    return result

imageScale = 5
width, height = 1660 // imageScale, 1020 // imageScale
result = octave([[0] * (width) for y in range(height)], 0.4, 1, 2, random.randint(10,20))