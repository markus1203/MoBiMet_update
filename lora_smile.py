#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#22.01.2021

from rak811 import Mode, Rak811
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
        lora = Rak811()
        print("rak")
        lora.hard_reset()
        print("reset")
        lora.mode = Mode.LoRaWan
        lora.band = 'EU868'
        print("band")
        #lora.set_config(dev_eui='303838365338710C',app_eui='70B3D57ED0030AF7',app_key='07487AD99477A0AEC0D02A75DA25D94F' )
        #lora.set_config(app_eui='70B3D57ED0030AF7',
        #                app_key='07487AD99477A0AEC0D02A75DA25D94F')

        print("DEV_ADDR: "+DEV_ADDR+" | NWKS_KEY: "+NWKS_KEY+" | APPS_KEY: "+APPS_KEY)
        lora.set_config(dev_addr=DEV_ADDR,
                        apps_key=APPS_KEY,
                        nwks_key=NWKS_KEY)

        print("config")
        lora.join_abp()
        print("join_abp")
        lora.dr = 1
        print("lora.dr")
        eins=bytes.fromhex('{:04x}'.format(1))
        lora.send(eins)
        print("LoRa Data transmitted")      
        lora.close()
        print("close")

        time.sleep(60)
               
    if key2state == False:
        print('zwei')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key2 Pressed '+b_time)
        print("start LoRa")
        lora = Rak811()
        print("rak")
        lora.hard_reset()
        print("reset")
        lora.mode = Mode.LoRaWan
        lora.band = 'EU868'
        print("band")
        #lora.set_config(dev_eui='303838365338710C',app_eui='70B3D57ED0030AF7',app_key='07487AD99477A0AEC0D02A75DA25D94F' )
        #lora.set_config(app_eui='70B3D57ED0030AF7',
        #                app_key='07487AD99477A0AEC0D02A75DA25D94F')

        print("DEV_ADDR: "+DEV_ADDR+" | NWKS_KEY: "+NWKS_KEY+" | APPS_KEY: "+APPS_KEY)
        lora.set_config(dev_addr=DEV_ADDR,
                        apps_key=APPS_KEY,
                        nwks_key=NWKS_KEY)

        print("config")
        lora.join_abp()
        print("join_abp")
        lora.dr = 1
        print("lora.dr")
        zwei=bytes.fromhex('{:04x}'.format(2))
        lora.send(zwei)
        print("LoRa Data transmitted")      
        lora.close()
        print("close")

        time.sleep(60)
                
    if key3state == False:
        print('drei')
        b_time=time.strftime("%Y-%m-%d %H:%M:%S")
        print('Key3 Pressed '+b_time)
        print("start LoRa")
        lora = Rak811()
        print("rak")
        lora.hard_reset()
        print("reset")
        lora.mode = Mode.LoRaWan
        lora.band = 'EU868'
        print("band")
        #lora.set_config(dev_eui='303838365338710C',app_eui='70B3D57ED0030AF7',app_key='07487AD99477A0AEC0D02A75DA25D94F' )
        #lora.set_config(app_eui='70B3D57ED0030AF7',
        #                app_key='07487AD99477A0AEC0D02A75DA25D94F')

        print("DEV_ADDR: "+DEV_ADDR+" | NWKS_KEY: "+NWKS_KEY+" | APPS_KEY: "+APPS_KEY)
        lora.set_config(dev_addr=DEV_ADDR,
                        apps_key=APPS_KEY,
                        nwks_key=NWKS_KEY)

        print("config")
        lora.join_abp()
        print("join_abp")
        lora.dr = 1
        print("lora.dr")
        drei=bytes.fromhex('{:04x}'.format(3))
        lora.send(drei)
        print("LoRa Data transmitted")      
        lora.close()
        print("close")

        time.sleep(60)


print("porgram closed")
