# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 19:14:51 2021

@author: Alex Akinin

Lorenz Attractor
Calculation of E and Pi

Contains:
    calc_e_prec() - calculate E 
    calc_pi_prec() - calculate Pi
    set_lorenz_var() - 
    lorenz_sys_odeint()
    plot_lorenz_attractor()
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


# import numpy as np
import sympy as sp
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def calc_e_prec(prec):
    ''' Calculate E using infinite sum '''
    i = 10
    while 1/sp.factorial(i) > 10**(-prec):
        i += 10
    stop = i
    
    i = sp.symbols('i')
    return sp.summation(sp.factorial(i).evalf(prec)**-1, (i,0,stop)).evalf(prec)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def calc_pi_prec(prec): 
    ''' Calculate Pi using one of Srinivasa Ramanujan infinite sums '''
    i = sp.symbols('i')
    con = sp.Rational(2 * sp.sqrt(2).evalf(prec) , 9801)
    up = sp.factorial(4*i) * (1103 + 26390*i)
    dn = sp.factorial(i)**4 * (396)**(4*i)
    summ = sp.summation(up/dn, (i, 0, 80)).evalf(prec)
    return (sp.Rational(1, con*summ).evalf(prec))


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def lorenz_sys_odeint(y,t):
    ''' Lorenz system differential equation '''
    x1,y1,z1 = y
    return [sigma*(y1-x1), x1*(r-z1) - y1, x1*y1 - b*z1]

def plot_lorenz_attractor():
    ''' 
    Lorenz system solver
    Plots the solution 
    '''
    # Set t_span
    t = np.linspace(0, 60, 10000)
    
    # Set random start point
    rad = 5
    y0 = [(rad*np.random.rand() - rad/2) for _ in range(3)]
    # y0 = [0,0,0]
    
    # Integrate
    a = odeint(lorenz_sys_odeint, y0, t)
    
    # Plot 3D
    x_t, y_t, z_t = a[:,0], a[:,1], a[:,2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot(x_t, y_t, z_t)
    plt.show()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Compare E
print(calc_e_prec(100))
print(sp.E.evalf(100))

# Compare Pi
print(calc_pi_prec(100))
print(sp.pi.evalf(100))

# Run Lorenz Attractor
sigma, b, r = 10, sp.Rational(8/3).evalf(10), 30
plot_lorenz_attractor()