import threading
import socket
import serial

pitch=0
yaw=0
roll=0
isConnected=False
fly=False
global addr

def controlServerThread():
    print('Control server running')
    controlSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    controlSock.bind(('', 3000))
    global pitch, yaw, roll, isConnected, addr
    while True:
        msg, addr = controlSock.recvfrom(16)
        print('Control signal received')
        isConnected=True
    
    print('Control server exit')


def flightServerThread():
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 3434))
    while True:
        data = sock.recv(24)


ser=serial.Serial('', 9600, timeout=0.01)

cThread=threading.Thread(target=controlServerThread)
cThread.start()

while True:
    sensorData=ser.readline
    #parse sensorData
    if isConnected:
        print(addr)
    
