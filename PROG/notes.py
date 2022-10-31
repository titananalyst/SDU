# Lists are ordered collections of zero or more objects. They can contain
# duplicates and can be modified.

# Here are some examples of lists

# an empty list
[]

# a list with some integers
numbers = [1,2,2,5,4,7,6]

# lists with some strings
nouns = ['apple','car','cat']

adjectives = ['red','big','old']

# objects stored in a list can be accessed by their position, called index
# indexes start from 0, like floors in a building: index 0 is the first element,
# 1 the second, and so on.
nouns[0] # 'apple'
nouns[1] # 'car'
# we can use negative indexes to start from the end of the list: -1 is the last
# element, -2 is the second to last and so on.
nouns[-1] # 'cat'

# Access to an index past the end or beginning of a list results in an IndexError
numbers[100] # IndexError: list index out of range

# lists with the same content are considered equal (order matters!)
# x and y are two lists both containing 1 and 2.
x = [1,2]
y = [1,2]
# z is defined as the same list denoted by x
z = x
# We can check this as follows
x == y # True: x and y contain both 1 and 2 in this order.
x is z # x and z mean the same object
x is y # x and y mean distinct (but equal) objects

# lists are heterogeneous: they can contain values of different types
stuff = [1,1.2,'a',True,'a']

# the type for lists is 'list'
type(numbers) # <class 'list'>

# However, this type is too "vague" for most scenarios where one wants or needs
# to consider only lists with objects of a specific type, say integers. Module
# typing provides a type for this purpose, List. Like Optional, List takes as
# parameter the type of the list elements. For instance, an annotation 
# List[int] indicates that values must be lists whose elements are of type int.
# (Observe that the empty list vacuously satisfies this constraint since it 
# has no elements).
from typing import List

def count_even(xs:List[int])->int:
  """ returns the number of even numbers in the given list
  >>> count_even([1,2,3,4])
  2
  >>> count_even([])
  0
  """
  # we'll see later how to implement this function, for the moment
  # we raise a NotImplementedError (this is a common strategy while
  # developing since returning a default value or None can go 
  # unnoticed if we forget to implement a function which results in 
  # subtle and frustrating bugs).
  raise NotImplementedError("To Do :p") 

# (Types with parameters like Optional and List are called Generic Types or 
# simply Generics).

# Python defines some built-in functions for common operations on lists
# len returns the length of its argument
len(numbers)
# max, min return the maximum and minimum
max(numbers)
min(numbers)
# sum returns the sum of all elements
sum(numbers)
# sorted returns a new list with the elements of the first from smallest to 
# largest
sorted(numbers)

# to check if an object occurs in a list, we can use the 'in' operator.
5 in numbers # True
3 in numbers # False

# like strings, we can create new lists by concatenation and repetition
nouns + [ 'truck', 'shirt' ]
nouns * 2
# these operations create new lists, the old ones are unchanged.
# Remember that the new list will contain the same objects of the arguments
# neither + nor * makes deep copies of the objects.
# To check this, let's make a list with a list inside and duplicate it
x = [ [1] ]
twice_x = x * 2 
# and check if the inner list [1] is the same
x[0] is twice_x[0] # True
x[0] is twice_x[1] # True
twice_x[0] is twice_x[1] # True
# It is important to keep this in mind when we update lists created in this way:
# editing the inner list at x[0] is the same as editing twice_x[0] or 
# twice_x[1]!

def sequence_up_to(n:int)->List[int]:
  """
  Returns a list with the sequence of numbers from 0 to n

  >>> sequence_up_to(-1)
  []
  >>> sequence_up_to(0)
  [0]
  >>> sequence_up_to(3)
  [0,1,2,3]
  """
  if n < 0:
    return []
  else:
    return sequence_up_to(n-1) + [n]
# List concatenation is ok but not always the most efficient option. We'll see 
# more efficient alternatives later.

# List comprehension is a general way of defining new lists using elements from
# other lists as inputs we can modify in a uniform way.
# For instance, the following creates a new list by taking each element from
# some numbers and incrementing it by 1. 
[ x + 1 for x in numbers ]
# The order of the elements is preserved from the input list.
# this is a list obtained by doubling all elements of numbers
[ y * 2 for y in numbers ]
# and a list obtained by taking the square root of all elements of numbers
[ z ** 0.5 for z in numbers ]
# The basic form is [ expression for name in list ]
# The name used to range over all elements of the list is immaterial.

# We can combine elements from more than one list by writing more 'for-in'
# clauses. For instance, here is a list of qualified names obtained from the lists nouns and adjectives.
[ adjective + ' ' + noun
  for noun in nouns
  for adjective in adjectives ]
# The order depends on the order of the for-in clauses: before we move to the next noun, we go through all adjectives. 
[ adjective + ' ' + noun
  for adjective in adjectives
  for noun in nouns ]
# In general, [ expression for name1 in list1 ... for nameN in listN ]
# for-in clauses don't need to be on different lines, but sometimes it makes
# code more readable.

# We can filter and skip some elements by specifying conditions (as boolean 
# expressions). This is the list of even numbers from numbers.
[ x for x in numbers if x % 2 == 0]
# And the list of odd numbers
[ x for x in numbers if x % 2 == 1]

# We can specify more than one if clause, they all need to be true for an
# element to be used.
[ adjective + ' ' + noun
  for noun in nouns
  for adjective in adjectives
  if len(noun) > 3
  if adjective.endswith('d') ]
# this is equivalent to taking their conjunction
[ adjective + ' ' + noun
  for noun in nouns
  for adjective in adjectives
  if len(noun) > 3 and adjective.endswith('d') ]
# if and for-in clauses can be interleaved
[ adjective + ' ' + noun
  for noun in nouns
  if len(noun) > 3
  for adjective in adjectives
  if adjective.endswith('d') ]
# The order matters however, an if clause cannot use names defined later
# The following example raises an UnboundLocalError saying that local variable 
# 'adjective' used before assignment
[ adjective + ' ' + noun
  for noun in nouns
  if len(noun) > 3
  if adjective.endswith('d')
  for adjective in adjectives ]

# for-in clauses can use as a list the element assigned by a previous for-in
# this is useful for lists of lists
# This defines the list of all elements in a list of lists.
pairs = [ [1,2], [3,4] ]
[ x for pair in pairs for x in pair]
# this operation is often called "flattening".

# We'll see next week that the same notation extends beyond lists.
# For the moment, we mention that it can also use strings as inputs
# This is the list of digits in a string
[ int(c) for c in "ab12c34" if c.isdigit() ]

# The slicing notation is another way of obtaining a list from another by 
# selecting elements in certain positions. the general form is list
#   [start:stop:step]
# and it returns the list obtained by reading the elements from the given list
# starting from index start, and advancing by step until we reach index stop
# (excluded). For instance, this is the list of all elements in even positions
numbers[0:7:2]
# And this is the sublist of the elements at indexes 2,3,4
numbers[2,5,1]
# we can omit the arguments for start, stop, and step in which case python will 
# use the following defaults:
# - no start -> default is 0 (beginning of the list)
# - no stop -> default is the length of the list (end of the list)
# - no step -> default is 1 (cover all elements)
# Negative values are supported. For instance, with step -1 we cover the list
# backwards
numbers[::-1]

# we can update lists by redefining one of its indexes like we assign a variable
numbers[0] = 7 # defines the first element as 7
# like for accessing an item of a list, assigning can raise an IndexError if the
# index is out of bounds. Try numbers[15] = 7

# we can delete a specific index from a list using the special keyword del
# all element past the deleted index are moved down by one position shortening
# the list.
del numbers[3] # deletes the item at index 3

# lists expose a number of methods for inserting, removing, searching, etc.
# (see book and documentation for details)

def sequence_up_to(n:int)->List[int]:
  """
  Returns a list with the sequence of numbers from 0 to n

  >>> sequence_up_to(-1)
  []
  >>> sequence_up_to(0)
  [0]
  >>> sequence_up_to(3)
  [0,1,2,3]
  """
  if n < 0:
    return []
  else:
    l = sequence_up_to(n-1) # build the sequence 0...n-1
    l.append(n) # add n at the end of the list
    return l
# compare this function with the one defined at the beginning of this file: 
# the first, creates a new list at each call whereas the last one operates on
# the same list (the one created in the case case of the recursion, when n<0).