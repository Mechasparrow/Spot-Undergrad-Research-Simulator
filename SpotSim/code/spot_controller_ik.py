import ikpy
from ikpy.chain import Chain

from spot_model import MotorType
import tempfile
from spot_model import LegLocation, SpotSimRobot
import webots_init
import time

webots_init.init_webots(webots_init.OS_ENV.WINDOWS)

from controller import Supervisor, Robot, Motor
import os

print("Connecting to Spot robot")

robot = Supervisor()
spot_bot = SpotSimRobot(robot)

# Create the arm chain from the URDF
#rightRearChain = Chain.from_urdf_file("../URDF/spot-rear-right.urdf")
leftRearChain = Chain.from_urdf_file("../URDF/spot-rear-left.urdf")

leftRearChain.active_links_mask[0] = False

#print("Right Rear Leg Chain")
#print(rightRearChain)

print("Left Rear Leg Chain")
print(leftRearChain)

controlling_motors = []
motor_positions = []
for orientation in [LegLocation.LEFT]:
  for motortype in [MotorType.ABDUCTION, MotorType.SHOULDER, MotorType.ELBOW]:

    pos_sensor = spot_bot.getMotorPosition(orientation, LegLocation.REAR, motortype)
    
    motor = spot_bot.getMotor(orientation, LegLocation.REAR, motortype)
    
    pos_sensor.enable(int(spot_bot.time_step))
    
    controlling_motors.append(motor)
    motor_positions.append(pos_sensor)

robot.step(int(spot_bot.time_step))

initial_position = [0] + [m.getValue() for m in motor_positions]


#wheel offset
# Shoulder: -0.6
# Elbow: -1.6

ik_results = leftRearChain.inverse_kinematics([-0.32,0,0], initial_position = initial_position)
offsets = [0, 0.5,0.6, 1.6]

print(ik_results)
for i in range(3):
  print(controlling_motors[i].getName())
  controlling_motors[i].setPosition(ik_results[i+1] - offsets[i+1])

while robot.step(int(spot_bot.time_step)) != -1:

  pass

      
  
