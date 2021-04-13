#!/usr/bin/env python3
"""RAK811 ABP demo.
Minimalistic ABP demo (v3.x firmware)
Copyright 2021 Philippe Vanhaesendonck
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
SPDX-License-Identifier: Apache-2.0
"""
import time
import random

random_sleep=random.randint(40,170)
print("Sleep: "+str(random_sleep))
time.sleep(random_sleep)
import logging
import csv
import sys
import os
from datetime import datetime

from rak811.rak811_v3 import Rak811
from ttn_secrets import APPS_KEY, DEV_ADDR, NWKS_KEY
logging.basicConfig(level=logging.DEBUG)
lora = Rak811()


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
print(time_RP,raspberryid,IP,dht22_vp_raw,dht22_temperature_raw,v,bg_raw,Light_Level,mlx_o)


# Most of the setup should happen only once...
print('Setup')
# Ensure we are in LoRaWan mode
lora.set_config('lora:work_mode:0')
# Select ABP
lora.set_config('lora:join_mode:1')
# Select region
lora.set_config('lora:region:EU868')
# Set keys
lora.set_config(f'lora:dev_addr:{DEV_ADDR}')
lora.set_config(f'lora:apps_key:{APPS_KEY}')
lora.set_config(f'lora:nwks_key:{NWKS_KEY}')
# Set data rate
# Note that DR is different from SF and depends on the region
# See: https://docs.exploratory.engineering/lora/dr_sf/
# Set Data Rate to 5 which is SF7/125kHz for EU868
lora.set_config('lora:dr:1')

# Print config
for line in lora.get_config('lora:status'):
    print(f'    {line}')

print('Joining')
lora.join()

print('Sending packets every minute - Interrupt to cancel loop')
print('You can send downlinks from the TTN console')
try:
    lora.send(dht22_vp_raw_b+dht22_temperature_raw_b+v_b+bg_raw_b+Light_Level_b+mlx_o_b)
except:  # noqa: E722
    pass

#try:
#    while True:
#        print('Sending packet')
#        #Cayenne lpp random value as analog
#        lora.send(bytes.fromhex('0102{:04x}'.format(randint(0, 0x7FFF))))
#        lora.send(dht22_vp_raw_b+dht22_temperature_raw_b+v_b+bg_raw_b+Light_Level_b+mlx_o_b)
#        while lora.nb_downlinks:
#            print('Received', lora.get_downlink()['data'].hex())
#
#        time.sleep(60)
#except:  # noqa: E722
#    pass

print('Cleaning up')
lora.close()
print('close')
exit(0)
