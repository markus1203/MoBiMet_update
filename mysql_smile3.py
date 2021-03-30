#! /usr/bin/python
# -*- coding: utf-8 -*-

# Version 02.11.

from __future__ import division

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import csv
import sys
import os
import time
picdir="/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic"
libdir="/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib"
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7b
from PIL import Image,ImageDraw,ImageFont
import traceback
import RPi.GPIO as GPIO

import pymysql.cursors

day=time.strftime("%d")

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])
print(str(raspberryid))

f1 = open("/home/pi/Desktop/connection.csv", "r")
line_id = f1.readlines()[1]
f1.close()
ip =  (line_id.split(',')[0])
name =  (line_id.split(',')[1])
pw =  (line_id.split(',')[2])

while day==time.strftime("%d"):
    smiley=0
    GPIO.setmode(GPIO.BCM)
    key1 = 5
    key2 = 6
    key3 = 13
    GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    key1state = GPIO.input(key1)
    key2state = GPIO.input(key2)
    key3state = GPIO.input(key3)
            
    if key1state == False:
        print('eins')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        smiley=1
        print('Key1 Pressed '+b_time)
        connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sqlQuery = "INSERT INTO `smiley` (`Rasp_Time`,`Rasp_ID`,`SMILEY`) VALUES (%s, %s, %s)"
                cursor.execute(sqlQuery,(b_time, raspberryid, smiley))
                connection.commit()
                print(str(smiley))
                print(connection)            
        finally:
            connection.close()
        time.sleep(60)
               
    if key2state == False:
        print('zwei')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        smiley=2
        print('Key2 Pressed '+b_time)
        connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sqlQuery = "INSERT INTO `smiley` (`Rasp_Time`,`Rasp_ID`,`SMILEY`) VALUES (%s, %s, %s)"
                cursor.execute(sqlQuery,(b_time, raspberryid, smiley))
                connection.commit()
                print(str(smiley))
                print(connection)            
        finally:
            connection.close()
        time.sleep(60)
                
    if key3state == False:
        print('drei')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        smiley=3
        print('Key3 Pressed '+b_time)
        connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sqlQuery = "INSERT INTO `smiley` (`Rasp_Time`,`Rasp_ID`,`SMILEY`) VALUES (%s, %s, %s)"
                cursor.execute(sqlQuery,(b_time, raspberryid, smiley))
                connection.commit()
                print(str(smiley))
                print(connection)            
        finally:
            connection.close()
        time.sleep(60)

print("porgram closed")
