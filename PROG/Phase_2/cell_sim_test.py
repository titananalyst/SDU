#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/11/08 01:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
'''

from __future__ import annotations # to use a class in type hints of its members
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
# TODO: count the number of CellPatches in initialize_grid
# TODO: import menu.py and run menu in cell_sim.py
# TODO:

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

COLS = 0
ROWS = 0
GRID = []
cells = []
strGrid = 'grid_1.txt'


class Grid():
    def __init__(self:Grid):
        # TODO: add the functions as methods, global variables as attributes
        self._cols = 0
        self._rows = 0
        self._grid = []
        self._cells = []
        self._list_grids = []
        self._strGrid = 'grid_1.txt'
        self._grid_data = None
        self._list_patches = []
        self._list_cell_patches = []
        
    def cols(self:Grid)->int:
        """Return the number of columns in the grid"""
        return self._cols

    def rows(self:Grid)->int:
        """Return the number of rows in the grid"""
        return self._rows

    def list_patches(self:Grid)->list:
        """Return the list of patches from the initialized grid"""
        return self._list_patches

    def list_grids(self):
        """Return a list of all grid files in the current directory."""
        for i in os.listdir(dname):
            if i[-4:] == '.txt':
                self._list_grids.append(i)

    def loader(self):
        """Returns a list with separated strings loaded from a chosen file
        from list_grids."""
        self._grid_data = open(self._strGrid).read().split('\n')


    def checker(self):
        # TODO: try to implement doctests (look it up)
        """Checks if the input is valid to initialize a grid
        
        >>> checker(input_grid, rows, cols)
        Traceback (most recent call last):
            ...
        raise ValueError("colums are not equal")
        ValueError: colums are not equal

        """
        # check that all lines contain % or int and not other letters
        for element in self._grid_data:
            for character in element:
                if character != '%' and not isinstance(int(character), int):
                    raise ValueError("This line contains invalid characters: ", element)
                    # print("This line contains invalid characters: ", element)
                    # return False 
        # TODO: also check special characters! now just numbers letters and "%"

        # Check if any element has a different length
        first_length = len(self._grid_data[0])
        if all(len(element) == first_length for element in self._grid_data):
            print("all columns equal")
        else:
            raise ValueError("colums are not equal")
            # print("colums are not equal")
            # return False

        # check if rows are bigger than 3
        if len(self._grid_data) >= 3:
            print("rows bigger than 3")
            self._rows = len(self._grid_data)
        else:
            raise ValueError("therea re not enough rows")
            # print("there are not enough rows")
            # return False

        # check if colums are bigger than 3
        if all(len(element) >= 3 for element in self._grid_data):
            print("cols bigger than 3")
            self._cols = len(self._grid_data[0])
        else:
            raise ValueError("there are not enough cols")
            # print("there are not enough cols")
            # return False


    def initialize_grid(self):
        """Return a list of BasePatches with the size of the input grid and
        returns a list of Obstacle- and CellPatches.
        The CellPatches have assigned the toxicity level to them."""
        
        base_patches = [BasePatch(i, j) for i in range(self._rows) for j in range(self._cols)]

        for row in self._grid_data:
            for col in row:
                base_patch = base_patches[0]

                if col == '%':
                    temp = ObstaclePatch(base_patch.row(), base_patch.col())
                    self._list_patches.append(temp)

                elif int(col) >= 0 and int(col) <= 9:
                    temp = CellPatch(base_patch.row(), base_patch.col(), int(col))
                    self._list_patches.append(temp)
                    self._list_cell_patches.append(temp)

                base_patches.pop(0)

    def init_pop(patches, cells):
        # TODO: initialize population random from CellPatches exlude ObstaclePatches
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
    # docstest
    # import doctest
    # doctest.testmod()

    # oop
    g = Grid()
    # print(g.list_grids())  # access to all grids in the directory
    g.loader()  # loads the grid of the desired grid.txt file
    g.checker()  # checks the grid input about errors
    g.initialize_grid() # initializes the grid

    vis = Visualiser(g.list_patches(), g.rows(), g.cols(), grid_lines=True)
    vis.wait_close()

