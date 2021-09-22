#Setup a plot with the sun and a planet
# I will create an animation scene
# I will make the planet move.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

from orbit_structural_modules import planetCoordInit

fig, ax = plt.subplots()
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_aspect('equal')

ax.plot([0],[0],'o',ms=30, c='gold')


planetCoords = planetCoordInit()
planetVels   = np.asarray([0.0,0.5])*0.01


line1, =ax.plot([],[],'b.',ms=20)

def animate(i,planetCoords,planetVels):
    #VelocityVerlet
    G = 0.00002
    deltaRMag = np.sqrt(np.sum(np.square(planetCoords)))
    AcceDir  = -planetCoords/deltaRMag
    AcceMag  = G/deltaRMag**2
    Acce_n_1  = AcceMag*AcceDir
    
    planetCoords += 0.5*AcceMag*AcceDir + planetVels
    deltaRMag = np.sqrt(np.sum(np.square(planetCoords)))
    AcceDir  = -planetCoords/deltaRMag
    AcceMag  = G/deltaRMag**2
    
    planetVels   += 0.5*(AcceMag*AcceDir + Acce_n_1) 
    
    
    line1.set_data(planetCoords[0],planetCoords[1])  # update the data
    return line1,

ani = animation.FuncAnimation(fig, animate, 
                              fargs=(planetCoords,planetVels),
                              interval=2, 
                              blit=True,
                              )






