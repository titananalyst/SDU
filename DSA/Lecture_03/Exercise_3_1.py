#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercise_3_1
@Time    :   2022/09/25 16:34:59
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''


def power(x, n):
    """Compute the value x n for integer n."""
    if n == 0:
        return 1
    else:
        print("without calc:", x, n)
        print('input calc:', x, n-1)
        print("...................")
        return x * power(x, n-1)


print(power(2, 5), '\nwow it works')







