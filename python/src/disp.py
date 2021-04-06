#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys;
import os;
import datetime;

from waveshare_epd import epd2in13_V2;
from PIL import Image,ImageDraw,ImageFont;

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir);

epd, font15, font24, time_image, time_draw = None, None, None, None, None;

def init_display():
    global epd, font15, font24, time_image, time_draw;
    epd = epd2in13_V2.EPD();
    epd.init(epd.FULL_UPDATE);
    epd.Clear(0xFF);

    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15);
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24);
    time_image = Image.new('1', (epd.height, epd.width), 255);
    time_draw = ImageDraw.Draw(time_image);
    
    epd.displayPartBaseImage(epd.getbuffer(time_image));
    epd.init(epd.PART_UPDATE);

def update_disp(mystats, textLine1, textLine2):
    try:
        global epd, font15, font24, time_image, time_draw;
        #time_draw.rectangle((0, 0, 220, 105), fill = 255);
        time_draw.rectangle((0, 0, epd.height, epd.width), fill = 255);

        time_draw.text((0, 40), textLine1, font = font24, fill = 0);
        time_draw.text((0, 80), textLine2, font = font24, fill = 0);

        time_draw.text((170, 0), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), font = font15, fill = 0);
        time_draw.text((0, 0), mystats[0], font = font15, fill = 0);
        time_draw.text((60, 0), mystats[1], font = font15, fill = 0);
        time_draw.text((120, 0), mystats[2], font = font15, fill = 0);

        epd.displayPartial(epd.getbuffer(time_image));
    except IOError as e:
        i = 5 + 2;


def cleanup():
    epd.Clear(0xFF);
    epd.sleep();
