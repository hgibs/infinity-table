# infinity-table
My code for driving RGB leds in an infinity table using python and MQTT (mosquitto) as the interface, or a simple stand-alone program.

## Requirements:
- SPI enabled (use <code>raspi-config</code>)
- up-to-date OS

## Set up
### (not functional yet)
- Installing the System V init script and executable:
<code>
sudo add-apt-repository ppa:holland-gibson/inftable && apt install inftable-lights
</code>

- Installing just the Gibson_LED_Driver package for importing in other scripts:
<code> pip install Gibson_LED_Driver </code> 

- Manually install the System V (init.d) init script:
    + Edit <code>src/init.d_shell_main-mqtt</code> to match this git repository local on your machine
    + Copy that file to <code>/etc/init.d/inftable-lights</code>
    

- Lastly, you can clone this repository and just copy the src folder to wherever you want to use it


However, all you need to do is edit the <code>inftable-lights.conf</code> and move to <code> /etc/inftable-lights/infable-lights.conf </code> or <code> src/inftable-lights.conf </code> if running locally.

## Running
For using MQTT as an interface:

<code> sudo python main-mqtt.py </code>

or for running in the background (default runs at boot):

<code> sudo service inftable-mqtt status </code>

## How it works
Uhhh... I'll type this up later

## Config file:
1) Configure your GPIO pins and SPI
2) install your mosquitto server
3) configure the settings.conf file
4) run
