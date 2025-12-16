import math
import numpy as np
from PIL import Image, ImageOps
class Quaternion:
    def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
    def __mul__(self, other):
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = other.w, other.x, other.y, other.z
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        return Quaternion(w, x, y, z)
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    def rotate_vector(self, v):
        q_vec = Quaternion(0, v[0], v[1], v[2])
        q_conj = self.conjugate()
        rotated = self * q_vec * q_conj
        return np.array([rotated.x, rotated.y, rotated.z])

width = 1000
height = 800
u_center = width / 2
v_center = height / 2
scale = [500, 1500, 1500]
alpha = [0, 0, 0]
beta = [0, 180, 0]
gamma = [0, 0, 0]
t_x = [0, -100/width, 80/width]
t_y = [0, -100/height, -100/height]
t_z = [2, 0.15, 0.15]
filename = ['12268_banjofrog_v1_L3.obj', 'model_1.obj', 'model_1.obj']
textureName = ['12268_banjofrog_diffuse.jpg', 'bunny-atlas.jpg', 'bunny-atlas.jpg']
numOBJ = 1

def minmax(point1, point2, point3):
    mincoord = min(int(point1), int(point2), int(point3))
    maxcoord = max(int(point1), int(point2), int(point3)) + 1
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
    qx = Quaternion(math.cos(alpha / 2), math.sin(alpha / 2), 0, 0)
    qy = Quaternion(math.cos(beta / 2), 0, math.sin(beta / 2), 0)
    qz = Quaternion(math.cos(gamma / 2), 0, 0, math.sin(gamma / 2))
    q = qx * qy * qz
    point = np.array([x, y, z])
    rotated_point = q.rotate_vector(point)
    final_point = rotated_point + np.array([t_x, t_y, t_z])
    return final_point[0], final_point[1], final_point[2]
def draw_triangle(img_mat, x0, y0, z0, x1, y1, z1, x2, y2, z2, i0, i1, i2, u0, v0, u1, v1, u2, v2, texture, hasTexture):
    minX, maxX = minmax(x0, x1, x2)
    if(minX < 0):
        minX = 0
    if(maxX > width):
        maxX = width
    minY, maxY = minmax(y0, y1, y2)
    if (minY < 0):
        minY = 0
    if (maxY > height):
        maxY = height
    for j in range(minX, maxX):
        for k in range(minY, maxY):
            lambda0, lambda1, lambda2 = barycentriccoords(j, k, x0, y0, x1, y1, x2, y2)
            i = (lambda0*i0 + lambda1*i1 + lambda2*i2)
            if(i < 0):
                i *= -1
            if (lambda0 >= 0 and lambda1 >= 0 and lambda2 >= 0):
                z = lambda0*z0 + lambda1*z1 + lambda2*z2
                if(z < z_buff[k, j]):
                    if(hasTexture):
                        img_mat[k, j] = texture[math.ceil(1024 * (lambda0 * v0 + lambda1 * v1 + lambda2 * v2)), math.ceil(1024 * (lambda0 * u0 + lambda1 * u1 + lambda2 * u2))] * i
                    else:
                        img_mat[k, j] = 225*i
                    z_buff[k, j] = z
def parcingOBJ(v, f, vt, vn, filename):
    file = open(filename)
    for s in file:
        s = s.strip()
        if not s:
            continue
        sp = s.split()
        if not sp:
            continue
        if (sp[0] == 'v'):
            v_triple = []
            for i in range(1, 4):
                v_triple.append(sp[i])
            v.append(v_triple)
        if (sp[0] == 'f'):
            lengthSP = len(sp)
            lengthSPI = len(sp[1].split('/'))
            f_buffer1 = []
            f_buffer2 = []
            f_buffer3 = []
            for i in range(1, lengthSP):
                f_line = sp[i].split('/')
                if(lengthSPI == 1):
                    f_buffer1.append(f_line[0])
                else:
                    if (lengthSPI == 2):
                        f_buffer1.append(f_line[0])
                        f_buffer2.append(f_line[1])
                    else:
                        if (lengthSPI == 3):
                            f_buffer1.append(f_line[0])
                            f_buffer2.append(f_line[1])
                            f_buffer3.append(f_line[2])
            lengthBuf1 = len(f_buffer1)
            f_buffer4 = []
            for i in range(1, lengthBuf1 - 1):
                if(lengthSPI == 1):
                    f_buffer4.append([f_buffer1[0], f_buffer1[1], f_buffer1[2]])
                else:
                    if (lengthSPI == 2):
                        f_buffer4.append(
                            [f_buffer1[0], f_buffer1[i], f_buffer1[i + 1], f_buffer2[0], f_buffer2[i],
                             f_buffer2[i + 1]])
                    else:
                        if (lengthSPI == 3):
                            f_buffer4.append(
                                [f_buffer1[0], f_buffer1[i], f_buffer1[i + 1], f_buffer2[0], f_buffer2[i],
                                 f_buffer2[i + 1], f_buffer3[0], f_buffer3[i], f_buffer3[i + 1]])
            lengthBuf4 = len(f_buffer4)
            for j in range(0, lengthBuf4):
                f.append(f_buffer4[j])
        if (sp[0] == 'vt'):
            vt_double = []
            for i in range(1, 3):
                vt_double.append(sp[i])
            vt.append(vt_double)
        if (sp[0] == 'vn'):
            vn_triple = []
            for i in range(1, 4):
                vn_triple.append(sp[i])
            vn.append(vn_triple)
    file.close()
def draw_image(img_mat, numOBJ, filename, textureName, scale, alpha, beta, gamma, t_x, t_y, t_z):
    for k in range(numOBJ):
        v = []
        f = []
        vt = []
        vn = []
        texture_image = Image.open(textureName[k])
        flipped = texture_image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        texture = np.array(flipped, dtype=np.uint8)
        hasTexture = True
        parcingOBJ(v, f, vt, vn, filename[k])
        for j in v:
            j[0], j[1], j[2] = rotatedcoords(float(j[0]), float(j[1]), float(j[2]), alpha[k], beta[k], gamma[k], t_x[k],
                                             t_y[k], t_z[k])
        flag = 0
        if(len(vn) == 0):
            vn = np.zeros((len(v), 3), dtype=int).tolist()
            for j in f:
                x0, y0, z0, x1, y1, z1, x2, y2, z2 = v[int(j[0]) - 1][0], v[int(j[0]) - 1][1], v[int(j[0]) - 1][2], \
                    v[int(j[1]) - 1][0], v[int(j[1]) - 1][1], v[int(j[1]) - 1][2], v[int(j[2]) - 1][0], \
                v[int(j[2]) - 1][1], \
                    v[int(j[2]) - 1][2]
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
        else:
            flag += 1
            for j in vn:
                j[0], j[1], j[2] = rotatedcoords(float(j[0]), float(j[1]), float(j[2]), alpha[k], beta[k], gamma[k], t_x[k],
                                             t_y[k], t_z[k])
        for j in f:
            x0, y0, z0, x1, y1, z1, x2, y2, z2 = v[int(j[0]) - 1][0], v[int(j[0]) - 1][1], v[int(j[0]) - 1][2], \
                v[int(j[1]) - 1][0], v[int(j[1]) - 1][1], v[int(j[1]) - 1][2], v[int(j[2]) - 1][0], v[int(j[2]) - 1][1], \
                v[int(j[2]) - 1][2]
            u0, v0, u1, v1, u2, v2 = float(vt[int(j[3]) - 1][0]), float(vt[int(j[3]) - 1][1]), float(
                vt[int(j[4]) - 1][0]), float(vt[int(j[4]) - 1][1]), float(vt[int(j[5]) - 1][0]), float(
                vt[int(j[5]) - 1][1])
            if(flag == 1):
                length0 = math.sqrt(vn[int(j[6]) - 1][0] ** 2 + vn[int(j[6]) - 1][1] ** 2 + vn[int(j[6]) - 1][2] ** 2)
                length1 = math.sqrt(vn[int(j[7]) - 1][0] ** 2 + vn[int(j[7]) - 1][1] ** 2 + vn[int(j[7]) - 1][2] ** 2)
                length2 = math.sqrt(vn[int(j[8]) - 1][0] ** 2 + vn[int(j[8]) - 1][1] ** 2 + vn[int(j[8]) - 1][2] ** 2)
                n0 = [vn[int(j[6]) - 1][0] / length0, vn[int(j[6]) - 1][1] / length0, vn[int(j[6]) - 1][2] / length0]
                n1 = [vn[int(j[7]) - 1][0] / length1, vn[int(j[7]) - 1][1] / length1, vn[int(j[7]) - 1][2] / length1]
                n2 = [vn[int(j[8]) - 1][0] / length2, vn[int(j[8]) - 1][1] / length2, vn[int(j[8]) - 1][2] / length2]
            else:
                length0 = math.sqrt(vn[int(j[0]) - 1][0] ** 2 + vn[int(j[0]) - 1][1] ** 2 + vn[int(j[0]) - 1][2] ** 2)
                length1 = math.sqrt(vn[int(j[1]) - 1][0] ** 2 + vn[int(j[1]) - 1][1] ** 2 + vn[int(j[1]) - 1][2] ** 2)
                length2 = math.sqrt(vn[int(j[2]) - 1][0] ** 2 + vn[int(j[2]) - 1][1] ** 2 + vn[int(j[2]) - 1][2] ** 2)
                n0 = [vn[int(j[0]) - 1][0] / length0, vn[int(j[0]) - 1][1] / length0, vn[int(j[0]) - 1][2] / length0]
                n1 = [vn[int(j[1]) - 1][0] / length1, vn[int(j[1]) - 1][1] / length1, vn[int(j[1]) - 1][2] / length1]
                n2 = [vn[int(j[2]) - 1][0] / length2, vn[int(j[2]) - 1][1] / length2, vn[int(j[2]) - 1][2] / length2]
            i0 = n0[2] / math.sqrt(n0[0] ** 2 + n0[1] ** 2 + n0[2] ** 2)
            i1 = n1[2] / math.sqrt(n1[0] ** 2 + n1[1] ** 2 + n1[2] ** 2)
            i2 = n2[2] / math.sqrt(n2[0] ** 2 + n2[1] ** 2 + n2[2] ** 2)
            draw_triangle(img_mat, scale[k] * x0 / z0 + u_center, scale[k] * y0 / z0 + height / 2, z0,
                            scale[k] * x1 / z1 + u_center, scale[k] * y1 / z1 + height / 2, z1,
                            scale[k] * x2 / z2 + u_center,
                            scale[k] * y2 / z2 + height / 2, z2, i0, i1, i2, u0, v0, u1, v1, u2, v2, texture, hasTexture)

img_mat = np.zeros((height, width, 3), dtype=np.uint8)
for i in range(height):
    for j in range(width):
        img_mat[i, j] = [0, 0, 0]
z_buff = np.full((height, width), np.inf)
draw_image(img_mat, numOBJ, filename, textureName, scale, alpha, beta, gamma, t_x, t_y, t_z)
img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img5_frog3.png")