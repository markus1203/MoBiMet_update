#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rak811 import Mode, Rak811
import csv
import sys
import os
import time
from datetime import datetime


#time.sleep(60)
print("start")
f1 = open("/home/pi/Desktop/r_id.csv", "r")
raspberryid = f1.read()
f1.close()
logfile_path = "/home/pi/Desktop/Data/"
logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"
raspberryid_int=int(raspberryid)
raspberryid_b=bytes.fromhex('{:02x}'.format(raspberryid_int))

f1 = open(logfile, "r")
last_line = f1.readlines()[-1]
f1.close()

IP=(last_line.split(',')[2])
#if ip --> dann lora ?
time_RP=(last_line.split(',')[0])

time_RP=datetime.strptime(time_RP,"%Y-%m-%d %H:%M") 
day=int(time_RP.strftime("%d"))
day_b=bytes.fromhex('{:02x}'.format(day))
month=int(time_RP.strftime("%m"))
month_b=bytes.fromhex('{:02x}'.format(month))
year=int(time_RP.strftime("%Y"))
year_b=bytes.fromhex('{:04x}'.format(year))
hour=int(time_RP.strftime("%H"))
hour_b=bytes.fromhex('{:02x}'.format(hour))
minute=int(time_RP.strftime("%M"))
minute_b=bytes.fromhex('{:02x}'.format(minute))

dht22_vp=int(round(float(last_line.split(',')[3]),2)*100)
if dht22_vp==-999900: dht22_vp=9999
dht22_vp_b=bytes.fromhex('{:04x}'.format(dht22_vp))
print(dht22_vp_b)

dht22_vp_raw=int(round(float(last_line.split(',')[4]),2)*100)
if dht22_vp_raw==-999900: dht22_vp_raw=9999
dht22_vp_raw_b=bytes.fromhex('{:04x}'.format(dht22_vp_raw))

dht22_humidity=int(round(float(last_line.split(',')[5]),1)*10)
if dht22_humidity==-99990: dht22_humidity=9999
dht22_humidity_b=bytes.fromhex('{:04x}'.format(dht22_humidity))
print(dht22_humidity_b)

dht22_humidity_raw=int(round(float(last_line.split(',')[6]),1)*10)
if dht22_humidity_raw==-99990: dht22_humidity_raw=9999
dht22_humidity_raw_b=bytes.fromhex('{:04x}'.format(dht22_humidity_raw))

dht22_temperature=int(round(float(last_line.split(',')[7])+273.1,1)*10)
if dht22_temperature==-97259: dht22_temperature=9999
print(dht22_temperature)
dht22_temperature_b=bytes.fromhex('{:04x}'.format(dht22_temperature))
print(dht22_temperature_b)

dht22_temperature_raw=int(round(float(last_line.split(',')[8])+273.1,1)*10)
if dht22_temperature_raw==-97259: dht22_temperature_raw=9999
dht22_temperature_raw_b=bytes.fromhex('{:04x}'.format(dht22_temperature_raw))
print(dht22_temperature_raw_b)

v=int(round(float(last_line.split(',')[9]),1)*10)
if v==-99990: v=9999
v_b=bytes.fromhex('{:04x}'.format(v))
print(v_b)

bg_calib=int(round(float(last_line.split(',')[10])+273.1,1)*10)
if bg_calib==-97259: bg_calib=9999
bg_calib_b=bytes.fromhex('{:04x}'.format(bg_calib))
print(bg_calib_b)

bg_raw=int(round(float(last_line.split(',')[11])+273.1,1)*10)
if bg_raw==-97259: bg_calib=9999
bg_raw_b=bytes.fromhex('{:04x}'.format(bg_raw))
print(bg_raw_b)

tmrt=int(round(float(last_line.split(',')[12])+273.1,1)*10)
if tmrt==-97259: tmrt=int(9999)
print(tmrt)
tmrt_b=bytes.fromhex('{:04x}'.format(tmrt))
print(tmrt_b)


#Light_Level=65535
Light_Level=int(round(float(last_line.split(',')[13]),0))
if Light_Level==-9999: Light_Level=9999
print(Light_Level)
Light_Level_b=bytes.fromhex('{:04x}'.format(Light_Level))
print(Light_Level_b)

mlx_e=int(round(float(last_line.split(',')[14]))*10)
if mlx_e==-99990: mlx_e=9999
print(mlx_e)
mlx_e_b=bytes.fromhex('{:04x}'.format(mlx_e))
print(mlx_e_b)

mlx_o=int(round(float(last_line.split(',')[15])+273.1,1)*10)
if mlx_o==-97259: mlx_o=9999
print(mlx_o)
mlx_o_b=bytes.fromhex('{:04x}'.format(mlx_o))
print(mlx_o_b)

mlx_a=int(round(float(last_line.split(',')[16])+273.1,1)*10)
if mlx_a==-97259: mlx_a=9999
print("mlx_a: "+str(mlx_a))
mlx_a_b=bytes.fromhex('{:04x}'.format(mlx_a))
print("mlx_a_b: "+str(mlx_a_b))
 
utci=(last_line.split(',')[17])
#if float(utci)==-9999: utci=None
sl=(last_line.split(',')[18])
#if float(sl)==-9999: sl=None
#Insert Data to mysql
print(time_RP,raspberryid,IP,dht22_humidity,dht22_humidity_raw,dht22_vp,dht22_vp_raw,dht22_temperature,dht22_temperature_raw,v,bg_calib,bg_raw,tmrt,Light_Level,mlx_e,mlx_o,mlx_a,utci,sl)

#print(year_b+month_b+day_b+hour_b+minute_b+raspberryid_b+dht22_vp_b+dht22_vp_raw_b+dht22_humidity_b+dht22_humidity_raw_b+dht22_temperature_b+dht22_temperature_raw_b+v_b+bg_calib_b+bg_raw_b+tmrt_b+Light_Level_b+mlx_e_b+mlx_o_b+mlx_a_b)


print("start LoRa")
lora = Rak811()
print("rak")
lora.hard_reset()
print("reset")
lora.mode = Mode.LoRaWan
lora.band = 'EU868'
print("band")
#lora.set_config(dev_eui='303838365338710C',app_eui='70B3D57ED0030AF7',app_key='07487AD99477A0AEC0D02A75DA25D94F' )
lora.set_config(app_eui='70B3D57ED0030AF7',
                app_key='07487AD99477A0AEC0D02A75DA25D94F')
print("config")
lora.join_otaa()
print("join_otaa")
lora.dr = 5
#lora.send(year_b+month_b+day_b+hour_b+minute_b+raspberryid_b+dht22_vp_b+dht22_vp_raw_b+dht22_humidity_b+dht22_humidity_raw_b+dht22_temperature_b+dht22_temperature_raw_b+v_b+bg_calib_b+bg_raw_b+tmrt_b+Light_Level_b+mlx_e_b+mlx_o_b+mlx_a_b)
#lora.send(year_b+month_b+day_b+hour_b+minute_b+raspberryid_b+dht22_vp_b+dht22_humidity_b+dht22_temperature_b+v_b+bg_calib_b+tmrt_b+Light_Level_b+mlx_e_b)
lora.send(dht22_vp_b+dht22_temperature_b+v_b+tmrt_b+Light_Level_b+mlx_e_b)
print(dht22_vp_b+dht22_temperature_b+v_b+tmrt_b+Light_Level_b+mlx_e_b)
print("send")   
lora.close()
print("LoRa Data transmitted")
