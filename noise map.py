import random, math
from objects import *
from cmu_112_graphics import *
from map_generation import noiseMap
from perlin_noise import result

def appStarted(app):
    # now let's make a copy that only uses the red part of each rgb pixel:
    app.image1 = Image.new(mode='RGB', size=(app.width, app.height))
    pic = result
    for x in range(app.image1.width):
        for y in range(app.image1.height):
            val = int(pic[y // 10][x // 10] * 255)
            app.image1.putpixel((x,y),(val,val,val))

def redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image1))

runApp(width = len(result[0] * 10), height = len(result) * 10)