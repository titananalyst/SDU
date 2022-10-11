from abc import ABCMeta, abstractmethod
import random


class Creature(metaclass=ABCMeta):      ##unfortunately not used widely in the code :(

    @abstractmethod
    def isbear(self):
        pass

class Bear(Creature):

    def __init__(self, type):
        self.type = type
    def isbear(self):
        return True

class Fish(Creature) :

    def __init__(self, type):
        self.type = type
    def isbear(self):
        return False

class River:
    
    def __init__(self, n, eco):
        self.n = n          # Size of the ecosystem
        self.eco = None     # Initialize the ecosystem - iteration count
        self.list = []

        fish_type = ['salmon', 'trout', 'bass']
        bear_type = ['polar', 'brown', 'grizzly']

        for count in range(n):         ##this creates a random list of the river environment    
            spottaken = random.randint(0, 2)
            if spottaken == 0: self.list.append(None)
            if spottaken == 1: self.list.append(Fish(random.choice(fish_type)))         
            if spottaken == 2: self.list.append(Bear(random.choice(bear_type)))
        
        print(self.list)            ## prints original list

        for skaicius in range(eco):     #iterations as provided by the user

            temp_list = [[] for count in range(n)]      ##array of lists for collisions
            movement_list = []

            for count in range(n):          ##filling up the mentioned list
                temp_list[count].append(None)
                if self.list[count] == None:     
                    temp_list[count].append(self.list[count])
                    movement_list.append(0)
                else:
                    if count == 0:
                        randomas = random.randint(0, 1)
                        movement_list.append(randomas)
                        temp_list[count + randomas].append(self.list[count])
                    if count == (n-1):
                        randomas = random.randint(-1, 0)
                        movement_list.append(randomas)
                        temp_list[count + randomas].append(self.list[count])
                    if 0 < count < (n-1):
                        randomas = random.randint(-1, 1)
                        movement_list.append(randomas)
                        temp_list[count + randomas].append(self.list[count])

            print(movement_list) ##movement list to check if iteration went without errors

            newtestlist = []
            fswitch = False
            bswitch = False
            parentfish = False
            parentbear = False
            skip = False
            bearrrparent = None
            fishhhparent = None
            superskip = False

            for count in range(n):
                bobjlist = []
                fobjlist = []
                if 0 < count:
                    if parentfish == True:          ##feature to keep parent objects original in case of a collision
                        if movement_list[count-1] == 1:
                            newtestlist[count-1] = fishhhparent
                            parentfish = False
                    if parentbear == True:
                        if movement_list[count-1] == 1:
                            newtestlist[count-1] = bearrrparent
                            parentbear = False
                if count < (n-1):
                    if parentfish == True:
                        if movement_list[count+1] == -1:
                            fswitch = True
                            parentfish = False
                    if parentbear == True:
                        if movement_list[count+1] == -1:
                            bswitch = True
                            parentbear = False
                determ = 0      ## this determines the new locations for fish objects

                for j in range(len(temp_list[count])):      ##checks array and extracts objects into a temp location
                    if temp_list[count][j] == None:
                        determ += 0
                    else: 
                        if temp_list[count][j].isbear() == True:
                            bobjlist.append(temp_list[count][j])
                            determ += 5
                        if temp_list[count][j].isbear() == False:
                            fobjlist.append(temp_list[count][j])
                            determ += 2
                print(determ) 

                if 0 < count:           ##feature to keep parent objects original in case of a collision
                    if parentfish == True:
                        if movement_list[count-1] == 1:
                            newtestlist[count-1] = fishhhparent
                            parentfish = False
                        if movement_list[count] == -1 or movement_list[count] == 1:
                            if determ == 0:
                                newtestlist.append(fishhhparent)
                                skip = True
                    if parentbear == True:
                        if movement_list[count-1] == 1:
                            newtestlist[count-1] = bearrrparent
                            parentbear = False
                        if movement_list[count] == -1 or movement_list[count] == 1:
                            if determ == 0:
                                newtestlist.append(bearrrparent)
                                skip = True
                if count < (n-1):       ##feature to keep parent objects original in case of a collision
                    if parentfish == True:
                        if movement_list[count+1] == -1:
                            fswitch = True
                            parentfish = False
                    if parentbear == True:
                        if movement_list[count+1] == -1:
                            bswitch = True
                            parentbear = False


                if determ == 0:         ##Null in list, + additions for particular conditions in case of collision
                    if superskip == False:
                        if bswitch == False and fswitch == False:
                            if skip == False:
                                newtestlist.append(None)
                        if bswitch == True:
                            if skip == False:
                                newtestlist.append(Bear(random.choice(bear_type)))
                                bswitch = False
                        if fswitch == True:
                            if skip == False:
                                newtestlist.append(Fish(random.choice(fish_type)))
                                fswitch = False
                        if skip == True:
                            skip = False
                    else:
                        superskip = False
                if determ == 2:                     ##fish
                    newtestlist.append(fobjlist[0])
                if determ == 5:                     ##bear
                    newtestlist.append(bobjlist[0])
                if determ == 7 or determ == 9:      ##bear eats either one or 2 fishes
                    newtestlist.append(bobjlist[0])
                if determ == 4:     ##two fish
                    newtestlist.append(fobjlist[0])
                    fishhhparent = fobjlist[1]
                    parentfish = True
                    for i, b in enumerate(newtestlist):
                        if b == None:
                            newtestlist[i] = Fish(random.choice(fish_type))
                            break
                        else:
                            fswitch = True
                            break
                if determ == 10 or determ == 12:   ## two bears ( + 1 fish )
                    newtestlist.append(bobjlist[0])
                    bearrrparent = bobjlist[1]
                    parentbear = True
                    for i, b in enumerate(newtestlist):
                        if b == None:
                            newtestlist[i] = Bear(random.choice(bear_type))
                            break
                        else:
                            bswitch = True
                            break
                if determ == 6:         ## 3 fishes jumping in the same block
                    newtestlist[count-1] = (fobjlist[0])
                    newtestlist.append(fobjlist[1])
                    newtestlist.append(fobjlist[2])
                    fswitch == True
                    superskip = True
                if determ == 15:        ## 3 bears jumping in the same block
                    newtestlist[count-1] = (bobjlist[0])
                    newtestlist.append(bobjlist[1])
                    newtestlist.append(bobjlist[2])
                    bswitch == True
                    superskip = True

            self.list = newtestlist
            print (newtestlist)
            print("length:", len(newtestlist)) ##easy check for: if something went wrong


test = River(10, 50)

## PS sorry about the code being VERY messy and inefficient