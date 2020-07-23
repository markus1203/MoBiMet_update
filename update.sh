#!/bin/bash
# -*- coding: utf-8 -*-
cd /home/pi
git clone https://Markus1203:MeteoMarkus3@github.com/markus1203/MoBiMet_update.git
sudo cp -r /home/pi/MoBiMet_update/*.py /home/pi/Desktop/py-Scripts/
sudo cp -r /home/pi/MoBiMet_update/*.csv /home/pi/Desktop/
sudo rm -r /home/pi/MoBiMet_update/
