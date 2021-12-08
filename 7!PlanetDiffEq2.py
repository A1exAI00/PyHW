# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 18:09:01 2021

@author: Alex Akinin

Attempt to scale 7!PlanetDiffEq1.py to have more planets
Does not work for some reason
The project is abandoned 


Contains:
    two_planets() - diff eq for 2 planets in 2D
    three_planets() - diff eq for 3 planets in 3D
    four_planets() - diff eq for 4 planets in 3D
    five_planets() - diff eq for 5 planets in 3D
    plot_3d() - plot 2 planets in 2D in [x, y, time] coords
    two_d_plot() - animated plot for 2 planets in 2D
    redraw2d() - redrawing func for two_d_plot()
    three_d_plot_3p() - animated plot for 3 planets in 3D
    redraw3d_3p() - redrawing func for three_d_plot_3p()
    three_d_plot_4p() - animated plot for 4 planets in 3D
    redraw3d_4p() - - redrawing func for three_d_plot_4p()
    three_d_plot_5p() - animated plot for 5 planets in 3D
    redraw3d_5p() - - redrawing func for three_d_plot_5p()
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


class Planet3d:
    def __init__(self, mass, pos_arr):
        global axes
        self.m = mass
        self.x, self.Vx, self.y, self.Vy, self.z, self.Vz = pos_arr
        self.X, self.VX, self.Y, self.VY, self.Z, self.VZ = pos_arr
        self.ax, self.ay, self.az = 0,0,0
        self.xpath, self.ypath, self.zpath = [],[],[]
        self.line, = axes.plot([], [], markersize=ms)
        self.line.set_marker('*')
        self.tail, = axes.plot([], [], markersize=ms)
    
    def getVect(self, p2):
        x2, y2, z2 = p2
        rx = x2 - self.x
        ry = y2 - self.y
        rz = z2 - self.z
        r = np.sqrt(rx**2 + ry**2 + rz**2)
        return [rx, ry, rz, r]
    
    def getParam(self):
        return self.X, self.VX, self.Y, self.VY, self.Z, self.VZ
    
    def addAc(self, m2, p2):
        x2, y2, z2 = p2
        rx = x2 - self.x
        ry = y2 - self.y
        rz = z2 - self.z
        r = np.sqrt(rx**2 + ry**2 + rz**2)
        self.ax += G*(m2/r**3)*rx
        self.ay += G*(m2/r**3)*ry
        self.az += G*(m2/r**3)*rz
    
    def getPos(self):
        return [self.x, self.y, self.z]
    
    def getVel(self):
        return [self.Vx, self.Vy, self.Vz]
    
    def setVal(self, val):
        tmp_val = val.copy()
        self.x, self.Vx, self.y, self.Vy, self.z, self.Vz = tmp_val
    
    def getVal(self, val):
        return self.x, self.Vx, self.y, self.Vy, self.z, self.Vz
    
    def getAc(self):
        return self.ax, self.ay, self.az
    
    def getM(self):
        return self.m
    
    def set_data(self, time):
        self.line.set_data(self.xpath[time], self.ypath[time])
        self.line.set_3d_properties(self.zpath[time])
    
    def setXYZpath(self, x, y, z):
        self.xpath = x.copy()
        self.ypath = y.copy()
        self.zpath = z.copy()
    
    # def setXpath(self, x):
    #     self.xpath = x
    
    # def setYpath(self, y):
    #     self.ypath = y
    
    # def setZpath(self, z):
    #     self.zpath = z


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def n_planets(input_f, t):
    tmp_y = input_f.copy()
    # global output
    for i in range(NUM_PLANETS):
        Planets[i].setVal(tmp_y[6*i:6*(i+1)].copy())

    
    
    output = []
    for first in Planets:
        for second in Planets:
            if first == second: 
                pass
            else:
                first.addAc(second.getM(), second.getPos())
    
    for first in Planets:
        V = first.getVel()
        A = first.getAc()
        
        for j in range(3):
            output.append(A[j])
            output.append(V[j])
    print(output)
    return output


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# def plot_3d():
#     x1_t, y1_t, x2_t, y2_t = a[:, 0], a[:, 2], \
#         a[:, 4], a[:, 6]
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('TIME')
#     ax.plot(x1_t, y1_t, t)
#     ax.plot(x2_t, y2_t, t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# def stupid_graph():
#     x1_t, y1_t = a[:, 0], a[:, 2]
#     x2_t, y2_t = a[:, 4], a[:, 6]
#     plt.plot(x1_t, y1_t)
#     plt.plot(x2_t, y2_t)
        


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# def two_d_plot():
#     global line1, line2, anim1
#     fig = plt.figure(facecolor='white')
#     ax = plt.axes(xlim=(-Z, Z), ylim=(-Z, Z))
    
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
    
#     ms = 10
#     line1, = ax.plot([], [], markersize=ms)
#     line2, = ax.plot([], [], markersize=ms)
    
#     line1.set_marker('*')
#     line2.set_marker('D')
    
#     ax.grid(True)

#     anim1 = animation.FuncAnimation(fig, redraw2d, frames=NUM_P, interval=1)
#     plt.show()


# def redraw2d(time):
#     x1_t, y1_t = a[time, 0], a[time, 2]
#     x2_t, y2_t = a[time, 4], a[time, 6]
#     # x_mean = np.mean([x1_t, x2_t])
#     # y_mean = np.mean([y1_t, y2_t])
#     # ax = plt.axes(xlim=(-Z+x_mean, Z+x_mean), \
#     #               ylim=(-Z+y_mean, Z+y_mean) )
#     line1.set_data(x1_t, y1_t)
#     line2.set_data(x2_t, y2_t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# def three_d_plot_5p():
#     global line1, line2, line3, line4, line5, anim4
#     global tail1, tail2, tail3, tail4, tail5
#     fig = plt.figure()
#     ax = p3.Axes3D(fig, xlim3d=(-Z, Z), ylim3d=(-Z, Z), zlim3d=(-Z, Z))
    
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')
    
#     ms, c = 10, (0.6,0.6,0.6)
#     line1, = ax.plot([], [], markersize=ms)
#     line2, = ax.plot([], [], markersize=ms)
#     line3, = ax.plot([], [], markersize=ms)
#     line4, = ax.plot([], [], markersize=ms)
#     line5, = ax.plot([], [], markersize=ms)
    
#     tail1, = ax.plot([], [], markersize=ms, color='blue')
#     tail2, = ax.plot([], [], markersize=ms, color='orange')
#     tail3, = ax.plot([], [], markersize=ms, color='green')
#     tail4, = ax.plot([], [], markersize=ms, color='red')
#     tail5, = ax.plot([], [], markersize=ms, color='purple')
    
#     line1.set_marker('*')
#     line2.set_marker('D')
#     line3.set_marker('^')
#     line4.set_marker('s')
#     line5.set_marker('8')
    
#     ax.plot([-Z, Z], [0, 0], [0, 0], color=c)
#     ax.plot([0, 0], [-Z, Z], [0, 0], color=c)
#     ax.plot([0, 0], [0, 0], [-Z, Z], color=c)
    
#     anim4 = animation.FuncAnimation(fig, redraw3d_5p, frames=NUM_P, interval=1)


# def redraw3d_5p(time):
#     x1_t, y1_t, z1_t = d[time, 0], d[time, 2], d[time, 4]
#     x2_t, y2_t, z2_t = d[time, 6], d[time, 8], d[time, 10]
#     x3_t, y3_t, z3_t = d[time, 12], d[time, 14], d[time, 16]
#     x4_t, y4_t, z4_t = d[time, 18], d[time, 20], d[time, 22]
#     x5_t, y5_t, z5_t = d[time, 24], d[time, 26], d[time, 28]
    
#     tx1, ty1, tz1 = d[0:time, 0], d[0:time, 2], d[0:time, 4]
#     tx2, ty2, tz2 = d[0:time, 6], d[0:time, 8], d[0:time, 10]
#     tx3, ty3, tz3 = d[0:time, 12], d[0:time, 14], d[0:time, 16]
#     tx4, ty4, tz4 = d[0:time, 18], d[0:time, 20], d[0:time, 22]
#     tx5, ty5, tz5 = d[0:time, 24], d[0:time, 26], d[0:time, 28]
    
#     line1.set_data(x1_t, y1_t)
#     line2.set_data(x2_t, y2_t)
#     line3.set_data(x3_t, y3_t)
#     line4.set_data(x4_t, y4_t)
#     line5.set_data(x5_t, y5_t)
    
#     tail1.set_data(tx1, ty1)
#     tail2.set_data(tx2, ty2)
#     tail3.set_data(tx3, ty3)
#     tail4.set_data(tx4, ty4)
#     tail5.set_data(tx5, ty5)
    
#     line1.set_3d_properties(z1_t)
#     line2.set_3d_properties(z2_t)
#     line3.set_3d_properties(z3_t)
#     line4.set_3d_properties(z4_t)
#     line5.set_3d_properties(z5_t)
    
#     tail1.set_3d_properties(tz1)
#     tail2.set_3d_properties(tz2)
#     tail3.set_3d_properties(tz3)
#     tail4.set_3d_properties(tz4)
#     tail5.set_3d_properties(tz5)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def reDRAW(time):
    for planet in Planets:
        planet.set_data(time)
    


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


POINT_1, POINT_2, NUM_P = 0, 10, 100
t = np.linspace(POINT_1, POINT_2, NUM_P)

# m1, m2, m3, m4, m5 = 1, 20, 3, 1, 2
# x1, y1, z1, V1x, V1y, V1z = 5, -5, 3, -2, -2, 1
# x2, y2, z2, V2x, V2y, V2z = 0, 0, 0, 0, 0, 0
# x3, y3, z3, V3x, V3y, V3z = -3, -3, -3, 1, -3, -1
# x4, y4, z4, V4x, V4y, V4z = -5, -5, -1, -1, 3, 3
# x5, y5, z5, V5x, V5y, V5z = 5, 5, 1, 3, 1, -3

G = 1
Z = 100
# pw = 3
NUM_PLANETS = 2

# initparam_2p_2d = [x1, V1x, y1, V1y,
#                    x2, V2x, y2, V2y]
# initparam_3p_3d = [x1, V1x, y1, V1y, z1, V1z,
#                    x2, V2x, y2, V2y, z2, V2z,
#                    x3, V3x, y3, V3y, z3, V3z]
# initparam_4p_3d = [x1, V1x, y1, V1y, z1, V1z,
#                    x2, V2x, y2, V2y, z2, V2z,
#                    x3, V3x, y3, V3y, z3, V3z,
#                    x4, V4x, y4, V4y, z4, V4z]
# initparam_5p_3d = [x1, V1x, y1, V1y, z1, V1z,
#                    x2, V2x, y2, V2y, z2, V2z,
#                    x3, V3x, y3, V3y, z3, V3z,
#                    x4, V4x, y4, V4y, z4, V4z,
#                    x5, V5x, y5, V5y, z5, V5z]


# a = odeint(two_planets, initparam_2p_2d, t)
# b = odeint(three_planets, initparam_3p_3d, t)
# c = odeint(four_planets, initparam_4p_3d, t)
# d = odeint(five_planets, initparam_5p_3d, t)


# plot_3d()
# stupid_graph()
# two_d_plot()
# three_d_plot_3p()
# three_d_plot_4p()
# three_d_plot_5p()

fig = plt.figure()
axes = p3.Axes3D(fig, xlim3d=(-Z, Z), ylim3d=(-Z, Z), zlim3d=(-Z, Z))
ms, c = 10, (0.6,0.6,0.6)

randomizer = lambda: 5*(np.random.rand() - 0.5)

Planets = [Planet3d(10, [randomizer() for _ in range(6)]) for i in range(NUM_PLANETS)]

initparam = []
for i in range(len(Planets)):
    initparam += Planets[i].getParam()

ititparam = [0,3,0,3,0,3,
             3,5,3,-5,3,10]

b = odeint(n_planets, initparam, t)

i = 0
j = 0
while i < NUM_PLANETS*3*2:
    Planets[j].setXYZpath(b[:,i], b[:,i+2], b[:,i+4])
    i += 6
    j += 1

animn = animation.FuncAnimation(fig, reDRAW, frames=NUM_P, interval=100)



axes.set_xlabel('X')
axes.set_ylabel('Y')
axes.set_zlabel('Z')

# three_d_plot_3p()
print(Planets[0].X)
print(Planets[0].x)

print(Planets[0].Y)
print(Planets[0].y)