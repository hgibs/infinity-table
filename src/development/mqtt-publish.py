#!/usr/bin/python

import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("server.arcnet", 1883)
mqttc.publish("hello/world", "Hello, World!")
mqttc.loop(2) #timeout = 2s