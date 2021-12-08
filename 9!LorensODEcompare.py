# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 23:09:02 2021

@author: Alex Akinin

Lorenz attractor using odeint and solve_ivp
Comparison of different integration functions

Contains: 
    lorenz_sys_odeint() - differential equation for odeint from odeint_solveivp_lorenz()
    lorenz_sys_solve_ivp() - differential equation for solve_ivp from odeint_solveivp_lorenz()
    odeint_solveivp_lorenz() - Comparison of odeint and solve_ivp using Lorenz attractor
    fun_odeint() - differential equation for odeint from compare_func
    fun_solve_ivp() - differential equation for solve_ivp from compare_func
    compare_func() - Comparison of odeint and solve_ivp using a somewhat stiff differential equation
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mpl_toolkits.mplot3d.axes3d as p3


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def lorenz_sys_odeint(y,t):
    ''' Differential equation for odeint from odeint_solveivp_lorenz() '''
    x1,y1,z1 = y
    return [sigma*(y1-x1), x1*(r-z1) - y1, x1*y1 - b*z1]


def lorenz_sys_solve_ivp(t,y):
    ''' Differential equation for solve_ivp from odeint_solveivp_lorenz() '''
    x1,y1,z1 = y
    return [sigma*(y1-x1), x1*(r-z1) - y1, x1*y1 - b*z1]


def odeint_solveivp_lorenz() -> None:
    '''
    Lorenz attractor solver
    Plots two 3D graphs: 
        blue - odeint
        orange - solve_ivp
    and one plot on ХУ-plane - difference between odeint and solve_ivp in time
    '''

    global a, b
    
    # Set t_span
    P1, P2, NUM_P = 0, 50, 10000
    t = np.linspace(P1, P2, NUM_P)
    
    # Set initial parameters
    r0 = [0, 1, 0]
    
    a = odeint(lorenz_sys_odeint, r0, t)
    b = solve_ivp(lorenz_sys_solve_ivp, [0, 50], r0, t_eval=t)
    
    # Set axis projections 
    ax_t, ay_t, az_t = a[:,0], a[:,1], a[:,2]
    bx_t, by_t, bz_t = b.y[0,:], b.y[1,:], b.y[2,:]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot(ax_t, ay_t, az_t)
    ax.plot(bx_t, by_t, bz_t)
    
    # Find difference in time 
    diff = []
    for i in range(NUM_P):
        r_a = np.sqrt(ax_t[i]**2 + ay_t[i]**2 + az_t[i]**2)
        r_b = np.sqrt(bx_t[i]**2 + by_t[i]**2 + bz_t[i]**2)
        diff.append(r_b - r_a)
     
    plt.plot(t, diff)
    plt.show()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def fun_odeint(y, t):
    '''Функция для метода odeint ниже'''
    return 2*t + 50 * t**49 + 500*np.pi*np.cos(10*np.pi*t)*np.sin(10*np.pi*t)**49


def fun_solve_ivp(t, y):
    '''Функция для метода solve_ivp ниже'''
    return 2*t + 50 * t**49 + 500*np.pi*np.cos(10*np.pi*t)*np.sin(10*np.pi*t)**49


def compare_func() -> None:
    '''
    Comparison of odeint and solve_ivp using a somewhat stiff differential equation 
    
    Solves ODE using odeint, RK45, RK23, LSODA 
    Plots correct solution and odeint, RK45, RK23, LSODA solutions
        and difference between them 
    '''

    global a, b, c
    
    P1, P2, NUM_P = 0, 1, 1000
    t = np.linspace(P1, P2, NUM_P)
    
    # Original func: x^50 + x^2 + sin(10*pi*x)^50
    orig_func = lambda x: x**50 + x**2  + np.sin(10*np.pi*x)**50
    
    r0 = [0]
    
    # Solves ODE using odeint, RK45, RK23, LSODA
    a = odeint(fun_odeint, r0, t)
    b_RK45 = solve_ivp(fun_solve_ivp, [P1, P2], r0, method='RK45', t_eval=t).y[0,:]
    b_RK23 = solve_ivp(fun_solve_ivp, [P1, P2], r0, method='RK23', t_eval=t).y[0,:]
    b_DOP853 = solve_ivp(fun_solve_ivp, [P1, P2], r0, method='DOP853', t_eval=t).y[0,:]
    # b_Radau = solve_ivp(fun_solve_ivp, [P1, P2], r0, method='Radau', t_eval=t).y[0,:]
    # b_BDF = solve_ivp(fun_solve_ivp, [P1, P2], r0, method='BDF', t_eval=t).y[0,:]
    b_LSODA = solve_ivp(fun_solve_ivp, [P1, P2], r0, method='LSODA', t_eval=t).y[0,:]
    c = list(map(orig_func, t))
    
    # Find difference
    diff_a = []
    diff_b_RK45 = []
    diff_b_DOP853 = []
    diff_b_RK23 = []
    # diff_b_Radau = []
    # diff_b_BDF = []
    diff_b_LSODA = []
    for i in range(NUM_P):
        diff_a.append(a[i] - c[i])
        diff_b_RK45.append(b_RK45[i] - c[i])
        diff_b_RK23.append(b_RK23[i] - c[i])
        diff_b_DOP853.append(b_DOP853[i] - c[i])
        # diff_b_Radau.append(b_Radau[i] - c[i])
        # diff_b_BDF.append(b_BDF[i] - c[i])
        diff_b_LSODA.append(b_LSODA[i] - c[i])
         
    red_p = mpatches.Patch(color='red', label='odeint')
    blue_p = mpatches.Patch(color='blue', label='RK45')
    cyan_p = mpatches.Patch(color='cyan', label='RK23')
    green_p = mpatches.Patch(color='green', label='DOP853')
    # magenta_p = mpatches.Patch(color='magenta', label='Radau')
    # yellow_p = mpatches.Patch(color='yellow', label='BDF')
    grey_p = mpatches.Patch(color='0.8', label='LSODA')
    handles1 = [red_p, blue_p, cyan_p, green_p, grey_p]
    
    plt.subplot(211)
    plt.plot(t, c, 'black')
    plt.plot(t, a, 'r')
    plt.plot(t, b_RK45, 'b')
    plt.plot(t, b_RK23, 'c')
    plt.plot(t, b_DOP853, 'g')
    # plt.plot(t, b_Radau, 'm')
    # plt.plot(t, b_BDF, 'y')
    plt.plot(t, b_LSODA, '0.8')
    
    plt.subplot(212)
    plt.plot(t, diff_a, 'r')
    plt.plot(t, diff_b_RK45, 'b')
    plt.plot(t, diff_b_RK23, 'c')
    plt.plot(t, diff_b_DOP853, 'g')
    # plt.plot(t, diff_b_Radau, 'm')
    # plt.plot(t, diff_b_BDF, 'g')
    plt.plot(t, diff_b_LSODA, '0.8')
    plt.legend(handles=handles1)
    plt.ylim(-0.03, 0.03)
    
    plt.grid()
    plt.show()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


sigma = 10
b = 8/3
r = 30
# odeint_solveivp_lorenz()


compare_func()
plt.show()