#!/usr/bin/python

import serial

def parseSensor(sensorData):
    print("Received a continuous SDS011 packet")
    if compareCheckSum(sensorData[2:9]):
        PM2_5 = ((ord(sensorData[2]) << 8 + ord(sensorData[3])))/10
        PM10 = ((ord(sensorData[4]) << 8 + ord(sensorData[5])))/10
        return (PM2_5, PM10)
    
def compareCheckSum(sensorData):
    checkSum = 0
    for x in range(0, len(sensorData)-1):
        checkSum = checkSum + ord(sensorData[x])
    print(len(sensorData))
    checkSum = checkSum & 255
    print(checkSum)
    print(ord(sensorData[-1]))
    return (checkSum == ord(sensorData[-1]))

def main():
    sds011 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

    while True:
        sensorData = sds011.read(10) # Read 10 bytes from sensor
        print(len(sensorData))
        PM2_5, PM10 = parseSensor(sensorData)
    
        print('SDS-011 Reading: PM2.5 = %f and PM10 = %f'%(PM2_5, PM10))

main()
