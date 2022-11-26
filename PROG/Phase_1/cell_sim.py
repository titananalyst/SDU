#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/11/08 01:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
'''

from model import Patch, Cell
from visualiser import Visualiser
import random
from random import randint, choice
from time import sleep

class Grid():
    '''
    Create a grid with patches and cells and 
    useful functions are defiend
    '''
    def __init__(self):
        self.row = 15
        self.col = 20
        self.list_patches = []
        self.list_cells = []
        self.init_pop = 2
        self.prob = 0.2
        self.age_lim = 10
        self.div_lim = 2
        self.cooldown = 2


    def start(self):
        '''
        This method initializes the patches with a size
        (row*col) and randomly sets the initial population
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
        3x3 block. Returns a list of objects with the neighbors
        patches.
        
        Keyword arguments:
        curr_cell -- living cell which is attached to a patch
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


class Simulation(Grid):
    '''
    Class for running the simulation, the Grid class is 
    enharitanced and methods to run the simulation are implemented.
    '''
    def __init__(self):
        super().__init__()
        self.board = Grid()
        self.max_ticks = 100
        self.tot_cells = 0
        self.tot_deaths = 0
        self.age_limit = 0
        self.div_limit = 0
        self.overcrowding = 0
        self.visualisation = True

        
    def start(self):
        '''
        This method starts the simulation, it also starts the visualisation,
        it makes the whole simulation iterate and execute all statements
        for a successful simulation.
        Further explanation is written with one-line, or multi-line docstrings. 
        '''
        print('\nSimulation is running ...')
        self.board.start()
        ticks = 0
        if self.visualisation == True:
            vis = Visualiser(self.board.list_patches, self.board.row, self.board.col, grid_lines= True)
        while ticks < self.max_ticks and len(self.board.list_cells) > 0:
        
            temp = []
            # print('\n' + 20 * '-')
            # print("Iteration", ticks)
            # print(20 * '-', '\n')
            
            '''
            start iteration over all living cells, at start 
            every living cell ages and the timestep for 
            the last division increments by 1            
            '''
            for i in self.board.list_cells:
                i.tick()
                # print('age:', i.age(), 'div:', i.divisions(), 'cd:', i.last_division())
                # print(i.age())

                '''
                die of division limit reached, if the cell
                reaches the max amount of division it dies
                and gets removed from the list of living cells
                '''
                if i.divisions() == self.board.div_lim:
                    i.die()
                    self.board.list_cells.remove(i)
                    self.div_limit += 1
                    # print("died from division limit")
                    # vis.update()
                else:
                    '''
                    die of age limit reached, if a cell gets as old
                    as the age limit it dies and gets removed from 
                    the list of living cells
                    '''
                    if i.age() >= self.board.age_lim:
                        # print(self.board.list_cells)
                        i.die()
                        self.board.list_cells.remove(i)
                        self.age_limit += 1
                        # print(self.board.list_cells)
                        # vis.update()
                    '''
                    If age limit is not reached go further and chose 
                    a random probability
                    '''
                    if i.age() < self.board.age_lim:
                        prob = round(random.random(), 2)
                        # print(prob)
                        '''
                        Go further if the random probability is within
                        the division probability.
                        Check surounding patches if they are not! occupied by
                        a living cell append them to a new list.
                        '''
                        if prob <= self.board.prob:
                            # print("++++++++++++ good prob", prob, "<=", self.board.prob)
                            # print(prob)
                            temp_neighbor = self.board.find_neighbors(i)  # find surounding patches
                            neighbor_list = []
                            for j in temp_neighbor:
                                if not j.has_cell():
                                    neighbor_list.append(j)
                            '''
                            overcrowding, check if all neighbors are occupied
                            by living cells, for this the list neighbor_list has to be empty,
                            that means that every patch is occupied and no patch is free. 
                            If yes, a random one of the eldest cells will dies.

                            To do this the list with the surounding neighbors is taken
                            and the max age of the list is evaluated. Then a list with
                            the eldest cells from the neighbors is created and a random
                            choice of the eldest cells is chosen and then dies to solve
                            the overcrowding problem.
                            '''
                            if neighbor_list == []:
                                # print("die of overcrowding")
                                age = [i.cell().age() for i in temp_neighbor]
                                max_age = max(age)
                                # print("age:", age)
                                # print("max_age:", max_age)
                                elder_list = [i for i in temp_neighbor if i.cell().age() == max_age]
                                # print("list:", elder_list)
                                rand_elder = choice(elder_list)
                                rand_elder_cell = rand_elder.cell()
                                # print("rand_elder:", rand_elder)
                                # print("rand_elder_cell:", rand_elder_cell)
                                rand_elder_cell.die()
                                self.board.list_cells.remove(rand_elder_cell)
                                self.overcrowding += 1
                                # sleep(0.5)
                                # vis.update()
                            '''
                            Division, if there are free patches surounding the cell
                            perform a random divison to a free patch, then append
                            it to the list of living cells
                            '''
                            if neighbor_list != []:
                                # print("no overcrowding")
                                if i.last_division() >= self.board.cooldown:
                                    # print("cooldown good:", i.last_division())
                                    # print("Last division:", i.last_division())
                                    choice_neighbor = choice(neighbor_list)
                                    # print(choice_neighbor) # debugging
                                    temp.append(i.divide(choice_neighbor))
                                    self.tot_cells += 1
                                    # print("new cell")
                                    # sleep(0.5)
                                    # vis.update()
                                else:
                                    # print("cooldown not good:", i.last_division())
                                    continue
                            
                            else:
                                continue
                        else:
                            '''
                            Overcrowing, if the probability for division is not within the
                            range of the division probability.
                            Make a overcrowding test, to cover all living cells with a
                            overcrowding test at every iteration.
                            Works the same way as the inner overcroding test. To evaluate
                            to perform the test, the list of neighbors with the patches must
                            contain living cells on every patch.
                            '''
                            # print("------------ bad prob:", prob, ">", self.board.prob)
                            overcrowd = self.board.find_neighbors(i)
                            # print("Nr. of occupied N: ", len([i.has_cell() for i in overcrowd if i.has_cell() == True]))
                            # for i in overcrowd:
                            #     print(i.has_cell())
                            if len([i.has_cell() for i in overcrowd if i.has_cell() == True]) == 8:
                                # print("Nr. of occupied N: ", len([i.has_cell() for i in overcrowd]))
                                # print("die of overcrowding")
                                age = [i.cell().age() for i in overcrowd]
                                max_age = max(age)
                                # print("age:", age)
                                # print("max_age:", max_age)
                                elder_list = [i for i in overcrowd if i.cell().age() == max_age]
                                # print("list:", elder_list)
                                rand_elder = choice(elder_list)
                                rand_elder_cell = rand_elder.cell()
                                # print("rand_elder:", rand_elder)
                                # print("rand_elder_cell:", rand_elder_cell)
                                rand_elder_cell.die()
                                self.board.list_cells.remove(rand_elder_cell)
                                self.overcrowding += 1
                                # vis.update()
                            else:
                                # print("no overcrowding")
                                continue
            '''
            If the visualisation is enabeld it will turn on here and the 
            iteration tick will increment by one.
            The board of living cells gets updated.
            '''
            #sleep(0.4)
            if self.visualisation == True:
                vis.update()
            ticks += 1
            self.board.list_cells.extend(temp) # append new cells to the list
            # print(self.board.list_cells)
        '''
        Calculate total created cells and total died cells,
        then reset the board, print the statistics and afterwards
        also reset the statistics for the next simulation run.
        The program end until the visualisation window is closed.
        '''
        self.tot_cells = self.tot_cells + self.board.init_pop
        self.tot_deaths = self.age_limit + self.div_limit + self.overcrowding

        self.reset_board()
        
        self.statistics()
        self.reset_stats()
        if self.visualisation == True: 
            print("Simulation finished, please close the window in other to do call the menu.")
            vis.wait_close()

    def reset_board(self):
        '''This method resets the list for the patches and cells'''
        self.board.list_patches = []
        self.board.list_cells = []

    def reset_stats(self):
        '''This method resets the statistics for the next simulation run'''
        self.tot_cells = 0
        self.tot_deaths = 0
        self.age_limit = 0
        self.div_limit = 0
        self.overcrowding = 0

    def statistics(self):
        '''This method prints the statistics for a simulation'''
        print("Statistics")
        print(' - Duration (ticks) {:>7}'.format(self.max_ticks))
        print(' - Total cells {:>12}'.format(self.tot_cells))
        print(' - Total deaths {:>11}'.format(self.tot_deaths))
        print(' - Cause of death')
        print('   - Age limit {:>12}'.format(self.age_limit))
        print('   - Division limit {:>7}'.format(self.div_limit))
        print('   - Overcrowding {:>9}'.format(self.overcrowding))
        print('\n')
        print('Statistics printed.')

# S = Simulation()
# S.start()

if __name__ == "__main__":
    Grid()
    Simulation()