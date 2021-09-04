from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
#from gpiozero import Servo
import sys
import socket
import array
import os
import time
import pandas as pd
import csv
import subprocess
#import incServo
#import decServo
import _csv as csv


#GPIO.setup(11, GPIO.OUT)
#servo = GPIO.PWM(11, 500)
#servo.start(0)
array = []

#servo = Servo(17)
lights = 0
servostatus = 50
#os.system('sudo pigpiod')

class Relay(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True
        #os.system('sudo pigpiod')
        #subprocess.run(["python3", "/opt/mycroft/skills/relay-skill/app.py"])
        

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get('my_setting')
        #os.system('sudo pigpiod')
        

    @intent_handler('desk_on.intent')
    def desk_on_intent(self, message):
        global array
        array = []
        with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
        array[0] = 1
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        self.speak_dialog("turnon")
        
        
    @intent_handler('desk_off.intent')
    def desk_off_intent(self, message):
        global array
        array = []
        with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
        array[0] = 0
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        self.speak_dialog("turnoff")
        
        
        ###############################################################################################################
        
    @intent_handler('office_on.intent')
    def office_on_intent(self, message):
        global array
        array = []
        with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
        array[1] = 1
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        self.speak_dialog("turnon")
        
        
    @intent_handler('office_off.intent')
    def office_off_intent(self, message):
        global array
        array = []
        with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
        array[1] = 0
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        self.speak_dialog("turnoff")
  ##############################################################################
  
    @intent_handler('alarm_on.intent')
    def alarm_on_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        global array
        array = []
        with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
        array[2] = 1
        array[3] = 1
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        self.speak_dialog("turnon")
        
        
    @intent_handler('alarm_off.intent')
    def alarm_off_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        global array
        array = []
        with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
        array[2] = 0
        array[3] = 0
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        self.speak_dialog("turnoff")
    '''      
    @intent_handler('increase.intent')
    def increase_intent(self, message):
        global servostatus
        
        if (servostatus >= 100):
            #servostatus = 100
            self.speak_dialog("alreadymax")
            servo.ChangeDutyCycle(100)
        elif (servostatus < 100):
            servostatus = servostatus + 10
            self.speak_dialog("increase")
            #os.system("python3 /opt/mycroft/skills/relay-skill/incServo.py")
            #Servo(33).min()
            servo.ChangeDutyCycle(servostatus)
        
    @intent_handler('decrease.intent')
    def decrease_intent(self, message):
        global servostatus
        if (servostatus <= 0):
            #servostatus = 0
            servo.ChangeDutyCycle(servostatus)
            self.speak_dialog("alreadymin")
        elif (servostatus > 0):
            servostatus = servostatus - 10
            self.speak_dialog("decrease")
            #os.system("python3 /opt/mycroft/skills/relay-skill/decServo.py")
            #Servo(33).max()
            servo.ChangeDutyCycle(0)
    '''
        
        
    def stop(self):
        pass


def create_skill():
    return Relay()
    