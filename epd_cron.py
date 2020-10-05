#! /usr/bin/python
# -*- coding: utf-8 -*-

# Version 25.9.2020

from __future__ import division

from StringIO import StringIO
import csv
import sys
import os
import time
picdir="/home/pi/e-Paper/RaspberryPi&JetsonNano/python/pic"
libdir="/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib"
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
import traceback

from UTCI import *

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])

#time.sleep(30)


epd = epd2in7b.EPD()
    
'''2Gray(Black and white) display'''
#logging.info("init and Clear")
#epd.init()
#epd.Clear()
    
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)  

logfile_path = "/home/pi/Desktop/Data/"
logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"

f1 = open(logfile, "r")
last_line = f1.readlines()[-1]
f1.close()

IP=(last_line.split(',')[2])
time=(last_line.split(',')[0])
dht22_humidity=(last_line.split(',')[5])
dht22_temperature=(last_line.split(',')[7])
utci=(last_line.split(',')[17])
comf=comfortable(float(utci))

epd.init()
HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126   

drawblack = ImageDraw.Draw(HBlackimage)
drawred = ImageDraw.Draw(HRedimage)
drawblack.text((5, 5), ' MoBiMet ' + raspberryid, font = font35, fill = 0)
drawblack.text((5,55), time, font = font22, fill = 0)
#draw.text((2,70), 'Ta: ' +"{0:.1f}".format(dht22_temperature)+u' °C', font = font18, fill = 0)
#draw.text((2,100), 'RH: '+"{0:.1f} %".format(dht22_humidity), font = font18, fill = 0)
#draw.text((2,130), 'UTCI: '+"{0:.1f}".format(utci) + u' °C', font = font18, fill = 0)
drawblack.text((5,90), 'Ta: ' +dht22_temperature+u' °C' + '       RH: '+dht22_humidity+' %', font = font22, fill = 0)
#drawblack.text((2,100), 'RH: '+dht22_humidity+' %', font = font18, fill = 0)
#drawblack.text((2,130), 'UTCI: '+utci+u' °C', font = font18, fill = 0)
drawred.text((5,120), comf,font = font22, fill = 0)
drawblack.text((5,150), 'IP: ' +IP, font = font14, fill = 0)
epd.display(epd.getbuffer(HBlackimage),epd.getbuffer(HRedimage))

print(str(time)+","+str(utci))
print("printed on EPD")
