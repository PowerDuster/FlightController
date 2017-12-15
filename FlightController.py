import threading
import socket
import signal
import os
import time
import serial
import RPi.GPIO as GPIO
from random import *

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.OUT)
##GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
##GPIO.setup(11, GPIO.OUT)
fr = GPIO.PWM(3, 50)
##fl = GPIO.PWM(5, 50)
sr = GPIO.PWM(7, 50)
##sl = GPIO.PWM(11, 50)
fr.start(7.5)
##fl.start(7.5)
sr.start(7.5)
##sl.start(7.5)

pitch=0
roll=0
thrust=0
##serl=serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)

def flightServerThread():
    global roll, pitch, sock
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6666))
    while True:
        data = sock.recv(1024)
        roll, pitch = data.split(",")
        pitch = round(float(pitch), 2) + 90
        roll = round(float(roll), 2) + 90

##def SensorDataThread():
##    global alt, forw, back, right
##    while True:
##        sensorData = serl.readline()
##        print(sensorData)
##        alt, forw, back, right = (serl.readline()).split(",")
##        print(alt)
##        print(forw)
##        print(back)
##        print(right)


def handler(sigtype, frame):
    global sock
    sock.close()
    fr.stop()
    sr.stop()
    GPIO.cleanup()
    os._exit(0)

signal.signal(signal.SIGINT, handler)

def main():
    fThread=threading.Thread(target=flightServerThread)
    fThread.start()
##    sThread=threading.Thread(target=SensorDataThread)
##    sThread.start()
    
    while True:
##        os.system('clear')
##        print(pitch)
##        print(roll)
        pD = float(pitch)/12
        if pD>24/12 and pD<100:
            fr.ChangeDutyCycle(pD)
        rD = float(roll)/12
        if rD>24/12 and rD<100:
            sr.ChangeDutyCycle(rD)
##        x = round(pitch/12, 2)
##        if x>0 and x<100:
##            fr.ChangeDutyCycle(x)
##        print(x)
##        print(x)
##        print('')
##        time.sleep(3)


if __name__=='__main__':
    main()
