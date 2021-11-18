#!/usr/bin/python
import sys;
import os;
import time;
import signal;
import subprocess;
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
currentStats = ['', '', ''];
currentLine1 = "";
currentLine2 = "";
simgood = False;
isRinging = False;
inCall = False;

#func.print_test();
disp.init_display();
serInput = serial.Serial('/dev/ttyUSB0',9600,timeout=0.1);
serInput.flushInput();

app = Flask(__name__);

def check_for_input():
    #func.log('main.py', 'check_for_input', 'start');
    global inCall, isRinging, currentLine1, currentLine2;
    rec_buff = '';
    try:
        time.sleep(0.25);
        if serInput.inWaiting():
            time.sleep(0.01);
            rec_buff = serInput.read(serInput.inWaiting());
        resp = str(rec_buff.decode());

        if len(resp) > 0:
            if "S" in rec_buff.decode():
                shutdown();
            elif "H" in rec_buff.decode():
                sim.hangup();
                currentLine1 = 'Hangup';
                currentLine2 = '';
                isRinging = False;
                inCall = False;
            elif "C" in rec_buff.decode():
                if isRinging:
                    sim.answer_call();
                else:
                    sim.make_call(currentLine2);
                    currentLine1 = 'Calling';
                isRinging = False;
                inCall = True;
            else:
                currentLine2 = currentLine2 + rec_buff.decode();
                if inCall:
                    sim.send_tone(rec_buff.decode());
            func.log('main.py', 'check_for_input', 'rec_buff: ' + rec_buff.decode());
    except:
        func.log('main.py', 'check_for_input', 'Exception (' + str(sys.exc_info()[0]) + ') has been caught.');

    #func.log('main.py', 'check_for_input', 'end');
    return resp;

def check_sim_notification():
    try:
        #func.log('main.py', 'check_sim_notification', 'start');
        global inCall, isRinging, currentLine1, currentLine2, simgood;
        msg = sim.check_for_msg();
        if (len(msg) > 0):
            if "PB DONE" in msg:
                simgood = True;
                currentLine1 = "Ready";
                currentLine2 = "";
                
            if "RING" in msg:
                call_info = sim.get_call_info();
                currentLine1 = "INCOMING CALL:";
                currentLine2 = call_info;
                isRinging = True;

            if "MISSED" in msg:
                # |MISSED_CALL: 02:22AM +12076192651|
                currentLine1 = "MISSED CALL: ";
                currentLine2 = msg[14:33];
                isRinging = False;

            if "NO CARRIER" in msg:
                currentLine1 = "NO CARRIER";
                currentLine2 = "";
                inCall = False;
            
            if "VOICE CALL" in msg:
                temp = msg.split('|');
                temp = temp.split(' ');
                currentLine1 = temp[1];
                currentLine2 = temp[2];
                inCall = False
                
    except:
        func.log('main.py', 'check_sim_notification', 'Exception (' + str(sys.exc_info()[0]) + ') has been caught.');

    #func.log('main.py', 'check_sim_notification', 'end');

def get_voltage():
    v = "NA";
    try:
        #result = subprocess.getoutput("echo get battery | nc -q 0 127.0.0.1 8423");
        result = subprocess.check_output(['bash','-c', "echo get battery | nc -q 0 127.0.0.1 8423"]);
        if "battery: " in result:
            v = result[9:];
    except:
        func.log('main.py', 'get_voltage', 'Exception (' + str(sys.exc_info()) + ') has been caught.');
    return v;

def shutdown():
    global currentLine1;
    currentLine1 = "Shutting down...";
    disp.cleanup();
    time.sleep(5);
    os.system("sudo shutdown now");


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

def display_loop():
    global currentStats, currentLine1, currentLine2
    time_disp = time.time();
    while True:
        try:
            #func.log('main.py', 'myloop', 'looping...');
            #if (time.time() - time_disp > 1):
            disp.update_disp(currentStats, currentLine1, currentLine2);
            time_disp = time.time();
        except:
            func.log('main.py', 'display_loop', 'Exception: ' + str(sys.exc_info()[0]) );



def main_loop():
    global doLoop, isRunning, simgood;
    global currentStats, currentLine1, currentLine2
    turn_off_sim();
    turn_on_sim();
    time_updates = time.time();
    while doLoop:
        try:
            #func.log('main.py', 'myloop', 'looping...');s
            if (time.time() - time_updates > 5):
                currentStats[0] = get_voltage();
                if (simgood):
                    currentStats[1] = sim.get_signal();
                    currentStats[2] = sim.get_network();
                time_updates = time.time();
            check_sim_notification();
            check_for_input();
        except:
            func.log('main.py', 'main_loop', 'Exception: ' + str(sys.exc_info()));

def start_flask():
    try:
        func.log('main.py', 'start_flask', 'Flask running');
        app.run(debug=False, host='0.0.0.0');
    except:
        func.log('main.py', 'start_flask', 'Exception: ' + str(sys.exc_info()));

if __name__ == '__main__':
    try:
        thread1 = Thread(target=display_loop);
        thread2 = Thread(target=main_loop);
        #thread3 = Thread(target=start_flask);

        thread1.start();
        thread2.start();
        #thread3.start();
        
        thread1.join();
        thread2.join();
        #thread3.join();
    except :
        func.log('main.py', '__main__', 'Exception (ID: {}) has been caught. Cleaning up...'.format(signal));
        disp.cleanup();
        exit(0);
