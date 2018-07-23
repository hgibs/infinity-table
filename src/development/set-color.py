#!/usr/bin/python
import RPi.GPIO as GPIO
import os, time, threading, sys

from Gibson_LED_Driver import Gibson_LED_Driver

# init LED driver on /dev/spidev0.0 with 50 LEDs
ledstring = Gibson_LED_Driver(0,0,50)
ledstring.colorwheel()
