#! /usr/bin/env python3
# monte carlo simulation of phase separation

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter
from scipy.signal import convolve
import random

dimension=50
frames=10000

def makeAnimation(gridlist):
    fig,ax=plt.subplots()
    with writer.saving(fig, "llps_monte_carlo.mp4", 100):
        for tval in range(0,len(gridlist)):
            ax.imshow(gridlist[tval], cmap='hot', interpolation='nearest')
            writer.grab_frame()
            plt.cla()

def get_energy(grid):
    def flip_energy(a,b,c): #flips the energy if center is 0
        if a == 0: return c
        elif a == 1: return b
    energy_matrix_1=convolve(grid,kernel,'same')
    energy_matrix_2=convolve(1-grid,kernel,'same')
    energy_matrix=np.vectorize(flip_energy)(grid, energy_matrix_1, energy_matrix_2)
    return np.sum(energy_matrix)

def swap_nos(grid):
    idx_11 = random.randint(0,dimension-1)
    idx_12 = random.randint(0,dimension-1)
    idx_21 = random.randint(0,dimension-1)
    idx_22 = random.randint(0,dimension-1)
    swapped_grid = grid.copy()
    swapped_grid[idx_11,idx_12] = grid[idx_21,idx_22]
    swapped_grid[idx_21,idx_22] = grid[idx_11,idx_12]
    return swapped_grid

metadata = dict(title='monte_carlo_llps', artist='k')
writer = FFMpegWriter(fps=15, metadata=metadata)

grid=np.random.randint(2,size=(dimension,dimension))
kernel = np.array([[0,-1,0],[-1,0,-1],[0,-1,0]])

gridlist = [grid]

while len(gridlist) < frames:
    oldgrid = gridlist[-1]
    old_energy = get_energy(oldgrid)
    newgrid = swap_nos(oldgrid)
    new_energy = get_energy(newgrid)
    if new_energy <= old_energy:
        gridlist.append(newgrid)

makeAnimation(gridlist)
