#!/usr/bin/env python3

from vapory import *
from math import sqrt
from moviepy.editor import VideoClip

#Code by Maksym Prokopovych

#code requires vapory, moviepy, and povray (non python utility)


#SETUP CONSTANTS
#EDIT HERE

#sampling frequency in hertz, steps the diffeq, bigger number is more physically accurate

sampleFreq = 9000;

#Gravity constant, increase for stronger gravity, or increase the mass

Gconst = 100;

#simulation time in seconds, length of video essentially

simulationTime = 5;

#video steeings
#ideally framerate should divide sampleFreq, it must not be greater than sampleFreq, code breaks if so
framerate = 30;
frameheight = 1080
framewidth = 1920
videoname="normalorbit.mp4"

#rendering settings
#texture for sphere, currently purple.
tex = Texture( Pigment( 'color', [1, 0, 1] ), Finish('ambient', 1.0)) #standard texture for sphere
camera = Camera( 'location', [10, 10, 10], 'look_at', [0, 0, 0] ) #camera location
light = LightSource( [2, 4, -3], 'color', [1, 1, 1] ) #light location and angle/color



class Orbitor:
    def __init__(self, initPos, initVel, mass, size):
        self.position = initPos; #3 list
        self.velocity = initVel; #3 list
        self.mass = mass;
        self.size = size;

orbitorList = []
def addObject(position, velocity, mass, size):
    orbitorList.append(Orbitor(position, velocity, mass, size))


#ORBITOR LIST
#add as many objects as you want here,
#syntax is addObject(position, velocity, mass)
#position and velocity are written as [x, y, z] 
addObject([0, 0, 0], [0, 10 * sqrt(Gconst)/1000, 0], 1000, 2)
addObject([10, 0, 0], [0, -10 * sqrt(Gconst), 0], 1, 0.1)
#addObject([0, 10, 0], [0, 0, -1], 1)
#addObject([0, -10, 0], [0, 0, 1], 1)



#simulation code below
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------



def stepDiffeq():
    for curframe in range(sampleFreq//framerate): #simulate movement to next frame
        #the actual physics simulation
        for current in orbitorList:
            #Position step loop
            for i in range(len(current.position)):
                current.position[i] += current.velocity[i]/sampleFreq #increment position
        for current in orbitorList:
            #This loop is in theory redundant but intervweaving position and velocity changes ruins symmetry, so we split them 
            for puller in orbitorList:
                if current is not puller: #object does not pull on itself, I can avoid this check by not being dumb and properly indexing nested loops but it looks cleaner this way
                    #calculate pythagorean distance
                    #first we normalize the vector between the two masses to get components to scale the acceleration
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
                        #velocity incremented, we done
    for current in orbitorList:
        print("New position ", current.position) #debug print for fun and profit
    return


def createScene():
    objs = [light]

    #add all the objects

    for i in orbitorList:
        objs.append(Sphere([i.position[0], i.position[1], i.position[2]], i.size, tex))
    return Scene(camera, objects=objs)

def renderScene(sn):
    #rendering of course takes the longest
    #turns out ray tracing is computationally expensive, what a surprise
    return sn.render(width=framewidth, height=frameheight, antialiasing=0.001) 
    
    
#we doing this functionally apparently
#need an argument here for functional reasons
    
def createFrame(unused):
    stepDiffeq()
    return renderScene(createScene())

def onlyPhysics(): #simulate without rendering, probably useful if you want to find out where objects end up, debug log prints all positions
    for i in range(sampleFreq * simulationTime):
        print("Loop ", i)
        stepDiffeq()


        
#stolen from http://zulko.github.io/blog/2014/11/13/things-you-can-do-with-python-and-pov-ray/
VideoClip(createFrame, duration=simulationTime).write_videofile(videoname, fps=framerate)
#onlyPhysics()
