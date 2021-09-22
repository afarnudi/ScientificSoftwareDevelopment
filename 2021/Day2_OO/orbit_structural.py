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

N=3

planetCoords, planetVels = planetInit(N)

tailLength=50
tails = np.ones((N,tailLength,2))*planetCoords.reshape(N,1,2)

from matplotlib.pyplot import cm
colors = cm.rainbow(np.linspace(0,1,N))

lines =[]
for c in colors:
    lines.append(ax.plot([],[],'.',ms=20, c= c)[0])
    lines.append(ax.plot([],[],ms=10, c= c)[0])

def animate(i,planetCoords,planetVels,tails, lines):
    G = 0.00002
    planetCoords, planetVels = VelocityVerlet(planetCoords, planetVels, G)
    
    tails[:,:-1] = tails[:,1:]
    tails[:,-1] =  planetCoords
    
    for i in range(planetCoords.shape[0]):
        lines[i*2].set_data(planetCoords[i,0],planetCoords[i,1])  # update the data
        lines[i*2+1].set_data(tails[i,:,0],tails[i,:,1])  # update the data
    return lines

ani = animation.FuncAnimation(fig, animate, 
                              fargs=(planetCoords,planetVels,tails, lines),
                              interval=2, 
                              blit=True,
                              )






