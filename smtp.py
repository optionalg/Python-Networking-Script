# Author: s905060

import socket, time

msg="\r\n I love computer networks!"
endmsg="\r\n.\r\n"
mailserver =  'gmail-smtp-in.l.google.com'
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver,25))
Recv=clientSocket.recv(1024)
print Recv

if Recv[:3]!='220':
  print '220 reply not received from server.'

heloCommand='HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1=clientSocket.recv(1024)
print recv1
if recv1[:3]!='250':
  print '250 reply not received from server.'  

clientSocket.send("MAIL FROM:<" +'s905060@gmail.com'+ ">\r\n")
respondline = clientSocket.recv(1024)
print respondline
clientSocket.send("RCPT TO:<" +'s905060@gmail.com'+ ">\r\n")
respondline = clientSocket.recv(1024)
print respondline
clientSocket.send("DATA\r\n")
respondline = clientSocket.recv(1024)
print respondline
clientSocket.send("Subject:" +'Programming Project SMTP'+ "\r\n" +msg + "\r\n.\r\n")
respondline = clientSocket.recv(1024)
print respondline
clientSocket.send("\r\n")
respondline = clientSocket.recv(1024)
print respondline
clientSocket.send("QUIT\r\n")
respondline = clientSocket.recv(1024)
print respondline
clientSocket.close() 
