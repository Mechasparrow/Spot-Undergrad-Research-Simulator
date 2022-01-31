import webots_init

webots_init.init_webots(webots_init.OS_ENV.WINDOWS)

from controller import Robot, Motor
import time
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

print("Connecting to robot")
robot = Robot()

time_step = robot.getBasicTimeStep()

goal_shoulder_motor = -0.99
goal_elbow_motor = 1.59

duration = 2

step_counter = 0
steps_for_move = (duration * 1000 / time_step)

current_shoulder_pos = getShoulderRotationMotor("left","rear").getTargetPosition()
current_elbow_pos = getElbowMotor("left", "rear").getTargetPosition()

delta_elbow = (goal_elbow_motor - current_elbow_pos) / (steps_for_move)
delta_shoulder = (goal_shoulder_motor - current_shoulder_pos) / (steps_for_move)

while robot.step(int(time_step)) != -1:
  
  if (step_counter < steps_for_move):
    for x in ["left", "right"]:
      for y in ["rear", "front"]:
        elbow_motor = getElbowMotor(x, y)
        shoulder_motor = getShoulderRotationMotor(x, y)  

        current_shoulder_motor_position = shoulder_motor.getTargetPosition()
        current_elbow_motor_position = elbow_motor.getTargetPosition()

        shoulder_motor.setPosition(current_shoulder_motor_position + delta_shoulder)
        elbow_motor.setPosition(current_elbow_motor_position + delta_elbow)

    step_counter+=1

      
  
