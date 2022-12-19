#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/11/08 01:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
'''

from model import BasePatch, ObstaclePatch, CellPatch, Cell
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

COLS = 0
ROWS = 0
GRID = []
strGrid = 'grid_1.txt'

def list_grids():
    """Return a list of all grid files in the current directory."""
    list_grids = []
    for i in os.listdir(dname):
        if i[-4:] == '.txt':
            list_grids.append(i)
    return list_grids
# print(list_grids())

def loader(strGrid):
    """Returns a list with separated strings loaded from a chosen file
    from list_grids."""
    data = open(strGrid).read().split('\n')
    return data
print(loader(strGrid))

def checker(input_grid, rows, cols):
    # check that all lines contain % or int and not other letters
    for element in input_grid:
        for character in element:
            if character != '%' and not isinstance(int(character), int):
                print("This line contains invalid characters: ", element)
                return False 


    # Check if any element has a different length
    first_length = len(input_grid[0])
    if all(len(element) == first_length for element in input_grid):
        print("all columns equal")
    else:
        print("colums are not equal")
        return False

    # check if rows are bigger than 3
    if len(input_grid) >= 3:
        print("rows bigger than 3")
        rows = len(input_grid)
    else:
        print("there are not enough rows")
        return False

    # check if colums are bigger than 3
    if all(len(element) >= 3 for element in input_grid):
        print("cols bigger than 3")
        cols = len(input_grid[0])
    else:
        print("there are not enough cols")
        return False
    return cols, rows, input_grid
# print(checker(loader(strGrid), ROWS, COLS))
COLS, ROWS, GRID = checker(loader(strGrid), ROWS, COLS)

def initialize_grid():
    """Return a list of BasePatches with the size of the input grid and
    returns a list of Obstacle- and CellPatches.
    The CellPatches have assigned the toxicity level to them."""
    global COLS, ROWS, GRID
    
    base_patches = [BasePatch(i, j) for i in range(ROWS) for j in range(COLS)]
    patches = []

    for row in GRID:
        for col in row:
            base_patch = base_patches[0]

            if col == '%':
                temp = ObstaclePatch(base_patch.row(), base_patch.col())
                patches.append(temp)

            elif int(col) >= 0 and int(col) <= 9:
                temp = CellPatch(base_patch.row(), base_patch.col(), int(col))
                patches.append(temp)
                
            base_patches.pop(0)

    return base_patches, patches

# test functions
base_patches, patches = initialize_grid()

# for i in patches:
#     print(i.row(), i.col())

vis = Visualiser(patches, ROWS, COLS, grid_lines=True)
vis.wait_close()