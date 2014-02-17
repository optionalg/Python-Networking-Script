# Author: s905060

import socket
import time

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.settimeout(1)
  
data = "CS6843 Programming Lab - UDP"
for i in range(10):
  starttime = time.time()
  endtime = 0
  serverSocket.connect(('localhost', 12000))
  serverSocket.sendall(data + str(i))
  while True:
    try:
      message, address = serverSocket.recvfrom(1024)
      endtime = time.time()
      print "Packet " + str(i) + " RTT: " + str(endtime-starttime)
      break
    except socket.timeout:
      print "Packet " + str(i) + " lost packet"
      break
serverSocket.close()
