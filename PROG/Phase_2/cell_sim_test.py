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
import re


# TODO: import menu.py and run menu in cell_sim.py

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


class Grid():
    def __init__(self:Grid):
        self._cols = 0
        self._rows = 0
        self._grid = []
        self._cells = []
        self._list_grids = []
        self._strGrid = 'grid_1.txt'
        self._grid_data = None
        self._list_patches = []
        self._list_cell_patches = []
        self._init_pop = 2
        self._intCellPatch = 0

        
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
        # check that all lines contain % or int and not other letters or characters
        # done with regex (regular expressions)
        for element in self._grid_data:
            for character in element:
                pattern = r'^[0-9%]*$'
                if not re.match(pattern, character):
                    raise ValueError("This line contains invalid characters: ", element, character)

        # Check if any element has a different length
        first_length = len(self._grid_data[0])
        if all(len(element) == first_length for element in self._grid_data):
            print("all columns equal")
        else:
            raise ValueError("colums are not equal")

        # check if rows are bigger than 3
        if len(self._grid_data) >= 3:
            print("rows bigger than 3")
            self._rows = len(self._grid_data)
        else:
            raise ValueError("therea re not enough rows")

        # check if colums are bigger than 3
        if all(len(element) >= 3 for element in self._grid_data):
            print("cols bigger than 3")
            self._cols = len(self._grid_data[0])
        else:
            raise ValueError("there are not enough cols")

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
                    self._intCellPatch += 1

                base_patches.pop(0)

    def init_pop(self):
        """Creates new instances of Cells on a CellPatch until the maximum number
        of initial population."""
        temp = [i for i in self._list_patches if isinstance(i, CellPatch)]

        if self._init_pop > self._intCellPatch:
            raise ValueError("Try again and enter a initial population equal or lower than", self._intCellPatch)

        while len(self._cells) < self._init_pop:
            patch = random.choice(temp)  # does not prevent of choosing the same patch twice
            self._cells.append(Cell(patch, 0))  # initialize resistance 0
            temp.remove(patch)  # remove choosen patch to avoid taking the same twice

    def find_neighbours(self, curr_cell)->list: 
        neighbors = []

        for i in range((curr_cell.patch().row()-1) , (curr_cell.patch().row() +2)):
            for j in range((curr_cell.patch().col()-1) , (curr_cell.patch().col() +2)):
                neighbors.extend([patch for patch in self._list_patches if patch.row() == (i % self.rows()) and patch.col() == (j % self.cols())])

                for k in neighbors:
                    if isinstance(k, CellPatch) and k.has_cell() == True:
                        neighbors.remove(k)
                    elif isinstance(k, ObstaclePatch):
                        neighbors.remove(k)
                    else:
                        continue
        return neighbors


class Simulation(Grid):
    def __init__(self:Simulation):
        super().__init__()
        self._max_ticks = 100
        self._visualisation = True
        # statistics:
        self._died_by_age = 0
        self._died_by_division = 0
        self._died_by_poisoning = 0 
        self._died_by_age_division_poisoning = 0
        self._died_by_age_division = 0
        self._died_by_age_poisoning = 0
        self._died_by_division_poisoning = 0 

    def start(self:Simulation):
        ticks = 0
        if self._visualisation == True:
            vis = Visualiser(g._list_patches, g.rows(), g.cols(), grid_lines= True)

        while ticks < self._max_ticks and len(g._cells) > 0:
            random.shuffle(g._cells)
            temp = []
            for cell in g._cells:

                new_cell = cell.divide(cell.patch(), g.find_neighbours(cell))
                temp.append(new_cell)
                #temp.append(s.append_neighbors(g.find_neighbours(cell), cell))
                temp = [i for i in temp if i is not None]
                temp = [i for i in temp if i is not False]
                
                cell.tick()
                if cell.died_by_age() and cell.died_by_division():
                    cell.patch().remove_cell()
                    g._cells.remove(cell)
                    self._died_by_age_division += 1
                elif cell.died_by_age():
                    g._cells.remove(cell)
                    self._died_by_age += 1
                elif cell.died_by_division():
                    g._cells.remove(cell)
                    self._died_by_division += 1
                # elif cell.died_by_poisoning():
                #     g._cells.remove(cell)
                #     self._died_by_poisoning += 1
                elif not cell.is_alive():  # remove poisoing dead cells
                    g._cells.remove(cell)
                    self._died_by_poisoning += 1

            
            if self._visualisation == True:
                vis.update()
            ticks += 1
            g._cells.extend(temp)

        print(self._died_by_age_division)
        print(self._died_by_age)
        print(self._died_by_division)
        print(self._died_by_poisoning)
        vis.wait_close()


class Menu(Simulation):
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.sim = Simulation()
        self._vis_status = True
        self._sim_status = "Default"
        self._menu_choice = 1

    def grid_menu(self):
        
        self.grid.list_grids()
        print("The following grids are in your folder, which one do you want to use?")
        print("Type in the number of the grid:")
        for i in range(len(self.grid._list_grids)):
            print(i+1, self.grid._list_grids[i])

        length = len(self.grid._list_grids)
        if length != 0:
            choice = int(input('Type in a your number between 0 and {} : '.format(length)))
            self.grid._strGrid = self.grid._list_grids[choice - 1]
            print("Choosen:", self.grid._strGrid)

        else: 
            raise IndexError('There are no grids available in the folder.')

        

    def print_menu(self):
        '''
        this print out the display of the menu, 
        where all the print-statements exicute one line at a time. 
        '''
        print("\nMenu:")
        print(34 * "-")
        print("1: Display configuration")
        print("2: Setup")
        print("3: Run simulation")
        print("4: Reset to default setup")
        print("5: Quit")
        print()
        self._menu_choice = int(input("Type in a number (1-5): "))

        if self._menu_choice == 1:
            if self.sim._visualisation == False:
                self._vis_status = "Disabled"
            '''
            this print out the display confuration menu, 
            with the parametres there has been chosen.
            '''
            print("\n" + 34 * "-")
            print("{:<22} {}".format("Parameter", self._sim_status))
            print(34 * "-")
            print("{:<22} {}".format("Active grid", self.grid._strGrid))
            print("{:<22} {}".format("Initial population", self.sim._init_pop))
            print("{:<22} {}".format("Age limit", 10))
            print("{:<22} {}".format("Division limit", 7))
            print("{:<22} {}".format("Division probability", 0.6))
            print("{:<22} {}".format("Division cooldown", 1))
            print("{:<22} {}".format("Time limit", self.sim._max_ticks))
            print("{:<22} {}\n".format("Visualisation", self._vis_status))
            self.print_menu()

        elif self._menu_choice == 2:
            '''
            this is a go through of the setting in Qick menu. 
            exaple 1:
            age_input is set to be an integere with the code int(). 
            Inside int there is a code input() witch make the user avalible to make its own choice,
            but that is restricted by the int().
            That is why there is a messege inside the input() that the user will get. 
            if the user select correctly the first if statement will be exicuted. 
            inside that if there i a logical statement that checks if the user has made an valid choice.
            if not the else statement will print, the "Default" are enabled and then return the user to the menue.
            '''

            self.simulation = "Setup"
            self.grid_menu()
            


            self.print_menu()

        

if __name__ == "__main__":
    # docstest
    # import doctest
    # doctest.testmod()

    m = Menu()
    m.print_menu()

    # oop
    # g = Grid()
    # # print(g.list_grids())  # access to all grids in the directory
    # g.loader()  # loads the grid of the desired grid.txt file
    # print(g._list_grids) # access to all grids in)
    # g.checker()  # checks the grid input about errors
    # g.initialize_grid() # initializes the grid
    # g.init_pop()  # initializes living cells on the grid

    # s = Simulation()
    # s.start() # starts the simulation

    # vis = Visualiser(g.list_patches(), g.rows(), g.cols(), grid_lines=True)
    # vis.wait_close()

