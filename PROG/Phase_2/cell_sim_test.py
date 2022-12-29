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

# TODO: make a loader DONE
# TODO: make a checker for the loaded grid validity DONE
# TODO: make it possible to list dir to chose a different grid to load DONE
# TODO: make function find neighbors of cells and implement the list of free neighbors
#       in the same function by popping the obstacles and have cells out.
# TODO: constaint of initialization population for row x col - obstacle patches

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

COLS = 0
ROWS = 0
GRID = []
cells = []
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
# print(loader(strGrid))

def checker(input_grid, rows, cols):
    # TODO: try to implement doctests (look it up)
    """Checks if the input is valid to initialize a grid
    
    >>> checker(input_grid, rows, cols)
    Traceback (most recent call last):
        ...
    raise ValueError("colums are not equal")
    ValueError: colums are not equal

    """
    # check that all lines contain % or int and not other letters
    for element in input_grid:
        for character in element:
            if character != '%' and not isinstance(int(character), int):
                raise ValueError("This line contains invalid characters: ", element)
                # print("This line contains invalid characters: ", element)
                # return False 
    # TODO: also check special characters! now just numbers letters and "%"

    # Check if any element has a different length
    first_length = len(input_grid[0])
    if all(len(element) == first_length for element in input_grid):
        print("all columns equal")
    else:
        raise ValueError("colums are not equal")
        # print("colums are not equal")
        # return False

    # check if rows are bigger than 3
    if len(input_grid) >= 3:
        print("rows bigger than 3")
        rows = len(input_grid)
    else:
        raise ValueError("therea re not enough rows")
        # print("there are not enough rows")
        # return False

    # check if colums are bigger than 3
    if all(len(element) >= 3 for element in input_grid):
        print("cols bigger than 3")
        cols = len(input_grid[0])
    else:
        raise ValueError("there are not enough cols")
        # print("there are not enough cols")
        # return False
    return cols, rows, input_grid
# print(checker(loader(strGrid), ROWS, COLS))


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

def init_pop():
    # patch = random.choice(patches)
    # print(type(patch))

    # cells.append(Cell(patches[30], 1))
    pass




class Simulation():
    def __init__(self):
        


        '''
        Sim.tick(Cell)
        #Deaths:
        if self.died_by_age and Cell.died_by_division:
            self._died_by_age +=1
            self._died_by_division +=1
            self._died_by_age_division += 1
            if self.died_by_poisening:
                self._died_by_poisening +=1
                self._died_by_age_poisening +=1
                self._died_by_division_poisening +=1
                self._died_by_age_division_poisening +=1
                self.die
            self.die

        elif self.died_by_age:
            self._died_by_age +=1
            if self.died_by_poisening:
                self._died_by_poisening +=1
                self._died_by_age_poisening +=1
                self.die
            self.die

        elif self.died_by_division:
            self._died_by_division +=1
            if self.died_by_poisening:
                self._died_by_poisening +=1
                self._died_by_division_poisening +=1
                self.die
            self.die

        elif self.died_by_poisening:
            self._died_by_poisening +=1
            self.die
        '''






# test functions
if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    COLS, ROWS, GRID = checker(loader(strGrid), ROWS, COLS)
    base_patches, patches = initialize_grid()

    vis = Visualiser(patches, ROWS, COLS, grid_lines=True)
    vis.wait_close()