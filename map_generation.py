import random, math
from cmu_112_graphics import *

def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.

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

# Let's give the new function a try!

def f(x, y):
    x, y = x / 100, y / 100
    return (x + y) ** 2 * math.sin(x) ** 10 + math.cos(10 + y * x) * math.cos(x)

width, height = 50,50

def createMap(L):
    for y in range(0, len(L)):
        for x in range(0, len(L[0])):
            L[y][x] = f(x, y)
    return L

L = [[0] * width for y in range(height)]
wind_map = createMap(L)

def appStarted(app):
    # now let's make a copy that only uses the red part of each rgb pixel:
    app.image1 = Image.new(mode='RGB', size=(app.width, app.height))
    board = [[0] * app.width for row in range(app.height)]
    pic = createMap(board)
    for x in range(app.image1.width):
        for y in range(app.image1.height):
            val = int(pic[y][x] * 255)
            app.image1.putpixel((x,y),(val,val,val))

def winds(L):
    for y in range(len(L)):
        for x in range(len(L[0])):
            L[y][x] = x

def redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image1))

runApp(width=500, height=500)