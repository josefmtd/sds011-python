#!/usr/bin/python3

import serial

def parseSensor(sensorData):
    if compareCheckSum(sensorData[2:9]):
        PM2_5 = sensorData[3] * 256 + sensorData[2]
        PM10 = sensorData[5] * 256 + sensorData[4]
        PM2_5 = float(PM2_5)/10
        PM10 = float(PM10)/10
        return (PM2_5, PM10)

def compareCheckSum(sensorData):
    checkSum = 0
    for x in range(0, len(sensorData)-1):
        checkSum = checkSum + sensorData[x]
    checkSum = checkSum & 255
    return (checkSum == sensorData[-1])

def main():
    sds011 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    while True:
        sensorData = sds011.read(10) # Read 10 bytes from sensor
        print(len(sensorData))
        PM2_5, PM10 = parseSensor(sensorData)
        print('SDS-011 Reading: PM2.5 = %.2f and PM10 = %.2f'%(PM2_5, PM10))

main()
