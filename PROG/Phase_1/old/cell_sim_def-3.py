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
import random
from random import randint, choice
from time import sleep

class Grid():
    def __init__(self):
        self.row = 15
        self.col = 25
        self.list_patches = []
        self.list_cells = []
        self.init_pop = 2
        self.prob = 0.2
        self.age_limit = 10
        

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
        
        # print(neighbors)
        # for i in neighbors:
        #     print(i, i.row(), i.col())

        return neighbors




    # def evolution(self):
    #     for i in self.list_cells:
    #         neighbors = find_neighbors(i)


    def show(self):
        vis = Visualiser(self.list_patches, self.row, self.col, grid_lines=True) # create a visualiser for this data
        vis.wait_close() # wait until the window is closed by the user



class Simulation():
    def __init__(self):
        self.board = Grid()

    def start(self):
        self.board.start()
        ticks = 0
        vis = Visualiser(self.board.list_patches, self.board.row, self.board.col, grid_lines= True)
        
        while ticks < 100:
          
            temp = []
            for i in self.board.list_cells:
                i.tick()
                print(i.age())
                if i.age() > self.board.age_limit:
                    print(self.board.list_cells)
                    i.die()
                    self.board.list_cells.remove(i)
                    print(self.board.list_cells)
                if i.age() <= self.board.age_limit:
                    prob = random.random()
                    # print(prob)
                    if prob <= self.board.prob:
                        # print(prob)
                        temp_neighbor = self.board.find_neighbors(i)
                        neighbor_list = []
                        for j in temp_neighbor:
                            if not j.has_cell():
                                neighbor_list.append(j)

                        if neighbor_list != []:
                            choice_neighbor = choice(neighbor_list)
                            # print(choice_neighbor) # debugging
                            temp.append(i.divide(choice_neighbor))
                            sleep(0.2)
                            vis.update()                                        
                        else:
                            continue
                vis.update()
            # else:
            #     continue
            #vis.update()
            ticks += 1
            self.board.list_cells.extend(temp) # append new cells to the list
            print(self.board.list_cells)
            vis.wait_close()
            # self.board.show()



    # used to make a while loop over the given ticks

# test = Grid()
# test.start()
# test.show()

S = Simulation()
S.start()