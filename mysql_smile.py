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

import pymysql.cursors

f1 = open("/home/pi/Desktop/r_id.csv", "r")
raspberryid = f1.read()
f1.close()

#Create DATABASE
connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019")
try:
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS mobimet')
        
finally:
    connection.close()

#Create Datatable
connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sqlQuery = "CREATE TABLE IF NOT EXISTS `smiley`(`ID` INT(11) NOT NULL AUTO_INCREMENT,`Timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,`Rasp_Time` DATETIME,`RASP_ID` INT,`SMILEY` INT, PRIMARY KEY(`ID`)) AUTO_INCREMENT=1"
        cursor.execute(sqlQuery)
         
finally:
     connection.close()
while True:
            smiley=0
            GPIO.setmode(GPIO.BCM)
            key1 = 5
            key2 = 6
            key3 = 13
            key4 = 19
            GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
            key1state = GPIO.input(key1)
            key2state = GPIO.input(key2)
            key3state = GPIO.input(key3)
            key4state = GPIO.input(key4)
            if key1state == False:
                b_time=time.strftime("%Y-%m-%d %H:%M:%S")
                smiley=1
                print('Key1 Pressed '+b_time)
                connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
                try:
                    with connection.cursor() as cursor:
                        sqlQuery = "INSERT INTO `smiley` (`Rasp_Time`,`Rasp_ID`,`SMILEY`) VALUES (%s, %s, %s)"
                        #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
                        cursor.execute(sqlQuery,(b_time, raspberryid, smiley))
                        connection.commit()
                        print(str(smiley))
                        print(connection)            
                finally:
                    connection.close()
                time.sleep(2)
            if key2state == False:
                smiley=2
                b_time=time.strftime("%Y-%m-%d %H:%M:%S")
                print('Key2 Pressed '+b_time)
                connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
                try:
                    with connection.cursor() as cursor:
                        sqlQuery = "INSERT INTO `smiley` (`Rasp_Time`,`Rasp_ID`,`SMILEY`) VALUES (%s, %s, %s)"
                        #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
                        cursor.execute(sqlQuery,(b_time, raspberryid, smiley))
                        connection.commit()
                        print(str(smiley))
                        print(connection)
                finally:
                    connection.close()
                time.sleep(2)
                
            if key3state == False:
                b_time=time.strftime("%Y-%m-%d %H:%M:%S")
                smiley=3
                print('Key3 Pressed '+b_time)
                connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
                try:
                    with connection.cursor() as cursor:
                        sqlQuery = "INSERT INTO `smiley` (`Rasp_Time`,`Rasp_ID`,`SMILEY`) VALUES (%s, %s, %s)"
                        #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
                        cursor.execute(sqlQuery,(b_time, raspberryid, smiley))
                        connection.commit()
                        print(str(smiley))
                        print(connection)            
                finally:
                    connection.close()
                time.sleep(2)


print("porgram closed")
