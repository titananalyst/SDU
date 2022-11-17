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

# menu achieved through while loop menu
# report could be written with overleaf (latex)

def create_grid(row, col):
    grid = [[None] * row for i in range(col)]
    print(grid)
    #for i in range(row):
        #for j in range(col):
    grid = [Patch(i, j) for i in range(row) for j in range(col)]
    return grid

#print(create_grid(3,3))

grid = [[0, 1, 0], # some 2D binary data
[0, 0, 1],
[1, 1, 1]]


from model import Patch, Cell
from visualiser import Visualiser
row = 15
col = 15
initial_population = 2

# the process behind creating patches and applying them to the cells 
# so we have like a boolean true value for living cells for the grid
# the patches are unsorted yet
list_patches = [Patch(i, j) for i in range(row) for j in range(col)]  # creating patches with coordinates from index row and col
#list_cells = [Cell(list_patches[i]) for i in range(len(list_patches)) if i % 2 == 0]  # creating cells attached with the patches
list_cells = [Cell(list_patches[randint(0, len(list_patches))]) for i in range(initial_population)]
print([list_cells[i].patch() for i in range(len(list_cells))])  # printing the patches attached to the cells
for i in range(len(list_cells)):
    print(list_cells[i].patch().row(), ",", list_cells[i].patch().col())

#print(list_cells[i].patch().row() for i in range(len(list_cells)))



vis = Visualiser(list_patches, row, col, grid_lines=True) # create a visualiser for this data
vis.wait_close() # wait until the window is closed by the user