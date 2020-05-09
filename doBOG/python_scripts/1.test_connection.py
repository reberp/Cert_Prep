#!/usr/bin/env python3
from pwn import *
r = remote('192.168.0.9',31337)

r.send("HI"+"\n")
resp = r.recv()
print(str(resp))
