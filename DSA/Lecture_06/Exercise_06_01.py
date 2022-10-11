#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   Exercise_06_01.py
@Time    :   2022/10/10 12:31:09
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

"""
Ex.1

Give a Python implementation for finding the second-to-last node
 in a singly linked list in which the last node is indicated by a
  next reference of None.
"""

class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage."""

    #-------------------------- nested Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element' , '_next' # streamline memory usage

        def __init__(self, element, next): # initialize node’s fields
            self._element = element # reference to user’s element
            self._next = next # reference to next node

    #------------------------------- stack methods -------------------------------
    def __init__(self):
        """Create an empty stack."""
        self._head = None # reference to the head node
        self._size = 0 # number of stack elements

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self._size == 0

    def push(self, e):
        """Add element e to the top of the stack."""
        self._head = self._Node(e, self._head) # create and link a new node
        self._size += 1

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

           Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element # top of stack is at head of list
    
    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

           Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        answer = self._head._element
        self._head = self._head._next # bypass the former top node
        self._size -= 1
        return answer

    def second_last(self):
        """Return (but do not remove) the element at the second last of the stack.
        """

        if self.is_empty():
            raise Empty('Stack is empty')
        if self._head == None:
            return None
        if self._head._next == None:
            self._head = None
        
        temp = self._head
        while temp._next._next != None:
            temp = temp._next
        
        second_last = temp
        return second_last._element

    def __str__(self):
        if self.is_empty():
            return ""
        temp = self._head
        s = str(temp._element)
        while temp._next != None:
            s += ", "
            temp = temp._next
            s += str(temp._element)
        return s


test = LinkedStack()
for i in range(0,11):
    test.push(i)

print(test) 
print(test.second_last())