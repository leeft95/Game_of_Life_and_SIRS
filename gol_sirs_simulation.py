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
        
        S == 0
        I == 1
        R == 2
    
    • S → I with probability p1 if at least one neighbour of i is I; otherwise site
      i is unchanged.
    • I → R with probability p2.
    • R → S with probability p3.
    
    Measurements:
        
        - Phase diagram for SIRS. We'll be looking for a resolution of 0.05 in 
        p1 and p3 (p2=0.5 is fixed). This is a 20 by 20 pixelation. For each 4
        value of p1 and p3, we suggest an equilibration time of 100 sweeps, 
        and a total measurement time of 1,000 sweeps, with measurement every 
        10 (same as Ising). This should be doable in max 2 hrs with a good 
        python code, so first check with smaller number of sweeps 
        (e.g., 10-fold smaller) and lower resolution that the phase diagram 
        is reasonable.
        

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm




class Gol_sirs():
    
    def __init__(self,n,mode,I):
        vals = [1,0]
        self.n = n
        if mode == 1:
            self.grid = np.random.choice(vals, n*n, p=[0.4, 0.6]).reshape(n, n)
        elif mode == 2:
            self.grid = np.zeros(n*n).reshape(n,n)
            glider = np.array([[0, 0, 1],[1, 0, 1],[0, 1, 1]])
            self.grid[0:0+3, 0:0+3] = glider
        elif mode == 3:
            self.grid = np.zeros(n*n).reshape(n,n)
            ossci = np.array([[0,0,0],[1,1,1],[0,0,0]])
            self.grid[1:1+3,1:1+3] = ossci
        elif mode == 4:
        #   self.grid = np.random.choice([0,1,2], size=(n, n))
            self.grid = np.zeros(n*n).reshape(n,n)
            a = int(np.random.uniform(0, n))
            b = int(np.random.uniform(0, n))
            self.grid[a,b] = 1
        self.I = I

        
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
    
    def nearest_Neighbours_s(self,i,j):
        
        nN = np.array([self.grid[i,(j-1)%(self.n-1)],
                                 self.grid[i,(j+1)%(self.n-1)],
                                 self.grid[(i+1)%(self.n-1),j],
                                 self.grid[(i-1)%(self.n-1),j]])
            
        return nN        
    
    def gol_Update(self):
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

    def sirs_Update(self,b,g,sus,I,rep):
        for a in range(rep):
            i = int(np.random.uniform(0, self.n))
            j = int(np.random.uniform(0, self.n))
                    
            nN = self.nearest_Neighbours_s(i,j)
            x = (np.random.uniform(low = 0,high = 1))
            
            # infec = 0       
            # for i in range(self.n):
            #     for j in range(self.n):
            #         if self.grid[i,j] == 1:
            #             infec +=1
            # print(infec)
            
            for k in range(len(nN)):
                if nN[k] == 1:
                    if self.grid[i,j] == 0:
                        if  x < b:
                            self.grid[i,j] = 1
                            return self.grid
            
            if self.grid[i,j] == 1:
                if x < g:
                    self.grid[i,j] = 2
                    return self.grid
            if self.grid[i,j] == 2:
                if x < sus:
                    self.grid[i,j] = 0
                    return self.grid

            
        return self.grid
    
    def avg_Infect(self):
        I = 0#self.n*self.n
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i,j] == 1:
                    I += 1
        avg_I = I/(self.n*self.n)
        
        return avg_I
    
    def avg_sus(self):
        I = self.n*self.n
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i,j] == 0:
                    I -= 1
        avg_I = I/(self.n*self.n)
        
        avg_i2 = (I**2)/(self.n*self.n)
        
        var = (avg_i2-(avg_I**2))/(self.n*self.n)
        
        
        return avg_I,var
    
        
                
        
   
def update(frameNum,img,grid):
    #for i in range(10):
    new = Gol_sirs.gol_Update(grid) 
    img.set_data(new)
    
    
    return img,


def update_s(frameNum,img,grid,b,g,sus,I):
    #for i in range(10):
    new = Gol_sirs.sirs_Update(grid,b,g,sus,I,1000) 
    img.set_data(new)
    
    
    return img,
        
'''
pulsing parameters:
    b = .8
    ga = .1
    sus = .01
    
phase res == 20
wave res == 15

'''    

print('This is the Simulation Program\n\n')
while True:
    try:
        num = int(input('Input the integer dimension of the grid:\n'))
        if num <= 5:
            raise ValueError
        else:
            break
    except ValueError:
        print('Please input a valid grid size \n')
while True:
    try:
        mod = int(input('Select the inital condition:\n' + 
                        'Game of Life:\n 1 = random\n 2 = glider\n' + 
                        ' 3 = oscillator\nSIRS\n 4 = SIRS\n'))
        if mod < 1 or mod > 4:
            raise ValueError
        else:
            break
    except(ValueError):
        print('Please input a valid option')
if mod == 4:
    while True:
        try:
            p1 = float(input('Simulation parameter -->  p1 = '))
            p2 = float(input('Simulation parameter -->  p2 = '))
            p3 = float(input('Simulation parameter -->  p3 = '))
            if p1 > 1 or p1 < 0 or p2 > 1 or p2 < 0 or p3 > 1 or p3 < 0:
                raise ValueError
            else:
                break
        except(ValueError):
            print('please input a valid option')
  

######__SIRS parameters__#######
        

        

I = 0

        
####_create grid object_####        
g = Gol_sirs(num,mod,I)


#####_Animations_#####
if mod != 4:
    fig,ax = plt.subplots()
    img = ax.imshow(g.grid,animated = True,cmap = cm.jet,vmin = 0,vmax =1)
    fig.colorbar(img)
    a = animation.FuncAnimation(fig,update,fargs=(img,g,),frames = 10,
                                repeat = True,blit = True)
if mod == 4:
    fig,ax = plt.subplots()
    g.sirs_Update(p1,p2,p3,I,10)
    img = ax.imshow(g.grid,animated = True,vmin = 0,vmax =2)
    fig.colorbar(img)
    plt.xlabel('0 = susecptible  1 = infected  2 = recovered')
    a = animation.FuncAnimation(fig,update_s,fargs=(img,g,p1,p2,p3,I,),frames = 10,
                                repeat = True,blit = True,interval = 1)

plt.show()
 

    
    

    


        
        
        
        