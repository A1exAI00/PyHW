# -*- coding: utf-8 -*-
"""
Created on Fri Oct 8 18:25:30 2021

@author: Alex Akinin

Contains:
    create_array(num) - creates array for sorting
    choice_sort(array) - choice sorting algorythm
    bouble_sort(array) - bouble sorting algorythm
    insertion_sort(array) - insertion sorting algorythm
    quick_sort(array) - qsort sorting algorythm
    merge_sort(array) - merge sorting algorythm
    heap_sort(array) - heap sorting algorythm
    python_sort(array) - python default sorting algorythm
    bogo_sort(array) - bogo sorting algorythm
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

    while swaps:
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


def quick_sort(array):
    '''
    Sorts array by using QuickSort sorting algorythm.

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
    tmp_a = np.array(quick_sort_recursion(tmp_a))
    
    if SHOW_OUTPUTS:
        print("Quick sort:", tmp_a)
    
    return tmp_a


def quick_sort_recursion(array):
    ''' Auxiliary function for quick_sort() '''
    tmp_a = array.copy()
    
    if len(tmp_a) <= 1:
        return tmp_a
    
    element = tmp_a[0]
    left = list(filter(lambda x: x < element, tmp_a))
    center = [i for i in tmp_a if i == element]
    right = list(filter(lambda x: x > element, tmp_a))
    
    return quick_sort_recursion(left) + center + quick_sort_recursion(right)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def merge_sort(array):
    '''
    Sorts array by using merge sorting algorythm.

    Parameters
    ----------
    array : list / numpy.ndarray
        Array to sort.

    Returns
    -------
    tmp_a : numpy.ndarray
        Sorted array.
    '''

    tmp_a = list(array.copy())
    
    tmp_a = np.array(split_and_merge_list(tmp_a))
    
    if SHOW_OUTPUTS:
        print("Merge sort:", tmp_a)
        
    return tmp_a


def split_and_merge_list(array):
    ''' Auxiliary function for merge_sort() '''
    N1 = len(array) // 2
    array1 = array[:N1]
    array2 = array[N1:]
    
    if len(array1) > 1:
        array1 = split_and_merge_list(array1)
    if len(array2) > 1:
        array2 = split_and_merge_list(array2)
        
    return merge_list(array1, array2)


def merge_list(a, b):
    ''' Function for merging list for merge_sort() '''
    c = []
    N = len(a); M = len(b)
    
    i = 0; j = 0
    while i < N and j < M:
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    c += a[i:] + b[j:]
    return c


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def heap_sort(array):
    '''
    Sorts array by using heap sorting algorythm.

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
    n = len(tmp_a)

    for i in range(n, -1, -1):
        create_heap(tmp_a, n, i)

    for i in range(n-1, 0, -1):
        tmp_a[i], tmp_a[0] = tmp_a[0], tmp_a[i]  # свап
        create_heap(tmp_a, i, 0)
    
    if SHOW_OUTPUTS:
        print("Heap sort:", tmp_a)
    
    return tmp_a


def create_heap(tmp_a, n, i):
    ''' Auxiliary function for heap_sort() '''
    maxim = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and tmp_a[i] < tmp_a[left]:
        maxim = left

    if right < n and tmp_a[maxim] < tmp_a[right]:
        maxim = right

    if maxim != i:
        tmp_a[i], tmp_a[maxim] = tmp_a[maxim], tmp_a[i]
        create_heap(tmp_a, n, maxim)


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


def plot_time() -> None:
    """
    Plots how much time diffetent algorythms take for arrays of 
    different lengths
    """
    
    global SHOW_OUTPUTS
    tmp_SHOW_OUTPUTS = SHOW_OUTPUTS; SHOW_OUTPUTS = False
    
    elements_to_average = 1
    t1, t2, t3, t4, t5, t6, t7 = [], [], [], [], [], [], []
    t_1, t_2, t_3, t_4, t_5, t_6, t_7 = [], [], [], [], [], [], []
    max_array_len = round(1e3)
    num_div = 10

    for index in range(10, max_array_len, round((max_array_len-10)/num_div)):
        for i in range(elements_to_average):
            create_array(index)

            st_time = time.perf_counter()
            choice_sort(array1)
            t1.append(time.perf_counter() - st_time)

            st_time = time.perf_counter()
            bouble_sort(array1)
            t2.append(time.perf_counter() - st_time)

            st_time = time.perf_counter()
            insertion_sort(array1)
            t3.append(time.perf_counter() - st_time)

            st_time = time.perf_counter()
            python_sort(array1)
            t4.append(time.perf_counter() - st_time)
            
            st_time = time.perf_counter()
            quick_sort(array1)
            t5.append(time.perf_counter() - st_time)
            
            st_time = time.perf_counter()
            merge_sort(array1)
            t6.append(time.perf_counter() - st_time)
            
            st_time = time.perf_counter()
            heap_sort(array1)
            t7.append(time.perf_counter() - st_time)

        t_1.append(sum(t1)); t_2.append(sum(t2))
        t_3.append(sum(t3)); t_4.append(sum(t4))
        t_5.append(sum(t5)); t_6.append(sum(t6))
        t_7.append(sum(t7))

    x = np.arange(10, max_array_len, round((max_array_len-10)/num_div))
    plt.plot(x, t_1[:num_div+1])  # blue
    plt.plot(x, t_2[:num_div+1])  # orange
    plt.plot(x, t_3[:num_div+1])  # green
    plt.plot(x, t_4[:num_div+1])  # red
    plt.plot(x, t_5[:num_div+1])  # purple
    plt.plot(x, t_6[:num_div+1])  # brown
    plt.plot(x, t_7[:num_div+1])  # pink
    
    plt.grid()
    plt.xlabel('Array length')
    plt.ylabel('Time')
    plt.yscale('log')

    # Code to create legend
    blue_patch = mpatches.Patch(color='blue', label='Choice sort')
    orange_patch = mpatches.Patch(color='orange', label='Bouble sort')
    green_patch = mpatches.Patch(color='green', label='Insertion sort')
    red_patch = mpatches.Patch(color='red', label='Python sort')
    purple_patch = mpatches.Patch(color='purple', label='Quick sort')
    brown_patch = mpatches.Patch(color='brown', label='Merge sort')
    pink_patch = mpatches.Patch(color='pink', label='Heap sort')
    plt.legend(handles=[blue_patch, orange_patch, green_patch, \
                        purple_patch, brown_patch, pink_patch,red_patch])
    SHOW_OUTPUTS = tmp_SHOW_OUTPUTS


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


st = time.perf_counter()

SHOW_OUTPUTS = True

ABS_MAX_VALUE = 10  # Max value of any number in an unsorted array
ARRAY_SIZE = 10  # Length of an array


# Create an array
array1 = create_array(ABS_MAX_VALUE, ARRAY_SIZE)

# Create an array for bogoSort
bogo_array = np.array(list(range(5)))
rn.shuffle(bogo_array)

# Run sorting alg
choice_sort(array1)
bouble_sort(array1)
insertion_sort(array1)
quick_sort(array1)
merge_sort(array1)
heap_sort(array1)
print()

# Run additional functions
plot_time()
# bogo_sort(bogo_array)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


print('\nExecution:', time.perf_counter() - st, 'sec')