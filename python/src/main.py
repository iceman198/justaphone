#!/usr/bin/python
import sys;
import os;
import time;
import signal;

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from flask import Flask, render_template;
from multiprocessing import Process;

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
    print('starting phone call to ', number);
    mybody = 'Making phone call to ', number;

    #disp.display_text("Calling " + number);
    #sim.make_call(number);
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return resp_obj;

@app.route('/nametest/<name>')
def nametest(name):
    global currentLine2;
    print('name test triggered');
    currentLine2 = name;
    return render_template('name.html', name=name);

def myloop():
    global doLoop, isRunning;
    #print('isRunning = ' + str(isRunning)); #something isn't working right here but right now I don't care
    if isRunning == False:
        isRunning = True;
        i = 0;
        signal.signal(signal.SIGINT, keyboard_interrupt_handler);        
        while doLoop:
            #print('looping...' + str(i));
            global currentStats, currentLine1, currentLine2
            i = i + 1;
            disp.update_disp(currentStats, currentLine1, currentLine2);
            time.sleep(1);

if __name__ == '__main__':
    #disp.display_text("Running");
    print('Flask Running...');
    p = Process(target=myloop);
    p.start();
    app.run(debug=False, host='0.0.0.0');

def keyboard_interrupt_handler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal));
    disp.cleanup();
    exit(0);

signal.signal(signal.SIGINT, keyboard_interrupt_handler);