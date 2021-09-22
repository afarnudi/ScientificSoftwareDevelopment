#Setup a plot with the sun and a planet
# I will create an animation scene
# I will make the planet move.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fig, ax = plt.subplots()
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_aspect('equal')

ax.plot([0],[0],'o',ms=30, c='gold')

planetCoords = np.asarray([0.7,0])
planetVels   = np.asarray([0.0,0.5])*0.01

G = 0.00002
line1, =ax.plot([],[],'b.',ms=20)

def animate(i,planetCoords,planetVels):
    deltaRMag = np.sqrt(np.sum(np.square(planetCoords)))
    AcceDir  = -planetCoords/deltaRMag
    AcceMag  = G/deltaRMag**2
    
    planetCoords += 0.5*AcceMag*AcceDir + planetVels
    planetVels   += AcceMag*AcceDir 
    
    
    line1.set_data(planetCoords[0],planetCoords[1])  # update the data
    return line1,

ani = animation.FuncAnimation(fig, animate, 
                              fargs=(planetCoords,planetVels),
                              interval=2, 
                              blit=True,
                              )






