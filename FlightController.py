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

global obstB
obstB=False
pitch=0
roll=0
thrust=0
serl=serial.Serial('/dev/ttyUSB0', 9600)

def SensorThread():
    global forw, left, right, alt
    while True:
        try:
            forw, left, right, alt = (serl.readline()).split(",")
##            print(forw+" "+left+" "+right+" "+alt)
            forw=int(forw)
            right=int(right)
            left=int(left)
        except:
            pass


def flightServerThread():
    global roll, pitch, sock, obstF, obstB, obstR, obstL
    global forw, left, right, alt
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6666))
    while True:
        data = sock.recv(1024)
        roll, pitch = data.split(",")
        pitch = round(float(pitch), 2) + 90
        roll = round(float(roll), 2) + 90
        print(pitch, roll)
        pD = float(pitch)/12
        rD = float(roll)/12
        
        if forw<50 and forw!=0 and pitch>90:  # Use accelerometer
            fr.ChangeDutyCycle(4.2)
##        elif back<50 and back!=0 and pitch<90 and False:
##            fr.ChangeDutyCycle(10.67)
        else:
            if pD>2 and pD<100:
                fr.ChangeDutyCycle(pD)
        
        if right<50 and right!=0 and roll>90:
            sr.ChangeDutyCycle(3.33)
        elif left<50 and left!=0 and roll<90:
            sr.ChangeDutyCycle(10.67)
        else:
            if rD>2 and rD<100:
                sr.ChangeDutyCycle(rD)

def handler(sigtype, frame):
    global sock
    sock.close()
    fr.stop()
    sr.stop()
    GPIO.cleanup()
    os._exit(0)

signal.signal(signal.SIGINT, handler)

def main():
    global forw, left, right, alt
    sThread=threading.Thread(target=SensorThread)
    sThread.start()
    fThread=threading.Thread(target=flightServerThread)
    fThread.start()
    
    while True:
        time.sleep(1)
##        os.system('clear')
##        print(pitch)
##        print(roll)
##        pD = float(pitch)/12
##        if pD>24/12 and pD<100:
##            fr.ChangeDutyCycle(pD)
##        rD = float(roll)/12
##        if rD>24/12 and rD<100:
##            sr.ChangeDutyCycle(rD)
##        x = round(pitch/12, 2)
##        if x>0 and x<100:
##            fr.ChangeDutyCycle(x)
##        print(x)
##        print(x)
##        print('')
##        time.sleep(3)


if __name__=='__main__':
    main()
