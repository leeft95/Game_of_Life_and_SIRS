# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:10:35 2019

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




import random
import numpy as np
import matplotlib.pyplot as plt
from progressbar import Percentage, ProgressBar,Bar,ETA




class Gol_sirs():
    
    def __init__(self,n,mode,I):
        self.n = n
        if mode == 1:
            self.grid = np.zeros(n*n).reshape(n,n)
            glider = np.array([[0, 0, 1],[1, 0, 1],[0, 1, 1]])
            self.grid[0:0+3, 0:0+3] = glider
        elif mode == 2:
#            self.grid = np.random.choice([0,1,2], size=(n, n))
            self.grid = np.zeros(n*n).reshape(n,n)
            a = int(np.random.uniform(0, n))
            b = int(np.random.uniform(0, n))
            self.grid[a,b] = 1
        self.I = I
        
###___Sirs update function___###        
def sirs_Update(grid,p1,p2,p3,imu,p4):
    x = 0
    i = np.random.randint(0,num)
    j = np.random.randint(0,num)
    
    pb = random.uniform(0,1)
    
    Nn = np.array([grid[i,(j-1)%num],
                                 grid[i,(j+1)%(num)],
                                 grid[(i+1)%(num),j],
                                 grid[(i-1)%(num),j]])

    if imu == 1:
        ui = 0
        for u in range(len(grid)):
            for h in range(len(grid)):
                if grid[u,h] == 2:
                    ui += 1
        avg_im = ui/((len(grid))**2)

    
    for k in range(len(Nn)):
        if Nn[k] == 1:
            x = 1
            
    if grid[i,j] == 0:
        if x == 1 and p1 > pb:
            return 1,i,j
        else:
            return 0,i,j
            
    elif grid[i,j] == 1:
        if p2 > pb:
            return 2,i,j
        else:
            return 1,i,j
    elif grid[i,j] == 2:
        if imu == 1:
            if p3 > pb and avg_im > p4:
                return 0,i,j
            else:
                return 2,i,j
        elif imu == 0:
            if p3 > pb:
                return 0,i,j
            else:
                return 2,i,j
            
            
###___update function for Game of Life___###       
def gol_Update(grid,n):
    grid_copy = grid.copy()
    
    for i in range(n):
        for j in range(n):
            
            total = nearest_Neighbours_g(grid,i,j,n)
            
            if grid[i,j] == 1:
                if (total < 2) or (total > 3):
                    grid_copy[i,j] = 0
            elif grid[i,j] == 0:
                if total == 3:
                    grid_copy[i,j] = 1
                
    grid = grid_copy
    return grid_copy 
 
###__nearest neighbours rules for GoL___###
def nearest_Neighbours_g(grid,i,j,n):
    
    nN = (grid[i, (j-1)%n] +  
                    grid[i, (j+1)%n] + 
                    grid[(i-1)%n, j] + 
                    grid[(i+1)%n, j] +
                    grid[(i-1)%n, (j-1)%n] + 
                    grid[(i-1)%n, (j+1)%n] +
                    grid[(i+1)%n, (j-1)%n] + 
                    grid[(i+1)%n, (j+1)%n])
    
    
    total_Sum = nN
    return total_Sum
###_Center of Mass function___###
def com(grid,n):
    indices = np.argwhere(grid == 1)
    ### Determine if cells are near boundaries ###
    for i in range(len(indices)):
        for j in range(0,1):
             if (indices[i,j] == 0 or indices[i,j] == n-1):
                     return None,None
    com_X = np.mean(indices[:,0])
    com_Y = np.mean(indices[:,1])
    
    return com_X,com_Y
    
    
    

print('This is the measurement program\n\n')
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
                        'Game of Life:\n 1 = glider(measurement)\n' + 
                        'SIRS\n 2 = SIRS\n'))
        if mod < 1 or mod > 4:
            raise ValueError
        else:
            break
    except(ValueError):
        print('Please input a valid option')

while True:
    try:
        mes = int(input('Choose the measurement:\nSIRS \n 1 = Phase and waves\n'+
                        ' 2 = waves cut\n 3 = immune fraction\n \nGame of Life' +
                        '\n 4 = glider velocity\n'))
        if mes > 4 or mes < 1: 
            raise ValueError
        elif mes == 4 and mod == 2:
            raise ValueError
        else:
            break
    except(ValueError):
        print('please input a valid option')

###___Initilaise parameters depending on measurement choice___###  
    
if mes == 1:
    nt = 20     
    p1 = np.linspace(0,1,nt)
    p2 = 0.5
    p3 = np.linspace(0,1,nt)
    p4 = 0
    imu = 0

    sweep = 1000
    passes = num*num
    avgI = np.zeros((len(p1),len(p3)))
    avgvar = np.zeros((len(p1),len(p3)))
    

if mes == 2:
    nt = 50     
    p1 = np.linspace(0.2,0.5,nt)
    p2 = 0.5
    p3 = 0.5#np.linspace(0,1,nt)
    p4 = 0
    imu = 0

    sweep = 10000
    passes = num*num
    
    var_list = []
    
if mes == 3:
    nt = 100  
    p1 = 0.5#np.linspace(0.2,0.5,nt)
    p2 = 0.5
    p3 = 0.5#np.linspace(0,1,nt)
    p4 = np.linspace(0,1,nt)
    imu = 1

    sweep = 100
    passes = num*num
    
    imu_list = []
    err_list = []

if mes == 4:
    sweep = 1000
    nt = 1
    x_list = []
    y_list = []

g = Gol_sirs(num,mod,1)

z = 0

I = 0
I_2 = 0
bar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Percentage(), ' ', ETA(),'\n'], maxval=nt).start()

###___Phase measurement___###
if mes == 1:
    
    for i in range(len(p1)):
        for j in range(len(p3)):
            I_list = []
            I2_list = []
            print(p1[i],p3[j])
            for q in range(sweep):
                for u in range(passes):
                    s,a,b = sirs_Update(g.grid,p1[i],p2,p3[j],imu,p4)
                    g.grid[a,b] = s
                if q%10 == 0 and q > 100:
                    I = 0
                    for m in range(num):
                        for n in range(num):
                            if g.grid[m,n] == 1:
                                I += 1
                    if I == 0.0:
                        I_list.append(0)
                        break
                    else:
                        I_list.append(I)

            I_list = np.asarray(I_list)
            avg_i = np.mean(I_list)
            print(avg_i)
            avg_i2 = np.mean(I_list**2)
            var = (avg_i2 - avg_i**2)/(num**2)
            avgI[i,j] = avg_i/(num**2)
            avgvar[i,j] = var

            g = Gol_sirs(num,mod,1)
        z += 1
        bar.update(z)
    
    print(avgI)
    plt.figure()
    CS = plt.contourf(p1, p3, avgI.T)
    
    plt.title('phase')
    plt.xlabel('p1')
    plt.ylabel('p3')
    plt.colorbar()
    
    plt.figure()
    CS = plt.contourf(p1, p3, avgvar.T)
    
    plt.title('var')
    plt.xlabel('p1')
    plt.ylabel('p3')
    plt.colorbar()
    
    bar.finish()

###___Waves cut measurement___###   
if mes == 2:
    for i in range(len(p1)):
        I_list = []
        I2_list = []
        print(p1[i],p3)
        for q in range(sweep):
            for u in range(passes):
                s,a,b = sirs_Update(g.grid,p1[i],p2,p3,imu,p4)
                g.grid[a,b] = s
            if q%10 == 0 and q > 100:
                I = 0
                for m in range(num):
                    for n in range(num):
                        if g.grid[m,n] == 1:
                            I += 1
                if I == 0.0:
                    I_list.append(0)
                    break
                else:
                    I_list.append(I)
        I_list = np.asarray(I_list)
        avg_i = np.mean(I_list)
        print(avg_i)
        avg_i2 = np.mean(I_list**2)
        var = (avg_i2 - avg_i**2)/(num**2)
#        avgI[i,j] = avg_i/(num**2)
#        avgvar[i,j] = var
        var_list.append(var)
        g = Gol_sirs(num,mod,1)
        z += 1
        bar.update(z)

    plt.figure()
    plt.plot(p1, var_list)
    
    plt.title('cut')
    plt.xlabel('p1')
    plt.ylabel('var')
    
    bar.finish()

###___immune frac cut___###   
if mes == 3:
    for i in range(len(p4)):
        I_list = []
        I2_list = []
        for q in range(sweep):
            for u in range(passes):
                s,a,b = sirs_Update(g.grid,p1,p2,p3,imu,p4[i])
                g.grid[a,b] = s
            if q%10 == 0 and q > 100:
                I = 0
                for m in range(num):
                    for n in range(num):
                        if g.grid[m,n] == 1:
                            I += 1
                if I == 0.0:
                    I_list.append(0)
                    break
                else:
                    I_list.append(I)
        I_list = np.asarray(I_list)
        avg_i = np.mean(I_list)
        print(str(avg_i) + ' i ')
        avg_i2 = np.mean(I_list**2)
        var = (avg_i2 - avg_i**2)/(num**2)
        std_error = np.std(I_list/num**2)/(len(I_list))**0.5
        print(std_error)
        imu_list.append(avg_i/(num**2))
        err_list.append(std_error)
        g = Gol_sirs(num,mod,1)
        z += 1
        bar.update(z)

    plt.figure()
    plt.errorbar(p4, imu_list, yerr = err_list)
    
    plt.title('imu frac')
    plt.xlabel('fraction')
    plt.ylabel('avg infec')
    
    bar.finish()


###___Glider velocity___###
if mes == 4:
    t = 0
    for i in range(sweep):
        grid = gol_Update(g.grid,g.n)
        g.grid = grid
        x,y = com(g.grid,g.n)
        if x != None:
            if t == 0:
                dist1 = np.sqrt(x**2. + y**2)
            dist = np.sqrt(x**2. + y**2)
            if t != 0:
                if dist == dist1:
                    break
            x_list.append(dist)
            y_list.append(t)
            t += 1


    t_dist = max(y_list)-min(y_list)
    x_rise = max(x_list)-min(x_list)
    
    x_dist = (t_dist**2 + x_rise**2)**0.5
    
    velocity = x_dist/t_dist
    
    plt.scatter(y_list,x_list,label = ('velocity = {:0.3f} lattice position/sweep'
                                       .format(velocity)))
    plt.legend(loc = 'best')
    plt.xlabel('t(sweeps)')
    plt.ylabel('avg position')
    
    bar.finish()

    
    
        
                
        