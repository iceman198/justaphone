#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir);

import logging;
from waveshare_epd import epd2in13_V2;
import time;
from PIL import Image,ImageDraw,ImageFont;
import traceback;

logging.basicConfig(level=logging.DEBUG);

epd, font15, font24, time_image, time_draw = None, None, None, None, None;

def init_display():
    logging.info("disp.initDisplay() ~ init and Clear");
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

        time_draw.text((170, 0), time.strftime('%H:%M:%S'), font = font15, fill = 0);
        time_draw.text((170, 20), mystats, font = font15, fill = 0);

        epd.displayPartial(epd.getbuffer(time_image));
        #logging.info("disp.updateDisp() ~ Goto Sleep...");
        #epd.sleep();
            
    except IOError as e:
        logging.info("disp.updateDisp() ~ " & e);


def cleanup():
    epd.Clear(0xFF);
    logging.info("disp.cleanup() ~ Goto Sleep...");
    epd.sleep();
