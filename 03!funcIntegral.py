# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 15:54:11 2021

@author: Alex Akinin

Program to calculate a signed definite integral
There is a better version  -  3.1!funcIntegral.py
"""

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def integral(expr, p1, p2):
    """
    Calculates signed definite integral on segment (p1,p2) for expr
    
    Parameters
    ----------
    expr : function
        The function for the integral.
    p1 : float/int
        First point of the segment.
    p2 : float/int
        Second point of the segment.

    Returns
    -------
    n/2 : int
        Number of colomns.
    s : float
        Value of the signed definite integral.
    """
    global n, s

    segm_length = p2 - p1

    n = 10
    delta_I = 1e100
    s1, s2 = 0, 0
    
    while delta_I > PREC:
        x = np.linspace(p1, p2, num=n, endpoint=True)
        y = expr(x)
        dx = segm_length/(n-1)
        ds = y * dx
        s = np.sum(ds)
        s1, s2 = s2, s

        delta_I = abs(s1 - s2)
        n *= 2
    
    n /= 2

    return (int(n), s)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def plot(expr, p1, p2):
    """
    Plots expr within (p1-1,p2+1) segment and highlights (p1,p2) segment

    Parameters
    ----------
    expr : function
        The function for the integral.
    p1 : float/int
        First point of the segment.
    p2 : float/int
        Second point of the segment.

    Returns
    -------
    None.
    """
    N = 10*np.log2(n)
    # N = n

    segm_length = p2 - p1
    
    x = np.linspace(p1-1, p2+1, num=int(n), endpoint=True)
    y = expr(x)
    x1 = np.linspace(p1, p2, num=round(N), endpoint=True, )
    y1 = expr(x1)
    
    plt.xlim((p1 - 1, p2 + 1))
    plt.grid(True)
    plt.axhline(0, color=(0,0,0))
    plt.axvline(0, color=(0,0,0))
    
    plt.plot(x, y)
    plt.bar(x1, y1, width=segm_length/N, color=(0.6,0.1,0.1,0.3))
    plt.show()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


PREC = 1e-5

POINT_1 = 0
POINT_2 = np.pi

if POINT_1 > POINT_2: 
        POINT_1, POINT_2 = POINT_2, POINT_1

EXPR1 = lambda x: np.sin(x)
EXPR2 = lambda x: np.cos(x)
EXPR3 = lambda x: 0*x
EXPR4 = lambda x: x**x
EXPR5 = lambda x: x**(np.sin(x) + 1)

expr = EXPR5

print("(Number of colomns, signed definite integral)")
print(integral(expr, POINT_1, POINT_2))
plot(expr, POINT_1, POINT_2)
