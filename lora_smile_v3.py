#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#22.01.2021

import csv
import sys
import os
import time
from datetime import datetime
from rak811.rak811_v3 import Rak811
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
        eins=bytes.fromhex('{:04x}'.format(1))
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key1 Pressed '+b_time)
        print("start LoRa")

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
            lora.send(eins)
        except:  # noqa: E722
            pass
        ##
        print('Close connection to module')
        lora.close()

        time.sleep(60)
        print('GO')
       
    if key2state == False:
        print('zwei')
        zwei=bytes.fromhex('{:04x}'.format(2))
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key2 Pressed '+b_time)
        print("start LoRa")

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
            lora.send(eins)
        except:  # noqa: E722
            pass
        ##
        print('Close connection to module')
        lora.close()

        time.sleep(60)
        print('GO')
                
    if key3state == False:
        print('drei')
        drei=bytes.fromhex('{:04x}'.format(3))        
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key3 Pressed '+b_time)
        print("start LoRa")
        print("start LoRa")

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
            lora.send(drei)
        except:  # noqa: E722
            pass
        ##
        print('Close connection to module')
        lora.close()

        time.sleep(60)
        print('GO')

print("porgram closed")
