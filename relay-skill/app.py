from flask import Flask, render_template, url_for, redirect, request
import time
import _csv as csv
import os

app = Flask(__name__)


lightstatus = 0
btn1 = False
btn2 = False
btn3 = 'off'

@app.route("/", methods=["POST", "GET"])
def main():
    global lightstatus 
    global btn1
    global btn2
    global btn3
    array = []
    light1 = ''
    light2 = ''
    alarm1 = ''
    alarm2 = ''
    
    with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            array = array + row
        
    
    if request.method == "POST":
        if (request.form['button'] == 'desk_on'):
            btn1 = False
            array[0] = 0
        elif request.form['button'] == 'desk_off':
            btn1 = True
            array[0] = 1
            
            ###################################################
        if request.form['button'] == 'office_on':
            btn2 = False
            array[1] = 0
        elif request.form['button'] == 'office_off':
            btn2 = True
            array[1] = 1
            
            ###################################################
            
        if request.form['button'] == 'settings':
            return redirect(url_for('login'))
            
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        return render_template("index.html", btn1 = btn1, btn2 = btn2, btn3 = btn3)
    else:
        light1 = ''
        light2 = ''
        alarm1 = ''
        alarm2 = ''
        
        light1 = light1 + array[0]
        light2 = light2 + array[1]
        alarm1 = alarm1 + array[2]
        alarm2 = alarm2 + array[3]
        
        light1 = int(light1)
        light2 = int(light2)
        alarm1 = int(alarm1)
        alarm2 = int(alarm2)
        
        if light1 == 1:
            btn1 = True
        elif light1 == 0:
            btn1 = False
        
        if light2 == 1:
            btn2 = True
        elif light2 == 0:
            btn2 = False
            
        if alarm1 == 1 and alarm2 == 1:
            btn3 = 'on'
        elif alarm1 == 0 and alarm2 == 0:
            btn3 = 'off'
        elif alarm2 == 2:
            btn3 = 'waitdisarm'
        elif alarm2 == 3:
            btn3 = 'alarm'
        
        return render_template("index.html", btn1 = btn1, btn2 = btn2, btn3 = btn3)
############################################################################
@app.route("/wrong_code", methods=["POST", "GET"])
def wrong_code():
    return render_template('wrong_code.html')
#######################################################################3
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['login_code'] == '2005':
            if request.form['button'] == 'login':
                return redirect(url_for('settings'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('wrong_code'))
    else:
        return render_template('login.html')
#######################################################################################
@app.route("/settings", methods=["POST", "GET"])
def settings():
    global btn3
    array = []
    alarm1 = ''
    alarm2 = ''
    
    with open('/home/pi/mycroft-core/values.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            array = array + row
    if request.method == "POST":
        if request.form['button'] == 'alarm_off':
            print('turning on')
            btn3 = 'on'
            array[2] = 1
            array[3] = 1
        elif request.form['button'] == 'alarm_on':
            print('turning off')
            btn3 = 'off'
            array[2] = 0
            array[3] = 0
        elif request.form['button'] == 'alarm_waitdisarm':
            print('alarm_waitdisarm')
            btn3 = 'off'
            array[3] = 0
            array[2] = 0
        elif request.form['button'] == 'alarm_alarm':
            print('alarm_alarm')
            btn3 = 'off'
            array[3] = 0
            array[2] = 0
        elif request.form['button'] == 'home':
            return redirect(url_for('main'))
        elif request.form['button'] == 'shutdown':
            os.system('sudo shutdown now')
        elif request.form['button'] == 'restart_motion':
            os.system('sudo systemctl restart button.service')
        elif request.form['button'] == 'restart_webserver':
            os.system('sudo systemctl restart mycroftflask.service')
        elif request.form['button'] == 'refresh':
            os.system('sudo reboot')
        
        
        with open('/home/pi/mycroft-core/values.csv', 'w') as csvwrite:
            writer = csv.writer(csvwrite)
            writer.writerow(array)
        return render_template('settings.html', btn3 = btn3)
    else:
        alarm1 = ''
        alarm2 = ''
        
        alarm1 = alarm1 + array[2]
        alarm2 = alarm2 + array[3]
        
        alarm1 = int(alarm1)
        alarm2 = int(alarm2)
        
        if alarm1 == 1 and alarm2 == 1:
            btn3 = 'on'
        elif alarm1 == 0 and alarm2 == 0:
            btn3 = 'off'
        elif alarm2 == 2:
            btn3 = 'waitdisarm'
        elif alarm2 == 3:
            btn3 = 'alarm'
    return render_template('settings.html', btn3 = btn3)
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
    
 