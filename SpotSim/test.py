import os 
import sys 

# TODO connect to webots from here
sys.path.append(os.environ["WEBOTS_HOME"] + "/lib/controller/python39")

from controller import Robot, Motor
from math import pi, sin

print("Connecting to robot")
robot = Robot()

lmotor = robot.getDevice("right wheel motor") 
rmotor = robot.getDevice("left wheel motor")

F = 2.0   # frequency 2 Hz
t = 0.0   # elapsed simulation time

while robot.step(32) != -1:
    position = sin(t * 2.0 * pi * F)
    lmotor.setPosition(position)
    rmotor.setPosition(position)
    t += 32 / 1000.0

# Windows
# set webots_home
# append other binaries 
# Python v3.9
# Append path C:\Program Files\Webots\lib\controller;C:\Program Files\Webots\msys64\mingw64\bin;C:\Program Files\Webots\msys64\mingw64\bin\cpp
# set WEBOTS_HOME=C:\Program Files\Webots