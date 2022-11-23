#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/11/08 01:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
@Version :   1.0
@ContactSDU  :   jokel22@sutdent.sdu.dk
@ContactZHAW :   kellejo6@students.zhaw.ch
@License :   (C)Copyright 2022-2023, Jonas Keller
@Desc    :   None
'''

from model import Patch, Cell
from visualiser import Visualiser
from random import randint

class Grid():
    def __init__(self):
        self.row = 15
        self.col = 25
        self.list_patches = []
        self.list_cells = []
        self.init_pop = 2

    def start(self):
        '''
        This method initializes the patches and randomly sets the initial population
        of cells on the grid. 
        '''
        self.list_patches = [Patch(i, j) for i in range(self.row) for j in range(self.col)]  # creating patches with coordinates from index row and col
        # self.list_cells = [Cell(self.list_patches[randint(0, len(self.list_patches))]) for i in range(self.init_pop)]
        # print(len(self.list_patches))
        if self.init_pop > (self.row * self.col):
            raise ValueError("Try again and enter a initial population equal or lower than", (self.row * self.col))
            
        while len(self.list_cells) < self.init_pop:
            patch = randint(0, len(self.list_patches)-1)
            # patch = 4
            # print(patch)
            if self.list_patches[patch].has_cell() == False:
                self.list_cells.append(Cell(self.list_patches[patch]))


    def find_neighbors(self, curr_cell):
        '''
        This method searches the neighbors arround a cell in a 
        3x3 block.
        '''
        neighbors = []
        for i in self.list_patches:
            # all upper patches
            if i.row() == (curr_cell.patch().row() - 1) % self.row:
                if i.col() == curr_cell.patch().col():
                    neighbors.append(i)
                if i.col() == (curr_cell.patch().col() - 1) % self.col:
                    neighbors.append(i)
                if i.col() == (curr_cell.patch().col() + 1) % self.col:
                    neighbors.append(i)

            # middle left and right patch
            if i.row() == curr_cell.patch().row():
                if i.col() == (curr_cell.patch().col() - 1) % self.col:
                    neighbors.append(i)
                if i.col() == (curr_cell.patch().col() + 1) % self.col:
                    neighbors.append(i)

            # all the lower patches
            if i.row() == (curr_cell.patch().row() + 1) % self.row:
                if i.col() == curr_cell.patch().col():
                    neighbors.append(i)
                if i.col() == (curr_cell.patch().col() - 1) % self.col:
                    neighbors.append(i)
                if i.col() == (curr_cell.patch().col() + 1) % self.col:
                    neighbors.append(i)

        print(neighbors)
        for i in neighbors:
            print(i, i.row(), i.col())



    def evolution(self):
        for row in range(self.row):
            for col in range(self.col):
                pass



    def show(self):
        vis = Visualiser(self.list_patches, self.row, self.col, grid_lines=True) # create a visualiser for this data
        vis.wait_close() # wait until the window is closed by the user

class Simulation():
    def __init__(self):
        self.board = Grid()

    def start(self):
        self.board.start()
        for i in self.board.list_cells:
            self.board.find_neighbors(i)
        #self.board.find_neighbors(self.board.list_cells[0])
        self.board.show()



    # used to make a while loop over the given ticks

# test = Grid()
# test.start()
# test.show()

S = Simulation()
S.start()