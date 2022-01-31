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

initial_position = [0] + [m.getValue() for m in motor_positions] + [0]
ik_results = leftRearChain.inverse_kinematics([-0.5,0,0])

for i in range(3):
  controlling_motors[i].setPosition(ik_results[i])

#spot_bot.scheduleTask("SIT", 2)
#spot_bot.scheduleTask("STAND", 1)
#spot_bot.scheduleTask("SIT", 2)
#spot_bot.scheduleTask("STAND", 1)
#spot_bot.scheduleTask("SIT", 0.5)

#motor_position = spot_bot.getMotorPosition(LegLocation.LEFT, LegLocation.REAR, MotorType.ELBOW)
#motor_position.enable(int(spot_bot.time_step))

#robot.step(int(spot_bot.time_step))

#print(f"Motor Position of Left Rear: {motor_position.getValue()}")

while robot.step(int(spot_bot.time_step)) != -1:
  #if (not spot_bot.taskSelected()):
   # print("No task selected. Pulling task from task queue")
    #print(f"Motor Position of Left Rear: {motor_position.getValue()}")
    #spot_bot.selectTask()
  #else:
   # spot_bot.runSelectedTask()
  pass

      
  
