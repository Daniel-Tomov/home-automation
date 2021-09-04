from gpiozero import Servo
import time

def incServo():
    servo = Servo(17)
    servo.min()
    time.sleep(.9)
