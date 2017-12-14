import threading
import socket
import signal
import os
import time

pitch=0
yaw=0
roll=0
thrust=0
isConnected=False
Run=True
fly=False
global addr

def handler(sigtype, frame):
    Run=False
    os._exit(0)

def controlServerThread():
    print('Control server running')
    controlSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    controlSock.bind(('', 7777))
    global pitch, yaw, roll, addr, isConnected
    isConnected=True


def flightServerThread():
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6666))
    global yaw, pitch
    while True:
        #print('recv')
        data = sock.recv(1024).decode("utf-8") 
        #print('recv\'d')
        #print(data)
        yaw, pitch = data.split(",")
        #print(yaw)
        #print(pitch)

#ser=serial.Serial('', 9600, timeout=0.01)

#def getSensorData():
#    #maybe use a fifo queue
#    l, r, f, b, d = ser.read(14).split("")# Or readline
#    sendData()
    

def main():
    global isConnected
    global yaw, pitch, roll
    signal.signal(signal.SIGINT, handler)
    cThread=threading.Thread(target=controlServerThread)
    cThread.start()
    fThread=threading.Thread(target=flightServerThread)
    fThread.start()
    
    while Run:
        #print(yaw)
        #print(pitch)
        os.system('cls')
        print(float(yaw)*10,'\n',float(pitch)*10,'\r'),
        time.sleep(0.01)
        #while isConnected:
            #if f>40 and b>40:
                #setLeftServo(pitch+roll)
                #setRightServo(pitch-roll)
                ##increase rpm to compensate
            #elif f<40:
                #setLeftServo(-35)
                #setRightServo(-35)
                ##increase rpm to compensate
            #elif b<40:
                #setLeftServo(35)
                #setRightServo(35)
                ##increase rpm to compensate
            #if l>40 and r>40:
                #setSidewayLeftServo(yaw)
                #setSidewayRightServo(yaw)
                ##increase rpm to compensate
            #elif l<40:
                #setSidewayLeftServo(35)
                #setSidewayRightServo(35)
                ##increase rpm to compensate
            #elif r<40:
                #setSidewayLeftServo(-35)
                #setSidewayRightServo(-35)
                ##increase rpm to compensate
            #if d>40:
                #setLeftSpeed(thrust)
                #setRightSpeed(thrust)
                ##increase rpm to compensate


if __name__=='__main__':
    main()
