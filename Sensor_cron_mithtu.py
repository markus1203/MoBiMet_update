#! /usr/bin/python
# -*- coding: utf-8 -*-
# Version 25.01.2021
import sys
import os
from datetime import datetime
import Adafruit_DHT
import numpy
import socket
import math
import csv
import glob
from smbus2 import SMBus
from mlx90614 import MLX90614
from StringIO import StringIO
from gpiozero import CPUTemperature
from UTCI import *
from PET import *


now = datetime.now() # current date and time

computer_time=now.strftime("%Y-%m-%d %H:%M") 
computer_day=now.strftime("%Y-%m-%d") 
computer_Hour=now.strftime("%H") 

f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])

calib_file = "/home/pi/Desktop/calibration_coefficients.csv"
f1 = open(calib_file, "r")
line = f1.readlines()[int(raspberryid)]
f1.close()

temperature_cal_a1 = float(line.split(',')[2]) # enter the calibration coefficient slope for temperature
temperature_cal_a0 =  float(line.split(',')[1]) # enter the calibration coefficient offset for temperature
vappress_cal_a1 =  float(line.split(',')[4]) # enter the calibration coefficient slope for vapour pressure
vappress_cal_a0 =  float(line.split(',')[3]) # enter the calibration coefficient offset for vapour pressure
bg_cal_a1 =  float(line.split(',')[6]) 
bg_cal_a0 =  float(line.split(',')[5]) 
HTU_RH_a0 =  float(line.split(',')[9]) 
HTU_RH_a1 =  float(line.split(',')[10]) 
HTU_Ta_a0 =  float(line.split(',')[11]) 
HTU_Ta_a1 =  float(line.split(',')[12]) 


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

#HTU

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os, sys, time, signal

#!/usr/bin/python
import struct, array, time, io, fcntl
try:
    I2C_SLAVE=0x0703
    HTU21D_ADDR = 0x40
    CMD_READ_TEMP_HOLD = "\xE3"
    CMD_READ_HUM_HOLD = "\xE5"
    CMD_READ_TEMP_NOHOLD = "\xF3"
    CMD_READ_HUM_NOHOLD = "\xF5"
    CMD_WRITE_USER_REG = "\xE6"
    CMD_READ_USER_REG = "\xE7"
    CMD_SOFT_RESET= "\xFE"

    class i2c(object):
       def __init__(self, device, bus):

          self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
          self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

          # set device address

          fcntl.ioctl(self.fr, I2C_SLAVE, device)
          fcntl.ioctl(self.fw, I2C_SLAVE, device)

       def write(self, bytes):
          self.fw.write(bytes)

       def read(self, bytes):
          return self.fr.read(bytes)

       def close(self):
          self.fw.close()
          self.fr.close()

    class HTU21D(object):
       def __init__(self):
          self.dev = i2c(HTU21D_ADDR, 1) #HTU21D 0x40, bus 1
          self.dev.write(CMD_SOFT_RESET) #soft reset
          time.sleep(.1)

       def ctemp(self, sensorTemp):
          tSensorTemp = sensorTemp / 65536.0
          return -46.85 + (175.72 * tSensorTemp)

       def chumid(self, sensorHumid):
          tSensorHumid = sensorHumid / 65536.0
          return -6.0 + (125.0 * tSensorHumid)

       def crc8check(self, value):
          # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
          remainder = ( ( value[0] << 8 ) + value[1] ) << 8
          remainder |= value[2]
          
          # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
          # divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
          divsor = 0x988000
          
          for i in range(0, 16):
             if( remainder & 1 << (23 - i) ): remainder ^= divsor
             divsor = divsor >> 1
          
          if remainder == 0:
             return True
          else:
             return False
       
       def read_tmperature(self):
          self.dev.write(CMD_READ_TEMP_NOHOLD) #measure temp
          time.sleep(.1)

          data = self.dev.read(3)
          buf = array.array('B', data)

          if self.crc8check(buf):
             temp = (buf[0] << 8 | buf [1]) & 0xFFFC
             return self.ctemp(temp)
          else:
             return -255
             
       def read_humidity(self):
          self.dev.write(CMD_READ_HUM_NOHOLD) #measure humidity
          time.sleep(.1)

          data = self.dev.read(3)
          buf = array.array('B', data)
          
          if self.crc8check(buf):
             humid = (buf[0] << 8 | buf [1]) & 0xFFFC
             return self.chumid(humid)
          else:
             return -255
             
    if __name__ == "__main__":
       obj = HTU21D()
       print "Temp:", obj.read_tmperature(), "C"
       print "Humid:", obj.read_humidity(), "% rH"
       htu_temp=round(obj.read_tmperature(),1)
       htu_rh=round(obj.read_humidity(),1)
       htu_temp_calib=round(HTU_Ta_a0+htu_temp*HTU_Ta_a1,1)
       htu_rh_calib=round(HTU_RH_a0+htu_rh*HTU_RH_a1,1)
       
except IOError:
       htu_temp=-9999
       htu_rh=-9999
       htu_temp_calib=-9999
       htu_rh_calib=-9999
# DHT22

dht22_pin = 27 # pin for DHT22 Data
dht22_sensor = Adafruit_DHT.DHT22

dht22_humidity, dht22_temperature = Adafruit_DHT.read_retry(dht22_sensor, dht22_pin)
if dht22_humidity is not None and dht22_temperature is not None:
    dht22_temperature_raw=round(dht22_temperature,5)
    dht22_temperature_calib=round(dht22_temperature * temperature_cal_a1 + temperature_cal_a0,3)
    dht22_temperature = dht22_temperature_calib
    saturation_vappress_ucalib = 6.113 * numpy.exp((2501000.0/461.5)*((1.0/273.15)-(1.0/(dht22_temperature_raw+273.15))))           #Clausius-Clapeyron-Gleichung
    saturation_vappress_calib = 6.113 * numpy.exp((2501000.0/461.5)*((1.0/273.15)-(1.0/(dht22_temperature_calib+273.15))))
    #saturation_vappress_ucalib= 6.1078 * numpy.exp((17.08085*dht22_temperature_raw)/(234.175+dht22_temperature_raw))      # Ansatz für VPmax in der Psychrometertafel
    #saturation_vappress_calib= 6.1078 * numpy.exp((17.08085*dht22_temperature_calib)/(234.175+dht22_temperature_calib))
    dht22_vappress=(dht22_humidity/100.0)*saturation_vappress_ucalib
    #dht22_vappress=(dht22_humidity/100.0)*saturation_vappress_calib
    dht22_vappress_raw=round(dht22_vappress,3)
    dht22_vappress_calib=round(dht22_vappress * vappress_cal_a1 + vappress_cal_a0,3)
    dht22_vappress = dht22_vappress_calib
    dht22_humidity_raw=round(dht22_humidity,5)
    dht22_humidity = round(100 * (dht22_vappress_calib / saturation_vappress_calib),5)
    if dht22_humidity >100:dht22_humidity=100
else:
    dht22_temperature_raw=-9999
    dht22_temperature=-9999
    dht22_vappress=-9999
    dht22_vappress_raw=-9999
    dht22_humidity=-9999
    dht22_humidity_raw=-9999

#CPU_TEMP
try:
    cpu = CPUTemperature()
    cpu_ta = cpu.temperature   
except (LookupError):
    cpu_ta=-9999

# Wind
logfile_wind="/home/pi/Desktop/wind.csv"

if os.path.exists(logfile_wind):
    f1 = open(logfile_wind, "r")
    v = float(f1.read())
    f1.close()
else:
    v= -9999

# Black Globe
try:
    pfad = "/sys/bus/w1/devices/"
    sensor_ordner = glob.glob(pfad + "28*")[0]
    sensor_daten_pfad = sensor_ordner + "/w1_slave"

    def temperatur_lesen():
      datei = open(sensor_daten_pfad, "r")
      zeilen = datei.readlines()
      datei.close()
      return zeilen

    def grad_lesen():
      zeilen = temperatur_lesen()
      while zeilen[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        zeilen = temperatur_lesen()
      equals_pos = zeilen[1].find('t=')
      if equals_pos != -1:
          temp_string = zeilen[1][equals_pos+2:]
          temp_c = float(temp_string) / 1000.0
          return temp_c

    bg_raw = grad_lesen()
    bg_calib = bg_cal_a0+ bg_raw * bg_cal_a1
    if v < 0.1: v_tmrt= 0.1
    else: v_tmrt= v
    try:
        tmrt=((((bg_calib+273.15)**4)+((1.54023939374378*(10**8)*(v_tmrt**0.462186526822537))/(0.95*(0.05**0.4)))*(bg_calib - dht22_temperature))**0.25)-273.15
      #  tmrt=((((bg_calib+273.15)**4)+((1.1*(10**8)*(v_tmrt**0.6))/(0.95*(0.04**0.4)))*(bg_calib - dht22_temperature))**0.25)-273.15
    except (ValueError):
        tmrt=-9999
except (IndexError):
    bg_raw = -9999
    bg_calib = -9999
    tmrt= -9999 

# Light Sensor BH1750
bus = SMBus(1)

try:
    #data=bus.read_i2c_block_data(0x23,0x21,0x07)
    data=bus.read_i2c_block_data(0x23,0x10,0x07)
    #print(data)
    lightLevel=(data[1] + (256 * data[0])) / 1.2
except (IOError):
    lightLevel=-9999
    
bus.close()

# mlx
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
try:
    mlx_a= sensor.get_ambient()
    mlx_o= sensor.get_object_1()
    mlx_e=(5.670374419 *(10**(-8)))*((mlx_o + 273.15)**4)
except (IOError):
    mlx_a= -9999
    mlx_o= -9999
    mlx_e=-9999

bus.close()
    

# UTCI
if v < 0.1: v_utci= 0.1
else: v_utci= v * 1.5

if dht22_temperature==-9999 or tmrt==-9999 :
    utci=-9999
    comf_utci=-9999
    sl_utci=-9999
else:
    if htu_rh_calib==-9999:
        utci=universal_thermal_climate_index(dht22_temperature, tmrt, v_utci, dht22_humidity)
    else:
        utci=universal_thermal_climate_index(dht22_temperature, tmrt, v_utci, htu_rh_calib)
    comf_utci=comfortable(utci)
    sl_utci=stresslevel(utci)

# PET
if v < 0.1: v_pet= 0.1
else: v_pet= v

if dht22_temperature==-9999 or tmrt==-9999 :
    pet=-9999
    comf_pet=-9999
    sl_pet=-9999
else:
    # Input data for the PET 
    age = 35
    sex = 1 # 1 for men and 2 for women
    pos = 2 #1 for standing 2 for sitting 
    mbody = 75 #[kg]
    ht = 1.80 #[m]
    p = 1013.25 #[hPa]
    M = 80 # [W] Metabolic activity level
    icl = 0.9 # [clo] Clothing level

    # Results 
    if htu_rh_calib==-9999:
         Tstable = resolution(dht22_temperature,tmrt,dht22_humidity,v_pet,age,sex,ht,mbody,pos,M,icl,T)[0]
    else:        
        Tstable = resolution(dht22_temperature,tmrt,htu_rh_calib,v_pet,age,sex,ht,mbody,pos,M,icl,T)[0]
    #print("Nodes temperature [T_core, T_skin, T_clo]",Tstable)
    #print('Thermal Balance', Syst(Tstable, Ta, Tmrt, HR, v, age, sex, ht, mbody, pos, M, icl,True)[0])
    #print('PET:', round(PET(age, sex, ht, mbody, pos, M, icl, Tstable, Tmin, Tmax, eps),2))
    pet = round(PET(age, sex, ht, mbody, pos, M, icl, Tstable, Tmin, Tmax, eps),1)
    sl_pet=stresslevel_PET(pet)
    comf_pet=comfortable_PET(pet)

logfile_path ="/home/pi/Desktop/Data/"
logfile =logfile_path+raspberryid+"-"+computer_day+".csv"

print(computer_time+","+raspberryid+","+get_ip()+","+"{0:.3f}".format(dht22_vappress)+","+"{0:.3f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.3f}".format(dht22_temperature_raw)+","+"{0:.3f}".format(v)+","+"{0:.2f}".format(bg_calib)+","+"{0:.2f}".format(bg_raw)+","+"{0:.2f}".format(tmrt)+","+"{0:.2f}".format(lightLevel)+","+"{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl_utci)+","+str(cpu_ta)+"\n")

if os.path.exists(logfile):
    f0=open(logfile,"a")
    f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.2f}".format(dht22_vappress)+","+"{0:.2f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.1f}".format(dht22_temperature_raw)+","+"{0:.3f}".format(v)+","+"{0:.1f}".format(bg_calib)+","+"{0:.1f}".format(bg_raw)+","+"{0:.1f}".format(tmrt)+","+"{0:.1f}".format(lightLevel)+","+"{0:.1f}".format(mlx_e)+","+"{0:.1f}".format(mlx_o)+","+"{0:.1f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl_utci)+","+"{0:.1f}".format(pet)+","+str(sl_pet)+","+"{0:.1f}".format(cpu_ta)+","+str(htu_temp)+","+str(htu_rh)+","+str(htu_temp_calib)+","+str(htu_rh_calib)+"\n")
    f0.close()
    print("Data in logfile "+computer_time)
else:
    f0=open(logfile,"w")
    f0.write("Raspi_Time,RaspberryID,IP,VP(hPa)_DHT22_calib,VP(hPa)_DHT22_raw,Rel_Hum(%)_DHT22_calib,Rel_Hum(%)_DHT22_raw,Ta(°C)_DHT22_calib,Ta(°C)_DHT22_raw,Wind(m/s),BG(°C)_calib,BG(°C)_raw,Tmrt(°C),Light_Level(lx),MLX_E(W/m²),MLX_O(°C),MLX_A(°C),UTCI(°C),Stresslevel_utci,PET(°C),Stresslevel_pet,CPU_TEMP(°C),Ta_HTU(°C),RH_HTU(%),Ta_HTU_calib(°C),RH_HTU_calib(%)\n")
    f0.close()
    f0=open(logfile,"a")
    f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.2f}".format(dht22_vappress)+","+"{0:.2f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.1f}".format(dht22_temperature_raw)+","+"{0:.3f}".format(v)+","+"{0:.1f}".format(bg_calib)+","+"{0:.1f}".format(bg_raw)+","+"{0:.1f}".format(tmrt)+","+"{0:.1f}".format(lightLevel)+","+"{0:.1f}".format(mlx_e)+","+"{0:.1f}".format(mlx_o)+","+"{0:.1f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl_utci)+","+"{0:.1f}".format(pet)+","+str(sl_pet)+","+"{0:.1f}".format(cpu_ta)+","+str(htu_temp)+","+str(htu_rh)+","+str(htu_temp_calib)+","+str(htu_rh_calib)+"\n")
    f0.close()
    print("Data in logfile "+computer_time)

if get_ip()=='127.0.0.1':
    print("connection lost")
    logfile_cl = "/home/pi/Desktop/"+raspberryid+"-connection-lost-"+computer_day+"_"+computer_Hour+".csv"
    if os.path.exists(logfile_cl):
        f0=open(logfile_cl,"a")
        f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.2f}".format(dht22_vappress)+","+"{0:.2f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.1f}".format(dht22_temperature_raw)+","+"{0:.3f}".format(v)+","+"{0:.1f}".format(bg_calib)+","+"{0:.1f}".format(bg_raw)+","+"{0:.1f}".format(tmrt)+","+"{0:.1f}".format(lightLevel)+","+"{0:.1f}".format(mlx_e)+","+"{0:.1f}".format(mlx_o)+","+"{0:.1f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl_utci)+","+"{0:.1f}".format(pet)+","+str(sl_pet)+","+"{0:.1f}".format(cpu_ta)+","+str(htu_temp)+","+str(htu_rh)+","+str(htu_temp_calib)+","+str(htu_rh_calib)+"\n")
        f0.close()
    else:
        f0=open(logfile_cl,"w")
        f0.write("Raspi_Time,RaspberryID,IP,VP(hPa)_DHT22_calib,VP(hPa)_DHT22_raw,Rel_Hum(%)_DHT22_calib,Rel_Hum(%)_DHT22_raw,Ta(°C)_DHT22_calib,Ta(°C)_DHT22_raw,Wind(m/s),BG(°C)_calib,BG(°C)_raw,Tmrt(°C),Light_Level(lx),MLX_E(W/m²),MLX_O(°C),MLX_A(°C),UTCI(°C),Stresslevel_utci,PET(°C),Stresslevel_pet,CPU_TEMP(°C),Ta_HTU(°C),RH_HTU(%),Ta_HTU_calib(°C),RH_HTU_calib(%)\n")
        f0.close()
        f0=open(logfile_cl,"a")
        f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.2f}".format(dht22_vappress)+","+"{0:.2f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.1f}".format(dht22_temperature_raw)+","+"{0:.3f}".format(v)+","+"{0:.1f}".format(bg_calib)+","+"{0:.1f}".format(bg_raw)+","+"{0:.1f}".format(tmrt)+","+"{0:.1f}".format(lightLevel)+","+"{0:.1f}".format(mlx_e)+","+"{0:.1f}".format(mlx_o)+","+"{0:.1f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl_utci)+","+"{0:.1f}".format(pet)+","+str(sl_pet)+","+"{0:.1f}".format(cpu_ta)+","+str(htu_temp)+","+str(htu_rh)+","+str(htu_temp_calib)+","+str(htu_rh_calib)+"\n")
        f0.close()
else: print("connected")
exit(0)
