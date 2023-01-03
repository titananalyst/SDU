#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/12/01 12:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
'''

from __future__ import annotations # to use a class in type hints of its members
from model import BasePatch, ObstaclePatch, CellPatch, Cell
from visualiser import Visualiser
import random
import os
import re
import matplotlib.pyplot as plt


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
                    raise ValueError("This line contains invalid characters: {}, {}".format(element, character))

        # Check if any element has a different length
        first_length = len(self._grid_data[0])
        if all(len(element) == first_length for element in self._grid_data):
            pass
        else:
            raise ValueError("Colums or rows are not equal! Insert valid m x n grid.")

        # check if rows are bigger than 3
        if len(self._grid_data) >= 3:
            self._rows = len(self._grid_data)
        else:
            raise ValueError("There are not enough rows! Insert valid m x n grid.")

        # check if colums are bigger than 3
        if all(len(element) >= 3 for element in self._grid_data):
            self._cols = len(self._grid_data[0])
        else:
            raise ValueError("There are not enough cols! Insert valid m x n grid.")

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
            raise ValueError("Try again and enter a initial population equal or lower than {}".format(self._intCellPatch))

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

    def set_parent(self, curr_cell, neighbours):
        if neighbours != []:
            new_patch = random.choice(neighbours) 

            if curr_cell.resistance() == 0:
                new_cell = Cell(new_patch, curr_cell.resistance() + int(random.randint(0, 2)))

            elif curr_cell.resistance() == 1:
                new_cell = Cell(new_patch, curr_cell.resistance() + int(random.randint(-1, 2)))
    
            elif curr_cell.resistance() == 8:
                new_cell = Cell(new_patch, curr_cell.resistance() + int(random.randint(-2, 1)))

            elif curr_cell.resistance() == 9:
                new_cell = Cell(new_patch, curr_cell.resistance() + int(random.randint(-2, 0)))
            
            else:
                new_cell = Cell(new_patch, curr_cell.resistance() + int(random.randint(-2, 2))) 

            curr_cell._last_division = 0  # reset the counter from the last division
            curr_cell._divisions = curr_cell._divisions + 1

            if isinstance(new_cell, Cell):
                new_cell._parent = curr_cell
                new_cell._generation = new_cell.parent().generation() + 1

                return new_cell

    def reset_data(self):
        self._list_patches = []
        self._grid = []
        self._cells = []
        self._grid_data = None
        self._list_patches = []
        self._list_cell_patches = []
        self._intCellPatch = 0


class Simulation(Grid):
    def __init__(self:Simulation):
        super().__init__()
        self.grid = Grid()
        self._max_ticks = 100
        self._visualisation = True
        # statistics:
        self._dictGen = {}
        self._dictResults = {
            "Generation": [],
            "intIndividuals": [],
            "min_res": [],
            "max_res": [],
            "avg_res": []
        }
        self._died_by_age = 0
        self._died_by_division = 0
        self._died_by_poisoning = 0 
        self._died_by_age_division = 0
        self._tot_cells = 0
        self._tot_died = 0
        self._tot_died_by_age = 0
        self._tot_died_by_division = 0

    def start(self:Simulation):
        print('\nSimulation is running ...')
        self.reset_graph()  # reset data structures for the graphs
        self.reset_stats()  # reset structures for the statistics
        ticks = 0
        if self._visualisation == True:
            vis = Visualiser(self.grid._list_patches, self.grid.rows(), self.grid.cols(), grid_lines= True)
        self._dictGen[0] = []
        for i in self.grid._cells:
            self._dictGen[0].append(i.resistance())

        while ticks < self._max_ticks and len(self.grid._cells) > 0:
            random.shuffle(self.grid._cells)
            temp = []
            for cell in self.grid._cells:

                if cell.divide(cell.patch()):
                    new_cell = self.grid.set_parent(cell, self.grid.find_neighbours(cell))
                    if isinstance(new_cell, Cell):
                        temp.append(new_cell)
                        self._tot_cells += 1
                        if new_cell.generation() in self._dictGen:
                            self._dictGen[new_cell.generation()].append(new_cell.resistance())
                        else:
                            self._dictGen[new_cell.generation()] = []
                            self._dictGen[new_cell.generation()].append(new_cell.resistance())

                cell.tick()
                if cell.died_by_age() and cell.died_by_division():
                    cell.patch().remove_cell()
                    self.grid._cells.remove(cell)
                    self._died_by_age_division += 1
                elif cell.died_by_age():
                    self.grid._cells.remove(cell)
                    self._died_by_age += 1
                elif cell.died_by_division():
                    self.grid._cells.remove(cell)
                    self._died_by_division += 1
                elif not cell.is_alive():  # remove poisoning dead cells
                    self.grid._cells.remove(cell)
                    self._died_by_poisoning += 1
            
            if self._visualisation == True:
                vis.update()
                
            ticks += 1
            self.grid._cells.extend(temp)

        self._tot_cells = self._tot_cells + self.grid._init_pop
        self._tot_died = self._died_by_age + self._died_by_age_division + self._died_by_division + self._died_by_poisoning
        self._tot_died_by_age = self._died_by_age_division + self._died_by_age
        self._tot_died_by_division = self._died_by_age_division + self._died_by_division
        self.grid.reset_data()

        if self._visualisation == True:
            print("Simulation finished, please close the window in order to do call the menu.")
            vis.wait_close()
        else:
            print("Simulation finished, please continue with further processing")

    def statistics(self):
        if self._dictGen != {}:
            '''This method prints the statistics for a simulation'''
            print("Statistics")
            print(' - Duration (ticks) {:>12}'.format(self._max_ticks))
            print(' - Total cells {:>17}'.format(self._tot_cells))
            print(' - Total deaths {:>16}'.format(self._tot_died))
            print(' - Cause of death')
            print('   - Age & Division limit {:>6}'.format(self._died_by_age_division))
            print('   - Age limit {:>17}'.format(self._tot_died_by_age))
            print('   - Division limit {:>12}'.format(self._tot_died_by_division))
            print('   - Poisoning {:>17}'.format(self._died_by_poisoning))
            print('\n')
            print('Statistics printed.')
        else:
            raise ValueError("\nThere is no data, run a simulation first.")

    def reset_stats(self):
        self._died_by_age = 0
        self._died_by_division = 0
        self._died_by_poisoning = 0 
        self._died_by_age_division = 0
        self._tot_cells = 0
        self._tot_died = 0
        self._tot_died_by_age = 0
        self._tot_died_by_division = 0

    def reset_graph(self):
        self._dictGen = {}
        self._dictResults = {
            "Generation": [],
            "intIndividuals": [],
            "min_res": [],
            "max_res": [],
            "avg_res": []
        }


class Menu(Simulation):
    def __init__(self):
        super().__init__()
        self.sim = Simulation()
        self.sim.grid.list_grids()
        self._vis_status = True
        self._sim_status = "Default"
        self._menu_choice = 1
    
    def grid_menu(self):
        self.sim.grid.reset_data()
        print("\nThe following grids are in your folder, which one do you want to use?")
        print("Type in the number of the grid:\n")
        for i in range(len(self.sim.grid._list_grids)):
            print(i+1, self.sim.grid._list_grids[i])

        length = len(self.sim.grid._list_grids)
        if length != 0:
            choice = input('\nType in a your number between 1 and {} : '.format(length))
            if choice.isdigit():
                choice = int(choice)
            else:
                raise ValueError("Please just use integers to interact with the menue.")

            if choice > 0 and choice <= length:
                self.sim.grid._strGrid = self.sim.grid._list_grids[choice - 1]
                print("Choosen:", self.sim.grid._strGrid)
                self.sim.grid.loader()
                self.sim.grid.checker()
                self.sim.grid.initialize_grid()
            else:
                raise ValueError("\nPlease enter a number between 1 and {}. You chose {}.".format(length, choice))
        else: 
            raise IndexError('\nThere are no grids available in the folder.')

        pop_input = input('\nEnter number of init population (1-{}): '.format(self.sim.grid._intCellPatch))
        if pop_input.isdigit():
            pop_input = int(pop_input)
        else:
            raise ValueError("Please just use integers to interact with the menue.")

        if pop_input > 0 and pop_input <= self.sim.grid._intCellPatch:
            self.sim.grid._init_pop = pop_input
        else:
            raise ValueError("Please enter a number between 1 and {}. You chose {}.".format(self.sim.grid._intCellPatch, pop_input))

        ticks_input = input('\nEnter tick duration for simulation (greater than 0): ')
        if ticks_input.isdigit():
            ticks_input = int(ticks_input)
        else:
            raise ValueError("Please just use integers to interact with the menue.")

        if ticks_input > 0:
            self.sim._max_ticks = ticks_input
        else:
            raise ValueError("\nPlease enter a duration greater than 0. You chose {}.".format(ticks_input))
        self.sim.grid.reset_data()

    def graph_data(self):
        for i in self.sim._dictGen:
            gen = i
            intIndividuals = len(self.sim._dictGen[i])
            min_res = min(self.sim._dictGen[i])
            max_res = max(self.sim._dictGen[i])
            avg_res = (round(sum(self.sim._dictGen[i])/len(self.sim._dictGen[i]), 2))
            
            self.sim._dictResults['Generation'].append(gen)
            self.sim._dictResults['intIndividuals'].append(intIndividuals)
            self.sim._dictResults['min_res'].append(min_res)
            self.sim._dictResults['max_res'].append(max_res)
            self.sim._dictResults['avg_res'].append(avg_res)         

    def figure(self):
        if self.sim._dictGen != {}:
            gen = self.sim._dictResults['Generation']
            individuals = self.sim._dictResults['intIndividuals']
            min_res =self.sim._dictResults['min_res']
            max_res =self.sim._dictResults['max_res']
            avg_res = self.sim._dictResults['avg_res']

            fig, (ax0, ax1,) = plt.subplots(2, 1)
            fig.suptitle("Cell Simulation Results")
            plt.subplots_adjust(hspace = 0.6)

            ax0.plot(gen, individuals)
            ax0.set_xlabel('Generation')
            ax0.set_ylabel('Individuals')
            ax0.set_title("Individuals vs. Generations")

            ax1.plot(gen, max_res, "tab:orange", label = "Max")
            ax1.plot(gen, avg_res, "-g", label = "Avg")
            ax1.plot(gen, min_res, "-b", label= "Min")
            ax1.set_xlabel("Generation")
            ax1.set_ylabel("Resistance level")
            ax1.set_title("Resistance level vs. Generations")
            
            ax1.legend(bbox_to_anchor=(1.14, 0.5), loc="center", borderaxespad = 0)
            fig.tight_layout()
            fig.show()
        else:
            raise ValueError("\nThere is no data, run a simulation first.")

            


    def print_menu(self):
        while True:
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
            print("5: Visualisation ON/OFF")
            print("6. Graphs & Statistics")
            print("7: Quit")
            print()
            try:
                self._menu_choice = int(input("Type in a number (1-7): "))
                if self._menu_choice == 1:
                    if self.sim._visualisation == False:
                        self._vis_status = "Disabled"
                    else: 
                        self._vis_status = "Enabled"
                    '''
                    this print out the display confuration menu, 
                    with the parametres there has been chosen.
                    '''
                    print("\n" + 34 * "-")
                    print("{:<22} {}".format("Parameter", self._sim_status))
                    print(34 * "-")
                    print("{:<22} {}".format("Active grid", self.sim.grid._strGrid))
                    print("{:<22} {}".format("Initial population", self.sim.grid._init_pop))
                    print("{:<22} {}".format("Age limit", 10))
                    print("{:<22} {}".format("Division limit", 2))
                    print("{:<22} {}".format("Division probability", 0.6))
                    print("{:<22} {}".format("Division cooldown", 2))
                    print("{:<22} {}".format("Time limit", self.sim._max_ticks))
                    print("{:<22} {}\n".format("Visualisation", self._vis_status))
                    # self.print_menu()

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
                    try:
                        self._sim_status = "Setup"
                        self.grid_menu()
                        print("Changed settings.")
                    except ValueError as e:
                        print(e)


                elif self._menu_choice == 3:
                    self.sim.grid.loader()
                    self.sim.grid.checker()
                    self.sim.grid.initialize_grid()
                    self.sim.grid.init_pop()
                    self.sim.start()
                    self.graph_data()
                    # self.print_menu()

                elif self._menu_choice == 4:
                    self._sim_status = "Default"
                    self.sim.grid._init_pop = 2
                    self.sim._max_ticks = 100
                    self.sim._visualisation = True
                    print("Settings reset to default settings.\n")
                    # self.print_menu()

                elif self._menu_choice == 5:
                    try:
                        vis_input = int(input("Enter 1 or 0 [ENABLE | DISABLE] the visualisation: "))
                        if vis_input == 0:
                            self.sim._visualisation = False
                        elif vis_input == 1:
                            self.sim._visualisation = True
                        else:
                            raise ValueError("\nPlease choose between 1 and 0 [ENABLE | DISABLE]. You chose {}.".format(vis_input))
                    except ValueError:
                        print("\nPlease choose between 1 and 0 [ENABLE | DISABLE].")

                elif self._menu_choice == 6:
                    try:
                        self.figure()
                        self.sim.statistics()
                    except ValueError as e:
                        print(e)

                elif self._menu_choice == 7:
                    quit()
                
                else:
                    raise ValueError("\nEnter a valid menu choice between 1 and 7!")
            except ValueError:
                print("\nEnter a valid menu choice between 1 and 7!")




if __name__ == "__main__":
    # docstest
    # import doctest
    # doctest.testmod()

    m = Menu()
    m.print_menu()
    

