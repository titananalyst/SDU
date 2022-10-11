
#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercise_3_3
@Time    :   2022/09/25 16:35:18
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# Exercise 3_3

def algo(m, n):
    if n == 1:
        return m
    else:
        return m + algo(m, n-1)

print(algo(8,2))