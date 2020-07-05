#! /usr/bin/python
# -*- coding: utf-8 -*-
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
from UTCI import *

import logging
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
import traceback
import RPi.GPIO as GPIO

f1 = open("/home/pi/Desktop/r_id.csv", "r")
raspberryid = f1.read()
f1.close()
    
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)  

logfile_path = "/home/pi/Desktop/Data/"


while True:
    GPIO.setmode(GPIO.BCM)
    key1 = 5
    key2 = 6
    key3 = 13
    #key4 = 19
    GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
    key1state = GPIO.input(key1)
    key2state = GPIO.input(key2)
    key3state = GPIO.input(key3)
    #key4state = GPIO.input(key4)
    if key1state == False:
        epd = epd2in7b.EPD()
        epd.init()
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        smiley=1
        
        logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"

        f1 = open(logfile, "r")
        last_line = f1.readlines()[-1]
        f1.close()

        IP=(last_line.split(',')[2])
        R_time=(last_line.split(',')[0])
        dht22_humidity=(last_line.split(',')[5])
        dht22_temperature=(last_line.split(',')[7])
        utci=(last_line.split(',')[17])
        comf=comfortable(float(utci))
        
        LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        LRedimage= Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

        drawblack = ImageDraw.Draw(LBlackimage)
        drawred = ImageDraw.Draw(LRedimage)
        drawblack.text((2, 0), ' MoBiMet ' + raspberryid, font = font24, fill = 0)
        drawblack.text((2,40), R_time, font = font18, fill = 0)
        drawblack.text((2,70), 'Ta: ' +dht22_temperature+' C', font = font18, fill = 0)
        drawblack.text((2,100), 'RH: '+dht22_humidity+' %', font = font18, fill = 0)
        drawblack.text((2,130), 'UTCI: '+utci+' C', font = font18, fill = 0)
        drawred.text((2,160), comf,font = font18, fill = 0)
        drawblack.text((2,200), ' I AM COLD ' , font = font24, fill = 0)       
        drawblack.text((2,250), 'IP: ' +IP, font = font14, fill = 0)
        epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))

                        
        print('Key1 Pressed '+b_time)
        print("Smiley pinted on EPD")

    if key2state == False:
        epd = epd2in7b.EPD()
        epd.init()
        smiley=2
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")

        logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"
        f1 = open(logfile, "r")
        last_line = f1.readlines()[-1]
        f1.close()
        IP=(last_line.split(',')[2])
        R_time=(last_line.split(',')[0])
        dht22_humidity=(last_line.split(',')[5])
        dht22_temperature=(last_line.split(',')[7])
        utci=(last_line.split(',')[17])
        comf=comfortable(float(utci))


        LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        LRedimage= Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

        drawblack = ImageDraw.Draw(LBlackimage)
        drawred = ImageDraw.Draw(LRedimage)
        drawblack.text((2, 0), ' MoBiMet ' + raspberryid, font = font24, fill = 0)
        drawblack.text((2,40), R_time, font = font18, fill = 0)
        drawblack.text((2,70), 'Ta: ' +dht22_temperature+' C', font = font18, fill = 0)
        drawblack.text((2,100), 'RH: '+dht22_humidity+' %', font = font18, fill = 0)
        drawblack.text((2,130), 'UTCI: '+utci+' C', font = font18, fill = 0)
        drawred.text((2,160), comf,font = font18, fill = 0)
        drawblack.text((2,200), ' I AM COMFORTABLE ' , font = font18, fill = 0)       
        drawblack.text((2,250), 'IP: ' +IP, font = font14, fill = 0)
        epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))

        print('Key2 Pressed '+b_time)
        print("Smiley pinted on EPD")
                
    if key3state == False:
        epd = epd2in7b.EPD()
        epd.init()
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        smiley=3

        logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"

        f1 = open(logfile, "r")
        last_line = f1.readlines()[-1]
        f1.close()

        IP=(last_line.split(',')[2])
        R_time=(last_line.split(',')[0])
        dht22_humidity=(last_line.split(',')[5])
        dht22_temperature=(last_line.split(',')[7])
        utci=(last_line.split(',')[17])
        comf=comfortable(float(utci))


        LBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        LRedimage= Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

        drawblack = ImageDraw.Draw(LBlackimage)
        drawred = ImageDraw.Draw(LRedimage)
        drawblack.text((2, 0), ' MoBiMet ' + raspberryid, font = font24, fill = 0)
        drawblack.text((2,40), R_time, font = font18, fill = 0)
        drawblack.text((2,70), 'Ta: ' +dht22_temperature+' C', font = font18, fill = 0)
        drawblack.text((2,100), 'RH: '+dht22_humidity+' %', font = font18, fill = 0)
        drawblack.text((2,130), 'UTCI: '+utci+' C', font = font18, fill = 0)
        drawred.text((2,160), comf,font = font18, fill = 0)
        drawblack.text((2,200), ' I AM HOT ' , font = font24, fill = 0)       
        drawblack.text((2,250), 'IP: ' +IP, font = font14, fill = 0)
        epd.display(epd.getbuffer(LBlackimage),epd.getbuffer(LRedimage))

        print('Key3 Pressed '+b_time)
        print("Smiley pinted on EPD")

           


print("prgram closed")
