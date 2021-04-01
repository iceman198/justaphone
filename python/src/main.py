#!/usr/bin/python
import sys;
import os;
import time;
import signal;

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from flask import Flask, jsonify, render_template;
from threading import Thread;

import func;
import disp;
import sim;

doLoop = True;
isRunning = False;
currentStats = "";
currentLine1 = "";
currentLine2 = "";

#func.print_test();
disp.init_display();

app = Flask(__name__);

@app.route('/')
def index():
    global currentLine1;
    currentLine1 = "Index Triggered";
    print('index triggered');
    #disp.display_text("Index hit");
    return render_template('index.html');

@app.route('/service/makecall/<number>')
def makecall(number):
    global currentLine1, currentLine2;
    currentLine1 = "Making call: ";
    currentLine2 = number;
    print('starting phone call to ' + str(number));
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
    print('name test triggered');
    currentLine1 = "";
    currentLine2 = name;
    return render_template('name.html', name=name);

def myloop():
    global doLoop, isRunning;
    global currentStats, currentLine1, currentLine2
    #print('isRunning = ' + str(isRunning)); #something isn't working right here but right now I don't care
    if isRunning == False:
        isRunning = True;
        i = 0;
        while doLoop:
            try:
                #print('looping...' + str(i));
                i = i + 1;
                disp.update_disp(currentStats, currentLine1, currentLine2);
                time.sleep(1);
            except KeyboardInterrupt:    
                print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal));
                disp.cleanup();
                exit(0);
                #epd2in13_V2.epdconfig.module_exit()

def start_flask():
    print('Flask Running...');
    app.run(debug=False, host='0.0.0.0');

if __name__ == '__main__':
    thread1 = Thread(target=myloop);
    thread2 = Thread(target=start_flask);
    thread1.start();
    thread2.start();
    thread1.join();
    thread2.join();
