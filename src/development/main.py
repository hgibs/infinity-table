#!/usr/bin/python
import RPi.GPIO as GPIO
import os, time, webiopi, threading
from Gibson_LED_Driver import Gibson_LED_Driver

try:

    ########### SET UP ###########
    # Enable debug output
    webiopi.setDebug()

    # init GPIO pins
    GPIO.setmode(GPIO.BCM)

    # init LED driver on /dev/spidev0.0 with 50 LEDs
    ledstring = Gibson_LED_Driver(0,0,50)

    ### Set up the shut-off switch
    # shutdown code
    def auto_shutdown(self):
        GPIO.cleanup()
        os.system("sudo shutdown -h now")
        ledstring.setAll([1,1,1])
        ledstring.update()
        time.sleep(0.01)
        while(True):
            ledstring.flyingcolor([255,0,0], 70)

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
    scheme = "static"
    thiscolor = [255,1,255]
    newScheme = True


    ########### MACRO DEFINITIONS ###########
    @webiopi.macro
    def getColorString():
        global thiscolor
        return str(thiscolor[0]) + "/" + str(thiscolor[1]) + "/" + str(thiscolor[2])

    @webiopi.macro
    def setPulse():
        global scheme
        scheme = "pulse"
        print "scheme set to pulse"

    @webiopi.macro
    def flyingColor(red=255,green=255,blue=255):
        global scheme, thiscolor
        scheme = "flyingcolor"
        thiscolor = [int(red),int(green),int(blue)]
        print "scheme set to flyingcolor"
        #return to update UI in web
        return getColorString()

    @webiopi.macro
    def colorwheel():
        global scheme, newScheme
        newScheme = True
        scheme = "colorwheel"

    @webiopi.macro
    def randomstatic():
        global scheme, newScheme
        newScheme = True
        scheme = "randomstatic"

    @webiopi.macro
    def rgb():
        global scheme, newScheme
        newScheme = True
        scheme = "rgb"

    @webiopi.macro
    def spin():
        global scheme
        scheme = "spin"

    @webiopi.macro
    def ranger():
        global scheme
        scheme = "ranger"


    @webiopi.macro
    def static(red=255,green=255,blue=255):
        global thiscolor, newScheme, scheme
        scheme = "static"
        thiscolor = [int(red),int(green),int(blue)]
        newScheme = True
        print "scheme set to static"
        return getColorString()

    def loop():
        global scheme, thiscolor, newScheme
        if scheme == "pulse":
            ledstring.fadeupdown(25)
        elif scheme == "flyingcolor":
            ledstring.flyingcolor(thiscolor,50)
        elif scheme == "static":
            if newScheme:
                print str(thiscolor)
                ledstring.static(thiscolor)
                newScheme = False
        elif scheme == "randomstatic":
            if newScheme:
                ledstring.randomstatic()
                newScheme = False
        elif scheme == "rgb":
            if newScheme:
                ledstring.rgb()
                newScheme = False
        elif scheme == "colorwheel":
            if newScheme:
                ledstring.colorwheel()
                newScheme = False
        elif scheme == "spin":
            ledstring.spiniteration(25)
        elif scheme == "ranger":
            ledstring.alternate(thiscolor, [1,1,1])


    ########### SERVER ###########
    # Instantiate the server on the port 80 (default http), it starts immediately in its own thread
    server = webiopi.Server(port=80)

    # Register the macros so you can call it with Javascript and/or REST API
    server.addMacro(getColorString)
    server.addMacro(setPulse)
    server.addMacro(flyingColor)
    server.addMacro(colorwheel)
    server.addMacro(randomstatic)
    server.addMacro(static)
    server.addMacro(rgb)
    server.addMacro(spin)
    server.addMacro(ranger)

    # notify the console
    # os.system("echo 'The LED driver has been initiated and is running' | wall &")

    # flash the string
    #ledstring.colorwheel()
    #time.sleep(0.5)




    ########### LOOP EXECUTION ###########
    # Run our loop until CTRL-C is pressed or SIGTERM received
    webiopi.runLoop(loop)

    # If no specific loop is needed and defined above, just use
    # webiopi.runLoop()
    # here instead

except KeyboardInterrupt:

    ########### SHUTDOWN ###########
    # Cleanly stop the server
    #server.stop()
    GPIO.cleanup()
    exit()