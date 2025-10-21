from random import randint
import numpy as np
from PIL import Image, ImageOps
img_mat = np.zeros((2000, 2000, 3), dtype=np.uint8)
for i in range(2000):
    for j in range(2000):
        img_mat[i, j] = [0, 0, 0]
"""
def draw_line_1(img_mat, x0, y0, x1, y1, count, color):
    step = 1.0/count
    for t in np.arange (0, 1, step):
        x = round ((1.0 - t)*x0 + t*x1)
        y = round ((1.0 - t)*y0 + t*y1)
        img_mat[y, x] = color
"""
"""
def draw_line_2(img_mat, x0, y0, x1, y1, color):
    count = math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
    step = 1.0/count
    for t in np.arange (0, 1, step):
        x = round ((1.0 - t)*x0 + t*x1)
        y = round ((1.0 - t)*y0 + t*y1)
        img_mat[y, x] = color
"""
"""
def draw_line_3(img_mat, x0, y0, x1, y1, color):
    for x in range (x0, x1):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        img_mat[y, x] = color
"""
"""
def draw_line_4(img_mat, x0, y0, x1, y1, color):
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range (x0, x1):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        img_mat[y, x] = color
"""
"""
def draw_line_5(img_mat, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    for x in range (x0, x1):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        if (xchange):
            img_mat[x, y] = color
        else:
            img_mat[y, x] = color
"""
"""
def draw_line_6(img_mat, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range (x0, x1):
        t = (x - x0)/(x1 - x0)
        y = round ((1.0 - t)*y0 + t*y1)
        if (xchange):
            img_mat[x, y] = color
        else:
            img_mat[y, x] = color
"""
"""
def draw_line_7(img_mat, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dy = abs(y1 - y0)/(x1 - x0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1
    for x in range (x0, x1):
        if (xchange):
            img_mat[x, y] = color
        else:
            img_mat[y, x] = color
        derror += dy
        if (derror > 0.5):
            derror -= 1.0
            y += y_update
"""
"""
def draw_line_8(img_mat, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dy = 2.0*(x1 - x0) * abs(y1 - y0)/(x1 - x0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1
    for x in range (x0, x1):
        if (xchange):
            img_mat[x, y] = color
        else:
            img_mat[y, x] = color
        derror += dy
        if (derror > 2.0*(x1 - x0)*0.5):
            derror -= 2.0*(x1 - x0)*1.0
            y += y_update
"""
def draw_line(img_mat, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    dy = 2.0*abs(y1 - y0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1
    for x in range (x0, x1):
        if (xchange):
            img_mat[x, y] = color
        else:
            img_mat[y, x] = color
        derror += dy
        if (derror > (x1 - x0)):
            derror -= 2*(x1 - x0)
            y += y_update
"""
pi = math.pi
for k in range(13):
    x0, y0 = 100, 100
    x1 = int(100+95*math.cos((2 * pi)/13 * k))
    y1 = int(100+95*math.sin((2 * pi)/13 * k))
    #draw_line_1(img_mat, x0, y0, x1, y1, 100, [0, 255, 0])
    draw_line_(img_mat, x0, y0, x1, y1,[0, 255, 0])
"""
file = open('model_1.obj')
v = []
f = []
for s in file:
    sp = s.split()
    if (sp[0] == 'v'):
        v_triple = []
        for i in range(3):
            v_triple.append(int(10000*float(sp[i+1])+1000))
        v.append(v_triple)
    if (sp[0] == 'f'):
        f_triple = []
        for i in range(3):
            f_line = sp[i+1].split('/')
            f_triple.append(int(f_line[0]))
        f.append(f_triple)
file.close()
for i in f:
    draw_line(img_mat, v[i[0]-1][0], v[i[0]-1][1]-500, v[i[1]-1][0], v[i[1]-1][1]-500, [255, randint(0, 255), randint(0, 255)])
    draw_line(img_mat, v[i[1]-1][0], v[i[1]-1][1]-500, v[i[2]-1][0], v[i[2]-1][1]-500, [255, randint(0, 255), randint(0, 255)])
    draw_line(img_mat, v[i[2]-1][0], v[i[2]-1][1]-500, v[i[0]-1][0], v[i[0]-1][1]-500, [255, randint(0, 255), randint(0, 255)])
img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img.png")