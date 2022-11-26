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

from cell_sim import Grid, Simulation
from time import sleep

def print_menu():
    print("\nMenu:")
    print(31 * "-")
    print("1: Display configuration")
    print("2: Quick setup")
    print("3: Advanced setup")
    print("4: Run simulation")
    print("5: Reset to default setup")
    print("6: Quit")
    print()


menu_choice = 0
print_menu()
grid = Grid()
sim = Simulation()
sim_status = "Default"
while True:
    try:
        menu_choice = int(input("Type in a number (1-6): "))
        vis_status = "Enabled"
        if menu_choice == 1:
            if sim.visualisation == False:
                vis_status = "Disabled"
            print("\n" + 31 * "-")
            print("{:<22} {}".format("Parameter", sim_status))
            print(31 * "-")
            print("{:<22} {}".format("Grid rows", sim.board.row))
            print("{:<22} {}".format("Grid columns", sim.board.col))
            print("{:<22} {}".format("Initial population", sim.board.init_pop))
            print("{:<22} {}".format("Age limit", sim.board.age_lim))
            print("{:<22} {}".format("Division limit", sim.board.div_lim))
            print("{:<22} {}".format("Division probability", sim.board.prob))
            print("{:<22} {}".format("Division cooldown", sim.board.cooldown))
            print("{:<22} {}".format("Time limit", sim.max_ticks))
            print("{:<22} {}\n".format("Visualisation", vis_status))
            print_menu()


        elif menu_choice == 2:
            sim_status = "Quick"
            row_input = int(input("\n" + "Enter the number of rows (min 3): "))
            if not row_input < 3:
                sim.board.row = row_input
            else:
                print("\nPlease enter a integer above 2")
                print("Try again!\n")
                continue

            col_input = int(input("Enter the number of columns (min 3): "))
            if not col_input < 3:
                sim.board.col = col_input
            else:
                print("\nPlease enter a integer above 2")
                print("Try again!\n")
                continue

            pop_input = int(input("Enter the number of initial population between 1 and " + str(sim.board.row*sim.board.col) + "): "))
            if not pop_input < 1 and not pop_input > (sim.board.row*sim.board.col):
                sim.board.init_pop = pop_input
            else:
                print("\nPlease enter a integer above between 1 and " + str(sim.board.row*sim.board.col))
                print("Try again!\n")
                continue
            
            sim.board.age_lim = 10
            sim.board.div_lim = 2
            sim.board.prob = 0.2
            sim.board.cooldown = 2
            sim.max_ticks = 100
            sim.visualisation = True
            print("Changed to quick setup.")
            print_menu()


        
        elif menu_choice == 3:
            sim_status = "Advanced"
            row_input = int(input("\n" + "Enter the number of rows (min 3): "))
            if not row_input < 3:
                sim.board.row = row_input
            else:
                print("\nPlease enter a integer above 2")
                print("Try again!\n")
                continue

            col_input = int(input("Enter the number of columns (min 3): "))
            if not col_input < 3:
                sim.board.col = col_input
            else:
                print("\nPlease enter a integer above 2")
                print("Try again!\n")
                continue

            pop_input = int(input("Enter the number of initial population between 1 and " + str(sim.board.row*sim.board.col) + "): "))
            if not pop_input < 1 and not pop_input > (sim.board.row*sim.board.col):
                sim.board.init_pop = pop_input
            else:
                print("\nPlease enter a integer above between 1 and " + str(sim.board.row*sim.board.col))
                print("Try again!\n")
                continue
            
            age_input = int(input("Enter a age limit for a cell (min 1): "))
            if not age_input < 1:
                sim.board.age_lim = age_input
            else:
                print("\nPlease enter a integer above 0")
                print("Try again!\n")
                continue

            div_input = int(input("Enter number of max divisions of a cell (min 1): "))
            if not div_input < 1:
                sim.board.div_lim = div_input
            else:
                print("\nPlease enter a integer above 0")
                print("Try again!\n")
                continue

            prob_input = float(input("Enter probability for a cell to divide (between 0 and 1): "))
            if prob_input >= 0 and prob_input <= 1:
                sim.board.prob = prob_input
            else:
                print("\nPlease enter a float between 0 and 1")
                print("Try again!\n")
                continue

            cooldown_input = int(input("Enter ticks of cooldown for one cell to divide (not negative): "))
            if not cooldown_input < 0:
                sim.board.cooldown = cooldown_input
            else:
                print("\nPlease enter a non negative number")
                print("Try again!\n")
                continue

            ticks_input = int(input("Enter number of ticks for the duration of the simulation (min 1): "))
            if ticks_input >= 1:    
                sim.max_ticks = ticks_input
            else:
                print("\nPlease enter a number above 0")
                print("Try again!\n")
                continue

            vis_input = int(input("Enter 1 or 0 [ENABLE | DISABLE] the visualisation: "))
            if vis_input == 0:
                sim.visualisation = False
            elif vis_input == 1:
                sim.visualisation = True
            else:
                print("\nVisualisation configuration has not changed!")
                print("Please chose between 1 and 0 [ENABLE | DISABLE]")
                print("Try again!\n")

            print("Changed to advanced setup.")
            print_menu()


        elif menu_choice == 4:
            sim.start()
            print_menu()

        
        elif menu_choice == 5:
            sim_status = "Default"
            sim.board.row = 15
            sim.board.col = 20
            sim.board.init_pop = 2
            sim.board.age_lim = 10
            sim.board.div_lim = 2
            sim.board.prob = 0.2
            sim.board.cooldown = 2
            sim.max_ticks = 100
            sim.visualisation = True

            print("Settings reset to default settings.\n")

        
        elif menu_choice == 6:
            quit()
        
        elif menu_choice == 33:
            sim.max_ticks = 25

        elif menu_choice == 34:
            vis_input = int(input("Enter 1 or 0 [ENABLE | DISABLE] the visualisation: "))
            if vis_input == 0:
                sim.visualisation = False
            elif vis_input == 1:
                sim.visualisation = True
            else:
                print("Please chose between 0 and 1 [ENABLE | DISABLE")
                print("Try again\n")



        else:
            print('\nEnter a valid option!')


    except ValueError:
        print('\n--- fatal ERROR!--- | Try again and enter just integer numbers!\n')
        sleep(1)
        print_menu()