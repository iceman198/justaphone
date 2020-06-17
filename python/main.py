#!/usr/bin/python

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
    mybody = "Making phone call to " + number;
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
    app.run(debug=True, host='0.0.0.0');
    disp.displayText("Running");

