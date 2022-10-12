#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercises.py
@Time    :   2022/10/12 12:27:16
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# 1. For each of the following programs, 
# compute its output without running them.
print('\na)')
xs = [0,1,2,3,4,5]
print(xs[0],xs[2],xs[-1])
print(xs[1:15:2])
print(xs[15:1:2])

print('\nb)')
xs = [0,1,2,3,4,5]
print(xs[1:2])
print(xs[1:3])
print(xs[:3])
print(xs[3:])
print(xs[1:4:2])
print(xs[1:5:2])

print('c)\n')
xs = [[0,1],[2,3,4],[],[5]]
print(xs[1])
print(xs[1][1])
print(xs[:3][1])
print(xs[1][1:])

print('d)\n')
xs = [0,1,2,3,4,5]
# print(xs[len(xs)])
# list index out of range

# 2. For each of the following programs, compute its output
# without running them
print('\na)')
xs = [0,1,2,3,4,5]
xs[0] = xs[2]
print(xs[0],xs[2])

print('\nb)')
xs = [0,1,2,3,4,5]
del xs[2]
print(xs)

print('\nc)')
xs = [0,1,2,3,4,5]
xs.append(7)
print(xs)

print('\nd)')
xs = [0,1,2,3,4,5]
print(xs.pop())  # without index pops the last element
print(xs)