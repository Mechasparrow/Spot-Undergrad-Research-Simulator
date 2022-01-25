import os 
import sys 

#environ init
os.environ["WEBOTS_HOME"] = r"C:\Program Files\Webots"
sys.path.append(os.environ["WEBOTS_HOME"] + r'\lib\controller')
sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin')
sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin\cpp')
sys.path.append(os.environ["WEBOTS_HOME"] + r"/lib/controller/python39")

from controller import Robot, Motor
import math

motor_names = [
  "front left shoulder abduction motor",  "front left shoulder rotation motor",  "front left elbow motor",
  "front right shoulder abduction motor", "front right shoulder rotation motor", "front right elbow motor",
  "rear left shoulder abduction motor",   "rear left shoulder rotation motor",   "rear left elbow motor",
  "rear right shoulder abduction motor",  "rear right shoulder rotation motor",  "rear right elbow motor"]

camera_names = ["left head camera", "right head camera", "left flank camera",
                                                      "right flank camera", "rear camera"]

led_names = ["left top led",          "left middle up led", "left middle down led",
                                                "left bottom led",       "right top led",      "right middle up led",
                                                "right middle down led", "right bottom led"]

print("Connecting to robot")
robot = Robot()

larmmotor = Motor("rear left elbow motor")
larmmotor.setPosition(0.5)

rarmmotor = Motor("rear right elbow motor")
rarmmotor.setPosition(0.5)

while robot.step(32) != -1:
    print("Spot working")    
