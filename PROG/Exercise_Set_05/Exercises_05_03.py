#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   loops.py
@Time    :   2022/11/02 12:40:44
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# 11 function dealing
def dealing(l:list, n:int):
    i = 0
    new_l = [[] for i in range(n)]
    for i in l:
        new_l[i].append(x)
        i = (i+1) % n
    return new_l
    
# 13 differences
def differences(l:list[int])->list[list]:
    new_l = [l]
    last_row = l
    for i in range(len(l)-1):
        new_row = []
        for j in range(len(last_row)-1):
            new_row.append(last_row[j]-last_row[j+1])
        new_l.append(new_row)
        last__row = new_row
    return new_l