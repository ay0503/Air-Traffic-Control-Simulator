import random, math
from cmu_112_graphics import *
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise = PerlinNoise(octaves=10, seed=1)

from cmu_112_graphics import *

def appStarted(app):
    # now let's make a copy that only uses the red part of each rgb pixel:
    app.image1 = Image.new(mode='RGB', size=(app.width, app.height))
    pic = [[noise([i/app.width, j/app.height]) for j in range(app.width)] for i in range(app.height)]
    for x in range(app.image1.width):
        for y in range(app.image1.height):
            val = int(pic[y][x] * 255)
            app.image1.putpixel((x,y),(val,val,val))

def redrawAll(app, canvas):
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.image1))

runApp(width=600, height=600)