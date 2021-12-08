# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 14:40:35 2021

@author: Alex Akinin

Comparison of sorting algorithms
There is an improved version  -  5.1!SortMethods.py

Contains:
    create_array(num) - creates array for sorting
    choice_sort(array) - choice sorting algorythm
    bouble_sort(array) - bouble sorting algorythm
    insertion_sort(array) - insertion sorting algorythm
    python_sort(array) - python default sorting algorythm
    bogo_sort(array) - bogo sorting algorythm
    check_if_ok() - compares diffetent algorythm outputs with sorted array
    plot_time() - plots how much time diffetent algorythms take
"""

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import random as rn


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def create_array(max, num):
    """
    Creates an array  of num elements for sorting
    Abs value of elements is less then abs_max_value

    Parameters
    ----------
    max : float/int
        Max value of any number in an unsorted array
    num : int
        Length of an array to create.

    Returns
    -------
    array1 : numpy.ndarray
        Sorted array.
    """

    global array1
    tmp_a = np.random.rand(num)
    tmp_a = tmp_a * (max*2) - max
    array1 = tmp_a.copy()

    if SHOW_OUTPUTS:
        print('Not sorted:', array1, end='\n\n')

    return array1


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def choice_sort(array):
    '''
    Sorts array by using choice sorting algorythm.

    Parameters
    ----------
    array : list / numpy.ndarray
        Array to sort.

    Returns
    -------
    tmp_a : numpy.ndarray
        Sorted array.
    '''

    tmp_a = array.copy()

    for i in range(len(tmp_a)-1):
        for j in range(i+1, len(tmp_a)):
            if tmp_a[j] < tmp_a[i]:
                tmp_a[j], tmp_a[i] = tmp_a[i], tmp_a[j]

    if SHOW_OUTPUTS:
        print("Choice sort:", tmp_a)

    return tmp_a


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def bouble_sort(array):
    '''
    Sorts array by using bouble sorting algorythm.

    Parameters
    ----------
    array : list / numpy.ndarray
        Array to sort.

    Returns
    -------
    tmp_a : numpy.ndarray
        Sorted array.
    '''

    tmp_a = array.copy()
    swaps = True

    while swaps == True:
        swaps = False
        for i in range(0, len(tmp_a)-1):
            if tmp_a[i+1] < tmp_a[i]:
                tmp_a[i+1], tmp_a[i] = tmp_a[i], tmp_a[i+1]
                swaps = True

    if SHOW_OUTPUTS:
        print("Bouble sort:", tmp_a)

    return tmp_a


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def insertion_sort(array):
    '''
    Sorts array by using insertion sorting algorythm.

    Parameters
    ----------
    array : list / numpy.ndarray
        Array to sort.

    Returns
    -------
    tmp_a : numpy.ndarray
        Sorted array.
    '''

    tmp_a = array.copy()

    for i in range(1, len(tmp_a)):
        elem = tmp_a[i]
        j = i
        while j > 0 and tmp_a[j-1] > elem:
            tmp_a[j] = tmp_a[j-1]
            j -= 1
        tmp_a[j] = elem

    if SHOW_OUTPUTS:
        print("Insertion sort:", tmp_a)

    return tmp_a


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def python_sort(array):
    '''
    Sorts array by using default python sorting algorythm.

    Parameters
    ----------
    array : list / numpy.ndarray
        Array to sort.

    Returns
    -------
    tmp_a : list
        Sorted array.
    '''
    tmp_a = array.copy()
    return sorted(tmp_a)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def bogo_sort(array):
    '''
    Sorts array by using bogo sorting algorythm:
    Elements are shaffled randomly and checked if they are in order

    Parameters
    ----------
    array : list / numpy.ndarray
        Array to sort.

    Returns
    -------
    tmp_a : numpy.ndarray
        Sorted array.
    '''
    
    tmp_a = array.copy()
    isSorted = False

    while isSorted == False:
        rn.shuffle(tmp_a)
        if np.array_equal(tmp_a, sorted(tmp_a)):  
            # Заметка: стоит заменить условие sorted(tmp_a)
            isSorted = True

    if SHOW_OUTPUTS:
        print("Bogo sort:", tmp_a)

    return tmp_a


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def check_if_ok():
    """
    Compares diffetent algorythm outputs with sorted array
    Prints if output is correct of incorrect

    Returns
    -------
    None.

    """
    test_array = sorted(array1)
    functions = [choice_sort(array1), bouble_sort(
        array1), insertion_sort(array1)]
    method_name = ['Choice sort', 'Bouble sort', 'Insertion sort']

    for i in range(len(method_name)):
        if np.array_equal(functions[i], test_array):
            print(method_name[i], ': OK')
        else:
            print(method_name[i], ': FAIL')


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def plot_time() -> None:
    """
    Plots how much time diffetent algorythms take for arrays of 
    different lengths
    """

    elements_to_average = 1  # How many times to run each sort alg
    t1, t2, t3, t4 = [], [], [], []  
    t_1, t_2, t_3, t_4 = [], [], [], []
    max_array_len = round(1e3)
    num_div = 7

    for index in range(10, max_array_len, round((max_array_len-10)/num_div)):
        for i in range(elements_to_average):
            create_array(index)

            st_time = time.time()
            choice_sort(array1)
            t1.append(time.time() - st_time)

            st_time = time.time()
            bouble_sort(array1)
            t2.append(time.time() - st_time)

            st_time = time.time()
            insertion_sort(array1)
            t3.append(time.time() - st_time)

            st_time = time.time()
            python_sort(array1)
            t4.append(time.time() - st_time)

        t_1.append(sum(t1))
        t_2.append(sum(t2))
        t_3.append(sum(t3))
        t_4.append(sum(t4))

    x = np.arange(10, max_array_len, round((max_array_len-10)/num_div))
    plt.plot(x, t_1[:50])  # blue
    plt.plot(x, t_2[:50])  # orange
    plt.plot(x, t_3[:50])  # green
    plt.plot(x, t_4[:50])  # red
    
    plt.grid()
    plt.xlabel('Array length')
    plt.ylabel('Time')

    # Code to create legend
    blue_patch = mpatches.Patch(color='blue', label='Choice sort')
    orange_patch = mpatches.Patch(color='orange', label='Bouble sort')
    green_patch = mpatches.Patch(color='green', label='Insertion sort')
    red_patch = mpatches.Patch(color='red', label='Python sort')
    plt.legend(handles=[blue_patch, orange_patch, green_patch, red_patch])


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

st = time.time()

SHOW_OUTPUTS = True

abs_max_value = 10  # Max value of any number in an unsorted array
array_size = 10  # Length of an array

# Array for BogoSort
bogo_array = np.array(list(range(5)))
rn.shuffle(bogo_array)


# Create an array
create_array(abs_max_value, array_size)

# Run sorting alg
choice_sort(array1)
bouble_sort(array1)
insertion_sort(array1)
print()

# Run additional functions
# check_if_ok()
# plot_time()
# bogo_sort(bogo_array)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


print('\nExecution:', time.time() - st, 'sec')
