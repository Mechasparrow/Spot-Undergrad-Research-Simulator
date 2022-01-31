

from enum import Enum
from tkinter.tix import WINDOW
import os 
import sys 

class OS_ENV(Enum):
    WINDOWS = 1

def init_webots(env: OS_ENV):
    if (env == OS_ENV.WINDOWS):
        os.environ["WEBOTS_HOME"] = r"C:\Program Files\Webots"
        sys.path.append(os.environ["WEBOTS_HOME"] + r'\lib\controller')
        sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin')
        sys.path.append(os.environ["WEBOTS_HOME"] + r'\msys64\mingw64\bin\cpp')
        sys.path.append(os.environ["WEBOTS_HOME"] + r"/lib/controller/python39")
