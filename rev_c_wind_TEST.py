#!/usr/bin/python

# Version 28.10.2021

import time
import math
import os


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

	import Adafruit_GPIO.SPI as SPI

	import Adafruit_MCP3008

	TMP = 0
	RV = 1

	zeroWindAdjustment =  -.32

#mcp = Adafruit_MCP3008.MCP3008(clk=18,cs=25,miso=23,mosi=24)

	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	sum=0
	num=0
	minute=time.strftime("%M")

	print(minute)
	while minute==time.strftime("%M"):
    		TMP_ADunits = mcp.read_adc(TMP)
   		Wind_ADunits = mcp.read_adc(RV)
 		Wind_Volts = (Wind_ADunits * 0.0048828125)
    		TempCtimes100 = (0.005 * (float(TMP_ADunits) * float(TMP_ADunits))) - (16.862 * float(TMP_ADunits)) + 9075.4
    		zeroWind_ADunits = -0.0006 * (float(TMP_ADunits) * float(TMP_ADunits)) + 1.0727 * float(TMP_ADunits) + 47.172
   		zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment
    		try:
        		WindSpeed_MPH =  pow(((Wind_Volts - zeroWind_volts) /.2300) , 2.7265)
        		W = float(WindSpeed_MPH*0.44704)
    		except: W = None

    		print(W)
    		print(TMP_ADunits," | ", Wind_ADunits, " | ", Wind_Volts )
   		sum=sum+W
		num=num+1
		time.sleep(1)
	v=sum/num

  	print( str(v) + " m/s " + " // "  +time.strftime("%Y-%m-%d %H:%M:%S"))
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

