#! /usr/bin/python
# -*- coding: utf-8 -*-

# Version 5.10.2020

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import csv
import sys
import os
import time
import datetime
import socket

import pymysql.cursors

time.sleep(10)

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])

print(raspberryid)


f1 = open("/home/pi/Desktop/connection.csv", "r")
line_con = f1.readlines()[int(raspberryid)]
f1.close()
ip =  (line_con.split(',')[0])
name =  (line_con.split(',')[1])
pw =  (line_con.split(',')[2])

#before: pip install PyMySQL
#Create DATABASE
#connection = pymysql.connect (host=ip, user=name, port=3306, password=pw)
#try:
#    with connection.cursor() as cursor:
#        cursor.execute('CREATE DATABASE IF NOT EXISTS mobimet_data')
#        
#finally:
#    connection.close()
#
##Create Database
#connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", cursorclass=pymysql.cursors.DictCursor)
#try:
#    with connection.cursor() as cursor:
#        sqlQuery = "CREATE TABLE IF NOT EXISTS `connection`(`ID` INT(11) NOT NULL AUTO_INCREMENT,`Timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,`Rasp_Time` DATETIME,`RASP_ID` INT,`IP_MOBIMET` TEXT, PRIMARY KEY(`ID`)) AUTO_INCREMENT=1"
#        cursor.execute(sqlQuery)
         
#finally:
#    connection.close()

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
connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", cursorclass=pymysql.cursors.DictCursor)
try:
        with connection.cursor() as cursor:
            sqlQuery = "INSERT INTO `connection` (`Rasp_Time`,`Rasp_ID`,`IP_MOBIMET`) VALUES (%s, %s, %s)"
            #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
            cursor.execute(sqlQuery,(time, raspberryid, IP))
            connection.commit()
            print(connection)            
finally:
        connection.close()
