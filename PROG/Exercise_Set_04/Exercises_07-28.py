#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercises_07-28.py
@Time    :   2022/10/12 13:45:15
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''


# 22
def replace(xs:List[int], a:int, b:int) -> List[int]:
    return [b if x == a else x for x in xs]