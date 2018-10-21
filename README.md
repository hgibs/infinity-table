### infinity-table
My code for driving RGB leds in an infinity table using python and MQTT (mosquitto) as the interface, or a simple stand-alone program.

# Requirements:
- SPI enabled (use <code>raspi-config</code>)
- up-to-date OS

# Set up
Installing the System V init script and executable:
<code> apt install Gibson_LED_Driver </code>

Installing just the Gibson_LED_Driver package for importing in other scripts:
<code> pip install Gibson_LED_Driver </code> 

Lastly, you can clone this repository and just copy the src folder to wherever you want to use it


However, all you need to do is edit the <code>config.ini</code> and move to <code> src/config.local </code>

# Running
For using MQTT as an interface:

<code> sudo python main-mqtt.py </code>

or for running in the background (default runs at boot):

<code> sudo service inftable-mqtt status </code>

# How it works
Uhhh... I'll type this up later

# Installation
1) Configure your GPIO pins and SPI
2) install your mosquitto server
3) configure the settings.conf file
4) run
