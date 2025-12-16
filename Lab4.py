import math
import numpy as np
from PIL import Image, ImageOps
width = 2000
height = 2000
u_center = width / 2
v_center = height / 2
scaleX = 1500
scaleY = 1500
alpha = 0
beta = 180
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
def rotatedcoords(x, y, z, alpha, beta, gamma, t_x, t_y, t_z):
    xr = math.cos(beta)*math.cos(gamma)*x + math.cos(beta)*math.sin(gamma)*y + math.sin(beta)*z + t_x
    yr = -math.sin(alpha)*math.sin(beta)*math.cos(gamma)*x - math.cos(alpha)*math.sin(gamma)*x - math.sin(alpha)*math.sin(beta)*math.sin(gamma)*y + math.cos(alpha)*math.cos(gamma)*y + math.sin(alpha)*math.cos(beta)*z + t_y
    zr = -math.cos(alpha)*math.sin(beta)*math.cos(gamma)*x + math.sin(alpha)*math.sin(gamma)*x - math.cos(alpha)*math.sin(beta)*math.sin(gamma)*y - math.sin(alpha)*math.cos(gamma)*y + math.cos(alpha)*math.cos(beta)*z + t_z
    return xr, yr, zr
def draw_triangle(img_mat, x0, y0, z0, x1, y1, z1, x2, y2, z2, i0, i1, i2, u0, v0, u1, v1, u2, v2, texture):
    minX, maxX = minmax(x0, x1, x2)
    minY, maxY = minmax(y0, y1, y2)
    for j in range(minX, maxX):
        for k in range(minY, maxY):
            lambda0, lambda1, lambda2 = barycentriccoords(j, k, x0, y0, x1, y1, x2, y2)
            i = -1 * (lambda0*i0 + lambda1*i1 + lambda2*i2)
            if (lambda0 >= 0 and lambda1 >= 0 and lambda2 >= 0):
                z = lambda0*z0 + lambda1*z1 + lambda2*z2
                if(z < z_buff[k, j]):
                    img_mat[k, j] = texture[math.ceil(1024*(lambda0*v0+lambda1*v1+lambda2*v2)), math.ceil(1024*(lambda0*u0+lambda1*u1+lambda2*u2))] * i
                    z_buff[k, j] = z
texture_image = Image.open('bunny-atlas.jpg')
flipped = texture_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
texture = np.array(flipped, dtype=np.uint8)
file = open('model_1.obj')
v = []
f = []
vt = []
for s in file:
    sp = s.split()
    if (sp[0] == 'v'):
        v_triple = []
        for i in range(1, 4):
            v_triple.append(sp[i])
        v.append(v_triple)
    if (sp[0] == 'f'):
        f_triple = []
        f_buffer = []
        for i in range(1,4):
            f_line = sp[i].split('/')
            f_buffer.append(f_line[0])
            f_buffer.append(f_line[1])
        f.append([f_buffer[0], f_buffer[2], f_buffer[4], f_buffer[1], f_buffer[3], f_buffer[5]])
    if (sp[0] == 'vt'):
        vt_double = []
        for i in range(1, 3):
            vt_double.append(sp[i])
        vt.append(vt_double)
file.close()
vn = np.zeros((len(v), 3), dtype=int).tolist()
for j in v:
    j[0], j[1], j[2] = rotatedcoords(float(j[0]), float(j[1]), float(j[2]), alpha, beta, gamma, t_x, t_y, t_z)
for j in f:
    x0, y0, z0, x1, y1, z1, x2, y2, z2 = v[int(j[0]) - 1][0], v[int(j[0]) - 1][1], v[int(j[0]) - 1][2], v[int(j[1]) - 1][0], v[int(j[1]) - 1][1], v[int(j[1]) - 1][2], v[int(j[2]) - 1][0], v[int(j[2]) - 1][1], v[int(j[2]) - 1][2]
    xn, yn, zn = normal_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    vn[int(j[0]) - 1][0] += xn
    vn[int(j[0]) - 1][1] += yn
    vn[int(j[0]) - 1][2] += zn
    vn[int(j[1]) - 1][0] += xn
    vn[int(j[1]) - 1][1] += yn
    vn[int(j[1]) - 1][2] += zn
    vn[int(j[2]) - 1][0] += xn
    vn[int(j[2]) - 1][1] += yn
    vn[int(j[2]) - 1][2] += zn
for j in f:
    x0, y0, z0, x1, y1, z1, x2, y2, z2 = v[int(j[0]) - 1][0], v[int(j[0]) - 1][1], v[int(j[0]) - 1][2], v[int(j[1]) - 1][0], v[int(j[1]) - 1][1], v[int(j[1]) - 1][2], v[int(j[2]) - 1][0], v[int(j[2]) - 1][1], v[int(j[2]) - 1][2]
    u0, v0, u1, v1, u2, v2 = float(vt[int(j[3]) - 1][0]), float(vt[int(j[3]) - 1][1]), float(vt[int(j[4]) - 1][0]), float(vt[int(j[4]) - 1][1]), float(vt[int(j[5]) - 1][0]), float(vt[int(j[5]) - 1][1])
    length0 = math.sqrt(vn[int(j[0]) - 1][0] ** 2 + vn[int(j[0]) - 1][1] ** 2 + vn[int(j[0]) - 1][2] ** 2)
    length1 = math.sqrt(vn[int(j[1]) - 1][0] ** 2 + vn[int(j[1]) - 1][1] ** 2 + vn[int(j[1]) - 1][2] ** 2)
    length2 = math.sqrt(vn[int(j[2]) - 1][0] ** 2 + vn[int(j[2]) - 1][1] ** 2 + vn[int(j[2]) - 1][2] ** 2)
    n0 = [vn[int(j[0]) - 1][0]/length0, vn[int(j[0]) - 1][1]/length0, vn[int(j[0]) - 1][2]/length0]
    n1 = [vn[int(j[1]) - 1][0]/length1, vn[int(j[1]) - 1][1]/length1, vn[int(j[1]) - 1][2]/length1]
    n2 = [vn[int(j[2]) - 1][0]/length2, vn[int(j[2]) - 1][1]/length2, vn[int(j[2]) - 1][2]/length2]
    i0 = n0[2]/math.sqrt(n0[0]**2 + n0[1]**2 + n0[2]**2)
    i1 = n1[2]/math.sqrt(n1[0]**2 + n1[1]**2 + n1[2]**2)
    i2 = n2[2]/math.sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2)
    draw_triangle(img_mat, scaleX * x0 / z0 + u_center, scaleY * y0 / z0 + height / 2, z0, scaleX * x1 / z1 + u_center, scaleY * y1 / z1 + height / 2, z1, scaleX * x2 / z2 + u_center, scaleY * y2 / z2 + height / 2, z2, i0, i1, i2, u0, v0, u1, v1, u2, v2, texture)
img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img4.png")