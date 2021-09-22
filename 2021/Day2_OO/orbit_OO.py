#Setup a plot with the sun and a planet
# I will create an animation scene
# I will make the planet move.

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


class Planet():
    def __init__(self):
        self.xy  = np.random.rand(2)*2-1
        self.vxy = self.genVelocities()  
    def genVelocities(self):
        vxy = np.zeros(2)
        vxy[0]=np.sqrt(1/(1+self.xy[0]**2/self.xy[1]**2))
        vxy[1]=-vxy[0]*self.xy[0]/self.xy[1]
        return vxy
    def getCoords(self):
        return self.xy
    def evolveTimeStep(self):
        self.xy+=self.vxy

fig, ax = plt.subplots()
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_aspect('equal')

ax.plot([0],[0],'o',ms=30, c='gold')

earth = Planet()

G = 0.00002
line1, =ax.plot([],[],'b.',ms=20)

print(earth.getCoords())

def animate(i,earth):
    earth.evolveTimeStep()    
    
    line1.set_data(earth.getCoords()[0],earth.getCoords()[1])  # update the data
    return line1,

ani = animation.FuncAnimation(fig, animate, 
                              fargs=(earth,),
                              interval=2, 
                              blit=True,
                              )






