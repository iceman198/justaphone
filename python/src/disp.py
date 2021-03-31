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

global epd;
global font15;
global font24;

def initDisplay():
    logging.info("disp.initDisplay() ~ init and Clear");
    epd = epd2in13_V2.EPD();
    epd.init(epd.FULL_UPDATE);
    epd.Clear(0xFF);
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15);
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24);

def displayText(text):
    try:
        time_image = Image.new('1', (epd.height, epd.width), 255);
        time_draw = ImageDraw.Draw(time_image);
        
        epd.init(epd.FULL_UPDATE);
        epd.displayPartBaseImage(epd.getbuffer(time_image));
        
        epd.init(epd.PART_UPDATE);
        num = 0;
        while (True):
            time_draw.rectangle((120, 80, 220, 105), fill = 255);
            time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0);
            epd.displayPartial(epd.getbuffer(time_image));
            num = num + 1;
            if(num == 20):
                break;
        # epd.Clear(0xFF);
        logging.info("disp.displayText() ~ Clear...");
        epd.init(epd.FULL_UPDATE);
        epd.Clear(0xFF);
        
        logging.info("disp.displayText() ~ Goto Sleep...");
        epd.sleep();
            
    except IOError as e:
        logging.info("disp.displayText() ~ " & e);
        
    except KeyboardInterrupt:    
        logging.info("disp.displayText() ~ KeyboardInterrupt: ctrl + c:");
        epd2in13_V2.epdconfig.module_exit();
        exit();
