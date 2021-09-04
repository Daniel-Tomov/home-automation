# My Home Automation

This skill first started out as triggering one relay with Mycroft voice recognition. Then, I wanted to add a webserver to control the relay as well. Since my Raspberry Pi 2 does not support Home Assistant. Later, I added another relay and a script that uses GPIO pins to take inputs from 2 buttons and a motion detector. I used the motion detector to setup an alarm system that sends emails if it is not turned off. They all communicate through a .csv file.


relay-skill\__init__.py     Is the main file for the Mycroft Skill. It edits the csv file

relay-skill\app.py      Is the main file for the webserver. It edits the csv file 

button.py     Is the file for the 2 buttons and motion detector. It reads the csv file and controls the relays
