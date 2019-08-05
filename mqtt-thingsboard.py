#!/usr/bin/python3

import os
import time
import sys
import board
import busio
import adafruit_bme280
import paho.mqtt.client as mqtt
import json
import serial

def parseSensor(sensorData):
    if compareCheckSum(sensorData[2:9]):
        PM2_5 = sensorData[3] * 256 + sensorData[2]
        PM10 = sensorData[5] * 256 + sensorData[4]
        PM10 = float(PM10)/10
        PM2_5 = float(PM2_5)/10
        return (PM2_5, PM10)

def compareCheckSum(sensorData):
    checkSum = 0
    for x in range(0, len(sensorData)-1):
        checkSum = checkSum + sensorData[x]
    checkSum = checkSum & 255
    return (checkSum == sensorData[-1])


THINGSBOARD_HOST = '35.202.142.241'
ACCESS_TOKEN = 'zWXZswSVxPtZPCCgfwch'

INTERVAL = 0.5
sensorData = {'temperature': 0, 'humidity': 0, 'pressure': 0, 'pm2.5': 0, 'pm10': 0}

# Initiate sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
sds011 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Initiate MQTT
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        sensorData['pm2.5'], sensorData['pm10'] = parseSensor(sds011.read(10))
        sensorData['temperature'] = bme280.temperature
        sensorData['humidity'] = bme280.humidity
        sensorData['pressure'] = bme280.pressure

        client.publish('v1/devices/me/telemetry', json.dumps(sensorData), 1)
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
