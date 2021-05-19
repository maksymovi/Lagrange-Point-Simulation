#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import animation

#each object has 2 3 vectors, first for position second for velocity.


#INITIAL CONSTANTS
#EDIT HERE

#sampling frequency in hertz

sampleFreq = 100;

#Gravity constant, increase for stronger gravity, or increase the mass

Gconst = 1;

#simulation time in seconds

simulationTime = 10;

#frame per second of video
#ideally should be a mutiple of simulationFreq, must be greater than samplefreq though
fps = 30;


#DONE

class Orbitor:
    def __init__(self, initPos, initVel, mass):
        self.position = initPos; #3 list
        self.velocity = initVel; #3 list
        self.mass = mass;

orbitorList = []


#ORBITOR LIST
#EDIT HERE
orbitorList.append(Orbitor([1, 0, 0], [0, 1, 0]), 1)
orbitorList.append(Orbitor([-1, 0, 0], [0, -1, 0]), 1)



#initialize the figure to plot on.
fig = plt.figure()
ax = plt.axes(projection='3d')

#we doing this functionally apparently
def generateMovement():
    for _ in range(sampleFreq//fps): #simulate movement to next frame
        #the actual physics simulation
        for current in orbitorList:
            #there is a better way to loop this but eh
            for p, v in zip(current.position, current.velocity):
                p += v/sampleFreq #increment velocity
            for puller in orbitorList:
                if current is not puller: #object does not pull on itself
                    #calculate pythagorean distance
                    #first we normalize the vector between the two masses to get components once we get acceleration
                    vector = []
                    for axis in range(len(current.position)):
                        vector[axis] = puller.position[axis] - current.position[axis]
                        vectorLenSquare = vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2
                        vectorLen = sqrt(vectorLenSquare)
                    for vec in vector:
                        vec /= vectorLen #normalize
                        #now that it is normalized, we calculate acceleration and multiply by normalized vector to get acceleration components

                    acceleration = Gconst * puller.mass / vectorLenSquare #a = G m1 / r^2
                    acceleration /= sampleFreq #scale by the frequency we sample
                    for vec, vel in zip(vector, current.velocity):
                        vel += vec * acceleration
                        #velocity acceleration calculated
                        #display code here, there is a better way to loop this but im lazy
    #calculate frame to return here
    x = []
    y = []
    z = []
    mass = []

    for i in orbitorList:
        x.append(i.position[0])
        y.append(i.position[1])
        z.append(i.position[2])
        mass.append(i.mass)


    return ax.scatter(x, y, z, mass, marker = ".") #return things to plot

#stolen from https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
anim = animation.FuncAnimation(fig, generateMovement, frames=fps*simulationTime, interval = 100//fps)

anim.save('anim.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])

plt.show()
