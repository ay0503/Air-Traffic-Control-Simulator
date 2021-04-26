import random, math
from objects import *
from cmu_112_graphics import *
from map_generation import noise, noiseMap
import numpy as np

def appStarted(app):
    # now let's make a copy that only uses the red part of each rgb pixel:
    app.image1 = Image.new(mode='RGB', size=(app.width, app.height))
    pic = noiseMap
    #print2dList(pic)
    for x in range(app.image1.width):
        for y in range(app.image1.height):
            val = int(pic[y // 20][x // 20] * 255)
            app.image1.putpixel((x,y),(val,val,val))

def redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image1))

runApp(width=1660, height=1020)