import RPi.GPIO as GPIO
import time
import _csv as csv
import os
from email.message import EmailMessage
import smtplib

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT) #Relay 1
GPIO.setup(38, GPIO.OUT) #LED for Relay 1
GPIO.setup(13, GPIO.OUT) #Relay 2
GPIO.setup(36, GPIO.OUT) #LED for Relay 2
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button for Relay 1
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Motion Detector
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button for Relay 2

EMAIL_PASSWORD = 'Your password'
EMAIL_ADDRESS = 'Your email'
RECIEVER_ADDRESS = 'Your receiver'


msg = EmailMessage()
msg['Subject'] = 'Alarm was triggered'
msg['From'] = EMAIL_ADDRESS
msg['To'] = RECIEVER_ADDRESS
msg.set_content('The alarm was triggered by the motion detector')

light1 = ''
light2 = ''
alarm1 = ''
alarmtrg = 1
date = int(time.clock_gettime(time.CLOCK_REALTIME))
date2 = date
date3 = int(time.clock_gettime(time.CLOCK_REALTIME))
date4 = date3

while True:
    #print(GPIO.input(18))
    array = []
    light1 = ''
    light2 = ''
    alarm1 = ''
    
    with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                array = array + row
    #print("Button is on")
    #print(array)
    light1 = light1 + array[0]
    light2 = light2 + array[1]
    alarm1 = alarm1 + array[2]
    
    light1 = int(light1)
    light2 = int(light2)
    alarm1 = int(alarm1)
    
    #Code for Motion detector
    if light1 == 1:
        date = int(time.clock_gettime(time.CLOCK_REALTIME))
        if GPIO.input(18) == 0:
            date = int(time.clock_gettime(time.CLOCK_REALTIME))
            date2 = date + 10
        if date < date2:
            GPIO.output(40, True)
            GPIO.output(38, True)
        elif date > date2:
            GPIO.output(40, False)
            GPIO.output(38, False)
    elif light1 == 0:
        GPIO.output(40, False)
        GPIO.output(38, False)
    
    if light2 == 1:
            GPIO.output(13, True)
            GPIO.output(36, True)
    elif light2 == 0:
        GPIO.output(13, False)
        GPIO.output(36, False)
        
    #Code for the alarm
    if alarm1 == 1:
        #print('The alarm is activated')
        if GPIO.input(18) == 0:
            #print('Motion is detected')
            #print(date3)
            #print(date4)
            if alarmtrg == 1:
                #print('Waiting to be deactivated')
                date3 = int(time.clock_gettime(time.CLOCK_REALTIME))
                date4 = date3 + 60
                alarmtrg = 0
                array[3] = 2   
                with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
                    writer = csv.writer(csvwrite)
                    writer.writerow(array)
        if alarmtrg == 0:
            date3 = int(time.clock_gettime(time.CLOCK_REALTIME))
        if date3 > date4:
            #print('Sending email')
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            date3 = int(time.clock_gettime(time.CLOCK_REALTIME))
            date4 = date3 + 120
            array[3] = 3
            with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
                writer = csv.writer(csvwrite)
                writer.writerow(array)
            
    elif alarm1 == 0:
        alarmtrg = 1
     
    #Code for the button 1
    if GPIO.input(16) == 1: 
        #print(array)
        if  light1 == 0:
            #print("Turning on")
            array[0] = 1
            light1 = 1
            with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
                writer = csv.writer(csvwrite)
                writer.writerow(array)
        elif light1 == 1:
            #print("Turning off")
            array[0] = 0
            light1 = 0
            with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
                writer = csv.writer(csvwrite)
                writer.writerow(array)
        time.sleep(2)
    
    #Code for the button 2
    if GPIO.input(32) == 1:
        #print(array)
        if  light2 == 0:
            #print("Turning on")
            array[1] = 1
            light2 = 1
            with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
                writer = csv.writer(csvwrite)
                writer.writerow(array)
        elif light2 == 1:
            #print("Turning off")
            array[1] = 0
            light2 = 0
            with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
                writer = csv.writer(csvwrite)
                writer.writerow(array)
        time.sleep(2)
    
    time.sleep(0.2)