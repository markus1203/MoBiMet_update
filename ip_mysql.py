#! /usr/bin/python
# -*- coding: utf-8 -*-
from StringIO import StringIO
import csv
import sys
import os
import time
import datetime
import socket

import pymysql.cursors

time.sleep(10)

#before: pip install PyMySQL
#Create DATABASE
connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019")
try:
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS mobimet')
        
finally:
    connection.close()

#Create Database
connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sqlQuery = "CREATE TABLE IF NOT EXISTS `connection`(`ID` INT(11) NOT NULL AUTO_INCREMENT,`Timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,`Rasp_Time` DATETIME,`RASP_ID` INT,`IP_MOBIMET` TEXT, PRIMARY KEY(`ID`)) AUTO_INCREMENT=1"
        cursor.execute(sqlQuery)
         
finally:
    connection.close()

f1 = open("/home/pi/Desktop/r_id.csv", "r")
raspberryid = f1.read()
f1.close()

print(raspberryid)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

IP =get_ip()

print (IP)

time=time.strftime("%Y-%m-%d %H:%M:%S")
print(time)
connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
try:
        with connection.cursor() as cursor:
            sqlQuery = "INSERT INTO `connection` (`Rasp_Time`,`Rasp_ID`,`IP_MOBIMET`) VALUES (%s, %s, %s)"
            #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
            cursor.execute(sqlQuery,(time, raspberryid, IP))
            connection.commit()
            print(connection)            
finally:
        connection.close()