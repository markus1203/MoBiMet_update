#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#22.01.2021

from rak811v2 import Rak811v2
import csv
import sys
import os
import time
from datetime import datetime
from ttn_secrets_2 import APPS_KEY, DEV_ADDR, NWKS_KEY
# from StringIO import StringIO
# picdir="/home/pi/e-Paper/RaspberryPi&JetsonNano/python/pic"
# libdir="/home/pi/e-Paper/RaspberryPi&JetsonNano/python/lib"
# if os.path.exists(libdir):
    # sys.path.append(libdir)

# import logging
# from waveshare_epd import epd2in7b
# from PIL import Image,ImageDraw,ImageFont
# import traceback
import RPi.GPIO as GPIO

day=time.strftime("%d")
print("GO")

while day==time.strftime("%d"):
    joinmode = 'ABP'
    smiley=0
    GPIO.setmode(GPIO.BCM)
    key1 = 5
    key2 = 6
    key3 = 13
    GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    key1state = GPIO.input(key1)
    key2state = GPIO.input(key2)
    key3state = GPIO.input(key3)
            
    if key1state == False:
        print('eins')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key1 Pressed '+b_time)
        print("start LoRa")

        lora = Rak811v2()
        print("rak")
        lora.hard_reset()
        print("reset")

        lora.set_config('lora:region:EU868')
        print('Set loRa region')
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
    
        print('Set data rate to 5')
        lora.set_config('lora:dr:5')

        print('Join to LoRa network')
        status = lora.join()

        print('Set LoRa to confirmation mode')
        lora.set_config('lora:confirm:0')
        eins=bytes.fromhex('{:04x}'.format(1))
        lora.send_lora(eins,port=1)
        #print('Wait for and display confirmation response')
        #events=lora.get_events(timeout=10)
        #for x in events:
        #    print('\t',x)
        ##
        print('Close connection to module')
        lora.close()

        time.sleep(60)
        print('GO')
       
    if key2state == False:
        print('zwei')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key2 Pressed '+b_time)
        print("start LoRa")
        lora = Rak811v2()
        print("rak")
        lora.hard_reset()
        print("reset")

        lora.set_config('lora:region:EU868')
        print('Set loRa region')
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
    
        print('Set data rate to 5')
        lora.set_config('lora:dr:5')

        print('Join to LoRa network')
        status = lora.join()

        print('Set LoRa to confirmation mode')
        lora.set_config('lora:confirm:0')
        zwei=bytes.fromhex('{:04x}'.format(2))
        lora.send_lora(zwei,port=1)
        #print('Wait for and display confirmation response')
        #events=lora.get_events(timeout=10)
        #for x in events:
        #    print('\t',x)
        ##
        print('Close connection to module')
        lora.close()

        time.sleep(60)
        print('GO')
                
    if key3state == False:
        print('drei')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key3 Pressed '+b_time)
        print("start LoRa")
        lora = Rak811v2()
        print("rak")
        lora.hard_reset()
        print("reset")

        lora.set_config('lora:region:EU868')
        print('Set loRa region')
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
    
        print('Set data rate to 5')
        lora.set_config('lora:dr:5')

        print('Join to LoRa network')
        status = lora.join()

        print('Set LoRa to confirmation mode')
        lora.set_config('lora:confirm:0')
        drei=bytes.fromhex('{:04x}'.format(3))
        lora.send_lora(drei,port=1)
        #print('Wait for and display confirmation response')
        #events=lora.get_events(timeout=10)
        #for x in events:
        #    print('\t',x)
        ##
        print('Close connection to module')
        lora.close()

        time.sleep(60)
        print('GO')

print("porgram closed")
