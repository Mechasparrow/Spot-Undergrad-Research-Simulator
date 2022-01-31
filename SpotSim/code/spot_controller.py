from spot_model import LegLocation, SpotSimRobot
import webots_init

webots_init.init_webots(webots_init.OS_ENV.WINDOWS)

from controller import Robot, Motor

print("Connecting to Spot robot")

robot = Robot()
spot_bot = SpotSimRobot(robot)
spot_bot.scheduleTask("SIT", 2)

while robot.step(int(spot_bot.time_step)) != -1:
  if (not spot_bot.taskSelected()):
    print("No task selected. Pulling task from task queue")
    spot_bot.selectTask()
  else:
    spot_bot.runSelectedTask()
  
  #if (step_counter < steps_for_move):
   # for x in [LegLocation.LEFT,LegLocation.RIGHT]:
    #  for y in [LegLocation.FRONT,LegLocation.REAR]:
     #   elbow_motor = spot_bot.getElbowMotor(x, y)
      #  shoulder_motor = spot_bot.getShoulderRotationMotor(x, y)  

       # current_shoulder_motor_position = shoulder_motor.getTargetPosition()
       # current_elbow_motor_position = elbow_motor.getTargetPosition()

       # shoulder_motor.setPosition(current_shoulder_motor_position + delta_shoulder)
       # elbow_motor.setPosition(current_elbow_motor_position + delta_elbow)

    # step_counter+=1

      
  
