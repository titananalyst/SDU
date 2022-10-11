#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exrecise_04_1.py
@Time    :   2022/09/26 12:18:03
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

import ctypes # provides low-level arrays

class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0 # count actual elements
        self._capacity = 1 # default array capacity
        self._A = self._make_array(self._capacity) # low-level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k] # retrieve from array

    def append(self, obj):
        """Add object to end of the array."""
        if self._n == self._capacity: # not enough room
            self._resize(2 * self._capacity) # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def pop(self, obj):
        """Removes object from the end of the array
        
        contains an error!!!
        """
        ind = self._n -1
        if self._n <= (self._capacity * 0.25):
            self._capacity = (self._capacity // 2)
            self._resize(self._capacity)
        self._A[ind] = obj
        self._n -= 1

    def pop_method(self):
        self._n -= 1
        self._A[self._n] = ''
        if self._n > self._capacity // 4:
            self._resize(self._capacity // 2)
        


    def _resize(self, c): # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c) # new (bigger) array
        for k in range(self._n): # for each existing value
            B[k] = self._A[k]
        self._A = B # use the bigger array
        self._capacity = c

    def _make_array(self, c): # nonpublic utitity
        """Return new array with capacity c."""
        return (c * ctypes.py_object)() # see ctypes documentation


A = DynamicArray()
list_demo = ["ABC", "hkjfds", "wehfds", "fdskl", "fsdjkl", "fdjski", "ufsdi", "fjsia"]
b = []

for i in range(len(list_demo)):
    A.append(list_demo[i-1])
    print(A._n)
    b = [j for j in A]
    print(b)
    print("Capacity:", A._capacity)

print("\n" + (20 * "*"))
for i in range(len(A)):
    print(A.__getitem__(i))
print((20 * "*") + "\n")

# for i in range(len(list_demo)):
#     A.pop(list_demo[i-1])
#     b = [j for j in A]
#     print(b)
#     print("Capacity:", A._capacity)

for i in range(len(list_demo)):
    A.pop_method()
    b = [j for j in A]
    print(b)
    print("Capacity:", A._capacity)