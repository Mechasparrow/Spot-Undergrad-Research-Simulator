import os 
import sys 

#environ init
os.environ["WEBOTS_HOME"] = r"C:\Program Files\Webots"
sys.path.append(os.environ["WEBOTS_HOME"] + r'\lib\controller')
sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin')
sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin\cpp')
sys.path.append(os.environ["WEBOTS_HOME"] + r"/lib/controller/python39")

import time
from controller import Robot, Motor
import math


def getElbowMotor(x_side, y_side):
  return Motor(f'{y_side} {x_side} elbow motor')

def getShoulderRotationMotor(x_side, y_side):
  return Motor(f'{y_side} {x_side} shoulder rotation motor')

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

elbow_pos = 0
shoulder_pos = 0

elbow_goal = 1.59
shoulder_goal = -0.80

time_step = robot.getBasicTimeStep()
print(time_step)
steps_to_achieve_target = 3 * 1000 / time_step

while robot.step(int(time_step)) != -1:
  elbow_pos = getElbowMotor("left", "rear").getTargetPosition()
  shoulder_pos = getShoulderRotationMotor("left", "rear").getTargetPosition()
  elbow_step_difference = (elbow_goal - elbow_pos) / steps_to_achieve_target
  shoulder_step_difference = (shoulder_goal - shoulder_pos) / steps_to_achieve_target

  if (elbow_pos < elbow_goal):
    elbow_pos += elbow_step_difference

  if (abs(shoulder_pos) < abs(shoulder_goal)):
    shoulder_pos += shoulder_step_difference

  for x in ["left", "right"]:
    for y in ["rear", "front"]:
      elbow_motor = getElbowMotor(x, y)
      shoulder_motor = getShoulderRotationMotor(x, y)

      
      if (elbow_pos < elbow_goal):
        elbow_motor.setPosition(elbow_pos)
      
      if (abs(shoulder_pos) < abs(shoulder_goal)):
        shoulder_motor.setPosition(shoulder_goal)

  
