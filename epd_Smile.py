#! /usr/bin/python
# -*- coding: utf-8 -*-

# Version 03.11.2020

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
#from UTCI import *

import logging
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
import traceback
import RPi.GPIO as GPIO

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])


calib_file = "/home/pi/Desktop/calibration_coefficients.csv"
f1 = open(calib_file, "r")
line = f1.readlines()[int(raspberryid)]
f1.close()
lang = str(line.split(',')[7])
    
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)  
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16) 
font17 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 17) 
font38 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 38)  

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
        utci=(last_line.split(',')[19])
        #comf=comfortable(float(utci))
        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126   

        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRedimage)
        drawblack.text((0, 2), ' MoBiMet ' + raspberryid, font = font17, fill = 0)
        drawblack.text((130,2), ' ' +time, font = font17, fill = 0) 

        drawred.line((0, 24, 265, 24), fill = 0)
        drawred.line((0, 25, 265, 25), fill = 0)
        drawred.line((0, 26, 265, 26), fill = 0)
        #drawred.line((130, 0, 130, 200), fill = 0)
        #drawred.line((131, 0, 131, 200), fill = 0)
        #drawred.line((132, 0, 132, 200), fill = 0)

        if lang=='g':
            drawred.text((0,30), ' Lufttemperatur',font = font16, fill = 0)
            drawred.text((130,30), ' Luftfeuchte',font = font16, fill = 0)
            drawred.text((0,105), '   PET',font = font16, fill = 0)
            drawred.text((120,105), 'Thermische Belastung',font = font14, fill = 0)

            if float(dht22_temperature) ==-9999:
                drawblack.text((0,50), ' keine', font = font24, fill = 0)
                drawblack.text((0,70), ' Daten', font = font24, fill = 0)
            else:
                drawblack.text((0,50), ' ' +dht22_temperature+u'°C', font = font38, fill = 0)

            if float(dht22_humidity) ==-9999:
                drawblack.text((130,50), ' keine', font = font24, fill = 0)
                drawblack.text((130,70), ' Daten', font = font24, fill = 0)
            else:
                drawblack.text((130,50), ' ' +dht22_humidity+u' %', font = font38, fill = 0)

            if float(PET) ==-9999:
                drawblack.text((0,120), ' keine', font = font24, fill = 0)
                drawblack.text((0,145), ' Daten', font = font24, fill = 0)
            else:
                drawblack.text((0,125), ' ' +PET+u'°C', font = font38, fill = 0)

          
            drawblack.text((130,120), ' mir ist', font = font24, fill = 0)
            drawblack.text((130,145), ' kalt', font = font24, fill = 0)


        if lang=='f':
            drawred.text((0,30), u" Température",font = font16, fill = 0)
            drawred.text((130,30), u' Humidité',font = font16, fill = 0)
            drawred.text((0,105), '   PET',font = font16, fill = 0)
            drawred.text((130,105), ' Charge thermique',font = font16, fill = 0)

            if float(dht22_temperature) ==-9999:
                drawblack.text((0,45), ' pas de', font = font24, fill = 0)
                drawblack.text((0,70), u' données', font = font24, fill = 0)
            else:
                drawblack.text((0,50), ' ' +dht22_temperature+u'°C', font = font38, fill = 0)

            if float(dht22_humidity) ==-9999:
                drawblack.text((130,45), ' pas de', font = font24, fill = 0)
                drawblack.text((130,70), u' données', font = font24, fill = 0)
            else:
                drawblack.text((130,50), ' ' +dht22_humidity+u' %', font = font38, fill = 0)

            if float(PET) ==-9999:
                drawblack.text((0,120), ' pas de', font = font24, fill = 0)
                drawblack.text((0,145), u' données', font = font24, fill = 0)
            else:
                drawblack.text((0,125), ' ' +PET+u'°C', font = font38, fill = 0)


        drawblack.text((130,140), u" j'ai froid", font = font24, fill = 0)


        drawred.line((0, 99, 265, 99), fill = 0)
        drawred.line((0, 100, 265, 100), fill = 0)
        drawred.line((0, 101, 265, 101), fill = 0)

        epd.display(epd.getbuffer(HBlackimage),epd.getbuffer(HRedimage))

        print(str(time)+","+str(PET))
        print(lang)
        print("printed on EPD")

                        
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


        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126   

        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRedimage)
        drawblack.text((5, 5), ' MoBiMet ' + raspberryid, font = font35, fill = 0)
        drawblack.text((5,55),R_time, font = font22, fill = 0)
        #draw.text((2,70), 'Ta: ' +"{0:.1f}".format(dht22_temperature)+u' °C', font = font18, fill = 0)
        #draw.text((2,100), 'RH: '+"{0:.1f} %".format(dht22_humidity), font = font18, fill = 0)
        #draw.text((2,130), 'UTCI: '+"{0:.1f}".format(utci) + u' °C', font = font18, fill = 0)
        drawblack.text((5,90), 'Ta: ' +dht22_temperature+u' °C' + '       RH: '+dht22_humidity+' %', font = font22, fill = 0)
        #drawblack.text((2,100), 'RH: '+dht22_humidity+' %', font = font18, fill = 0)
        #drawblack.text((2,130), 'UTCI: '+utci+u' °C', font = font18, fill = 0)
        drawred.text((5,120), comf,font = font22, fill = 0)
        drawblack.text((5,150), ' I AM COMFORTABLE ' , font = font24, fill = 0) 
        epd.display(epd.getbuffer(HBlackimage),epd.getbuffer(HRedimage))   

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


        HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
        HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126   

        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRedimage)
        drawblack.text((5, 5), ' MoBiMet ' + raspberryid, font = font35, fill = 0)
        drawblack.text((5,55),R_time, font = font22, fill = 0)
        #draw.text((2,70), 'Ta: ' +"{0:.1f}".format(dht22_temperature)+u' °C', font = font18, fill = 0)
        #draw.text((2,100), 'RH: '+"{0:.1f} %".format(dht22_humidity), font = font18, fill = 0)
        #draw.text((2,130), 'UTCI: '+"{0:.1f}".format(utci) + u' °C', font = font18, fill = 0)
        drawblack.text((5,90), 'Ta: ' +dht22_temperature+u' °C' + '       RH: '+dht22_humidity+' %', font = font22, fill = 0)
        #drawblack.text((2,100), 'RH: '+dht22_humidity+' %', font = font18, fill = 0)
        #drawblack.text((2,130), 'UTCI: '+utci+u' °C', font = font18, fill = 0)
        drawred.text((5,120), comf,font = font22, fill = 0)
        drawblack.text((5,150), ' I AM HOT ' , font = font24, fill = 0) 
        epd.display(epd.getbuffer(HBlackimage),epd.getbuffer(HRedimage))

        print('Key3 Pressed '+b_time)
        print("Smiley pinted on EPD")

           


print("prgram closed")
