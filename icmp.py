# Author: s905060

import os
import sys
import struct
import time
import select
import socket
 
ICMP_ECHO_REQUEST = 8
 
def checksum(str):
  csum = 0
  countTo = (len(str) / 2) * 2
  count = 0
  while count < countTo:
    thisVal = ord(str[count + 1]) * 256 + ord(str[count])
    csum = csum + thisVal
    csum = csum & 0xffffffffL 
    count = count + 2
 
  if countTo < len(str):
    csum = csum + ord(str[len(str) - 1])
    csum = csum & 0xffffffffL 
 
  csum = (csum >> 16) + (csum & 0xffff)
  csum = csum + (csum >> 16)
  answer = ~csum
  answer = answer & 0xffff

  answer = answer >> 8 | (answer << 8 & 0xff00)
  return answer
 
 
def receiveOnePing(mySocket, ID, timeout, destAddr):
  timeLeft = timeout
  while 1:
    startedSelect = time.time()
    whatReady = select.select([mySocket], [], [], timeLeft)
    howLongInSelect = (time.time() - startedSelect)
    if whatReady[0] == []: 
      return "Request timed out."
 
    timeReceived = time.time()
    recPacket, addr = mySocket.recvfrom(1024)
 
    #Fill in start 
    icmp_Header = recPacket[20:28]
    type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmp_Header)
    if packetID == ID:
      bytesInDouble = struct.calcsize("d")
      timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
      return timeReceived - timeSent
    # Fill in end
    
    timeLeft = timeLeft - howLongInSelect
    if timeLeft <= 0:
      return "Request timed out."
 
 
def sendOnePing(mySocket, destAddr, ID):
 
  myChecksum = 0
  header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
  data = struct.pack("d", time.time())
  myChecksum = checksum(header + data)
  if sys.platform == 'darwin':
    myChecksum = socket.htons(myChecksum) & 0xffff
  else:
    myChecksum = socket.htons(myChecksum)
 
  header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
  packet = header + data
  mySocket.sendto(packet, (destAddr, 1))
 
def doOnePing(destAddr, timeout):
  icmp = socket.getprotobyname("icmp")
 
  # Fill in start  
  try:
   #print "1"
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    #print "2"
  except socket.error, (errno, error_msg):
    if errno == 1:
      error_msg = error_msg + (" ICMP messages need to use root account to running.")
      raise socket.error(error_msg)
  # Fill in end
  
    myID = os.getpid() & 0xFFFF  
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
 
    mySocket.close()
    return delay
 
 
def ping(host, timeout=1):
   dest = socket.gethostbyname(host)
   print "Pinging " + dest + " using Python:"
   print ""
   while 1 :
     delay = doOnePing(dest, timeout)
     print delay
     time.sleep(1)
     return delay


if __name__ == '__main__':         
  ping("www.google.com")
  ping("www.yahoo.com") 
  ping("www.google.com.tw")
  ping("www.yahoo.com.tw")   

