import os 
import sys 

#environ init
os.environ["WEBOTS_HOME"] = r"C:\Program Files\Webots"
sys.path.append(os.environ["WEBOTS_HOME"] + r'\lib\controller')
sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin')
sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin\cpp')
sys.path.append(os.environ["WEBOTS_HOME"] + r"/lib/controller/python39")

print(sys.path)

from controller import Robot, Motor
import math

print("Connecting to robot")
robot = Robot()

lmotor = robot.getDevice("right wheel motor") 
rmotor = robot.getDevice("left wheel motor")


lmotor.setPosition(math.inf)
rmotor.setPosition(math.inf)

lmotor.setVelocity(5)
rmotor.setVelocity(-5)

while robot.step(32) != -1:
    continue    

# Windows
# set webots_home
# append other binaries 
# Python v3.9
# Append path C:\Program Files\Webots\lib\controller;C:\Program Files\Webots\msys64\mingw64\bin;C:\Program Files\Webots\msys64\mingw64\bin\cpp
# set WEBOTS_HOME=C:\Program Files\Webots