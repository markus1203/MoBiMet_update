#! /usr/bin/python
# -*- coding: utf-8 -*-
from StringIO import StringIO
import csv
import sys
import os
import time
import datetime

import pymysql.cursors

from UTCI import *


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
        sqlQuery = "CREATE TABLE IF NOT EXISTS `Data`(`ID` INT(11) NOT NULL AUTO_INCREMENT,`Timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,`Rasp_Time` DATETIME,`RASP_ID` INT,`IP_MOBIMET` TEXT, `VP_hPa` DECIMAL(7,3),`VP_hPa_raw` DECIMAL(7,3), `RH` DECIMAL(5,1),`RH_raw` DECIMAL(5,1),`Ta_C` DECIMAL(5,1), `Ta_C_raw` DECIMAL(5,1),`v_m/s` DECIMAL(5,1),`BlackGlobeT_C` DECIMAL(5,1),`BlackGlobeT_C_raw` DECIMAL(5,1),`Tmrt_C` DECIMAL(5,1),`LightLevel_lux` DECIMAL(7,2),`MLX_E_W/m²` DECIMAL(5,1),`MLX_O_C` DECIMAL(5,1),`MLX_A_C` DECIMAL(5,1),`UTCI_C` DECIMAL(5,1), `Stress` INT, PRIMARY KEY(`ID`)) AUTO_INCREMENT=1"
        cursor.execute(sqlQuery)
         
finally:
    connection.close()

f1 = open("/home/pi/Desktop/r_id.csv", "r")
raspberryid = f1.read()
f1.close()

# check if data ist already transmited to mysql

connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet")
try:
    with connection.cursor() as cursor:
        cursor.execute(("SELECT `Rasp_Time` FROM `Data` where`RASP_ID` ='%s' AND `Rasp_Time`=(select max(`Rasp_Time`) from `Data`)") % int(raspberryid))
        lastmysqltime = cursor.fetchone()
finally:
    connection.close()


if lastmysqltime == None : lastmysqltime=(datetime.datetime(1990,1,1,1,1),)

logfile_cl = "/home/pi/Desktop/"+raspberryid+"-connection-lost"+".csv"

if os.path.exists(logfile_cl):
    connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", charset='utf8')
    cur=connection.cursor()   
    with open(logfile_cl) as csvfile:
        sp=csv.DictReader(csvfile)
        for row in sp:
            sql= "INSERT INTO Data (Rasp_Time,RASP_ID, IP_MOBIMET, RH,RH_raw, VP_hPa,VP_hPa_raw, Ta_C, Ta_C_raw, `v_m/s`, `BlackGlobeT_C`,`BlackGlobeT_C_raw`,`Tmrt_C`,`LightLevel_lux`,`MLX_E_W/m²`,`MLX_O_C`,`MLX_A_C`,UTCI_C,Stress) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)"
            cur.execute(sql, (row['Raspi_Time'],row['RaspberryID'], row['IP'],row['Rel_Hum(%)_DHT22_calib'],row['Rel_Hum(%)_DHT22_raw'],row['VP(hPa)_DHT22_calib'],row['VP(hPa)_DHT22_raw'],row['Ta(°C)_DHT22_calib'], row['Ta(°C)_DHT22_raw'],row['Wind(m/s)'],row['BG(°C)_calib'],row['BG(°C)_raw'],row['Tmrt(°C)'],row['Light_Level(lx)'],row['MLX_E(W/m²)'],row['MLX_O(°C)'],row['MLX_A(°C)'],row['UTCI(°C)'], row['Stresslevel']))
    connection.commit() 
    cur.close()
    os.remove(logfile_cl)
    print("Lost DATA submitted")

time.sleep(30)

logfile_path= "/home/pi/Desktop/Data/"  
logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"

f1 = open(logfile, "r")
last_line = f1.readlines()[-1]
f1.close()

IP=(last_line.split(',')[2])
time=(last_line.split(',')[0])

if time > (lastmysqltime[0].strftime('%Y-%m-%d %H:%M')):
    dht22_vp=(last_line.split(',')[3])
    #if float(dht22_vp)==-9999: dht22_vp=None
    dht22_vp_raw=(last_line.split(',')[4])
    #if float(dht22_vp_raw)==-9999: dht22_vp_raw=None
    dht22_humidity=(last_line.split(',')[5])
    #if float(dht22_humidity)==-9999: dht22_humidity=None
    dht22_humidity_raw=(last_line.split(',')[6])
    #if float(dht22_humidity_raw)==-9999: dht22_humidity_raw=None
    dht22_temperature=(last_line.split(',')[7])
    #if float(dht22_temperature)==-9999: dht22_temperature=None
    dht22_temperature_raw=(last_line.split(',')[8])
    #if dht22_temperature_raw=="-9999.0": dht22_temperature_raw=None
    v=(last_line.split(',')[9])
    #if float(v)==-9999: v=None 
    bg_calib=(last_line.split(',')[10])
    bg_raw=(last_line.split(',')[11])
    Tmrt=(last_line.split(',')[12])
    Light_Level=(last_line.split(',')[13])
    mlx_e=(last_line.split(',')[14])
    mlx_o=(last_line.split(',')[15])
    mlx_a=(last_line.split(',')[16])  
    utci=(last_line.split(',')[17])
    #if float(utci)==-9999: utci=None
    sl=(last_line.split(',')[18])
    #if float(sl)==-9999: sl=None
    #Insert Data to mysql
    print(time,raspberryid,IP,dht22_humidity,dht22_humidity_raw,dht22_vp,dht22_vp_raw,dht22_temperature,dht22_temperature_raw,v,bg_calib,bg_raw,Tmrt,Light_Level,mlx_e,mlx_o,mlx_a,utci,sl)

    
    connection = pymysql.connect (host="132.230.102.174", user="mobimet_RP", port=3306, password="mobimet2019", db ="mobimet", cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sqlQuery = "INSERT INTO `Data` (`Rasp_Time`,`Rasp_ID`,`IP_MOBIMET`, `RH`, `RH_raw`, `VP_hPa`,`VP_hPa_raw`,`Ta_C`,`Ta_C_raw`, `v_m/s`, `BlackGlobeT_C`,`BlackGlobeT_C_raw`,`Tmrt_C`,`LightLevel_lux`,`MLX_E_W/m²`,`MLX_O_C`,`MLX_A_C`, `UTCI_C`, `Stress`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)"
            #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
            cursor.execute(sqlQuery,(time,raspberryid,IP,dht22_humidity,dht22_humidity_raw,dht22_vp,dht22_vp_raw,dht22_temperature,dht22_temperature_raw,v,bg_calib,bg_raw,Tmrt,Light_Level,mlx_e,mlx_o,mlx_a,utci,sl))
            connection.commit()
            print(connection)            
    finally:
        connection.close()
    print("newest Data submitted " + time)
else: print("no new Data available"+ time)
