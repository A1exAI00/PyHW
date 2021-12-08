# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 14:19:20 2021

@author: Alex Akinin
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def monte_carlo_area(tmp_expr, p1, p2, N):
    '''
    Find area using Monte Carlo method

    Parameters
    ----------
    p1 : float/int
        Left point on X-axis
    p2 : float/int
        Right point on X-axis
    N : int
        Number of random points
    
    Returns
    -------
    area : float
        An area under the function
    '''

    # Create rand points
    rand_points = np.random.rand(N, 2)  

    # Create bounding box for the function
    ract_length = p2 - p1 
    x = np.linspace(p1, p2, num=round(ract_length*10))
    y = tmp_expr(x)
    ract_height = np.max(y) + 1
    ract_area = ract_height * ract_length
    
    # Count points in an area
    count = 0
    for i in range(N):
        rand_points[i][0] *= ract_length
        rand_points[i][1] *= ract_height
        rand_points[i][0] += p1
        if tmp_expr(rand_points[i][0]) >= rand_points[i][1]:
            count += 1
    
    area = ract_area * count/N
    return area


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


N = int(1e5)  # Number of random points
M = 50  # How many times to run monte_carlo_area

# Set left and right points
POINT_1 = 0
POINT_2 = np.pi
if POINT_1 > POINT_2:
    POINT_1, POINT_2 = POINT_2, POINT_1

# Example functions
EXPR1 = lambda x: x**(np.sin(x))
EXPR2 = lambda x: x**x
EXPR3 = lambda x: np.sin(x)
EXPR4 = lambda x: 1
EXPR5 = lambda x: x**2
EXPR6 = lambda x: x**(np.sin(x) + 1)

# Set expression
expr = EXPR6

# Run monte_carlo_area
res = []
for _ in range(M):
    res.append(monte_carlo_area(POINT_1, POINT_2, N))

# Print all results and the avarage
print(res)
print(np.average(res))