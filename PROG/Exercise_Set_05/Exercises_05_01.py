#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercises_05_01.py
@Time    :   2022/10/26 12:40:45
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# 2. Write a function increment(xs:List[int]) that increments 
# every number in xs by one.
input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def increment(xs:list[int]):
    new_list = [i + 1 for i in xs]
    print(new_list)
increment(input_list)


# 5. Define an iterative function reverse(l:list) that takes a list
# and reverses it in place (without invoking list.reverse).
input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
def reverse(l:list[int]):
    reversed_list = []
    for i in l:
        reversed_list = [i] + reversed_list
    print(reversed_list)
reverse(input_list)


# 13. Define an iterative function remove_all(xs:List[int],v:int)->List[int] 
# that returns a new list with all elements of xs that are not equal v.
input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
number = 9
def remove_all(xs:list[int], v:int)->list[int]:
    removed_list = [i for i in xs if i != v]
    print(f'List without {v}:', removed_list)
remove_all(input_list, number)


# 17. Define an iterative function maximum(xs:List[float])->float 
# that returns the maximum in a list of numbers.
def maximum(xs:list[float])->float:
    for i in xs:
        pass

# 19. Define an iterative function first_index_max(xs:List[float])->int 
# that returns the indexof the first occurrence of the maximum element 
# in xs.

# 20. Define an iterative function last_index_max(xs:List[float])->int 
# that returns the index of the last occurrence of the maximum element 
# in xs.

# 33. Define an iterative function comp_table(xs:List[int],ys:List[int])->None 
# that prints a len(xs)-by-len(ys) matrix of characters where a 
# character in position i,j is '+' if xs[i] > ys[j], '-' if xs[i] < ys[j], 
# and ' ' otherwise.

# 38. Define an iterative function longest_increasing_sequence(xs:List[int])->int 
# that returns the length of the longest increasing sequence of elements 
# in xs.