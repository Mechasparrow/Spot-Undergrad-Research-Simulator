from matplotlib import backends
import roboticstoolbox as rtb
from roboticstoolbox.backends.swift import Swift

robot = rtb.models.URDF.Panda()  # load URDF version of the Panda
print(robot)    # display the model

from spatialmath import SE3

T = SE3(0.7, 0.2, 0.1) * SE3.OA([0, 1, 0], [0, 0, -1])
sol = robot.ikine_LM(T)         # solve IK
print(sol)

q_pickup = sol.q
print(robot.fkine(q_pickup))    # FK shows that desired end-effector pose was achieved

qt = rtb.jtraj(robot.qz, q_pickup, 50)
robot.plot(qt.q, movie='panda1.gif')