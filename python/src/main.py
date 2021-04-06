#!/usr/bin/python
import sys;
import os;
import time;
import signal;
import serial;

from flask import Flask, jsonify, render_template;
from threading import Thread;

import disp;
import sim;
import func;

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

doLoop = True;
isRunning = False;
currentStats = "";
currentLine1 = "";
currentLine2 = "";
simgood = False;

#func.print_test();
disp.init_display();
serInput = serial.Serial('/dev/ttyUSB0',9600);
serInput.flushInput();

app = Flask(__name__);

def check_for_input():
    #func.log('main.py', 'check_for_input', 'start');
    global currentLine1, currentLine2;
    rec_buff = '';
    time.sleep(0.25);
    if serInput.inWaiting():
        time.sleep(0.01);
        rec_buff = serInput.read(serInput.inWaiting());

    if "S" in rec_buff.decode():
        turn_off_sim();
    else:
        currentLine2 = currentLine2 + rec_buff.decode();
    
    resp = str(rec_buff.decode());
    if len(resp) > 0:
        func.log('main.py', 'check_for_input', 'rec_buff: ' + rec_buff.decode());
    #func.log('main.py', 'check_for_input', 'end');
    return resp;

def check_sim_notification():
    #func.log('main.py', 'check_sim_notification', 'start');
    global currentLine1, currentLine2, simgood;
    msg = sim.check_for_msg();
    if (len(msg) > 0):
        if "PB DONE" in msg:
            simgood = True;
            currentLine1 = "Ready";
            currentLine2 = "";
            
        if "RING" in msg:
            currentLine1 = "INCOMING CALL:";
            currentLine2 = "";

        if "MISSED" in msg:
            currentLine1 = "MISSED CALL: ";
            currentLine2 = msg;
    #func.log('main.py', 'check_sim_notification', 'end');

def turn_on_sim():
    global currentLine1, currentLine2;
    currentLine1 = "turning on sim";
    currentLine2 = "";
    sim.power_on();

def turn_off_sim():
    global currentLine1, currentLine2, simgood;
    simgood = False;
    currentLine1 = "turning off sim";
    currentLine2 = "";
    sim.power_off();

@app.route('/')
def index():
    global currentLine1;
    currentLine1 = "Index Triggered";
    #disp.display_text("Index hit");
    return render_template('index.html');


@app.route('/service/jsontest/')
def json_test():
    mybody = "This is my json test";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/service/makecall/<number>')
def make_call(number):
    global currentLine1, currentLine2;
    currentLine1 = "Making call: ";
    currentLine2 = number;
    mybody = 'Making phone call to ' + str(number);

    #disp.display_text("Calling " + number);
    #sim.make_call(number);
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    #return resp_obj;
    return jsonify(resp_obj);

@app.route('/nametest/<name>')
def nametest(name):
    global currentLine1, currentLine2;
    currentLine1 = "";
    currentLine2 = name;
    return render_template('name.html', name=name);

def myloop():
    global doLoop, isRunning, simgood;
    global currentStats, currentLine1, currentLine2
    if isRunning == False:
        isRunning = True;
        turn_on_sim();
        start_time = time.time();
        while doLoop:
            try:
                #func.log('main.py', 'myloop', 'looping...');
                if (simgood):
                    currentStats = sim.check_voltage();

                if (time.time() - start_time > 1):
                    start_time = time.time();
                    disp.update_disp(currentStats, currentLine1, currentLine2);
                
                check_sim_notification();
                check_for_input();

            except :
                func.log('main.py', 'myloop', 'Exception (' + str(sys.exc_info()[0]) + ') has been caught.');

def start_flask():
    func.log('main.py', 'start_flask', 'Flask running');
    app.run(debug=False, host='0.0.0.0');

if __name__ == '__main__':
    try:
        thread1 = Thread(target=myloop);
        thread2 = Thread(target=start_flask);
        thread1.start();
        thread2.start();
        thread1.join();
        thread2.join();
    except :
        func.log('main.py', '__main__', 'Exception (ID: {}) has been caught. Cleaning up...'.format(signal));
        disp.cleanup();
        exit(0);
