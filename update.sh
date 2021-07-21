#!/bin/bash
# -*- coding: utf-8 -*-
cd /home/pi
git clone https://github.com/markus1203/MoBiMet_update.git
sudo cp -r /home/pi/MoBiMet_update/*.py /home/pi/Desktop/py-Scripts/
sudo cp -r /home/pi/MoBiMet_update/*.csv /home/pi/Desktop/
sudo cp -r /home/pi/MoBiMet_update/*.sh /home/pi/
sudo rm -r /home/pi/MoBiMet_update/
sudo reboot
