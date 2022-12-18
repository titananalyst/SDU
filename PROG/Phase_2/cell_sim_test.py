#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/11/08 01:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
'''

from model import CellPatch, Cell
from visualiser import Visualiser
import random
from random import randint, choice
from time import sleep

import os

# TODO: make a loader 
# TODO: make a checker for the loaded grid validity
# TODO: make it possible to list dir to chose a different grid to load
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

strGrid = 'grid_1.txt'

def list_grids():
    """Return a list of all grid files in the current directory."""
    list_grids = []
    for i in os.listdir(dname):
        if i[-4:] == '.txt':
            list_grids.append(i)
    return list_grids
print(list_grids())

def loader(strGrid):    
    data = open(strGrid).read().split('\n')
    return data
print(loader(strGrid))

def checker(input_grid):
    # check if rows are bigger than 3
    if len(input_grid) >= 3:
        print("rows bigger than 3")
    else:
        print("there are not enough rows")
        return False

    # check if colums are bigger than 3
    if all(len(element) >= 3 for element in input_grid):
        print("cols bigger than 3")
    else:
        print("there are not enough cols")
        return False

    # Check if any element has a different length
    first_length = len(input_grid[0])
    if all(len(element) == first_length for element in input_grid):
        print("all columns equal")
    else:
        print("colums are not equal")
        return False
    return True , input_grid

print(checker(loader(strGrid)))



