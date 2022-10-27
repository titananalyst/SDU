#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercises_05_02.py
@Time    :   2022/10/26 13:23:54
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

import numpy as np
from typing import List, Callable

# 4. Define an iterative function factorial(n:int)->int that returns n!, 
# the factorial of n (n! = 1 · 2 · . . . · n).


# 9. Define an iterative function sum_even_between(m:int,n:int)->int 
# that returns the sum of all integer even numbers greater than m 
# and smaller than n.
from distutils.command import sdist


def sum_even_between(m : int, n : int)->int:
    assert m < n
    m = (m // 2 + 1) * 2 # smallest even number > m
    accumulator = 0
    for i in range(m,n,1):
        accumulator += i
    return accumulator

print(sum_even_between(2, 6))




# 15. Suppose that f is a continuous and positive function over an interval [a, b]. 
# The area between axis and the graph of f in the interval [a, b] (also called the 
# integral of f in [a, b]) can be computed as precisely as required by the 
# following method: we divide the interval [a, b] in n subintervals of equal width, 
# and approximate the integral of f in each subinterval by the area of the rectangle
# whose height is given by the value of f value in the midpoint of the interval. 
# Define a function integrate(f:Callable[[float],float],a:float,b:float,n:int)->float 
# that given a function f(x:float)->float1, floats a and b, and a positive integer n, 
# returns the approximate value of the integral of f over [a, b] using the algorithm above.
def integrate(f : Callable[[float],float], a : float, b : float, n : int) -> float:
    assert n > 0, "Number of approximation interval n must be > 0"
    assert a < b, "a must be smaller than b!"
    accumulator = 0
    interval = (b-a) / n
    for i in np.linspace(a, b, num =n):
        x = (i + i + interval) / 2
        accumulator += interval * f(x)
        return accumulator


def g(x:float)->float: return x * 2
print(integrate(g, -2, 3, 1000))

# jiawei is the tutor
