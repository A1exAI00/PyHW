# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:41:57 2021

@author: Alex Akinin

Program for different oscillators

Contains:
    simple_oscillator() - differential equation function for x'' + w^2 * x = 0
    plot_simple_oscillator() - plots answer for x'' + w^2 * x = 0
    simple_oscillator_sin() - function for x'' + w^2 * sin(x) = 0
    plot_simple_oscillator_sin() - plots answer for x'' + w^2 * sin(x) = 0
    complex_oscillator() - function for 
        x'' + 2β*x' + w^2 * sin(x) - A0 * cos(Ω*t) = 0
    plot_compl_x_t() - plots x(t) for complex oscillator
    plot_compl_v_t() - plots v(t) for complex oscillator
    plot_compl_x_v() - plots x(v) for complex oscillator
    plot_compl_Amax_O() - plots A_max(Ω) for complex oscillator
    plot_compl_all() - plots all for complex oscillator
    draw_fancy_plot() - adds beauty to plots
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def simple_oscillator(y, t, w):
    ''' Differential equation for odeint for a plot_simple_oscillator() '''
    tmp_y0, tmp_y1 = y
    return [tmp_y1, -tmp_y0 * w**2]


def plot_simple_oscillator():
    '''
    Solver for x'' + w^2 * x = 0 equation
    Plots the solution
    '''
    y_plot = odeint(simple_oscillator, y0, t, args=(w,))
    y_plot = np.transpose(y_plot)
    plt.plot(t, y_plot[1])


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def simple_oscillator_sin_odeint(y, t, w):
    ''' Differential equation for odeint for a plot_simple_oscillator_sin() '''
    tmp_y0, tmp_y1 = y
    return [tmp_y1, -np.sin(tmp_y0) * w**2]

def plot_simple_oscillator_sin():
    '''
    Solver for x'' + w^2 * sin(x) = 0 equation
    Plots the solution
    '''
    y_plot = odeint(simple_oscillator_sin_odeint, y0, t, args=(w,))
    y_plot = np.transpose(y_plot)
    plt.plot(t, y_plot[1])


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def complex_oscillator_odeint(y, t, B, w, A0, O):
    ''' Differential equation for odeint for a complex oscillator '''
    tmp_y0, tmp_y1 = y
    return [tmp_y1, \
            (-2*B * tmp_y1) - (w**2 * np.sin(tmp_y0) + A0 * np.cos(O*t))]


def plot_compl_x_t(plot=True):
    '''
    Solver for x'' + 2β*x' + w^2 * sin(x) - A0 * cos(Ω*t) = 0 equation
    Plots x(t)
    '''
    y_plot = odeint(complex_oscillator_odeint, y0, t, args=(B,w,A0,O))
    y_plot = np.transpose(y_plot)[1]
    
    if plot == True:
        plt.plot(t, y_plot)
    else:
        return t, y_plot


def plot_compl_v_t(plot=True):
    '''
    Solver for x'' + 2β*x' + w^2 * sin(x) - A0 * cos(Ω*t) = 0 equation
    Plots V(t)
    '''
    y_plot = odeint(complex_oscillator_odeint, y0, t, args=(B,w,A0,O))
    y_plot = np.transpose(y_plot)[1]
    v = []
    for i in range(len(y_plot)):
        v.append((y_plot[i] - y_plot[i-1])/dt)
    v[0] = 0
    
    if plot == True:
        plt.plot(t, v)
    else:
        return t, v


def plot_compl_x_v(plot=True):
    '''
    Solver for x'' + 2β*x' + w^2 * sin(x) - A0 * cos(Ω*t) = 0 equation
    Plots x(V)
    '''
    y_plot = odeint(complex_oscillator_odeint, y0, t, args=(B,w,A0,O))
    y_plot = np.transpose(y_plot)[1]
    v = []
    for i in range(len(y_plot)):
        v.append((y_plot[i] - y_plot[i-1])/dt)
    v[0] = -y0[1] * 3
    
    if plot == True:
        plt.plot(y_plot, v)
    else:
        return y_plot, v


def plot_compl_Amax_O(plot=True):
    '''
    Solver for x'' + 2β*x' + w^2 * sin(x) - A0 * cos(Ω*t) = 0 equation
    Plots A(O)
    '''
    y0 = [0, 0]
    A_max = []
    O_array = np.linspace(Omin, Omax, dO)
    for i in O_array:
        O = i
        y_plot = odeint(complex_oscillator_odeint, y0, t, args=(B,w,A0,O))
        y_plot = np.transpose(y_plot)[1]
        A_max.append(max(y_plot))
    
    if plot == True:
        plt.plot(O_array, A_max)
    else:
        return O_array, A_max


def plot_compl_all():
    '''
    Solver for x'' + 2β*x' + w^2 * sin(x) - A0 * cos(Ω*t) = 0 equation
    Plots everything above
    '''
    plt.subplot(221)
    plt.title('X(t)')
    plot_touple = plot_compl_x_t(plot=False)
    plt.plot(plot_touple[0], plot_touple[1])
    draw_fancy_plot()
    
    plt.subplot(222)
    plt.title('V(t)')
    plot_touple = plot_compl_v_t(plot=False)
    plt.plot(plot_touple[0], plot_touple[1])
    draw_fancy_plot()
    
    plt.subplot(223)
    plt.title('X(V)')
    plot_touple = plot_compl_x_v(plot=False)
    plt.plot(plot_touple[0], plot_touple[1])
    draw_fancy_plot()
    
    plt.subplot(224)
    plt.title('A_max(Ω)')
    plot_touple = plot_compl_Amax_O(plot=False)
    plt.plot(plot_touple[0], plot_touple[1])
    draw_fancy_plot()
    

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def draw_fancy_plot():
    ''' Adds ✨beauty✨ to plots '''
    plt.grid(True)
    plt.axhline(0, color=(0,0,0))
    plt.axvline(0, color=(0,0,0))
    plt.tight_layout(pad=0.1)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


st = time.perf_counter()

# Set start/end points for t
POINT_1, POINT_2, NUM_POINTS = 0, 20, 1000
dt = (POINT_2 - POINT_1)/NUM_POINTS

# Set Ω
Omin, Omax, dO = 0, 10, 100

t = np.linspace(POINT_1, POINT_2, NUM_POINTS)

# Initial parameters
y0 = [0, 1]
B, w, A0, O = 1, 1, 1, 6

# Run integration
# plot_simple_oscillator()
# plot_simple_oscillator_sin()
# plot_compl_x_t()
# plot_compl_v_t()
# plot_compl_x_v()
# plot_compl_Amax_O()
plot_compl_all()


draw_fancy_plot()
plt.show()

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


print('\nExecution took:', time.perf_counter() - st)
