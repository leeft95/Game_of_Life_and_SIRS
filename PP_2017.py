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
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animate
from matplotlib import cm


class Gol_sirs():
	'''
	Combined Game of life and SIRS model class
	'''

	def __init__(self, n, mode, seed):
		vals = [1, 0]
		self.n = n
		if mode == 1:
			self.grid = np.random.choice(vals, n * n, p=[0.4, 0.6]).reshape(n, n)
		elif mode == 2:
			self.grid = np.zeros(n * n).reshape(n, n)
			glider = np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]])
			self.grid[0:0 + 3, 0:0 + 3] = glider
		elif mode == 3:
			self.grid = np.zeros(n * n).reshape(n, n)
			ossci = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
			self.grid[1:1 + 3, 1:1 + 3] = ossci

		elif mode == 4:
			self.grid = np.zeros(n * n).reshape(n, n)
			absorber = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]])
			self.grid[0:0 + 4, 0:0 + 4] = absorber
		elif mode == 5:
			if seed == 0:
				self.grid = np.random.choice([0, 1, 2], size=(n, n), p = [1/3,1/3,1/3])
			elif seed == 1:
				self.grid = np.zeros(n * n).reshape(n, n)
				a = int(np.random.uniform(0, n))
				b = int(np.random.uniform(0, n))
				self.grid[a, b] = 1

	def nearest_Neighbours_g(self, i, j):

		nN = (self.grid[i, (j - 1) % self.n]
		      + self.grid[i, (j + 1) % self.n]
		      + self.grid[(i - 1) % self.n, j]
		      + self.grid[(i + 1) % self.n, j]
		      + self.grid[(i - 1) % self.n, (j - 1) % self.n]
		      + self.grid[(i - 1) % self.n, (j + 1) % self.n]
		      + self.grid[(i + 1) % self.n, (j - 1) % self.n]
		      + self.grid[(i + 1) % self.n, (j + 1) % self.n])

		total_Sum = nN
		return total_Sum

	def nearest_Neighbours_s(self, i, j):

		nN = np.array([self.grid[i, (j - 1) % (self.n)],
		               self.grid[i, (j + 1) % (self.n)],
		               self.grid[(i + 1) % (self.n), j],
		               self.grid[(i - 1) % (self.n), j]])

		return nN

	def gol_Update(self):
		grid_copy = self.grid.copy()

		for i in range(self.n):
			for j in range(self.n):

				total = self.nearest_Neighbours_g(i, j)

				if self.grid[i, j] == 1:
					if (total < 2) or (total > 3):
						grid_copy[i, j] = 0
				elif self.grid[i, j] == 0:
					if total == 3:
						grid_copy[i, j] = 1

		self.grid = grid_copy
		return grid_copy

	def sirs_Update(self, p1, p2, rep):
		for a in range(rep):
			i = int(np.random.uniform(0, self.n))
			j = int(np.random.uniform(0, self.n))

			nN = self.nearest_Neighbours_s(i, j)
			pb = np.random.uniform(low=0, high=1)
			rand_n = np.random.choice([0,1,2],p = [1/3,1/3,1/3])
			test = nN[rand_n]

			if self.grid[i, j] == 0:
				if test == 1 and p2 > pb:
					self.grid[i,j] = 1
					return self.grid
				elif test == 2 and p1 > pb:
					self.grid[i,j] = 2
					return self.grid
				else:
					return self.grid
				return self.grid
			elif self.grid[i, j] == 1:
				if test == 0 and p1 > pb:
					self.grid[i,j] =  0
				elif test == 2 and p2 > pb:
					self.grid[i,j] =  2
				else:
					return self.grid
				return self.grid
			elif self.grid[i, j] == 2:
				if test == 0 and p2 > pb:
					self.grid[i,j] =  0
				elif test == 1 and p1 > pb:
					self.grid[i,j] =  2
				else:
					return self.grid
				return self.grid

	def avg_Infect(self):
		I = 0  # self.n*self.n
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i, j] == 1:
					I += 1
		avg_I = I / (self.n * self.n)

		return avg_I

	def avg_sus(self):
		I = self.n * self.n
		for i in range(self.n):
			for j in range(self.n):
				if self.grid[i, j] == 0:
					I -= 1
		avg_I = I / (self.n * self.n)

		avg_i2 = (I ** 2) / (self.n * self.n)

		var = (avg_i2 - (avg_I ** 2)) / (self.n * self.n)

		return avg_I, var


def update(frameNum, img, grid):
	# for i in range(10):
	new = Gol_sirs.gol_Update(grid)
	img.set_data(new)

	return (img,)


def update_s(frameNum, img, grid, g, sus, num):
	for i in range(50):
		new = Gol_sirs.sirs_Update(grid, g, sus, num * num)
		img.set_data(new)

	return (img,)


'''
pulsing parameters:
    p1 = .9
    p2 = .095
    p3 = .01

Dynamic parameters:
    p1 = .5
    p2 = .5
    p3 = .5

Absorbing parameters:
    p1 = .6
    p2 = .5
    p3 = .2


'''


def main():
	print('\n\nThis is the Simulation Program\n\n')
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
			                ' 3 = oscillator\n 4 = Absorbing state\n \nSIRS\n' +
			                '5 = SIRS\n'))
			if mod < 1 or mod > 5:
				raise ValueError
			else:
				break
		except(ValueError):
			print('Please input a valid option')
	if mod == 5:
		while True:
			try:
				p1 = float(input('Simulation parameter -->  p1 = '))
				p2 = float(input('Simulation parameter -->  p2 = '))
				if p1 > 1 or p1 < 0 or p2 > 1 or p2 < 0:
					raise ValueError
				else:
					break
			except(ValueError):
				print('please input a valid option')

	if mod == 5:
		while True:
			try:
				seed = int(input('Select Random or Seed statring state:\n' +
				                 ' 0 = Random\n 1 = Seed\n'))
				if seed > 1 or seed < 0:
					raise ValueError
				else:
					break
			except(ValueError):
				print('please input a valid option')

	else:
		seed = 0

	####_create grid object_####
	g = Gol_sirs(num, mod, seed)

	#####_Animations_#####
	if mod != 5:
		fig, ax = plt.subplots()
		img = ax.imshow(g.grid, animated=True, vmin=0,
		                vmax=1, cmap=cm.prism)
		ani = animate.FuncAnimation(fig, update, fargs=(img, g,), frames=10,
		                            repeat=True, blit=True, interval=100)
	if mod == 5:
		print(len(g.grid))
		fig, ax = plt.subplots()
		g.sirs_Update(p1, p2, 5000)
		img = ax.imshow(g.grid, animated=True, vmin=0, vmax=2,)
		fig.colorbar(img)
		plt.xlabel('0 = susecptible  1 = infected  2 = recovered')
		ani = animate.FuncAnimation(fig, update_s, fargs=(img, g, p1, p2, num,),
		                            frames=10,
		                            repeat=True,
		                            blit=True,
		                            interval=1)

	return ani


if __name__ == "__main__":
	ani = main()
	plt.show()

