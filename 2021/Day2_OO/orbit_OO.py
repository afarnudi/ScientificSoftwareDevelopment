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
        return vxy*0.005
    def getCoords(self):
        return self.xy
    def evolveTimeStep(self, G):
        self.calcAcc()
        f_n_1 = np.copy(self.acc)
        self.xy += self.vxy + 0.5*self.acc
        self.calcAcc()
        self.vxy += 0.5*(f_n_1 + self.acc)
    def calcAcc(self):
        self.r = np.sqrt(np.sum(np.square(self.xy)))
        self.accDir = -self.xy/self.r
        self.acc = self.accDir*G/self.r**2
    def getColour(self):
        return self.color


class Earth(Planet):
    def __init__(self):
        Planet.__init__(self)
        self.vxy*=0.1
        self.color = [0.09607843, 0.80538092, 0.89240058, 1.        ]
    def calcAcc(self):
        self.r = np.sqrt(np.sum(np.square(self.xy)))
        self.accDir = -self.xy/self.r
        self.acc = self.accDir*G*0.1/self.r**2
        
        
class Jupiter(Planet):
    def __init__(self):
        Planet.__init__(self)
        self.color = [1.,         0.41796034, 0.21393308, 1.        ]

fig, ax = plt.subplots()
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)
ax.set_aspect('equal')

ax.plot([0],[0],'o',ms=30, c='gold')

N= 50

planets = []
for i in range(N):
    if np.random.rand()<0.5:
        planets.append(Earth())
    else:
        planets.append(Jupiter())



G = 0.00002
lines =[]
for planet in planets:
    lines.append(ax.plot([],[],'.',ms=20, c=planet.getColour()  )[0] )



def animate(i,earth, lines):
    
    for planet, line in zip(planets,lines):
        planet.evolveTimeStep(G)    
        line.set_data(planet.getCoords()[0],planet.getCoords()[1])  # update the data
    return lines

ani = animation.FuncAnimation(fig, animate, 
                              fargs=(planets,lines),
                              interval=2, 
                              blit=True,
                              )



class CelestialObject():
    def __init__(self, name, coords, vels):
        self.name = name
        self.coordinates = coords
        self.velocity = vels
    
    
class Palnet(CelestialObject):
    def __init__(self, name, coords, vels, moons):
        CelestialObject.__init__(name, coords, vels)
        self.number_of_moons = moons
        self.atmosphere = False

class Palnet(CelestialObject):
    def __init__(self, name, coords, vels, temperature):
        CelestialObject.__init__(name, coords, vels)
        self.temperature = temperature


earth = Planet('Earth', [0,0], [-1,2], 1)
mars  = Planet('Mars',  [10,0], [-4,3], 2)



        
        
        
        
        















