from pickle import FALSE
from spot_model import MotorType
from spot_model import LegLocation, SpotSimRobot
import webots_init

webots_init.init_webots(webots_init.OS_ENV.WINDOWS)

from controller import Supervisor, Robot, Motor

print("Connecting to Spot robot")

robot = Supervisor()

testFoot = robot.getFromDef("FOOT")


spot_bot = SpotSimRobot(robot)

y = 0.5
x = 0.4

leg_masks = [ (False, False, False, True), (True, False, False, False), (False, True, False, False), (False, False, True, False)]

spot_bot.scheduleTask("POS", 0.5, (True, True, True, True), (-0.541052,0.9320058))



for i in range(10):
  for leg_mask in leg_masks:
    spot_bot.scheduleTask("POS", 0.05, leg_mask, (-0.541052,1.0088))
    spot_bot.scheduleTask("POS", 0.05, leg_mask, (-0.1937315,1.0088))
    spot_bot.scheduleTask("POS", 0.05, leg_mask, (-0.1937315,0.855211))

  spot_bot.scheduleTask("POS", 0.3, (True, True, True, True), (-0.541052,0.9320058))

spot_bot.scheduleTask("STAND", 0.5)  


while robot.step(int(spot_bot.time_step)) != -1:

  if (not spot_bot.taskSelected()):
    spot_bot.selectTask()
  else:
    spot_bot.runSelectedTask()

      
  
