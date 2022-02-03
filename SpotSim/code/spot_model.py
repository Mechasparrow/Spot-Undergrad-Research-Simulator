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
   
def pos_task_init(spot_robot, extra_data):
    shoulder_motor_goal_pos, elbow_motor_goal_pos = extra_data

    spot_robot.task_data["goal_shoulder_motor"] = shoulder_motor_goal_pos
    spot_robot.task_data["goal_elbow_motor"] = elbow_motor_goal_pos

    legs_to_control = spot_robot.task_data["legs_to_control"]
    
    spot_robot.task_data["position_tracking"] = {}
    for x, y in legs_to_control:
        spot_robot.task_data["position_tracking"][(x,y)] = {}
        spot_robot.task_data["position_tracking"][(x,y)]["current_shoulder_pos"] = spot_robot.getMotor(x,y, MotorType.SHOULDER).getTargetPosition()
        spot_robot.task_data["position_tracking"][(x,y)]["current_elbow_pos"] = spot_robot.getMotor(x,y, MotorType.ELBOW).getTargetPosition()
        spot_robot.task_data["position_tracking"][(x,y)]["delta_elbow"] = (spot_robot.task_data["goal_elbow_motor"] - spot_robot.task_data["position_tracking"][(x,y)]["current_elbow_pos"]) / (spot_robot.task_data["steps_to_complete_move"])
        spot_robot.task_data["position_tracking"][(x,y)]["delta_shoulder"] = (spot_robot.task_data["goal_shoulder_motor"] - spot_robot.task_data["position_tracking"][(x,y)]["current_shoulder_pos"]) / (spot_robot.task_data["steps_to_complete_move"])

def pos_task_act(spot_robot):
    legs_to_control = spot_robot.task_data["legs_to_control"]

    for x, y in legs_to_control:
        elbow_motor = spot_robot.getMotor(x, y, MotorType.ELBOW)
        shoulder_motor = spot_robot.getMotor(x, y, MotorType.SHOULDER)  

        current_shoulder_motor_position = shoulder_motor.getTargetPosition()
        current_elbow_motor_position = elbow_motor.getTargetPosition()

        shoulder_motor.setPosition(current_shoulder_motor_position + spot_robot.task_data["position_tracking"][(x,y)]["delta_shoulder"])
        elbow_motor.setPosition(current_elbow_motor_position + spot_robot.task_data["position_tracking"][(x,y)]["delta_elbow"])

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

    def scheduleTask(self, task:str, task_duration: Double, motor_mask = (True, True, True, True), extra_data = None):
        self.tasks = [(task, task_duration, motor_mask, extra_data)] + self.tasks

    def runSelectedTask(self):
        # First time running task
        if (self.task_data == None):
            task, duration, motor_mask, extra_data = self.running_task
            self.task_data = {
                "task": task,
                "duration": duration,
                "step_counter": 0,
                "steps_to_complete_move": (duration * 1000 / self.time_step)
            }

            self.task_data["legs_to_control"] = []

            i = 0
            for leg_x in [LegLocation.LEFT, LegLocation.RIGHT]:
                for leg_y in [LegLocation.REAR, LegLocation.FRONT]:
                    control_motor = motor_mask[i]

                    if (control_motor == True):
                        self.task_data["legs_to_control"].append((leg_x,leg_y))

                    i+=1

            print(self.task_data["legs_to_control"])

            print("Task initialized")

            if (task == "SIT"):
                pos_task_init(self, (-0.99, 1.59))
            elif (task == "POS"):
                pos_task_init(self, extra_data)
            elif(task == "STAND"):
                pos_task_init(self, (0,0))

        self.task_data["step_counter"] += 1

        if (self.task_data["task"] == "SIT" or self.task_data["task"] == "POS" or self.task_data["task"] == "STAND"):
            pos_task_act(self)
       
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