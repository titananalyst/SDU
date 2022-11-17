from grid_visualizer import BinaryVisualiser
import random

def running_dot(height:int,width:int)->None:
    '''Displays a window with a dot running across it.'''
    grid = zero_mat(height,width)# a grid of all zeros
    x = width // 2
    y = height // 2
    grid[y][x] = 1 # now with a dot at (x,y)
    vis = BinaryVisualiser(grid) # visualiser
    while vis.is_open():
        grid[y][x] = 0 # erase the current dot
        x = (x + 1) % width # move its coordinates right by 1 square
        grid[y][x] = 1 # set the dot to its new position
        vis.update(grid,interval=0.2) # update the visualiser and pause for 0.2seconds

def zero_mat(height:int,width:int)->list:
    '''Returns a matrix (list of lists) of size width x height filled with zeros.'''
    assert(height>0)
    assert(width>0)
    return  [[0] * width  for i in range(height)]

def checker_mat(height:int,width:int)->list:
    '''returns a matrix (list of lists) of size width x height filled as a checkboard.'''
    mat=zero_mat(height,width)
    for i in range(height):
        for j in range(width):
            if ( (i+j)%2==0):
                mat[i][j] = 1
    return mat

def uniform_noise(height:int,width:int,p:float = 0.5)->list:
    '''returns a matrix (list of lists) of size width x height with each square colored with p probability.'''
    assert(p>=0 and p<=1)
    mat=zero_mat(height,width)
    for i in range(height):
        for j in range(width):
            mat[i][j] = random.choices([0,1], weights=(p,1-p))

    return mat


def uniform_ones(height:int,width:int,ones:int)->list:
    '''returns a matrix (list of lists) of size width x height with n=ones elements filled and randomly chosen.'''
    mat=zero_mat(height,width)
    assert(ones>=0)
    assert(ones<=height*width)
    pairs = [(x,y) for x in range(height) for y in range(width)] 
    selected_pairs = random.sample(pairs,ones)
    for (i,j) in selected_pairs:
        mat[i][j]=1

    return  mat

def flip(grid:list)->list:
    '''returns a matrix (list of lists) of size identical to the inputed one filled with reversed elements.'''
    height=len(grid)
    width=len(grid[0])
    mat=zero_mat(height,width)
    for i in range(height):
        for j in range(width):
            mat[i][j] = 1 - grid[i][j]

    return  mat

def random_flip(grid:list,p:float =0.5)->list:
    '''returns a matrix (list of lists) of size identical to the inputed one filled with each element reversed with probability p.'''
    height=len(grid)
    width=len(grid[0])
    mat=zero_mat(height,width)
    for i in range(height):
        for j in range(width):
            rval = random.choices([0,1], weights=(p,1-p))
            mat[i][j] = grid[i][j] + rval[0] * ( 1 - 2 * grid[i][j] )

    return  mat

def paste(source:list,target:list,offset_y:int,offset_x:int)->None:
    '''paste into a target matrix (list of lists) a shifted selection of the source matrix.'''
    height=min(len(source)+offset_y,len(target))
    width=min(len(source[0])+offset_x,len(target[0]))
    for i in range(max(0,offset_y),height):
        for j in range(max(0,offset_x),width):
            target[i][j] = source[i-offset_y][j-offset_x]

grid = [[0, 1, 0], # some 2D binary data
[0, 0, 1],
[1, 1, 1]]

mat = checker_mat(4, 4)

vis = BinaryVisualiser(mat) # create a visualiser for this data
vis.wait_close() # wait until the window is closed by the user