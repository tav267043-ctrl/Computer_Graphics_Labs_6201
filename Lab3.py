import math
from random import randint
import numpy as np
from PIL import Image, ImageOps
width = 2000
height = 2000
u_center = width / 2
v_center = height / 2
scaleX = 1500
scaleY = 1500
alpha = 0
beta = 0
gamma = 0
t_x = 0
t_y = -100/height
t_z = 0.15
img_mat = np.zeros((height, width, 3), dtype=np.uint8)
z_buff = np.full((height, width), np.inf)
for i in range(2000):
    for j in range(2000):
        img_mat[i, j] = [0, 0, 0]
def minmax(point1, point2, point3):
    mincoord = min(int(point1), int(point2), int(point3))
    maxcoord = max(int(point1), int(point2), int(point3)) + 1
    if(mincoord < 0): mincoord = 0
    if(maxcoord > 2000): maxcoord = 2000
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
def rotatedcoords(x, y, z, alpha, beta, gamma, t_x, t_y, t_z):
    xr = math.cos(beta)*math.cos(gamma)*x + math.cos(beta)*math.sin(gamma)*y + math.sin(beta)*z + t_x
    yr = -math.sin(alpha)*math.sin(beta)*math.cos(gamma)*x - math.cos(alpha)*math.sin(gamma)*x - math.sin(alpha)*math.sin(beta)*math.sin(gamma)*y + math.cos(alpha)*math.cos(gamma)*y + math.sin(alpha)*math.cos(beta)*z + t_y
    zr = -math.cos(alpha)*math.sin(beta)*math.cos(gamma)*x + math.sin(alpha)*math.sin(gamma)*x - math.cos(alpha)*math.sin(beta)*math.sin(gamma)*y - math.sin(alpha)*math.cos(gamma)*y + math.cos(alpha)*math.cos(beta)*z + t_z
    return xr, yr, zr
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
for j in v:
    j[0], j[1], j[2] = rotatedcoords(float(j[0]), float(j[1]), float(j[2]), alpha, beta, gamma, t_x, t_y, t_z)
for i in f:
    color1 = 255
    color2 = randint(0, 255)
    x0, y0, z0, x1, y1, z1, x2, y2, z2 = v[int(i[0]) - 1][0], v[int(i[0]) - 1][1], v[int(i[0]) - 1][2], v[int(i[1]) - 1][0], v[int(i[1]) - 1][1], v[int(i[1]) - 1][2], v[int(i[2]) - 1][0], v[int(i[2]) - 1][1], v[int(i[2]) - 1][2]
    xn, yn, zn = normal_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    cosA = light_angle(xn, yn, zn)
    if (cosA < 0):
        draw_triangle(img_mat, scaleX * x0 / z0 + u_center, scaleY * y0 / z0 + height / 2, z0, scaleX * x1 / z1 + u_center, scaleY * y1 / z1 + height / 2, z1, scaleX * x2 / z2 + u_center, scaleY * y2 / z2 + height / 2, z2, [color1 * -cosA, color1 * -cosA, color1 * -cosA])
img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img3.png")