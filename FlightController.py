import threading
import socket

pitch=0, yaw=0, roll=0


def controlServerThread():
	controlSock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', 3000))
	global pitch, yaw, roll
	while True:
		msg, addr = controlSock.recvfrom()
		

def flightServerThread():
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('', 3434))
	while True:
		data = sock.recv(24)


cThread=threading.Thread(target=controlServerThread)
cThread.start()
fThread=threading.Thread(target=flightServerThread)
fThread.start()

while True:
	#get sensor data