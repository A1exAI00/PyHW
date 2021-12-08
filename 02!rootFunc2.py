# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 12:36:31 2021

@author: Alexandr Akinin

Program to find roots for a function
"""

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def root_finder(p1,p2):
    """
    Finds the most left root on the (p1,p2) segment.
    
    Parameters
    ---------
    p1 : float / int
        First point of the segment.
    p2 : float / int
        Second point of the segment.
    
    Returns
    -------
    bool
        False, if no roots are sound
        float, if the root is found 
    """
    p1 = min(float(p1), float(p2)); p2 = max(float(p1), float(p2))
    mid = (p1+p2)/2
    mid_value = expr(mid)
    p1_value = expr(p1)
    p2_value = expr(p2)
    first_half, second_half = False, False
    
    # Check if endpoints are roots 
    if mid_value == 0 or abs(p1-p2) < PRECISION: 
        return mid
    if p1_value == 0: 
        return p1
    if p2_value == 0: 
        return p2
    
    # Check if function changes sign on half segments
    if p1_value*mid_value < 0: 
        first_half = True
    if p2_value*mid_value < 0: 
        second_half = True
    
    # Continue the recursion  
    if first_half == False and second_half == False: 
        return "no roots"
    else:
        if first_half == True:
            response = root_finder(p1, mid)
        else:
            response = root_finder(mid, p2)
        
        # Pass the results
        if type(response) == float: 
            return response
        else: 
            return False
    return False


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def root_loop(p1, p2, n):
    """
    Uses root_finder(p1, p2) to find n roots and store them in root_list
    
    Parameters
    ----------
    p1 : float / int
        First point of the segment.
    p2 : float / int
        Second point of the segment.
    n : int
        Number of roots.

    Returns 
    -------
    root_list : list
        List of roots
    """
    p1 = min(float(p1), float(p2)); 
    p2 = max(float(p1), float(p2))
    root_list = []
    for i in range(n):
        p = root_finder(p1, p2)
        if type(p) == float: 
            root_list.append(p)
            p1 = p + PRECISION
    return root_list


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def root_segment_div(p1, p2, N):
    """
    Divides the segment (p1, p2) into N parts and tries to find root there
    If the root is found, it is stored in root_list.

    Parameters
    ----------
    p1 : float / int
        First point of the segment.
    p2 : float / int
        Second point of the segment.
    N : int
        The number of smaller segments.
    
    Returns 
    -------
    root_list : list
        List of roots
    """
    p1 = min(float(p1), float(p2)); p2 = max(float(p1), float(p2))
    root_list = []
    small_segment_len = abs(p2-p1)/N
    for i in range(N):
        p = root_finder(p1, p1+small_segment_len)
        if type(p) == float: 
            root_list.append(p)
        p1 += small_segment_len + PRECISION
    return root_list


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


PRECISION = 1e-15

expr = lambda x: 4 * x**3 - x**2 - 5*x - 0.5

POINT_1 = -2
POINT_2 = 3

print(root_loop(POINT_1, POINT_2, 3))
print(root_segment_div(POINT_1, POINT_2, 10))
