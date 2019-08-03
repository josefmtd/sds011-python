import os
import time
import sys
import board
import busio
import adafruit_bme280
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = '35.202.142.241'
ACCESS_TOKEN = 'zWXZswSVxPtZPCCgfwch'

INTERVAL = 2
sensorData = {'temperature': 0, 'humidity': 0, 'pressure': 0}

# Initiate sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Initiate MQTT
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()


try:
    while True:
        sensorData['temperature'] = bme280.temperature
        sensorData['humidity'] = bme280.humidity
        sensorData['pressure'] = bme280.pressure

        client.publish('v1/devices/me/telemetry', json.dumps(sensorData), 1)
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
