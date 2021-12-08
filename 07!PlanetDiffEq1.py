# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 18:09:01 2021

@author: Alex Akinin

Planet motion simulation

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


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def two_planets_odeint(y, t):
    ''' Differential equation for 2 planets in 2D '''
    x1tt, v1xt, y1tt, v1yt, \
        x2tt, v2xt, y2tt, v2yt = y

    r12x = x2tt - x1tt
    r12y = y2tt - y1tt

    r12 = np.sqrt(r12x**2 + r12y**2)
    return [v1xt, +G*(m2/r12**3)*r12x,
            v1yt, +G*(m2/r12**3)*r12y,
            v2xt, -G*(m1/r12**3)*r12x,
            v2yt, -G*(m1/r12**3)*r12y]


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def three_planets_odeint(y, t):
    ''' Differential equation for 3 planets in 3D '''
    x1tt, v1xt, y1tt, v1yt, z1tt, v1zt,\
    x2tt, v2xt, y2tt, v2yt, z2tt, v2zt,\
    x3tt, v3xt, y3tt, v3yt, z3tt, v3zt = y

    r12x = x2tt - x1tt
    r12y = y2tt - y1tt
    r12z = z2tt - z1tt

    r13x = x3tt - x1tt
    r13y = y3tt - y1tt
    r13z = z3tt - z1tt

    r23x = x3tt - x2tt
    r23y = y3tt - y2tt
    r23z = z3tt - z2tt

    r12 = np.sqrt(r12x**2 + r12y**2 + r12z**2)
    r13 = np.sqrt(r13x**2 + r13y**2 + r13z**2)
    r23 = np.sqrt(r23x**2 + r23y**2 + r23z**2)

    return [v1xt, G*(+(m2/r12**3)*r12x + (m3/r13**3)*r13x),
            v1yt, G*(+(m2/r12**3)*r12y + (m3/r13**3)*r13y),
            v1zt, G*(+(m2/r12**3)*r12z + (m3/r13**3)*r13z),
            v2xt, G*(-(m1/r12**3)*r12x + (m3/r23**3)*r23x),
            v2yt, G*(-(m1/r12**3)*r12y + (m3/r23**3)*r23y),
            v2zt, G*(-(m1/r12**3)*r12z + (m3/r23**3)*r23z),
            v3xt, G*(-(m1/r13**3)*r13x - (m2/r23**3)*r23x),
            v3yt, G*(-(m1/r13**3)*r13y - (m2/r23**3)*r23y),
            v3zt, G*(-(m1/r13**3)*r13z - (m2/r23**3)*r23z)]


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def four_planets_odeint(y, t):
    ''' Differential equation for 4 planets in 3D '''
    x1tt, v1xt, y1tt, v1yt, z1tt, v1zt,\
    x2tt, v2xt, y2tt, v2yt, z2tt, v2zt,\
    x3tt, v3xt, y3tt, v3yt, z3tt, v3zt,\
    x4tt, v4xt, y4tt, v4yt, z4tt, v4zt = y
    
    r12x = x2tt - x1tt
    r12y = y2tt - y1tt
    r12z = z2tt - z1tt
    
    r13x = x3tt - x1tt
    r13y = y3tt - y1tt
    r13z = z3tt - z1tt
    
    r14x = x4tt - x1tt
    r14y = y4tt - y1tt
    r14z = z4tt - z1tt
    
    r23x = x3tt - x2tt
    r23y = y3tt - y2tt
    r23z = z3tt - z2tt
    
    r24x = x4tt - x2tt
    r24y = y4tt - y2tt
    r24z = z4tt - z2tt
    
    r34x = x4tt - x3tt
    r34y = y4tt - y3tt
    r34z = z4tt - z3tt
    
    r12 = np.sqrt(r12x**2 + r12y**2 + r12z**2)
    r13 = np.sqrt(r13x**2 + r13y**2 + r13z**2)
    r14 = np.sqrt(r14x**2 + r14y**2 + r14z**2)
    r23 = np.sqrt(r23x**2 + r23y**2 + r23z**2)
    r24 = np.sqrt(r24x**2 + r24y**2 + r24z**2)
    r34 = np.sqrt(r34x**2 + r34y**2 + r34z**2)
    
    return [v1xt, G*(+(m2/r12**3)*r12x + (m3/r13**3)*r13x + (m4/r14**3)*r14x),
            v1yt, G*(+(m2/r12**3)*r12y + (m3/r13**3)*r13y + (m4/r14**3)*r14y),
            v1zt, G*(+(m2/r12**3)*r12z + (m3/r13**3)*r13z + (m4/r14**3)*r14z),
            v2xt, G*(-(m1/r12**3)*r12x + (m3/r23**3)*r23x + (m4/r24**3)*r24x),
            v2yt, G*(-(m1/r12**3)*r12y + (m3/r23**3)*r23y + (m4/r24**3)*r24y),
            v2zt, G*(-(m1/r12**3)*r12z + (m3/r23**3)*r23z + (m4/r24**3)*r24z),
            v3xt, G*(-(m1/r13**3)*r13x - (m2/r23**3)*r23x + (m4/r34**3)*r34x),
            v3yt, G*(-(m1/r13**3)*r13y - (m2/r23**3)*r23y + (m4/r34**3)*r34y),
            v3zt, G*(-(m1/r13**3)*r13z - (m2/r23**3)*r23z + (m4/r34**3)*r34z),
            v4xt, G*(-(m1/r14**3)*r14x - (m2/r24**3)*r24x - (m3/r34**3)*r34x),
            v4yt, G*(-(m1/r14**3)*r14y - (m2/r24**3)*r24y - (m3/r34**3)*r34y),
            v4zt, G*(-(m1/r14**3)*r14z - (m2/r24**3)*r24z - (m3/r34**3)*r34z)]


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def five_planets_odeint(y, t):
    ''' Differential equation for 5 planets in 3D '''
    x1tt, v1xt, y1tt, v1yt, z1tt, v1zt,\
    x2tt, v2xt, y2tt, v2yt, z2tt, v2zt,\
    x3tt, v3xt, y3tt, v3yt, z3tt, v3zt,\
    x4tt, v4xt, y4tt, v4yt, z4tt, v4zt,\
    x5tt, v5xt, y5tt, v5yt, z5tt, v5zt = y
    
    r12x = x2tt - x1tt
    r12y = y2tt - y1tt
    r12z = z2tt - z1tt
    
    r13x = x3tt - x1tt
    r13y = y3tt - y1tt
    r13z = z3tt - z1tt
    
    r14x = x4tt - x1tt
    r14y = y4tt - y1tt
    r14z = z4tt - z1tt
    
    r15x = x5tt - x1tt
    r15y = y5tt - y1tt
    r15z = z5tt - z1tt
    
    r23x = x3tt - x2tt
    r23y = y3tt - y2tt
    r23z = z3tt - z2tt
    
    r24x = x4tt - x2tt
    r24y = y4tt - y2tt
    r24z = z4tt - z2tt
    
    r25x = x5tt - x2tt
    r25y = y5tt - y2tt
    r25z = z5tt - z2tt
    
    r34x = x4tt - x3tt
    r34y = y4tt - y3tt
    r34z = z4tt - z3tt
    
    r35x = x5tt - x3tt
    r35y = y5tt - y3tt
    r35z = z5tt - z3tt
    
    r45x = x5tt - x4tt
    r45y = y5tt - y4tt
    r45z = z5tt - z4tt
    
    r12 = np.sqrt(r12x**2 + r12y**2 + r12z**2)
    r13 = np.sqrt(r13x**2 + r13y**2 + r13z**2)
    r14 = np.sqrt(r14x**2 + r14y**2 + r14z**2)
    r15 = np.sqrt(r15x**2 + r15y**2 + r15z**2)
    r23 = np.sqrt(r23x**2 + r23y**2 + r23z**2)
    r24 = np.sqrt(r24x**2 + r24y**2 + r24z**2)
    r25 = np.sqrt(r25x**2 + r25y**2 + r25z**2)
    r34 = np.sqrt(r34x**2 + r34y**2 + r34z**2)
    r35 = np.sqrt(r35x**2 + r35y**2 + r35z**2)
    r45 = np.sqrt(r45x**2 + r45y**2 + r45z**2)
    
    return [v1xt, G*(+(m2/r12**3)*r12x + (m3/r13**3)*r13x + (m4/r14**3)*r14x + (m5/r15**3)*r15x),
            v1yt, G*(+(m2/r12**3)*r12y + (m3/r13**3)*r13y + (m4/r14**3)*r14y + (m5/r15**3)*r15y),
            v1zt, G*(+(m2/r12**3)*r12z + (m3/r13**3)*r13z + (m4/r14**3)*r14z + (m5/r15**3)*r15z),
            v2xt, G*(-(m1/r12**3)*r12x + (m3/r23**3)*r23x + (m4/r24**3)*r24x + (m5/r25**3)*r25x),
            v2yt, G*(-(m1/r12**3)*r12y + (m3/r23**3)*r23y + (m4/r24**3)*r24y + (m5/r25**3)*r25y),
            v2zt, G*(-(m1/r12**3)*r12z + (m3/r23**3)*r23z + (m4/r24**3)*r24z + (m5/r25**3)*r25z),
            v3xt, G*(-(m1/r13**3)*r13x - (m2/r23**3)*r23x + (m4/r34**3)*r34x + (m5/r35**3)*r25x),
            v3yt, G*(-(m1/r13**3)*r13y - (m2/r23**3)*r23y + (m4/r34**3)*r34y + (m5/r35**3)*r35y),
            v3zt, G*(-(m1/r13**3)*r13z - (m2/r23**3)*r23z + (m4/r34**3)*r34z + (m5/r35**3)*r35z),
            v4xt, G*(-(m1/r14**3)*r14x - (m2/r24**3)*r24x - (m3/r34**3)*r34x + (m5/r45**3)*r45x),
            v4yt, G*(-(m1/r14**3)*r14y - (m2/r24**3)*r24y - (m3/r34**3)*r34y + (m5/r45**3)*r45y),
            v4zt, G*(-(m1/r14**3)*r14z - (m2/r24**3)*r24z - (m3/r34**3)*r34z + (m5/r45**3)*r45z),
            v5xt, G*(-(m1/r15**3)*r15x - (m2/r25**3)*r25x - (m3/r35**3)*r35x - (m5/r45**3)*r45x),
            v5yt, G*(-(m1/r15**3)*r15y - (m2/r25**3)*r25y - (m3/r35**3)*r35y - (m5/r45**3)*r45y),
            v5zt, G*(-(m1/r15**3)*r15z - (m2/r25**3)*r25z - (m3/r35**3)*r35z - (m5/r45**3)*r45z)]


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def plot_3d():
    '''
    Static plot with 2 planets in 3D - (x, y, t) axis
    '''
    x1_t, y1_t, x2_t, y2_t = a[:, 0], a[:, 2], \
        a[:, 4], a[:, 6]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('TIME')
    ax.plot(x1_t, y1_t, t)
    ax.plot(x2_t, y2_t, t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def just_plot_stupid_graph():
    ''' Plot a very 💩 boring static plot 💩 of 2 planets in 2D'''
    x1_t, y1_t = a[:, 0], a[:, 2]
    x2_t, y2_t = a[:, 4], a[:, 6]
    plt.plot(x1_t, y1_t)
    plt.plot(x2_t, y2_t)
        


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def two_d_plot():
    ''' Animated 2D plot of 2 planets '''
    global line1, line2, anim1
    fig = plt.figure(facecolor='white')
    ax = plt.axes(xlim=(-Z, Z), ylim=(-Z, Z))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    ms = 10  # Set marker size

    # Create line var
    line1, = ax.plot([], [], markersize=ms)
    line2, = ax.plot([], [], markersize=ms)
    
    line1.set_marker('*')
    line2.set_marker('D')
    
    ax.grid(True)

    # Create animation
    anim1 = animation.FuncAnimation(fig, redraw2d, frames=NUM_P, interval=1)
    plt.show()


def redraw2d(time):
    ''' Redraw function for animation.FuncAnimation in two_d_plot() '''
    x1_t, y1_t = a[time, 0], a[time, 2]
    x2_t, y2_t = a[time, 4], a[time, 6]

    line1.set_data(x1_t, y1_t)
    line2.set_data(x2_t, y2_t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def three_d_plot_3p():
    ''' Animated 3D plot of 3 planets '''
    global line1, line2, line3, anim2
    fig = plt.figure()
    ax = p3.Axes3D(fig, xlim3d=(-Z, Z), ylim3d=(-Z, Z), zlim3d=(-Z, Z))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ms, c = 10, (0.6,0.6,0.6)  # Set marker size and color
    line1, = ax.plot([], [], markersize=ms)
    line2, = ax.plot([], [], markersize=ms)
    line3, = ax.plot([], [], markersize=ms)
    
    line1.set_marker('*')
    line2.set_marker('D')
    line3.set_marker('^')
    
    ax.plot([-Z, Z], [0, 0], [0, 0], color=c)
    ax.plot([0, 0], [-Z, Z], [0, 0], color=c)
    ax.plot([0, 0], [0, 0], [-Z, Z], color=c)
    
    anim2 = animation.FuncAnimation(fig, redraw3d_3p, frames=NUM_P, interval=1)
    plt.show()


def redraw3d_3p(time):
    ''' Redraw function for animation.FuncAnimation in three_d_plot_3p() '''
    x1_t, y1_t, z1_t = b[time, 0], b[time, 2], b[time, 4]
    x2_t, y2_t, z2_t = b[time, 6], b[time, 8], b[time, 10]
    x3_t, y3_t, z3_t = b[time, 12], b[time, 14], b[time, 16]
    line1.set_data(x1_t, y1_t)
    line2.set_data(x2_t, y2_t)
    line3.set_data(x3_t, y3_t)
    line1.set_3d_properties(z1_t)
    line2.set_3d_properties(z2_t)
    line3.set_3d_properties(z3_t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def three_d_plot_4p():
    ''' Animated 3D plot of 4 planets '''
    global line1, line2, line3, line4, anim3
    fig = plt.figure()
    ax = p3.Axes3D(fig, xlim3d=(-Z, Z), ylim3d=(-Z, Z), zlim3d=(-Z, Z))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ms, c = 10, (0.6,0.6,0.6)
    line1, = ax.plot([], [], markersize=ms)
    line2, = ax.plot([], [], markersize=ms)
    line3, = ax.plot([], [], markersize=ms)
    line4, = ax.plot([], [], markersize=ms)
    
    line1.set_marker('*')
    line2.set_marker('D')
    line3.set_marker('^')
    line4.set_marker('s')
    
    ax.plot([-Z, Z], [0, 0], [0, 0], color=c)
    ax.plot([0, 0], [-Z, Z], [0, 0], color=c)
    ax.plot([0, 0], [0, 0], [-Z, Z], color=c)
    
    anim3 = animation.FuncAnimation(fig, redraw3d_4p, frames=NUM_P, interval=1)
    plt.show()


def redraw3d_4p(time):
    ''' Redraw function for animation.FuncAnimation in three_d_plot_4p() '''
    x1_t, y1_t, z1_t = c[time, 0], c[time, 2], c[time, 4]
    x2_t, y2_t, z2_t = c[time, 6], c[time, 8], c[time, 10]
    x3_t, y3_t, z3_t = c[time, 12], c[time, 14], c[time, 16]
    x4_t, y4_t, z4_t = c[time, 18], c[time, 20], c[time, 22]
    
    line1.set_data(x1_t, y1_t)
    line2.set_data(x2_t, y2_t)
    line3.set_data(x3_t, y3_t)
    line4.set_data(x4_t, y4_t)
    
    line1.set_3d_properties(z1_t)
    line2.set_3d_properties(z2_t)
    line3.set_3d_properties(z3_t)
    line4.set_3d_properties(z4_t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def three_d_plot_5p():
    ''' Animated 3D plot of 5 planets and their tails'''
    global line1, line2, line3, line4, line5, anim4
    global tail1, tail2, tail3, tail4, tail5
    fig = plt.figure()
    ax = p3.Axes3D(fig, xlim3d=(-Z, Z), ylim3d=(-Z, Z), zlim3d=(-Z, Z))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ms, c = 10, (0.6,0.6,0.6)
    line1, = ax.plot([], [], markersize=ms)
    line2, = ax.plot([], [], markersize=ms)
    line3, = ax.plot([], [], markersize=ms)
    line4, = ax.plot([], [], markersize=ms)
    line5, = ax.plot([], [], markersize=ms)
    
    tail1, = ax.plot([], [], markersize=ms, color='blue')
    tail2, = ax.plot([], [], markersize=ms, color='orange')
    tail3, = ax.plot([], [], markersize=ms, color='green')
    tail4, = ax.plot([], [], markersize=ms, color='red')
    tail5, = ax.plot([], [], markersize=ms, color='purple')
    
    line1.set_marker('*')
    line2.set_marker('D')
    line3.set_marker('^')
    line4.set_marker('s')
    line5.set_marker('8')
    
    ax.plot([-Z, Z], [0, 0], [0, 0], color=c)
    ax.plot([0, 0], [-Z, Z], [0, 0], color=c)
    ax.plot([0, 0], [0, 0], [-Z, Z], color=c)
    
    anim4 = animation.FuncAnimation(fig, redraw3d_5p, frames=NUM_P, interval=1)
    plt.show()


def redraw3d_5p(time):
    ''' Redraw function for animation.FuncAnimation in three_d_plot_5p() '''
    x1_t, y1_t, z1_t = d[time, 0], d[time, 2], d[time, 4]
    x2_t, y2_t, z2_t = d[time, 6], d[time, 8], d[time, 10]
    x3_t, y3_t, z3_t = d[time, 12], d[time, 14], d[time, 16]
    x4_t, y4_t, z4_t = d[time, 18], d[time, 20], d[time, 22]
    x5_t, y5_t, z5_t = d[time, 24], d[time, 26], d[time, 28]
    
    tx1, ty1, tz1 = d[0:time, 0], d[0:time, 2], d[0:time, 4]
    tx2, ty2, tz2 = d[0:time, 6], d[0:time, 8], d[0:time, 10]
    tx3, ty3, tz3 = d[0:time, 12], d[0:time, 14], d[0:time, 16]
    tx4, ty4, tz4 = d[0:time, 18], d[0:time, 20], d[0:time, 22]
    tx5, ty5, tz5 = d[0:time, 24], d[0:time, 26], d[0:time, 28]
    
    line1.set_data(x1_t, y1_t)
    line2.set_data(x2_t, y2_t)
    line3.set_data(x3_t, y3_t)
    line4.set_data(x4_t, y4_t)
    line5.set_data(x5_t, y5_t)
    
    tail1.set_data(tx1, ty1)
    tail2.set_data(tx2, ty2)
    tail3.set_data(tx3, ty3)
    tail4.set_data(tx4, ty4)
    tail5.set_data(tx5, ty5)
    
    line1.set_3d_properties(z1_t)
    line2.set_3d_properties(z2_t)
    line3.set_3d_properties(z3_t)
    line4.set_3d_properties(z4_t)
    line5.set_3d_properties(z5_t)
    
    tail1.set_3d_properties(tz1)
    tail2.set_3d_properties(tz2)
    tail3.set_3d_properties(tz3)
    tail4.set_3d_properties(tz4)
    tail5.set_3d_properties(tz5)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# Set start/end points for t
POINT_1, POINT_2, NUM_P = 0, 10, 1000
t = np.linspace(POINT_1, POINT_2, NUM_P)

# Set planets' masses
m1, m2, m3, m4, m5 = 1, 20, 3, 1, 2

G = 10
Z = 10

# Set planets' initial parameters
x1, y1, z1, V1x, V1y, V1z = 5, -5, 3, -2, -2, 1
x2, y2, z2, V2x, V2y, V2z = 0, 0, 0, -1, -1, 0
x3, y3, z3, V3x, V3y, V3z = -3, -3, -3, 1, -3, -1
x4, y4, z4, V4x, V4y, V4z = -5, -5, -1, -1, 3, 3
x5, y5, z5, V5x, V5y, V5z = 5, 5, 1, 3, 1, -3

initparam_2p_2d = [x1, V1x, y1, V1y,
                   x2, V2x, y2, V2y]
initparam_3p_3d = [x1, V1x, y1, V1y, z1, V1z,
                   x2, V2x, y2, V2y, z2, V2z,
                   x3, V3x, y3, V3y, z3, V3z]
initparam_4p_3d = [x1, V1x, y1, V1y, z1, V1z,
                   x2, V2x, y2, V2y, z2, V2z,
                   x3, V3x, y3, V3y, z3, V3z,
                   x4, V4x, y4, V4y, z4, V4z]
initparam_5p_3d = [x1, V1x, y1, V1y, z1, V1z,
                   x2, V2x, y2, V2y, z2, V2z,
                   x3, V3x, y3, V3y, z3, V3z,
                   x4, V4x, y4, V4y, z4, V4z,
                   x5, V5x, y5, V5y, z5, V5z]

# Solve differential equations
a = odeint(two_planets_odeint, initparam_2p_2d, t)
b = odeint(three_planets_odeint, initparam_3p_3d, t)
c = odeint(four_planets_odeint, initparam_4p_3d, t)
d = odeint(five_planets_odeint, initparam_5p_3d, t)

# Plot
# plot_3d()
# just_plot_stupid_graph()
# two_d_plot()
# three_d_plot_3p()
# three_d_plot_4p()
three_d_plot_5p()
