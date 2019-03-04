# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:10:35 2019

@author: leeva
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from progressbar import Percentage, ProgressBar,Bar,ETA




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
#            self.grid = np.random.choice([0,1,2], size=(n, n))
            self.grid = np.zeros(n*n).reshape(n,n)
            a = int(np.random.uniform(0, n))
            b = int(np.random.uniform(0, n))
            self.grid[a,b] = 1
        self.I = I
        
def sirs_Update(grid,p1,p2,p3):
    x = 0
    i = np.random.randint(0,num)
    j = np.random.randint(0,num)
    
    pb = random.uniform(0,1)
    
    Nn = np.array([grid[i,(j-1)%num],
                                 grid[i,(j+1)%(num)],
                                 grid[(i+1)%(num),j],
                                 grid[(i-1)%(num),j]])

    
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
        if p3 > pb:
            return 0,i,j
        else:
            return 2,i,j
    
    


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
while True:
    try:
        a = int(input('Start ' + 
                      'simulation or measurements:'+
                      '\n 1 = Simulation \n 2 = Measurement\n'))
        if a > 2 or a < 1:
            raise ValueError
        else:
            break
    except(ValueError):
        print('please input a valid option')
if a == 2:
    while True:
        try:
            mes = int(input('Choose the measurement:\nSIRS \n 1 = Phase and waves\n'+
                            ' 2 = waves cut\n \nGame of Life' +
                            '\n 3 = glider velocity\n'))
            if mes > 4 or mes < 1: 
                raise ValueError
            else:
                break
        except(ValueError):
            print('please input a valid option')
else:
    mes = 0
    
if mes == 1:
    nt = 20     
    p1 = np.linspace(0,1,nt)
    p2 = 0.5
    p3 = np.linspace(0,1,nt)

    sweep = 1000
    passes = num*num
    avgI = np.zeros((len(p1),len(p3)))
    avgvar = np.zeros((len(p1),len(p3)))
    

if mes == 2:
    nt = 50     
    p1 = np.linspace(0.2,0.5,nt)
    p2 = 0.5
    p3 = 0.5#np.linspace(0,1,nt)

    sweep = 10000
    passes = num*num
    
    var_list = []

g = Gol_sirs(num,mod,1)



I = 0
I_2 = 0
bar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Percentage(), ' ', ETA(),'\n'], maxval=nt).start()

if mes == 1:
    
    for i in range(len(p1)):
        for j in range(len(p3)):
            I_list = []
            I2_list = []
            print(p1[i],p3[j])
            for q in range(sweep):
                for u in range(passes):
                    s,a,b = sirs_Update(g.grid,p1[i],p2,p3[j])
                    g.grid[a,b] = s
                if q%10 == 0 and q > 100:
                    I = 0
                    for m in range(num):
                        for n in range(num):
                            if g.grid[m,n] == 1:
                                I += 1
                    
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
    


    
if mes == 2:
    for i in range(len(p1)):
        I_list = []
        I2_list = []
        print(p1[i],p3)
        for q in range(sweep):
            for u in range(passes):
                s,a,b = sirs_Update(g.grid,p1[i],p2,p3)
                g.grid[a,b] = s
            if q%10 == 0 and q > 100:
                I = 0
                for m in range(num):
                    for n in range(num):
                        if g.grid[m,n] == 1:
                            I += 1
                
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

                
        