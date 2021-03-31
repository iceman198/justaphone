#!/usr/bin/python
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from flask import Flask, render_template

import func;
import disp;
import sim;

#func.print_test();

app = Flask(__name__);

@app.route('/')
def index():
    print('index triggered');
    disp.displayText("Index hit");
    return render_template('index.html');

@app.route('/service/makecall/<number>')
def makecall(number):
    print('starting phone call to ', number);
    mybody = 'Making phone call to ', number;
    disp.displayText("Calling " + number);
    sim.make_call(number);
    resp_obj = {
        'status': "SUCCESS",
        'body': mybody
        }
    return resp_obj;

@app.route('/nametest/<name>')
def nametest(name):
    print('name test triggered');
    return render_template('name.html', name=name);

if __name__ == '__main__':
    #disp.initDisplay();
    #disp.displayText("Running");
    print('Flask Running...');
    app.run(debug=True, host='0.0.0.0');

