#! /usr/bin/python
# -*- coding: utf-8 -*-

# Version 25.01.2021
import time
import random
day=time.strftime("%Y-%m-%d")
hour=time.strftime("%H")
minute=time.strftime("%M")

random_sleep=random.randint(40,200)
print("Sleep: "+str(random_sleep))
time.sleep(random_sleep)

print("import")
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import csv
import sys
import os
import pymysql.cursors

print("start")

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])

f1 = open("/home/pi/Desktop/connection.csv", "r")
line_con = f1.readlines()[int(raspberryid)]
f1.close()
ip =  (line_con.split(',')[0])
name =  (line_con.split(',')[1])
pw =  (line_con.split(',')[2])




logfile_path= "/home/pi/Desktop/Data/"  
logfile = logfile_path+raspberryid+"-"+day+".csv"

f1 = open(logfile, "r")
last_line = f1.readlines()[-1]
f1.close()

IP=(last_line.split(',')[2])
time_RP=(last_line.split(',')[0])

#if time > (lastmysqltime[0].strftime('%Y-%m-%d %H:%M')):
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
sl_utci=(last_line.split(',')[18])
#if float(sl)==-9999: sl=None
#Insert Data to mysql
pet=(last_line.split(',')[19])
sl_pet=(last_line.split(',')[20])
cpu_temp=(last_line.split(',')[21])
print(time_RP,raspberryid,IP,dht22_humidity,dht22_humidity_raw,dht22_vp,dht22_vp_raw,dht22_temperature,dht22_temperature_raw,v,bg_calib,bg_raw,Tmrt,Light_Level,mlx_e,mlx_o,mlx_a,utci,sl_utci,pet,sl_pet,cpu_temp)
   
connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        #sqlQuery = "INSERT  `Data` (`Rasp_Time`,`Rasp_ID`,`IP_MOBIMET`, `RH`, `RH_raw`, `VP_hPa`,`VP_hPa_raw`,`Ta_C`,`Ta_C_raw`, `v_m/s`, `BlackGlobeT_C`,`BlackGlobeT_C_raw`,`Tmrt_C`,`LightLevel_lux`,`MLX_E_W/m²`,`MLX_O_C`,`MLX_A_C`, `UTCI_C`, `Stresslevel_UTCI`,`PET_C`,`Stresslevel_PET`,`CPU_TEMP_C`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s, %s,%s)"
        #cursor.execute(sqlQuery,(time, raspberryid, IP,"{0:.1f}".format(dht22_humidity),"{0:.1f}".format(dht22_humidity_raw),"{0:.3f}".format(dht22_vp),"{0:.3f}".format(dht22_vp_raw),"{0:.1f}".format(dht22_temperature),"{0:.1f}".format(dht22_temperature_raw),"{0:.1f}".format(v),"{0:.1f}".format(utci), sl))
        sqlQuery = "UPDATE  `Data` SET `IP_MOBIMET`=%s,`RH`=%s, `RH_raw`=%s, `VP_hPa`=%s,`VP_hPa_raw`=%s,`Ta_C`=%s,`Ta_C_raw`=%s, `v_m/s`=%s, `BlackGlobeT_C`=%s,`BlackGlobeT_C_raw`=%s,`Tmrt_C`=%s,`LightLevel_lux`=%s,`MLX_E_W/m²`=%s,`MLX_O_C`=%s,`MLX_A_C`=%s, `UTCI_C`=%s, `Stresslevel_UTCI`=%s,`PET_C`=%s,`Stresslevel_PET`=%s,`CPU_TEMP_C`=%s WHERE `Rasp_Time`=%s AND `RASP_ID`=%s ORDER BY Rasp_Time DESC LIMIT 5"
        cursor.execute(sqlQuery,(IP,dht22_humidity,dht22_humidity_raw,dht22_vp,dht22_vp_raw,dht22_temperature,dht22_temperature_raw,v,bg_calib,bg_raw,Tmrt,Light_Level,mlx_e,mlx_o,mlx_a,utci,sl_utci,pet,sl_pet,cpu_temp,time_RP,raspberryid))
        connection.commit()
        print(connection)

except pymysql.err.InternalError as e:
    code, msg = e.args
    if code == 1292:
        print('false format')


finally:
     connection.close()
     print("connection_closed")
print("newest Data submitted " + time_RP)

logfile_cl = "/home/pi/Desktop/"+raspberryid+"-connection-lost-"+day+"_"+hour+".csv"
if os.path.exists(logfile_cl) and minute=="55":
         with open(logfile_cl) as csvfile:
                  sp=csv.DictReader(csvfile)
                  for row in sp:
                           connection = pymysql.connect (host=ip, user=name, port=3306, password=pw, db ="mobimet_data", charset='utf8')
                           try:
                                    with connection.cursor() as cur:
                           #cur=connection.cursor()   
                                             sqlQuery = "UPDATE  `Data_Archive` SET `RH`=%s, `RH_raw`=%s, `VP_hPa`=%s,`VP_hPa_raw`=%s,`Ta_C`=%s,`Ta_C_raw`=%s, `v_m/s`=%s, `BlackGlobeT_C`=%s,`BlackGlobeT_C_raw`=%s,`Tmrt_C`=%s,`LightLevel_lux`=%s,`MLX_E_W/m²`=%s,`MLX_O_C`=%s,`MLX_A_C`=%s, `UTCI_C`=%s, `Stresslevel_UTCI`=%s,`PET_C`=%s,`Stresslevel_PET`=%s,`CPU_TEMP_C`=%s WHERE `Rasp_Time`=%s AND `RASP_ID`=%s"
                                             cur.execute(sqlQuery, (row['Rel_Hum(%)_DHT22_calib'],row['Rel_Hum(%)_DHT22_raw'],row['VP(hPa)_DHT22_calib'],row['VP(hPa)_DHT22_raw'],row['Ta(°C)_DHT22_calib'], row['Ta(°C)_DHT22_raw'],row['Wind(m/s)'],row['BG(°C)_calib'],row['BG(°C)_raw'],row['Tmrt(°C)'],row['Light_Level(lx)'],row['MLX_E(W/m²)'],row['MLX_O(°C)'],row['MLX_A(°C)'],row['UTCI(°C)'], row['Stresslevel_utci'],row['PET(°C)'],row['Stresslevel_pet'], row['CPU_TEMP(°C)'],row['Raspi_Time'],row['RaspberryID']))
                                             connection.commit()
                                             print("Lost DATA submitted")
                           except pymysql.err.InternalError as e:
                              code, msg = e.args
                              if code == 1292:
                                 print('false format')
                           finally:
                                    cur.close()
                                    connection.close()
                                    time.sleep(5)

         os.remove(logfile_cl)         
exit(0)

