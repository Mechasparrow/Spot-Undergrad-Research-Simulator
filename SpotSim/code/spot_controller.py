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

for leg_mask in leg_masks:
  spot_bot.scheduleTask("POS", 0.2, leg_mask, (0.0,0.39))


while robot.step(int(spot_bot.time_step)) != -1:

  if (not spot_bot.taskSelected()):
    spot_bot.selectTask()
  else:
    spot_bot.runSelectedTask()

      
  
