#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercises_03-05.py
@Time    :   2022/10/12 12:45:39
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# 3. Define a function odd_positions(cs:list)->list that returns a
# list with all elements of xs in odd positions.
xs = [i for i in range(0, 6)]

def odd_positions(xs:list)->list:
    temp = [i for i in xs if not i % 2 == 0]
    return print(temp)

odd_positions(xs)

def even_positions(xs:list)->list:
    temp = [i for i in xs if i % 2 == 0]
    return print(temp)

even_positions(xs)

def reverse(xs:list)->list:
    temp = [i for i in xs[::-1]]
    return print(temp)

reverse(xs)

def runs(pattern:list, length:int)->list:
    temp = []
    counter = 0
    for i in range(0, length):
        if i < len(pattern):
            temp.append(pattern[i])
        else:
            temp.append(pattern[counter-i])
    counter += 1
    return print(temp)

runs(xs, 8)

