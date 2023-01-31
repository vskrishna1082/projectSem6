#! /usr/bin/env python3

'''------------------------------------
'Phase Separation' in 2-D lattice

Monte-Carlo Simulation of phase sepa-
ration with two 'states'. The 'states'
has a short-range attraction i.e. int-
eration energy is -1 if two states are
adjacent, else 0.

Starts with random mixture of phases
Output file: llps_monte_carlo.mp4
------------------------------------'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter, PillowWriter
from scipy.signal import convolve
import random

dimension=50
frames=10000

# Convert a list of numpy arrays into a video

def makeAnimation(gridlist):
    fig,ax=plt.subplots()
    with writer.saving(fig, "llps_monte_carlo.mp4", 100):
        for tval in range(0,len(gridlist)):
            ax.imshow(gridlist[tval], cmap='hot', interpolation='nearest')
            writer.grab_frame()
            plt.cla()

# Calculates total interaction energy for a configuration

def get_energy(grid):
    def flip_energy(a,b,c): #flips the energy if center is 0
        if a == 0: return c
        elif a == 1: return b

    # use convolution to extract sum of adjacent squares for ever point
    energy_matrix_1=convolve(grid,kernel,'same')

    # repeat the same after swapping 0s and 1s
    energy_matrix_2=convolve(1-grid,kernel,'same')

    # calculate final per-position interaction energies
    energy_matrix=np.vectorize(flip_energy)(grid, energy_matrix_1, energy_matrix_2)

    return np.sum(energy_matrix)

# Monte Carlo step: Randomly swap two gridpoints
def swap_nos(grid):
    idx_11 = random.randint(0,dimension-1)
    idx_12 = random.randint(0,dimension-1)
    idx_21 = random.randint(0,dimension-1)
    idx_22 = random.randint(0,dimension-1)
    swapped_grid = grid.copy()
    swapped_grid[idx_11,idx_12] = grid[idx_21,idx_22]
    swapped_grid[idx_21,idx_22] = grid[idx_11,idx_12]
    return swapped_grid

# Generate initial random/homogeneous configuration
grid=np.random.randint(2,size=(dimension,dimension))
kernel = np.array([[0,-1,0],[-1,0,-1],[0,-1,0]])

gridlist = [grid]

# Apply Monte Carlo Steps
while len(gridlist) < frames:
    oldgrid = gridlist[-1]
    old_energy = get_energy(oldgrid)
    newgrid = swap_nos(oldgrid)
    new_energy = get_energy(newgrid)
    # Accept if move does not increase energy
    if new_energy <= old_energy:
        gridlist.append(newgrid)

# Convert 'gridlist' into an animation
metadata = dict(title='monte_carlo_llps', artist='k')
writer = FFMpegWriter(fps=15, metadata=metadata)
makeAnimation(gridlist)
