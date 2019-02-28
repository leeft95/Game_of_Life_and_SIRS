# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 14:42:56 2019

@author: leeva


Game of Life:
    
    Rules:
        
    The evolution of the Game of Life on a lattice is fully deterministic and is
    set by the following set of rules:
    • Any live cell with less than 2 live neighbours dies.
    • Any live cell with 2 or 3 live neighbours lives on to the next step.
    • Any live cell with more than 3 live neighbours dies.
    • Any dead cell with exactly 3 live neighbours becomes alive.
    
    ------------------------------------------------------------------
    Nearest neighbours arrangement:
    
    (north, south, east, west, and the four neighbours along the lattice
    diagonals)
    
    i-1,j-1 | i-1,j | i-1,j+1
    i,j-1   |i,j    | i,j+1
    i+1,j-1 | i+1,j | i+1,j+1
    

SIRS:
    
    Rules:
    
    

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Gol_sirs():
    
    def __init__(self,n,mode):
        vals = [1,0]
        self.n = n
        if mode == 1:
            self.grid = np.random.choice(vals, n*n, p=[0.1, 0.9]).reshape(n, n)
        elif mode == 2:
            self.grid = np.zeros(n*n).reshape(n,n)
            glider = np.array([[0, 0, 1],[1, 0, 1],[0, 1, 1]])
            self.grid[0:0+3, 0:0+3] = glider
        elif mode == 3:
            self.grid = np.zeros(n*n).reshape(n,n)
            ossci = np.array([[0,0,0],[1,1,1],[0,0,0]])
            self.grid[0:0+3,0:0+3] = ossci
        
    def nearest_Neighbours_g(self,i,j):
        
        nN = (self.grid[i, (j-1)%self.n] +  
                        self.grid[i, (j+1)%self.n] + 
                        self.grid[(i-1)%self.n, j] + 
                        self.grid[(i+1)%self.n, j] +
                        self.grid[(i-1)%self.n, (j-1)%self.n] + 
                        self.grid[(i-1)%self.n, (j+1)%self.n] +
                        self.grid[(i+1)%self.n, (j-1)%self.n] + 
                        self.grid[(i+1)%self.n, (j+1)%self.n])
        
        
        total_Sum = nN
        return total_Sum
    
    def gol_Update(self):
        print('hello')
        grid_copy = self.grid.copy()
        
        for i in range(self.n):
            for j in range(self.n):
                
                total = self.nearest_Neighbours_g(i,j)
                
                if self.grid[i,j] == 1:
                    if (total < 2) or (total > 3):
                        grid_copy[i,j] = 0
                elif self.grid[i,j] == 0:
                    if total == 3:
                        grid_copy[i,j] = 1
                    
        self.grid = grid_copy
        return grid_copy     
   
def update(frameNum,img,grid):
    print('here')
    #for i in range(10):
    new = Gol_sirs.gol_Update(grid) 
    img.set_data(new)
    
    
    return img,
        
    


while True:
    try:
        num = int(input('Input the integer dimension of the grid:\n'))
        break
    except ValueError:
        print('Please input an integer\n')
while True:
    try:
        mod = int(input('Select the inital condition:\n' +
                     ' 1 = random\n 2 = glider\n 3 = oscillator\n'))
        if mod < 1 or mod > 3:
            raise ValueError
        else:
            break
    except(ValueError):
        print('Please input a valid option')


        
        
g = Gol_sirs(num,mod)

#    for i in range(10):
#Gol_sirs.gol_Update(g)
fig = plt.figure()
img = plt.imshow(g.grid,animated = True)
a = animation.FuncAnimation(fig,update,fargs=(img,g),frames = 100,
                            repeat = True,blit = True)
#    print(g.grid)

plt.show()
 

    
    

    


        
        
        
        