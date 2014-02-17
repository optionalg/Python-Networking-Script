# Author: s905060

from socket import *
import random


serverSocket = socket(AF_INET, SOCK_DGRAM) #assign IP address and port number to socket

serverSocket.bind(( 'localhost', 12001))

 

while True:
    rand = random.randint(0, 10)
    print rand
    message, address = serverSocket.recvfrom(1024)
    message = message.upper()
    if rand < 4:
        continue
    serverSocket.sendto(message, address)
