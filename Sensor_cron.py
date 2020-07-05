#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import Adafruit_DHT
import numpy
import socket
import math
import csv
import glob
from smbus2 import SMBus
from mlx90614 import MLX90614
from StringIO import StringIO
from UTCI import *

computer_time=time.strftime("%Y-%m-%d %H:%M") 


f1 = open("/home/pi/Desktop/r_id.csv", "r")
raspberryid = f1.read()
f1.close()

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
    #dht22_vappress=(dht22_humidity/100.0)*saturation_vappress_ucalib
    dht22_vappress=(dht22_humidity/100.0)*saturation_vappress_calib
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

# Wind

logfile_wind="/home/pi/Desktop/wind.csv"

if os.path.exists(logfile_wind):
    f1 = open(logfile_wind, "r")
    v = float(f1.read())
    f1.close()
else:
    v= -9999

# Black Globe

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
tmrt=-9999 #needed after Thorsson et al 2007: Tg = the globe temperature (°C),Va = the air velocity (ms−1),Ta = the air temperature (°C),D = the globe diameter (mm),ε = the globe emissivity



# Light Sensor BH1750

bus = SMBus(1)

try:
    #data=bus.read_i2c_block_data(0x23,0x21,0x07)
    data=bus.read_i2c_block_data(0x23,0x10,0x07)
    #print(data)
    lightLevel=(data[1] + (256 * data[0])) / 1.2
except (IOError):
    lightLevel=-9999


#if lightLevel==None : lightLevel=-9999

# mlx

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
try:
    mlx_a= sensor.get_ambient()
    mlx_o= sensor.get_object_1()
    mlx_e=(5.670374419 *(10**(-8)))*((mlx_a + 273.15)**4)
except (IOError):
    mlx_a= -9999
    mlx_o= -9999
    mlx_e=-9999

bus.close()
    

# UTCI
if v==-9999: v_utci= 0.1
else: v_utci= v * 1.5

if dht22_temperature==-9999:
    utci=-9999
    comf=-9999
    sl=-9999
else:
    utci=universal_thermal_climate_index(dht22_temperature, dht22_temperature, v_utci, dht22_humidity)
    comf=comfortable(utci)
    sl=stresslevel(utci)



logfile_path ="/home/pi/Desktop/Data/"
logfile =logfile_path+raspberryid+"-"+time.strftime("%Y-%m-%d")+".csv"


#print("{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+str(lightLevel))
#print(mlx_e,mlx_a,mlx_o,  computer_time,raspberryid,"{0:.2f} hPa".format(dht22_vappress),"{0:.1f} %".format(dht22_humidity),"{0:.1f} C".format(dht22_temperature),"{0:.1f} m/s".format(v),"{0:.1f} C".format(utci), "{0:.2f} lx".format(lightLevel), sl)   

print(computer_time+","+raspberryid+","+get_ip()+","+"{0:.3f}".format(dht22_vappress)+","+"{0:.3f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.3f}".format(dht22_temperature_raw)+","+"{0:.2f}".format(v)+","+"{0:.2f}".format(bg_calib)+","+"{0:.2f}".format(bg_raw)+","+"{0:.2f}".format(tmrt)+","+"{0:.2f}".format(lightLevel)+","+"{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl))


if os.path.exists(logfile):
    f0=open(logfile,"a")
    f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.3f}".format(dht22_vappress)+","+"{0:.3f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.3f}".format(dht22_temperature_raw)+","+"{0:.2f}".format(v)+","+"{0:.2f}".format(bg_calib)+","+"{0:.2f}".format(bg_raw)+","+"{0:.2f}".format(tmrt)+","+"{0:.2f}".format(lightLevel)+","+"{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl)+","+"\n")
    f0.close()
    print("Data in logfile "+time.strftime("%Y-%m-%d %H:%M:%S"))
else:
    f0=open(logfile,"w")
    f0.write("Raspi_Time,RaspberryID,IP,VP(hPa)_DHT22_calib,VP(hPa)_DHT22_raw,Rel_Hum(%)_DHT22_calib,Rel_Hum(%)_DHT22_raw,Ta(°C)_DHT22_calib,Ta(°C)_DHT22_raw,Wind(m/s),BG(°C)_calib,BG(°C)_raw,Tmrt(°C),Light_Level(lx),MLX_E(W/m²),MLX_O(°C),MLX_A(°C),UTCI(°C),Stresslevel\n")
    f0.close()
    f0=open(logfile,"a")
    f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.3f}".format(dht22_vappress)+","+"{0:.3f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.3f}".format(dht22_temperature_raw)+","+"{0:.2f}".format(v)+","+"{0:.2f}".format(bg_calib)+","+"{0:.2f}".format(bg_raw)+","+"{0:.2f}".format(tmrt)+","+"{0:.2f}".format(lightLevel)+","+"{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl)+","+"\n")
    f0.close()
    print("Data in logfile "+time.strftime("%Y-%m-%d %H:%M:%S"))

    
if get_ip()=='127.0.0.1':
    print("connection lost")
    logfile_cl = "/home/pi/Desktop/"+raspberryid+"-connection-lost"+".csv"
    if os.path.exists(logfile_cl):
        f0=open(logfile_cl,"a")
        f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.3f}".format(dht22_vappress)+","+"{0:.3f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.3f}".format(dht22_temperature_raw)+","+"{0:.2f}".format(v)+","+"{0:.2f}".format(bg_calib)+","+"{0:.2f}".format(bg_raw)+","+"{0:.2f}".format(tmrt)+","+"{0:.2f}".format(lightLevel)+","+"{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl)+","+"\n")
        f0.close()
    else:
        f0=open(logfile_cl,"w")
        f0.write("Raspi_Time,RaspberryID,IP,VP(hPa)_DHT22_calib,VP(hPa)_DHT22_raw,Rel_Hum(%)_DHT22_calib,Rel_Hum(%)_DHT22_raw,Ta(°C)_DHT22_calib,Ta(°C)_DHT22_raw,Wind(m/s),BG(°C)_calib,BG(°C)_raw,Tmrt(°C),Light_Level(lx),MLX_E(W/m²),MLX_O(°C),MLX_A(°C),UTCI(°C),Stresslevel\n")
        f0.close()
        f0=open(logfile_cl,"a")
        f0.write(computer_time+","+raspberryid+","+get_ip()+","+"{0:.3f}".format(dht22_vappress)+","+"{0:.3f}".format(dht22_vappress_raw)+","+"{0:.1f}".format(dht22_humidity)+","+"{0:.1f}".format(dht22_humidity_raw)+","+"{0:.1f}".format(dht22_temperature)+","+"{0:.3f}".format(dht22_temperature_raw)+","+"{0:.2f}".format(v)+","+"{0:.2f}".format(bg_calib)+","+"{0:.2f}".format(bg_raw)+","+"{0:.2f}".format(tmrt)+","+"{0:.2f}".format(lightLevel)+","+"{0:.2f}".format(mlx_e)+","+"{0:.2f}".format(mlx_o)+","+"{0:.2f}".format(mlx_a)+","+"{0:.1f}".format(utci)+","+str(sl)+","+"\n")
        f0.close()
else: print("connected")



