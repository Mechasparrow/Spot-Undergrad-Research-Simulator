from enum import Enum
import string
from tokenize import Double
import webots_init

webots_init.init_webots(webots_init.OS_ENV.WINDOWS)

from controller import Supervisor, Motor,PositionSensor

class LegLocation(Enum):
    LEFT=1
    RIGHT=2
    REAR=3
    FRONT=4

    def __str__(self):
        return self.name.lower()

class MotorType(Enum):
    ELBOW=1
    SHOULDER=2
    ABDUCTION=3

    def __str__(self):
        if (self == MotorType.SHOULDER):
            return "shoulder rotation"
        elif (self == MotorType.ABDUCTION):
            return "shoulder abduction"
        else:
            return self.name.lower()
   
def sit_task_init(spot_robot):
     spot_robot.task_data["goal_shoulder_motor"] = -0.99
     spot_robot.task_data["goal_elbow_motor"] = 1.59
     spot_robot.task_data["current_shoulder_pos"] = spot_robot.getShoulderRotationMotor(LegLocation.LEFT,LegLocation.REAR).getTargetPosition()
     spot_robot.task_data["current_elbow_pos"] = spot_robot.getElbowMotor(LegLocation.LEFT,LegLocation.REAR).getTargetPosition()

     spot_robot.task_data["delta_elbow"] = (spot_robot.task_data["goal_elbow_motor"] - spot_robot.task_data["current_elbow_pos"]) / (spot_robot.task_data["steps_to_complete_move"])
     spot_robot.task_data["delta_shoulder"] = (spot_robot.task_data["goal_shoulder_motor"] - spot_robot.task_data["current_shoulder_pos"]) / (spot_robot.task_data["steps_to_complete_move"])

def sit_task_act(spot_robot):
    for x in [LegLocation.LEFT,LegLocation.RIGHT]:
        for y in [LegLocation.FRONT,LegLocation.REAR]:
            elbow_motor = spot_robot.getElbowMotor(x, y)
            shoulder_motor = spot_robot.getShoulderRotationMotor(x, y)  

            current_shoulder_motor_position = shoulder_motor.getTargetPosition()
            current_elbow_motor_position = elbow_motor.getTargetPosition()

            shoulder_motor.setPosition(current_shoulder_motor_position + spot_robot.task_data["delta_shoulder"])
            elbow_motor.setPosition(current_elbow_motor_position + spot_robot.task_data["delta_elbow"])

def stand_task_init(spot_robot):
    spot_robot.task_data["goal_shoulder_motor"] = 0
    spot_robot.task_data["goal_elbow_motor"] = 0
    spot_robot.task_data["current_shoulder_pos"] = spot_robot.getShoulderRotationMotor(LegLocation.LEFT,LegLocation.REAR).getTargetPosition()
    spot_robot.task_data["current_elbow_pos"] = spot_robot.getElbowMotor(LegLocation.LEFT,LegLocation.REAR).getTargetPosition()

    spot_robot.task_data["delta_elbow"] = (spot_robot.task_data["goal_elbow_motor"] - spot_robot.task_data["current_elbow_pos"]) / (spot_robot.task_data["steps_to_complete_move"])
    spot_robot.task_data["delta_shoulder"] = (spot_robot.task_data["goal_shoulder_motor"] - spot_robot.task_data["current_shoulder_pos"]) / (spot_robot.task_data["steps_to_complete_move"])

def stand_task_act(spot_robot):
    sit_task_act(spot_robot)

class SpotSimRobot():
    def __init__(self, webots_robot: Supervisor):
        self.robot = webots_robot
        self.time_step = self.robot.getBasicTimeStep()

        self.tasks = []
        self.task_data = None        
        self.running_task = None

    def getMotorPosition(self, x_side: LegLocation, y_side: LegLocation, motor_type:MotorType):
        sensor = PositionSensor(f'{y_side} {x_side} {motor_type} sensor') 
        return sensor

    def getMotor(self, x_side: LegLocation, y_side: LegLocation, motor_type: MotorType):
        motor = Motor(f'{y_side} {x_side} {motor_type} motor')
        return motor

    def getElbowMotor(self,x_side: LegLocation, y_side: LegLocation) -> Motor:
        return Motor(f'{y_side} {x_side} elbow motor')

    def getShoulderRotationMotor(self,x_side: LegLocation, y_side: LegLocation) -> Motor:
        return Motor(f'{y_side} {x_side} shoulder rotation motor')

    def getShoulderAbductionMotor(self,x_side: LegLocation, y_side: LegLocation) -> Motor:
        return Motor(f'{y_side} {x_side} shoulder abduction motor')

    def scheduleTask(self, task:str, task_duration: Double):
        self.tasks = [(task, task_duration)] + self.tasks

    def runSelectedTask(self):
        # First time running task
        if (self.task_data == None):
            task, duration = self.running_task
            self.task_data = {
                "task": task,
                "duration": duration,
                "step_counter": 0,
                "steps_to_complete_move": (duration * 1000 / self.time_step)
            }

            print("Task initialized")

            if (task == "SIT"):
                sit_task_init(self)
            elif (self.task_data["task"] == "SLEEP"):
                pass
            elif(task == "STAND"):
                stand_task_init(self)
                print(self.task_data)

        self.task_data["step_counter"] += 1

        if (self.task_data["task"] == "SIT"):
            sit_task_act(self)
        elif (self.task_data["task"] == "SLEEP"):
            pass
        elif(self.task_data["task"] == "STAND"):
            stand_task_act(self)

        if (self.task_data["step_counter"] > self.task_data["steps_to_complete_move"]):
            print("Task complete")
            self.cleanupTask()

    def cleanupTask(self):
        self.task_data = None
        self.running_task = None

    def selectTask(self):
        if (len(self.tasks) > 0):
            self.running_task = self.tasks.pop()
            return True
        else:
            return False 

    def taskSelected(self):
        return self.running_task != None