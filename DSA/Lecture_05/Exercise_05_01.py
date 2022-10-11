#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercise_05_01.py
@Time    :   2022/10/03 13:38:57
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# Ex1.

"""
Implement a function that reverses a list of elements by pushing 
them onto a stack in one order, and writing them back to the list 
in reversed order.
"""

class ArrayStack:
    """LIFO Stack implementation using a Python list as underlying storage."""

    def __init__(self):
        """Create an empty stack."""
        self._data = [] # nonpublic list instance

    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self._data)

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._data) == 0

    def push(self, e):
        """Add element e to the top of the stack."""
        self._data.append(e) # new item stored at end of list

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

           Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1] # the last item in the list

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

           Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop() # remove last item from list


s_list = [i for i in range(1, 11)]
print(s_list)

d = ArrayStack()
for i in range(len(s_list)):
    d.push(s_list.pop())

d_list = [i for i in range(len(d))]
print(d._data)

