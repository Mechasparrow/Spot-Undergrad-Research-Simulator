from spot_model import MotorType
from spot_model import LegLocation, SpotSimRobot
import webots_init

webots_init.init_webots(webots_init.OS_ENV.WINDOWS)

from controller import Supervisor, Robot, Motor

print("Connecting to Spot robot")

robot = Robot()
spot_bot = SpotSimRobot(robot)

spot_bot.scheduleTask("POS", 1, (1.59,-0.99))

spot_bot.scheduleTask("POS", 1, (1.39,-0.99))

spot_bot.scheduleTask("POS", 1, (0.5,-0.99))

while robot.step(int(spot_bot.time_step)) != -1:
  if (not spot_bot.taskSelected()):
    spot_bot.selectTask()
  else:
    spot_bot.runSelectedTask()

      
  
