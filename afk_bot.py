import pyautogui as pag
import random
import time

while True:
    x = random.randint(600, 700)
    y = random.randint(200, 600)
    speed = random.random()
    print("Moving to " + str(x) + ", " + str(y) + " (speed:" + str(speed) + ")")
    pag.moveTo(x, y, speed)
    time.sleep(2)
