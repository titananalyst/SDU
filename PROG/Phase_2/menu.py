"menu"
#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   cell_sim.py
@Time    :   2022/11/08 01:28:29
@Author  :   Simone Wolff Nielsen
@Author  :   Mia Trabjerglund
@Author  :   Jonas Keller
'''

from cell_sim import Grid, Simulation
from time import sleep
from sys import exit

grid = Grid() # sets grid to the whole class Grid from cell_sim
sim = Simulation()
sim_status = "Default"
vis_status = "Enabled"

def grid_menu(grid:str, GRID)->bool:
    '''
    this menue has to be completed before the next one is availeble. 

    '''
    grid = input("What is the name of the grid you want to run?").strip()
    if GRID(grid):
        choose_number_of_cells()
    else:
        print("make an valid grid, for guide see the raport. When you have a valid grid run the program again")
        print("Bye!")
        exit()

def choose_number_of_cells(number:int):
    '''
    this should be running after the grid menue has come true
    '''
    print("choose an number of cell-population between 1 and", grid.total_num_cell_patc )
    number = int(input("coose an number of cell-population here: "))
    if 1 <= number >= grid.total_num_cell_patch:
        sim.board.init_pop = number
        print_menu()
    else:
        print("this number is not valied")
        number = int(input('''do you want to choose a valid number of cell-population or exit?
        1) try again.
        anny other input) exit. 
        choose here: '''))
        if number == 1:
            choose_number_of_cells()
        else:
            print("Bye!")
            exit()


def print_menu():
    '''
    this print out the display of the menu, 
    where all the print-statements exicute one line at a time. 
    '''
    print("\nMenu:")
    print(31 * "-")
    print("1: Display configuration")
    print("2: Setup")
    print("3: Run simulation")
    print("4: Reset to default setup")
    print("5: Quit")
    print()
    menu_choice = int(input("Type in a number (1-5): "))

    if menu_choice == 1:
        if sim.visualisation == False:
            vis_status = "Disabled"
        '''
        this print out the display confuration menu, 
        with the parametres there has been chosen.
        '''
        print("\n" + 31 * "-")
        print("{:<22} {}".format("Parameter", sim_status))
        print(31 * "-")
        print("{:<22} {}".format("Initial population", sim.board.init_pop))
        print("{:<22} {}".format("Age limit", sim.board.age_lim))
        print("{:<22} {}".format("Division limit", sim.board.div_lim))
        print("{:<22} {}".format("Division probability", sim.board.prob))
        print("{:<22} {}".format("Division cooldown", sim.board.cooldown))
        print("{:<22} {}".format("Time limit", sim.max_ticks))
        print("{:<22} {}\n".format("Visualisation", vis_status))
        print_menu()


    elif menu_choice == 2:
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
       
            sim_status = "Setup"
            
            age_input = int(input("Enter a age limit for a cell (min 1): "))
            if not age_input < 1:
                sim.board.age_lim = age_input
            else:
                print("\nPlease enter a integer above 0")
                print("Try again!\n")
                print("default values are enabled")
                sim_status = "Default"
                print_menu()
                continue

            div_input = int(input("Enter number of max divisions of a cell (min 1): "))
            if not div_input < 1:
                sim.board.div_lim = div_input
            else:
                print("\nPlease enter a integer above 0")
                print("Try again!\n")
                print("default values are enabled")
                sim_status = "Default"
                sim.board.age_lim = 10
                print_menu()
                continue

            prob_input = float(input("Enter probability for a cell to divide (between 0 and 1): "))
            if prob_input >= 0 and prob_input <= 1:
                sim.board.prob = prob_input
            else:
                print("\nPlease enter a float between 0 and 1")
                print("Try again!\n")
                print("default values are enabled")
                sim_status = "Default"
                sim.board.age_lim = 10
                sim.board.div_lim = 2
                print_menu()
                continue

            cooldown_input = int(input("Enter ticks of cooldown for one cell to divide (not negative): "))
            if not cooldown_input < 0:
                sim.board.cooldown = cooldown_input
            else:
                print("\nPlease enter a non negative number")
                print("Try again!\n")
                print("default values are enabled")
                sim_status = "Default"
                sim.board.age_lim = 10
                sim.board.div_lim = 2
                sim.board.prob = 0.2
                print_menu()
                continue

            ticks_input = int(input("Enter number of ticks for the duration of the simulation (min 1): "))
            if ticks_input >= 1:    
                sim.max_ticks = ticks_input
            else:
                print("\nPlease enter a number above 0")
                print("Try again!\n")
                print("default values are enabled")
                sim_status = "Default"
                sim.board.age_lim = 10
                sim.board.div_lim = 2
                sim.board.prob = 0.2
                sim.board.cooldown = 2
                print_menu()
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


        elif menu_choice == 3:
            '''
            this starts the simulation that has been called from the cell_sim.py
            '''
            sim.start()
            print_menu()

        
        elif menu_choice == 4:
            '''
            this reset alle tha parametres to the pre-chosen default values.
            '''
            sim_status = "Default"
            sim.board.age_lim = 10
            sim.board.div_lim = 2
            sim.board.prob = 0.2
            sim.board.cooldown = 2
            sim.max_ticks = 100
            sim.visualisation = True

            print("Settings reset to default settings.\n")
            print_menu()

        
        elif menu_choice == 5:
            '''
            quit the program with the imported quit function. 
            '''
            print('Bye!')
            exit()

        
        else:
            print('\nEnter a valid option!')


    except ValueError:
        print('\n--- fatal ERROR!--- | Try again and enter just integer numbers!\n')
        sleep(1)
        print_menu()