#!/usr/bin/env python3

from vapory import *
from math import sqrt
from moviepy.editor import VideoClip

#each object has 2 3 vectors, first for position second for velocity.


#INITIAL CONSTANTS
#EDIT HERE

#sampling frequency in hertz

sampleFreq = 1000;

#Gravity constant, increase for stronger gravity, or increase the mass

Gconst = 100;

#simulation time in seconds

simulationTime = 120;

#video steeings
#ideally framerate should divide sampleFreq, it must not be greater than sampleFreq, code breaks if so
framerate = 30;
frameheight = 1080
framewidth = 1920
videoname="anim3.mp4"

#rendering settings
#texture for sphere, currently purple.
tex = Texture( Pigment( 'color', [1, 0, 1] )) #standard texture for sphere
camera = Camera( 'location', [0, 20, -30], 'look_at', [0, 0, 0] ) #camera location
light = LightSource( [2, 4, -3], 'color', [1, 1, 1] ) #light location and angle/color







#simulation code below
class Orbitor:
    def __init__(self, initPos, initVel, mass):
        self.position = initPos; #3 list
        self.velocity = initVel; #3 list
        self.mass = mass;

orbitorList = []
def addObject(position, velocity, mass):
    orbitorList.append(Orbitor(position, velocity, mass))


#ORBITOR LIST
#add as many objects as you want here,
#syntax is addObject(position, velocity, mass)
#position and velocity are written as [x, y, z] 
addObject([10, 0, 0], [0, 1, 0], 1)
addObject([-10, 0, 0], [0, -1, 0], 1)
addObject([0, 10, 0], [0, 0, -1], 1)
addObject([0, -10, 0], [0, 0, 1], 1)




def stepDiffeq():
    for curframe in range(sampleFreq//framerate): #simulate movement to next frame
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
    return


def createScene():
    
    

    objs = [light]

    #add all the objects in

    for i in orbitorList:
        objs.append(Sphere([i.position[0], i.position[1], i.position[2]], sqrt(i.mass), tex))
    return Scene(camera, objects=objs)

def renderScene(sn):
    return sn.render(width=framewidth, height=frameheight, antialiasing=0.001)

#we doing this functionally apparently
#need an argument here for functional reasons
    
def createFrame(unused):
    stepDiffeq()
    return renderScene(createScene())
#stolen from http://zulko.github.io/blog/2014/11/13/things-you-can-do-with-python-and-pov-ray/
VideoClip(createFrame, duration=simulationTime).write_videofile(videoname, fps=framerate)

