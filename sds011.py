#!/usr/bin/python

import serial

def parseSensor(sensorData):
    if (sensorData[0] is '\xAA' and sensorData[1] is '\xC0' and sensorData[9] is '\xAB'):
        if compareCheckSum(sensorData[2:8]):
            PM2_5 = (sensorData[2] << 8 + sensorData[3])/10
            PM10 = (sensorData[4] << 8 + sensorData[5])/10
            return (PM2_5, PM10)
    
def compareCheckSum(sensorData):
    checkSum = 0
    for x in range(0, len(sensorData)-1):
        checkSum += sensorData[x]
    
    checkSum &= 255
    return (checkSum == sensorData[-1])

def main():
    sds011 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    while True:
        data = sds011.read(10) # Read 10 bytes from sensor
        PM2_5, PM10 = parseSensor(sensorData):
    
        print('SDS-011 Reading: PM2.5 = %f and PM10 = %f'%(PM2_5, PM10))
 
 main()
