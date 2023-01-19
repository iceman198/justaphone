#!/usr/bin/python
import sys;
import os;
import time;
import signal;
import subprocess;
import serial;

from flask import Flask, jsonify, render_template;
from threading import Thread;

import sim;
import func;

at_cmd_in_progress = False;
at_cmd_wait_time = 0.1;
stats_check_sleep = 5;
notifications_check_sleep = 0.5;
doLoop = True;
isRunning = False;
currentStats = ['0', '0', '0'];
currentLine1 = "";
currentLine2 = "";
simgood = False;
isRinging = False;
inCall = False;

#func.print_test();

app = Flask(__name__);

def check_sim_notification():
    global at_cmd_in_progress, at_cmd_wait_time;
    try:
        #func.log('main.py', 'check_sim_notification', 'start');
        global inCall, isRinging, currentLine1, currentLine2, simgood;
        while (at_cmd_in_progress):
            time.sleep(at_cmd_wait_time);

        at_cmd_in_progress = True;
        msg = sim.check_for_msg();
        at_cmd_in_progress = False;

        if (len(msg) > 0):
            func.log('main.py', 'check_sim_notification', 'receive msg:' + msg);
            if "PB DONE" in msg:
                simgood = True;
                currentLine1 = "Ready";
                currentLine2 = "";
                
            if "RING" in msg:
                at_cmd_in_progress = True;
                call_info = sim.get_call_info();
                at_cmd_in_progress = False;

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

            #if "ERROR" in msg:
                #simgood = False;
                
    except:
        func.log('main.py', 'check_sim_notification', 'Exception (' + str(sys.exc_info()[0]) + ') has been caught.');

    #func.log('main.py', 'check_sim_notification', 'end');

def get_voltage():
    v = "NA";
    try:
        #result = subprocess.getoutput("echo get battery | nc -q 0 127.0.0.1 8423");
        result = subprocess.check_output(['bash','-c', "echo get battery | nc -q 0 127.0.0.1 8423"]);
        func.log('main.py', 'get_voltage', 'Voltage received: ' + str(result) + '');
        if "battery: " in result:
            v = "B: " + result[9:11] + "%";
    except:
        func.log('main.py', 'get_voltage', 'Exception (' + str(sys.exc_info()) + ') has been caught.');
    return v;

def shutdown():
    global currentLine1;
    currentLine1 = "Shutting down...";
    sim.power_off();
    time.sleep(5);
    os.system("sleep 5; sudo shutdown now");

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
    #disp.display_text("Index hit");
    return render_template('index.html');

@app.route('/shutdown/')
def flask_shutdown():
    mybody = "Shutdown initiated";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    shutdown();
    return jsonify(resp_obj);

@app.route('/checkmessage/<msg_id>')
def flask_getmsg(msg_id):
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);

    at_cmd_in_progress = True;
    respstr = sim.receive_short_message(msg_id);
    at_cmd_in_progress = False;

    resp_obj = {
        'status': "SUCCESS",
        'body': respstr
        }
    return jsonify(resp_obj);

@app.route('/deletemessage/<msg_id>')
def flask_delmsg(msg_id):
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);

    at_cmd_in_progress = True;
    respstr = sim.delete_message(msg_id);
    at_cmd_in_progress = False;

    resp_obj = {
        'status': "SUCCESS",
        'body': respstr
        }
    return jsonify(resp_obj);


@app.route('/sendtestmessage/<number>')
def flask_testmsg(number):
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);

    at_cmd_in_progress = True;
    respstr = sim.send_short_message(number,"this is a test");
    at_cmd_in_progress = False;

    resp_obj = {
        'status': "SUCCESS",
        'body': respstr
        }
    return jsonify(resp_obj);

@app.route('/ATCMD/<cmd>')
def flask_customcommand(cmd):
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);

    at_cmd_in_progress = True;
    respstr = sim.send_at(cmd, 'OK', 4);
    at_cmd_in_progress = False;

    resp_obj = {
        'status': "SUCCESS",
        'body': respstr
        }
    return jsonify(resp_obj);

@app.route('/shutdownsim/')
def flask_shutdownsim():
    turn_off_sim();
    mybody = "Shutdown SIM initiated";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/getStats/')
def flask_getstats():
    global currentStats, currentLine1, currentLine2;
    voltage = currentStats[0];
    signal = currentStats[1];
    network = currentStats[2];
    callstatus = currentLine1 + ' | ' + currentLine2;

    resp_obj = {
        'status': "SUCCESS",
        'voltage': voltage,
        'signal': signal,
        'network': network,
        'callstatus': callstatus
        }
    return jsonify(resp_obj);

@app.route('/service/jsontest/')
def flask_jsontest():
    mybody = "This is my json test";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/answer/')
def flask_answer():
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);
    
    at_cmd_in_progress = True;
    sim.answer_call();
    at_cmd_in_progress = False;

    mybody = "Answer signaled";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/sendtone/<number>')
def flask_sendtone(number):
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);
    
    at_cmd_in_progress = True;
    sim.send_tone(str(number));
    at_cmd_in_progress = False;

    mybody = 'Sending tone for ' + str(number);
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/hangup/')
def flask_hangup():
    global at_cmd_in_progress, at_cmd_wait_time;

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);
    
    at_cmd_in_progress = True;
    sim.hangup();
    at_cmd_in_progress = False;

    mybody = "Hangup signaled";
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return jsonify(resp_obj);

@app.route('/makecall/<number>')
def flask_makecall(number):
    global currentLine1, currentLine2, at_cmd_in_progress, at_cmd_wait_time;
    currentLine1 = "Making call: ";
    currentLine2 = number;
    mybody = 'Making phone call to ' + str(number);

    while (at_cmd_in_progress):
        time.sleep(at_cmd_wait_time);
    
    #disp.display_text("Calling " + number);
    at_cmd_in_progress = True;
    sim.make_call(number);
    at_cmd_in_progress = False;

    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    #return resp_obj;
    return jsonify(resp_obj);

@app.route('/nametest/<name>')
def flask_nametest(name):
    global currentLine1, currentLine2;
    currentLine1 = "";
    currentLine2 = name;
    return render_template('name.html', name=name);

def main_loop():
    global doLoop, isRunning, simgood, at_cmd_in_progress, at_cmd_wait_time, stats_check_sleep, notifications_check_sleep;
    global currentStats, currentLine1, currentLine2;
    turn_off_sim();
    turn_on_sim();
    time_stats = time.time();
    time_notifications = time.time();
    while doLoop:
        try:
            #func.log('main.py', 'myloop', 'looping...');s
            if (time.time() - time_stats > stats_check_sleep):
                currentStats[0] = get_voltage();
                if (simgood):
                    while (at_cmd_in_progress):
                        time.sleep(at_cmd_wait_time);
                    
                    at_cmd_in_progress = True;
                    currentStats[1] = sim.get_signal();
                    currentStats[2] = sim.get_network();
                    at_cmd_in_progress = False;
                time_stats = time.time();
            if (time.time() - time_notifications > notifications_check_sleep):
                check_sim_notification();
                time_notifications = time.time();

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
        thread1 = Thread(target=main_loop);
        thread2 = Thread(target=start_flask);
        thread1.start();
        thread2.start();
        thread1.join();
        thread2.join();
    except :
        func.log('main.py', '__main__', 'Exception (ID: {}) has been caught. Cleaning up...'.format(signal));
        exit(0);
