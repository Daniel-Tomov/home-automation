from gpiozero import Servo
import time


def decServo():
    servo = Servo(17)
    servo.max()
    time.sleep(.9)
