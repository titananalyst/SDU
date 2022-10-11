#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercise_05_02.py
@Time    :   2022/10/03 14:32:20
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

# Ex2.

"""
Implement a function called transfer(S, T) that transfers
all elements from stack S onto stack T, so that the element
 that starts at the top of S is the first to be inserted onto T,
  and the element at the bottom of S ends up at the top of T.

Then, use this function along with the ArrayStack class,
which has already been defined in the lecture to test the
implementation of your transfer(S, T) function by printing
out S and T after applying the transfer(S, T) function.
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

    def transfer(self, S, T):
        for i in range(len(S)):
            T.push(S.pop())
        return T

# create two new arrayStack objects
s = ArrayStack()
t = ArrayStack()

# initial elements of the first arrayStack
for i in range(1,11):
    s.push(i)
print(s._data)


# use the transfer method to transfer elements
# from the first arrayStack to the second arrayStack
# and print them out

s.transfer(s, t)
print(s._data)
print(t._data)





