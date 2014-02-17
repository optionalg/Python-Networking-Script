# Author: s905060

#We will need the following module to generate random lost packets import random

from socket import *
from time import *

#create a UDP socket

serverIP= 'localhost'

serverPort= 12001

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(1.0)

count = 0

while (count<10) :

 sendtime = time()
 
 message = "seqNum:" + str(count)+" Sendtime: " + str(sendtime)

 clientSocket.sendto(message,(serverIP, serverPort))

 try:

  modifiedMessage, address = clientSocket.recvfrom(1024)

  print str(count), "RTT:",str((time()-sendtime))
  

 except timeout:

  print str(count),"The packet is lost"   

 count = count + 1
  
clientSocket.close()
 
