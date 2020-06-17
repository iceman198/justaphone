#!/usr/bin/python

from flask import Flask, render_template

import func;
#import sim;

import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

display = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=0x3C)
# Setup
display.begin()  # initialize graphics library for selected display module
display.clear()  # clear display buffer
display.display()  # write display buffer to physical display
displayWidth = display.width  # get width of display
displayHeight = display.height  # get height of display
image = Image.new('1', (displayWidth, displayHeight))  # create graphics library image buffer
draw = ImageDraw.Draw(image)  # create drawing object
font = ImageFont.load_default()  # load and set default font

# Draw text
draw.text(((displayWidth - font.getsize("Woolsey")[0]) / 2, 0), "Woolsey", font=font, fill=255)  # center text at top of screen
draw.text(((displayWidth - font.getsize("Workshop")[0]) / 2, 53), "Workshop", font=font, fill=255)  # center text at bottom of screen

#func.print_test();

app = Flask(__name__);

@app.route('/')
def index():
    print('index triggered');
    return render_template('index.html');

@app.route('/service/makecall/<number>')
def makecall(number):
    print('starting phone call to ', number);
    mybody = "Making phone call to %s" % number;
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

