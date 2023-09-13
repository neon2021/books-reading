# pip install playsound pyttsx3
# OR
# pip install playsound pypiwin32

import os
import time
from datetime import datetime
from playsound import playsound
import pyttsx3
import cv2 as cv

engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('volume', 0)
# engine.setProperty('volume', 1.0)

root_dir =os.path.abspath('.')
gunfire_path = os.path.join(root_dir, 'gunfire.wav')