# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:05:48 2021

@author: Alex Akinin

Lotka–Volterra simulation
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def aaa(y, t):
    x1, y1 = y
    return [(a - b*y1)*x1, (-g + d*x1)*y1]

a,b,g,d = 0.8, 0.5, 0.3, 0.1
T = 50
t = np.linspace(0, T, num=1000)

y0 = [5, 2]

m = odeint(aaa, y0, t)

plt.grid()

plt.plot(t, m[:,0])
plt.plot(t, m[:,1])
# plt.plot(m[:,0], m[:,1])
plt.show()