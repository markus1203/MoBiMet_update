#!/usr/bin/python

# Version 03.11.2020

from gpiozero import Button
import time
import math
import os


def spin():
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

def calculate_speed(time_sec):
    global wind_count
    if wind_count>0:
        speed=0.485451+wind_count*0.005361
    else:
        speed=0
    #circumference_m = (2*math.pi)*radius_m
    #rotations = wind_count / 2.0
        
    #dist_m = circumference_m * rotations
    #speed = dist_m / time_sec
    return speed


f1 = open("/home/pi/Desktop/r_id.csv", "r")
line_id = f1.readlines()[0]
f1.close()
raspberryid =  (line_id.split(',')[0])

calib_file = "/home/pi/Desktop/calibration_coefficients.csv"
f1 = open(calib_file, "r")
line = f1.readlines()[int(raspberryid)]
f1.close()
wind = str(line.split(',')[8])
print(wind)

logfile_wind="/home/pi/Desktop/wind.csv"

if wind=='y':
   
    wind_count = 0
    #radius_m = 0.0625
    wind_interval = 57
    
    wind_speed_sensor = Button(21)    
    wind_speed_sensor.when_pressed = spin

    time.sleep(wind_interval)    
    v=calculate_speed(wind_interval)
    
    print( str(v) + " m/s " + " // Windcount in last 55 seconds: " + str(wind_count) +" //  " +time.strftime("%Y-%m-%d %H:%M:%S") )
    f0=open(logfile_wind,"w")
    f0.write(str(v))
    f0.close()
    print("Data in logfile_wind  "+time.strftime("%Y-%m-%d %H:%M:%S"))

if wind=='n':
    v_na=-9999
    f0=open(logfile_wind,"w")
    f0.write(str(v_na))
    f0.close()
    print("NA in logfile_wind  "+time.strftime("%Y-%m-%d %H:%M:%S"))    
exit(0)

