#!/usr/bin/python
import RPi.GPIO as GPIO
import os, time, threading, sys, socket, logging, signal
import paho.mqtt.client as mqtt

from Gibson_LED_Driver import Gibson_LED_Driver

# ================================================================
# Configs
# ================================================================

loglocation = '/home/pi/inftable/run.log'

#status_id = "inftable1_stats"

mqtt_server = "bionic.mercury.intranet"
mqtt_port = 8883
mqtt_timeout = 60
mqtt_topic = "myhome/+/+/inftable"
#myhome/groundfloor/livingroom/inftable
mqtt_qos = 1 # PUB and PUBACK
mqtt_user = 'inftable'
mqtt_pwd = 'inftablemqtt'


# ================================================================
# Set up
# ================================================================

#log the start up
logging.basicConfig(filename=loglocation,level=logging.INFO,format='%(levelname)s:%(module)s:%(message)s')
logging.info("===========================")
logging.info("Starting up main-mqtt.py @" + str(time.time()))
logging.info("===========================")

# init GPIO pins
GPIO.setmode(GPIO.BCM)

# init LED driver on /dev/spidev0.0 with 50 LEDs
ledstring = Gibson_LED_Driver(0,0,50)

#pre-define function
def auto_shutdown():
    exit()
# pin 17 set up as input, pulled up to avoid false detection
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# pin is wired to connect to GND on button press
# so we'll be setting up falling edge detection
# this has a 300ms debounce so it should also reject errent presses
GPIO.add_event_detect(17, GPIO.FALLING, callback=auto_shutdown, bouncetime=300)

# set current scheme
#global scheme, thiscolor, newScheme
#scheme = "static"
program = "static"
colorpattern = "single"
thiscolor = [255,1,255]
altcolor = [255,255,255]
newScheme = True

#flash the string
ledstring.setAll(thiscolor)
ledstring.update()
time.sleep(0.1)
ledstring.update()
time.sleep(0.1)

# ================================================================
# Function Definitions
# ================================================================

# shutdown code
def auto_shutdown(self):
    ledstring.close()
    GPIO.cleanup()
    os.system("sudo shutdown -h now")
    ledstring.setAll([1,1,1])
    ledstring.update()
    time.sleep(0.01)
    exit()

#the main method controlling the LED driver
def step():
    global program, colorpattern, thiscolor, altcolor, newScheme

    if(newScheme):
        #update the driver for color and program
        logging.info("New program detected: "+program+','+colorpattern)
        ledstring.setColor(colorpattern, thiscolor, altcolor)
        ledstring.setProgram(program)
        newScheme = False
    ledstring.increment()

#### MACROS:

# def getColorString():
#     global thiscolor
#     return str(thiscolor[0]) + "/" + str(thiscolor[1]) + "/" + str(thiscolor[2])
#
# def setPulse():
#     global scheme
#     scheme = "pulse"
#     print "scheme set to pulse"
#
# def flyingColor(red=255,green=255,blue=255):
#     global scheme, thiscolor
#     scheme = "flyingcolor"
#     thiscolor = [int(red),int(green),int(blue)]
#     print "scheme set to flyingcolor"
#     #return to update UI in web
#     return getColorString()
#
# def colorwheel():
#     global scheme, newScheme
#     newScheme = True
#     scheme = "colorwheel"
#
# def randomstatic():
#     global scheme, newScheme
#     newScheme = True
#     scheme = "randomstatic"
#
# def rgb():
#     global scheme, newScheme
#     newScheme = True
#     scheme = "rgb"
#
# def spin():
#     global scheme
#     scheme = "spin"
#
# def static(red=255,green=255,blue=255):
#     global thiscolor, newScheme, scheme
#     scheme = "static"
#     thiscolor = [int(red),int(green),int(blue)]
#     newScheme = True
#     print "scheme set to static"
#     return getColorString()


# ================================================================
# MQTT handler init
# ================================================================

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    logging.info("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_topic, mqtt_qos)

def on_unsubscribe(client, userdata, mid):
    logging.info("Unsubscribing. Code "+str(mid))

def on_message(client, userdata, msg):
    global program, colorpattern, thiscolor, altcolor, newScheme

    print("Topic: " + str(msg.topic))
    logging.info("Topic: " + str(msg.topic))
    print('Message: '+str(msg.payload))
    logging.info('Message: '+str(msg.payload))
    #we're assuming we get commands in the form of set-______ = _______
    lines = str(msg.payload).split('\n')
    for line in lines:
        if "set" in line:
            parts = line.split('=')
            cmdraw = parts[0].split('set-')
            cmd = cmdraw[1].strip()

            param = parts[1].strip()
            if(cmd == 'color'):
                splitcolors = param.split(",")
                thiscolor = (int(splitcolors[0]),int(splitcolors[1]),int(splitcolors[2]))
                logging.info("Setting color to " + str(thiscolor))
                newScheme = True
            elif(cmd == 'altcolor'):
                splitcolors = param.split(",")
                altcolor = (int(splitcolors[0]),int(splitcolors[1]),int(splitcolors[2]))
                logging.info("Setting alternate color to " + str(altcolor))
                newScheme = True
            elif(cmd == 'program'):
                program = param
                logging.info("Setting program to "+param)
                newScheme = True
            elif(cmd == 'colorpattern'):
                colorpattern = param
                logging.info("Setting color pattern to "+param)
                newScheme = True
            elif(cmd == 'calibrate'):
                splitparams = param.split(",")
                speed = splitparams[0]
                width = splitparams[1]
                logging.info("Setting speed,width to "+param)
                #doesn't have to to update the program, does it on the fly
                ledstring.calibrate(speed,width)

def clean_exit():
    logging.info("Disconnecting and closing")
    client.disconnect()
    ledstring.close()
    GPIO.cleanup()
    exit()


# ================================================================
# Handle SIGTERM
# ================================================================
def signalhandler(signum, frame):
    logging.info("Received signal "+str(signum))
    clean_exit()

signal.signal(signal.SIGTERM, signalhandler)
signal.signal(signal.SIGINT, signalhandler)

# ================================================================
# Connect MQTT
# ================================================================
try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_unsubscribe = on_unsubscribe

    client.username_pw_set(mqtt_user, mqtt_pwd)

    client.connect(mqtt_server, mqtt_port, mqtt_timeout)
except socket.error as e:
    logging.warn("Connection error: "+str(e))
    ledstring.close()
    GPIO.cleanup()
    exit()

# ================================================================
# START!!!
# ================================================================
try:
    logging.info("Main-mqtt.py connected and initialized, starting up")
    client.loop_start()

    while(1):
        step()
except Exception as e:
    print(e)
    logging.error(str(e))
    client.loop_stop(force=False)
    clean_exit()
