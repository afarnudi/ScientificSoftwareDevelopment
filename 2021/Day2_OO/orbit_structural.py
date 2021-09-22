#Setup a plot with the sun and a planet
# I will create an animation scene
# I will make the planet move.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

from orbit_structural_modules import planetInit, VelocityVerlet

fig, ax = plt.subplots()
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_aspect('equal')

ax.plot([0],[0],'o',ms=30, c='gold')

planetCoords, planetVels = planetInit()

tailLength=200
tail = np.ones((tailLength,2))*planetCoords

line1, =ax.plot([],[],'b.',ms=20)
line2, =ax.plot([],[],'b',lw=2)

def animate(i,planetCoords,planetVels,tail, line, tailLine):
    G = 0.00002
    planetCoords, planetVels = VelocityVerlet(planetCoords, planetVels, G)
    
    tail[:-1] = tail[1:]
    tail[-1]  = planetCoords
    
    line.set_data(planetCoords[0],planetCoords[1])  # update the data
    tailLine.set_data(tail[:,0],tail[:,1])
    return line, tailLine

ani = animation.FuncAnimation(fig, animate, 
                              fargs=(planetCoords,planetVels,tail, line1, line2),
                              interval=2, 
                              blit=True,
                              )






