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



class Simulation(Grid):
    def __init__(self):
        super().__init__()
        self.board = Grid()
        # self.board.start()
        self.max_ticks = 100
        self.tot_cells = 0
        self.tot_deaths = 0
        self.age_limit = 0
        self.div_limit = 0
        self.overcrowding = 0
        self.visualisation = True

    # def max_ticks(self, number):
    #     self.max_ticks = number
        
    def start(self):
        self.board.start()
        ticks = 0
        if self.visualisation == True:
            vis = Visualiser(self.board.list_patches, self.board.row, self.board.col, grid_lines= True)
        while ticks < self.max_ticks and len(self.board.list_cells) > 0:
        
            
            temp = []
            print('\n' + 20 * '-')
            print("Iteration", ticks)
            print(20 * '-', '\n')
            for i in self.board.list_cells:
                i.tick()
                print('age:', i.age(), 'div:', i.divisions(), 'cd:', i.last_division())
                # print(i.age())
                if i.divisions() == self.board.div_lim:
                    i.die()
                    self.board.list_cells.remove(i)
                    self.div_limit += 1
                    print("died from division limit")
                else:
                    if i.age() >= self.board.age_lim:
                        # print(self.board.list_cells)
                        i.die()
                        self.board.list_cells.remove(i)
                        self.age_limit += 1
                        # print(self.board.list_cells)
                    if i.age() < self.board.age_lim:
                        prob = round(random.random(), 2)

                        # print(prob)
                        if prob <= self.board.prob:
                            print("++++++++++++ good prob", prob, "<=", self.board.prob)
                            # print(prob)
                            temp_neighbor = self.board.find_neighbors(i)
                            neighbor_list = []
                            for j in temp_neighbor:
                                if not j.has_cell():
                                    neighbor_list.append(j)
                            
                            # overcrowding
                            if neighbor_list == []:
                                print("die of overcrowding")
                                age = [i.cell().age() for i in temp_neighbor]
                                max_age = max(age)
                                print("age:", age)
                                print("max_age:", max_age)
                                elder_list = [i for i in temp_neighbor if i.cell().age() == max_age]
                                print("list:", elder_list)
                                rand_elder = choice(elder_list)
                                rand_elder_cell = rand_elder.cell()
                                print("rand_elder:", rand_elder)
                                print("rand_elder_cell:", rand_elder_cell)
                                rand_elder_cell.die()
                                self.board.list_cells.remove(rand_elder_cell)
                                self.overcrowding += 1
                                # sleep(0.5)
                                # vis.update()

                            if neighbor_list != []:
                                print("no overcrowding")
                                if i.last_division() >= self.board.cooldown:
                                    print("cooldown good:", i.last_division())
                                    # print("Last division:", i.last_division())
                                    choice_neighbor = choice(neighbor_list)
                                    # print(choice_neighbor) # debugging
                                    temp.append(i.divide(choice_neighbor))
                                    self.tot_cells += 1
                                    print("new cell")
                                    # sleep(0.5)
                                    # vis.update()
                                else:
                                    print("cooldown not good:", i.last_division())
                                    continue
                            
                            else:
                                continue
                        else:
                            print("------------ bad prob:", prob, ">", self.board.prob)
                            overcrowd = self.board.find_neighbors(i)
                            # print(overcrowd)
                            print("Nr. of occupied N: ", len([i.has_cell() for i in overcrowd if i.has_cell() == True]))
                            for i in overcrowd:
                                print(i.has_cell())
                            if len([i.has_cell() for i in overcrowd if i.has_cell() == True]) == 8:
                                print("Nr. of occupied N: ", len([i.has_cell() for i in overcrowd]))
                                print("die of overcrowding")
                                age = [i.cell().age() for i in overcrowd]
                                max_age = max(age)
                                print("age:", age)
                                print("max_age:", max_age)
                                elder_list = [i for i in overcrowd if i.cell().age() == max_age]
                                print("list:", elder_list)
                                rand_elder = choice(elder_list)
                                rand_elder_cell = rand_elder.cell()
                                print("rand_elder:", rand_elder)
                                print("rand_elder_cell:", rand_elder_cell)
                                rand_elder_cell.die()
                                self.board.list_cells.remove(rand_elder_cell)
                                self.overcrowding += 1
                            else:
                                print("no overcrowding")
                                continue
            # sleep(2)
            if self.visualisation == True:
                vis.update()
            ticks += 1
            self.board.list_cells.extend(temp) # append new cells to the list
            # print(self.board.list_cells)
        self.tot_cells = self.tot_cells + self.board.init_pop
        self.tot_deaths = self.age_limit + self.div_limit + self.overcrowding

        # reset lists to avoid being filled when program is in while True loop
        # FIXME: not working properly
        self.reset_board()
        
        
        self.statistics()
        self.reset_stats()
        if self.visualisation == True:    
            vis.wait_close()
        # self.board.show()

    def reset_board(self):
        self.board.list_patches = []
        self.board.list_cells = []

    def reset_stats(self):
        self.tot_cells = 0
        self.tot_deaths = 0
        self.age_limit = 0
        self.div_limit = 0
        self.overcrowding = 0

    def statistics(self):
        print("Statistics")
        print(' - Duration (ticks) {:>7}'.format(self.max_ticks))
        print(' - Total cells {:>12}'.format(self.tot_cells))
        print(' - Total deaths {:>11}'.format(self.tot_deaths))
        print(' - Cause of death')
        print('   - Age limit {:>12}'.format(self.age_limit))
        print('   - Division limit {:>7}'.format(self.div_limit))
        print('   - Overcrowding {:>9}'.format(self.overcrowding))
        print('\n')






# test = Grid()
# test.start()
# test.show()

# S = Simulation()
# S.start()

if __name__ == "__main__":
    Grid()
    Simulation()