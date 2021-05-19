#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#10.01.2021
import time
import random

random_sleep=random.randint(40,170)
print("Sleep: "+str(random_sleep))
time.sleep(random_sleep)

from rak811v2 import Rak811v2
import csv
import sys
import os
from datetime import datetime
from ttn_secrets import APPS_KEY, DEV_ADDR, NWKS_KEY
joinmode = 'ABP'

print("start LoRa")
lora = Rak811v2()
print("rak")
lora.hard_reset()
print("reset")

lora.set_config('lora:region:EU868')
print('Set loRa region')

#if joinmode == 'OTA':
#    print('Set join mode to OTA and configure appropriate keys')
#    lora.set_config('lora:join_mode:0')
#   lora.set_config('lora:app_eui:XXXXXXXXXXXXXX')
#    lora.set_config('lora:app_key:XXXXXXXXXXXXXX')
#else:
#    print('Set join mode to ABP and set appropriate keys')
#    lora.set_config('lora:join_mode:1')
#    lora.set_config('lora:dev_addr:XXXXXXXXXXXXXX')
#    lora.set_config('lora:nwks_key:XXXXXXXXXXXXXX')
#    lora.set_config('lora:apps_key:XXXXXXXXXXXXXX')

print("DEV_ADDR: "+DEV_ADDR+" | NWKS_KEY: "+NWKS_KEY+" | APPS_KEY: "+APPS_KEY)
dev="lora:dev_addr:"+DEV_ADDR
nwk="lora:nwks_key:"+NWKS_KEY
apps="lora:apps_key:"+APPS_KEY
print(dev+" "+nwk+" "+apps)
#lora.set_config(dev_addr=DEV_ADDR,
#                apps_key=APPS_KEY,
#                nwks_key=NWKS_KEY)
#
if joinmode == 'OTA':
    print('Set join mode to OTA and configure appropriate keys')
    lora.set_config('lora:join_mode:0')
    lora.set_config('lora:app_eui:XXXXXXXXXXXXXX')
    lora.set_config('lora:app_key:XXXXXXXXXXXXXX')
else:
    print('Set join mode to ABP and set appropriate keys')
    lora.set_config('lora:join_mode:1')
    lora.set_config(dev)
    lora.set_config(nwk)
    lora.set_config(apps)    
    
print('Set data rate to 5 (old version 1)')
lora.set_config('lora:dr:5')

print('Join to LoRa network')
status = lora.join()

print('Set LoRa to confirmation mode')
lora.set_config('lora:confirm:0')

#lora.set_config(dev_eui='303838365338710C',app_eui='70B3D57ED0030AF7',app_key='07487AD99477A0AEC0D02A75DA25D94F' )
#lora.set_config(app_eui='70B3D57ED0030AF7',
#                app_key='07487AD99477A0AEC0D02A75DA25D94F')




#print("config")
#lora.join_abp()
#print("join_abp")
#lora.dr = 1
#print("lora.dr")

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])
       
logfile_path = "/home/pi/Desktop/Data/"

logfile = logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"
f1 = open(logfile, "r")
last_line = f1.readlines()[-1]
f1.close()
IP=(last_line.split(',')[2])
#if ip --> dann lora ?
time_RP=(last_line.split(',')[0])
time_RP=datetime.strptime(time_RP,"%Y-%m-%d %H:%M") 
#day=int(time_RP.strftime("%d"))
#day_b=bytes.fromhex('{:02x}'.format(day))
#month=int(time_RP.strftime("%m"))
#month_b=bytes.fromhex('{:02x}'.format(month))
#year=int(time_RP.strftime("%Y"))
#year_b=bytes.fromhex('{:04x}'.format(year))
#hour=int(time_RP.strftime("%H"))
#hour_b=bytes.fromhex('{:02x}'.format(hour))
#minute=int(time_RP.strftime("%M"))
#minute_b=bytes.fromhex('{:02x}'.format(minute))

#dht22_vp=int(round(float(last_line.split(',')[3]),2)*100)
#if dht22_vp==-999900: dht22_vp=9999
#dht22_vp_b=bytes.fromhex('{:04x}'.format(dht22_vp))
#print(dht22_vp_b)

dht22_vp_raw=int(round(float(last_line.split(',')[4]),2)*100)
if dht22_vp_raw==-999900: dht22_vp_raw=9999
dht22_vp_raw_b=bytes.fromhex('{:04x}'.format(dht22_vp_raw))

#dht22_humidity=int(round(float(last_line.split(',')[5]),1)*10)
#if dht22_humidity==-99990: dht22_humidity=9999
#dht22_humidity_b=bytes.fromhex('{:04x}'.format(dht22_humidity))
#print(dht22_humidity_b)

#dht22_humidity_raw=int(round(float(last_line.split(',')[6]),1)*10)
#if dht22_humidity_raw==-99990: dht22_humidity_raw=9999
#dht22_humidity_raw_b=bytes.fromhex('{:04x}'.format(dht22_humidity_raw))

#dht22_temperature=int(round(float(last_line.split(',')[7])+273.15,1)*10)
#if dht22_temperature==-97259: dht22_temperature=9999
#print(dht22_temperature)
#dht22_temperature_b=bytes.fromhex('{:04x}'.format(dht22_temperature))
#print(dht22_temperature_b)

dht22_temperature_raw=int(round(float(last_line.split(',')[8])+273.15,1)*10)
if dht22_temperature_raw==-97259: dht22_temperature_raw=9999
dht22_temperature_raw_b=bytes.fromhex('{:04x}'.format(dht22_temperature_raw))
#print(dht22_temperature_raw_b)

v=int(round(float(last_line.split(',')[9]),1)*10)
if v==-99990: v=9999
v_b=bytes.fromhex('{:04x}'.format(v))
#print(v_b)

#bg_calib=int(round(float(last_line.split(',')[10])+273.15,1)*10)
#if bg_calib==-97259: bg_calib=9999
#bg_calib_b=bytes.fromhex('{:04x}'.format(bg_calib))
#print(bg_calib_b)

bg_raw=int(round(float(last_line.split(',')[11])+273.15,1)*10)
if bg_raw==-97259: bg_raw=9999
bg_raw_b=bytes.fromhex('{:04x}'.format(bg_raw))
#print(bg_raw_b)

#tmrt=int(round(float(last_line.split(',')[12])+273.15,1)*10)
#if tmrt==-97259: tmrt=int(9999)
#print(tmrt)
#tmrt_b=bytes.fromhex('{:04x}'.format(tmrt))
#print(tmrt_b)


#Light_Level=65535
Light_Level=int(round(float(last_line.split(',')[13]),0))
if Light_Level==-9999: Light_Level=9999
#print(Light_Level)
Light_Level_b=bytes.fromhex('{:04x}'.format(Light_Level))
#print(Light_Level_b)

#mlx_e=int(round(float(last_line.split(',')[14]))*10)
#if mlx_e==-99990: mlx_e=9999
#print(mlx_e)
#mlx_e_b=bytes.fromhex('{:04x}'.format(mlx_e))
#print(mlx_e_b)

mlx_o=int(round(float(last_line.split(',')[15])+273.15,1)*10)
if mlx_o==-97259: mlx_o=9999
#print(mlx_o)
mlx_o_b=bytes.fromhex('{:04x}'.format(mlx_o))
#print(mlx_o_b)


#mlx_a=int(round(float(last_line.split(',')[16])+273.15,1)*10)
#if mlx_a==-97259: mlx_a=9999
#print("mlx_a: "+str(mlx_a))
#mlx_a_b=bytes.fromhex('{:04x}'.format(mlx_a))
#print("mlx_a_b: "+str(mlx_a_b))
 
#utci=(last_line.split(',')[17])
#if float(utci)==-9999: utci=None
#sl=(last_line.split(',')[18])
#if float(sl)==-9999: sl=None
#Insert Data to mysql

#lora.send(year_b+month_b+day_b+hour_b+minute_b+raspberryid_b+dht22_vp_b+dht22_vp_raw_b+dht22_humidity_b+dht22_humidity_raw_b+dht22_temperature_b+dht22_temperature_raw_b+v_b+bg_calib_b+bg_raw_b+tmrt_b+Light_Level_b+mlx_e_b+mlx_o_b+mlx_a_b)
#lora.send(year_b+month_b+day_b+hour_b+minute_b+raspberryid_b+dht22_vp_b+dht22_humidity_b+dht22_temperature_b+v_b+bg_calib_b+tmrt_b+Light_Level_b+mlx_e_b)
#lora.send(dht22_vp_raw_b+dht22_temperature_raw_b+v_b+bg_raw_b+Light_Level_b+mlx_o_b)

#print("LoRa Data transmitted")      
#lora.close()
#print("close")
#exit(0)

print(time_RP,raspberryid,IP,dht22_vp_raw,dht22_temperature_raw,v,bg_raw,Light_Level,mlx_o)
print(dht22_vp_raw_b+dht22_temperature_raw_b+v_b+bg_raw_b+Light_Level_b+mlx_o_b)
lora.send_lora(dht22_vp_raw_b+dht22_temperature_raw_b+v_b+bg_raw_b+Light_Level_b+mlx_o_b, port=1)
#print('Wait for and display confirmation response')
#events=lora.get_events(timeout=10)
#for x in events:
#    print('\t',x)
#
print('Close connection to module')
lora.close()
