# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:01:38 2021

@author: Alex Akinin

Program to find prime numbers

Contains:
    My algorithm 
    Eratosthenes algorithm using default python lists
    Eratosthenes algorithm using NumPy arrays
    Ploting function, shows t(N) dependency
    SieveOfEratosthenes from the Internet
"""


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


import numpy as np
from matplotlib import pyplot as plt
import time


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def my_algorithm(N):
    """
    Parameters
    ----------
    N : int/float
        Biggest possible number in the list of primes.

    Returns
    -------
    primes : list
        List of prime numbers.

    """
    N = int(N-1)
    nums = np.arange(2, N+2)
    primes = np.array([])

    for i in range(N):
        not_prime = False

        for j in range(primes.shape[0]):
            if primes[j] > np.sqrt(nums[i]):
                break

            if nums[i] % primes[j] == 0:
                not_prime = True
                break

        if not_prime == False:
            primes = np.append(primes, nums[i])

    return primes.astype(int)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def eratosthenes_default(N):
    """
    Eratosthenes algorithm using default python lists

    Parameters
    ----------
    N : int/float
        Biggest possible number in the list of primes.

    Returns
    -------
    nums : list
        List of prime numbers.
    """
    N = int(N-1)
    nums = list(range(2, N+2))
    i = 0

    while i < len(nums):
        current = nums[i]
        j = i+1

        while j < len(nums):
            check = nums[j]
            if check % current == 0:
                nums.remove(check)

            j += 1
        i += 1

    return np.array(nums)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def eratosthenes_numpy(N):
    """
    Eratosthenes algorithm using NumPy arrays

    Parameters
    ----------
    N : int/float
        Biggest possible number in the list of primes.

    Returns
    -------
    nums : list
        List of prime numbers.
    """
    N = int(N-1)
    nums = np.arange(2, N+2)
    i = 0

    while i < nums.shape[0]:
        current = nums[i]
        j = i+1

        while j < nums.shape[0]:
            check = nums[j]
            if check % current == 0:
                nums = np.delete(nums, [j])

            j += 1
        i += 1

    return nums


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def SieveOfEratosthenes(n):

    # Create a boolean array "prime[0..n]" and initialize
    # all entries it as true. A value in prime[i] will
    # finally be false if i is Not a prime, else true.
    n = int(n)
    end = []
    prime = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):

        # If prime[p] is not changed, then it is a prime
        if (prime[p] == True):

            # Update all multiples of p
            for i in range(p ** 2, n + 1, p):
                prime[i] = False
        p += 1
    prime[0] = False
    prime[1] = False
    # Print all prime numbers
    for p in range(n + 1):
        if prime[p]:
            end.append(p)
    return np.array(end)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


def time_func_plot(func, N, M):
    """
    Plots t(N) dependency:
    Evaluates func at M number of points between 10 and N 
    Shows the plot

    Parameters
    ----------
    func : function
        Function that is being evaluated.
    N : int/float
        Biggest possible number in the list of primes.
    M : int
        Number of points on the plot.

    Returns
    -------
    None.

    """
    n = np.arange(10, int(N), int(N-10)/M)
    t = []

    for i in n:
        start = time.time()
        func(i)
        t.append(time.time() - start)

    plt.plot(n, t)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------


N = 1e3  # Number up to which you need to find prime numbers


print(my_algorithm(N))
print(eratosthenes_default(N))
print(eratosthenes_numpy(N))
print(SieveOfEratosthenes(N))


# Runs tests to plot t(N) dependency
# Set N∈(1e3,1e4)
# 1e5 took 20 min to evaluate
"""
time_func_plot(my_algorithm, N, M) # blue
time_func_plot(eratosthenes_default, N, M) # red
time_func_plot(eratosthenes_numpy, N, M) # green
time_func_plot(SieveOfEratosthenes, N, M)
plt.xlabel('N')
plt.ylabel('t')
plt.grid()
plt.show()
"""
