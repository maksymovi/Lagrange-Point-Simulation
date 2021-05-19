#!/usr/bin/env python3

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import animation
from math import sqrt
#each object has 2 3 vectors, first for position second for velocity.


#INITIAL CONSTANTS
#EDIT HERE

#sampling frequency in hertz

sampleFreq = 100;

#Gravity constant, increase for stronger gravity, or increase the mass

Gconst = 10;

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
orbitorList.append(Orbitor([1, 0, 0], [0, 1, 0], 1))
orbitorList.append(Orbitor([-1, 0, 0], [0, -1, 0], 1))



#initialize the figure to plot on.
fig = plt.figure()
ax = plt.axes(projection='3d')



def getcoords():

    x = []
    y = []
    z = []
    mass = []
    for i in orbitorList:
        x.append(i.position[0])
        y.append(i.position[1])
        z.append(i.position[2])
        mass.append(i.mass)
    
    return (x, y, z, mass)


curx, cury, curz, mass = getcoords()

points = ax.scatter(curx, cury, curz, s=mass, marker='o') 


#we doing this functionally apparently
#need an argument here for functional reasons
def generateMovement(unused):
    for curframe in range(sampleFreq//fps): #simulate movement to next frame
        print("Simulating ", curframe)
        #the actual physics simulation
        for current in orbitorList:
            #there is a better way to loop this but eh
            for i in range(len(current.position)):
                current.position[i] += current.velocity[i]/sampleFreq #increment velocity
            print("New position ", current.position)
            for puller in orbitorList:
                if current is not puller: #object does not pull on itself
                    #calculate pythagorean distance
                    #first we normalize the vector between the two masses to get components once we get acceleration
                    vector = []
                    for axis in range(len(current.position)):
                        vector.append(puller.position[axis] - current.position[axis])
                    vectorLenSquare = vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2
                    vectorLen = sqrt(vectorLenSquare)
                    for i in range(len(vector)):
                        vector[i] /= vectorLen #normalize
                        #now that it is normalized, we calculate acceleration and multiply by normalized vector to get acceleration components

                    acceleration = Gconst * puller.mass / vectorLenSquare #a = G m1 / r^2
                    acceleration /= sampleFreq #scale by the frequency we sample
                    for i in range(len(vector)):
                        current.velocity[i] += vector[i] * acceleration
                        #velocity acceleration calculated
                        #display code here, there is a better way to loop this but im lazy
    #calculate frame to return here
    x, y, z, mass = getcoords()
    

    print("frame ", unused)
    points.set_data(x, y)
    points.set_3d_properties(z)
    return points
    #ax.clear();
    #return ax.scatter(x, y, z, mass, marker = ".") #return things to plot

#stolen from https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
anim = animation.FuncAnimation(fig, generateMovement, frames=fps*simulationTime, interval = 100//fps)

anim.save('anim.mp4', fps=fps, extra_args=['-vcodec', 'libx264'])

#plt.show()
