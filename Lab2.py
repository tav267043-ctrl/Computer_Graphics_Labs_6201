import math
from random import randint
import numpy as np
from PIL import Image, ImageOps
color = [255, 255, 255]
factorA = 10000
factorB = 1000
factorC = 500
factorD = -1
img_mat = np.zeros((2000, 2000, 3), dtype=np.uint8)
z_buff = np.full((2000, 2000), np.inf)
for i in range(2000):
    for j in range(2000):
        img_mat[i, j] = [0, 0, 0]
def minmax(point1, point2, point3):
    mincoord = min(int(point1), int(point2), int(point3))
    maxcoord = max(int(point1), int(point2), int(point3)) + 1
    if(mincoord < 0): mincoord = 0.0
    if(maxcoord > 2000): maxcoord = 2000.0
    return mincoord, maxcoord
def barycentriccoords(x, y, x0, y0, x1, y1, x2, y2):
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2))/((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2))/((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0-lambda0-lambda1
    return lambda0, lambda1, lambda2
def normal_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    xn = (y1-y2)*(z1-z0)-(z1-z2)*(y1-y0)
    yn = (z1-z2)*(x1-x0)-(x1-x2)*(z1-z0)
    zn = (x1-x2)*(y1-y0)-(y1-y2)*(x1-x0)
    return xn, yn, zn
def light_angle(xn, yn, zn):
    cosA = zn/math.sqrt(xn**2 + yn**2 + zn**2)
    return cosA
def draw_triangle(img_mat, x0, y0, z0, x1, y1, z1, x2, y2, z2, color):
    minX, maxX = minmax(x0, x1, x2)
    minY, maxY = minmax(y0, y1, y2)
    for j in range(minX, maxX):
        for k in range(minY, maxY):
            lambda0, lambda1, lambda2 = barycentriccoords(j, k, x0, y0, x1, y1, x2, y2)
            if (lambda0 >= 0 and lambda1 >= 0 and lambda2 >= 0):
                z = lambda0*z0 + lambda1*z1 + lambda2*z2
                if(z < z_buff[k, j]):
                    img_mat[k, j] = color
                    z_buff[k, j] = z
file = open('model_1.obj')
v = []
f = []
for s in file:
    sp = s.split()
    if (sp[0] == 'v'):
        v_triple = []
        for i in range(1, 4):
            v_triple.append(sp[i])
        v.append(v_triple)
    if (sp[0] == 'f'):
        f_triple = []
        for i in range(1,4):
            f_line = sp[i].split('/')
            f_triple.append(f_line[0])
        f.append(f_triple)
file.close()
for i in f:
    x0, y0, z0, x1, y1, z1, x2, y2, z2 = float(v[int(i[0]) - 1][0]), float(v[int(i[0]) - 1][1]), float(v[int(i[0]) - 1][2]), float(v[int(i[1]) - 1][0]), float(v[int(i[1]) - 1][1]), float(v[int(i[1]) - 1][2]), float(v[int(i[2]) - 1][0]), float(v[int(i[2]) - 1][1]), float(v[int(i[2]) - 1][2])
    xn, yn, zn = normal_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    cosA = light_angle(xn, yn, zn)
    if (cosA < 0):
        draw_triangle(img_mat, factorA*x0+factorB, factorA*y0+factorB-factorC, z0, factorA*x1+factorB, factorA*y1+factorB-factorC, z1, factorA*x2+factorB, factorA*y2+factorB-factorC, z2, [255*factorD*cosA, randint(0, 255)*factorD*cosA, randint(0, 255)*factorD*cosA])
    #x0, y0, x1, y1, x2, y2 = scaleX*float(v[int(i[0]) - 1][0])+factorB, scaleX*float(v[int(i[0]) - 1][1])+factorB-factorC, scaleX*float(v[int(i[1]) - 1][0])+factorB, scaleX*float(v[int(i[1]) - 1][1])+factorB-factorC, scaleX*float(v[int(i[2]) - 1][0])+factorB, scaleX*float(v[int(i[2]) - 1][1])+factorB-factorC
    #draw_triangle(img_mat, x0, y0, x1, y1, x2, y2, [255, randint(0, 255), randint(0, 255)])
img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img1.png")