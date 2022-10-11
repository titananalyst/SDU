#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercise_3_2
@Time    :   2022/09/25 16:35:08
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# Exercise 3_2

def reverse(s):
    if len(s) == 0:
        return s
    else:
        return reverse(s[1:]) + s[0]
  
  
s = "Matas for the win"

print(reverse(s))
  
