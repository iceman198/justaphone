#!/usr/bin/python

from flask import Flask, render_template

import func;
#import sim;

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

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

    RST = 0

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

image1 = Image.new('1', (width, height))

draw = ImageDraw.Draw(image1)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding

bottom = height-padding
x = 0
font = ImageFont.load_default()

disp.clear()
disp.display()
draw.text((x, top),       "OLED Interfacing " ,  font=font, fill=255)
draw.text((x, top+8),     "Circuit Digest", font=font, fill=255)
draw.text((x, top+16),    "For more Videos",  font=font, fill=255)
draw.text((x, top+25),    "Visit at",  font=font, fill=255)
draw.text((x, top+34),    "www.circuitdigest.com",  font=font, fill=255)