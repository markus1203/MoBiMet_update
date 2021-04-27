#! /usr/bin/python
# -*- coding: utf-8 -*-

# Version 26.10.2020
from __future__ import division
import time
time.sleep(50)

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import csv
import sys
import os
picdir="/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic"
libdir="/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib"
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
import traceback

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])

calib_file = "/home/pi/Desktop/calibration_coefficients.csv"
f1 = open(calib_file, "r")
line = f1.readlines()[int(raspberryid)]
f1.close()
lang = str(line.split(',')[7])

epd = epd2in7b.EPD()
    
'''2Gray(Black and white) display'''
#logging.info("init and Clear")
#epd.init()
#epd.Clear()
    
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
font22 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 22)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font19 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 19)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16) 
font17 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 17) 
font38 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 38) 

logfile_path = "/home/pi/Desktop/Data/"
logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"

f1 = open(logfile, "r")
last_line = f1.readlines()[-1]
f1.close()

IP=(last_line.split(',')[2])
time=(last_line.split(',')[0])
dht22_humidity=(last_line.split(',')[5])
dht22_temperature=(last_line.split(',')[7])
PET=(last_line.split(',')[19])
#comf=comfortable_PET(float(PET))

epd.init()
HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
HRedimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126   

drawblack = ImageDraw.Draw(HBlackimage)
drawred = ImageDraw.Draw(HRedimage)
drawblack.text((0, 2), ' MoBiMet ' + raspberryid, font = font17, fill = 0)
if IP=='127.0.0.1':
    drawblack.text((160,2), '     NO WIFI', font = font17, fill = 0)     
else:
    drawblack.text((130,2), ' ' +time, font = font17, fill = 0) 

drawred.line((0, 24, 265, 24), fill = 0)
drawred.line((0, 25, 265, 25), fill = 0)
drawred.line((0, 26, 265, 26), fill = 0)
#drawred.line((130, 0, 130, 200), fill = 0)
#drawred.line((131, 0, 131, 200), fill = 0)
#drawred.line((132, 0, 132, 200), fill = 0)

if lang=='g':
    drawblack.text((0,30), ' Lufttemperatur',font = font16, fill = 0)
    drawblack.text((130,30), ' Luftfeuchte',font = font16, fill = 0)
    drawblack.text((0,105), '   PET',font = font16, fill = 0)
    drawblack.text((115,105), 'Thermische Belastung',font = font15, fill = 0)
    
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
    
    
    if float(PET)==-9999:
        drawblack.text((130,120), ' keine', font = font24, fill = 0)
        drawblack.text((130,145), ' Daten', font = font24, fill = 0)
    elif float(PET)>=18 and float(PET)<=23:
        drawblack.text((130,120), ' keine', font = font24, fill = 0)
        drawblack.text((130,145), ' Belastung', font = font24, fill = 0)
    elif float(PET) <= 4 and float(PET)>-9999:
        drawblack.text((130,120), ' extreme', font = font19, fill = 0)
        drawblack.text((130,145), u' Kältebelastung', font = font19, fill = 0)
    elif float(PET) <= 8:
        drawblack.text((130,120), 'starke', font = font20, fill = 0)
        drawblack.text((130,145), u'Kältebelastung', font = font20, fill = 0)
    elif float(PET) <= 13:
        drawblack.text((130,120), 'moderate', font = font20, fill = 0)
        drawblack.text((130,145), u'Kältebelastung', font = font20, fill = 0)
    elif float(PET) <= 18:
        drawblack.text((130,120), 'leichte', font = font20, fill = 0)
        drawblack.text((130,145), u'Kältebelastung', font = font20, fill = 0)
    elif float(PET)>=41:
        drawblack.text((130,120), 'extreme', font = font20, fill = 0)
        drawblack.text((130,145), u'Wärmebelastung', font = font17, fill = 0)
    elif float(PET)>=35:
        drawblack.text((130,120), 'starke', font = font20, fill = 0)
        drawblack.text((130,145), u'Wärmebelastung', font = font17, fill = 0)
    elif float(PET)>=29:
        drawblack.text((130,120), 'moderate', font = font20, fill = 0)
        drawblack.text((130,145), u'Wärmebelastung', font = font17, fill = 0)
    elif float(PET)>=23:
        drawblack.text((130,120), 'leichte', font = font20, fill = 0)
        drawblack.text((130,145), u'Wärmebelastung', font = font17, fill = 0)
        
if lang=='f':
    drawblack.text((0,30), u" Température",font = font16, fill = 0)
    drawblack.text((130,30), u' Humidité',font = font16, fill = 0)
    drawblack.text((0,105), '   PET',font = font16, fill = 0)
    drawblack.text((130,105), ' Charge thermique',font = font16, fill = 0)
    
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
    
    
    if float(PET)==-9999:
        drawblack.text((130,120), ' pas de', font = font24, fill = 0)
        drawblack.text((130,145), u' données', font = font24, fill = 0)
    elif float(PET)>=18 and float(PET)<=23:
        drawblack.text((130,120), ' pas de', font = font22, fill = 0)
        drawblack.text((130,145), ' fardeau', font = font22, fill = 0)
    elif float(PET) <= 4 and float(PET)>-9999:
        drawblack.text((130,120), ' stress de', font = font20, fill = 0)
        drawblack.text((130,145), u' froid extrême', font = font20, fill = 0)
    elif float(PET) <= 8:
        drawblack.text((130,120), ' fort stress', font = font22, fill = 0)
        drawblack.text((130,145), u' dû au froid', font = font22, fill = 0)
    elif float(PET) <= 13:
        drawblack.text((130,120), ' stress froid ', font = font22, fill = 0)
        drawblack.text((130,145), u' modéré', font = font22, fill = 0)
    elif float(PET) <= 18:
        drawblack.text((130,120), u' léger stress', font = font22, fill = 0)
        drawblack.text((130,145), u' dû au froid', font = font22, fill = 0)
    elif float(PET)>=41:
        drawblack.text((130,121), ' stress ', font = font18, fill = 0)
        drawblack.text((140,138), ' thermique', font = font18, fill = 0)
        drawblack.text((140,155), u' extrême', font = font18, fill = 0)
    elif float(PET)>=35:
        drawblack.text((140,125), ' fort stress', font = font20, fill = 0)
        #drawblack.text((140,138), ' stress ', font = font17, fill = 0)
        drawblack.text((140,145), u' thermique', font = font20, fill = 0)
    elif float(PET)>=29:
        drawblack.text((140,121), ' stress', font = font18, fill = 0)
        drawblack.text((140,138), ' thermique', font = font18, fill = 0)
        drawblack.text((140,155), u' modéré', font = font18, fill = 0)
    elif float(PET)>=23:
        drawblack.text((130,125), u' léger stress ', font = font20, fill = 0)
        #drawblack.text((140,138), ' stress ', font = font18, fill = 0)
        drawblack.text((130,145), u' thermique', font = font20, fill = 0)

if lang=='e':
    drawblack.text((0,30), ' Air Temperature',font = font16, fill = 0)
    drawblack.text((130,30), ' Humidity',font = font16, fill = 0)
    drawblack.text((0,105), '   PET',font = font16, fill = 0)
    drawblack.text((120,105), 'Thermal stress',font = font14, fill = 0)
    
    if float(dht22_temperature) ==-9999:
        drawblack.text((0,50), ' no', font = font24, fill = 0)
        drawblack.text((0,70), ' data', font = font24, fill = 0)
    else:
        drawblack.text((0,50), ' ' +dht22_temperature+u'°C', font = font38, fill = 0)

    if float(dht22_humidity) ==-9999:
        drawblack.text((130,50), ' no', font = font24, fill = 0)
        drawblack.text((130,70), ' data', font = font24, fill = 0)
    else:
        drawblack.text((130,50), ' ' +dht22_humidity+u' %', font = font38, fill = 0)

    if float(PET) ==-9999:
        drawblack.text((0,120), ' no', font = font24, fill = 0)
        drawblack.text((0,145), ' data', font = font24, fill = 0)
    else:
        drawblack.text((0,125), ' ' +PET+u'°C', font = font38, fill = 0)
    
    
    if float(PET)==-9999:
        drawblack.text((130,120), ' no', font = font24, fill = 0)
        drawblack.text((130,145), ' data', font = font24, fill = 0)
    elif float(PET)>=18 and float(PET)<=23:
        drawblack.text((130,120), ' no thermal', font = font24, fill = 0)
        drawblack.text((130,145), ' stress', font = font24, fill = 0)
    elif float(PET) <= 4 and float(PET)>-9999:
        drawblack.text((130,120), ' extreme', font = font20, fill = 0)
        drawblack.text((130,145), u' cold stress', font = font20, fill = 0)
    elif float(PET) <= 8:
        drawblack.text((130,120), ' strong', font = font20, fill = 0)
        drawblack.text((130,145), u' cold stress', font = font20, fill = 0)
    elif float(PET) <= 13:
        drawblack.text((130,120), ' moderate', font = font20, fill = 0)
        drawblack.text((130,145), u' cold stress', font = font20, fill = 0)
    elif float(PET) <= 18:
        drawblack.text((130,120), ' light', font = font20, fill = 0)
        drawblack.text((130,145), u' cold stress', font = font20, fill = 0)
    elif float(PET)>=41:
        drawblack.text((130,120), ' extreme', font = font20, fill = 0)
        drawblack.text((130,145), u' heat stress', font = font20, fill = 0)
    elif float(PET)>=35:
        drawblack.text((130,120), ' strong', font = font20, fill = 0)
        drawblack.text((130,145), u' heat stress', font = font20, fill = 0)
    elif float(PET)>=29:
        drawblack.text((130,120), ' moderate', font = font20, fill = 0)
        drawblack.text((130,145), u' heat stress', font = font20, fill = 0)
    elif float(PET)>=23:
        drawblack.text((130,120), ' light', font = font20, fill = 0)
        drawblack.text((130,145), u' heat stress', font = font20, fill = 0)
        
drawred.line((0, 99, 265, 99), fill = 0)
drawred.line((0, 100, 265, 100), fill = 0)
drawred.line((0, 101, 265, 101), fill = 0)

epd.display(epd.getbuffer(HBlackimage),epd.getbuffer(HRedimage))

print(str(time)+","+str(PET))
print(lang)
print("printed on EPD")
exit(0)
