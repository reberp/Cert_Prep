# Enumerate

```
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-14 11:56 EDT
Nmap scan report for 10.10.10.14
Host is up (0.026s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
| http-methods: 
|_  Potentially risky methods: TRACE COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT MOVE MKCOL PROPPATCH
|_http-server-header: Microsoft-IIS/6.0
|_http-title: Under Construction
| http-webdav-scan: 
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, COPY, PROPFIND, SEARCH, LOCK, UNLOCK
|   Server Date: Sun, 14 Jun 2020 16:00:23 GMT
|   WebDAV type: Unknown
|_  Server Type: Microsoft-IIS/6.0
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2003|2008|XP|2000 (92%)
OS CPE: cpe:/o:microsoft:windows_server_2003::sp1 cpe:/o:microsoft:windows_server_2003::sp2 cpe:/o:microsoft:windows_server_2008::sp2 cpe:/o:microsoft:windows_xp::sp3 cpe:/o:microsoft:windows_2000::sp4
Aggressive OS guesses: Microsoft Windows Server 2003 SP1 or SP2 (92%), Microsoft Windows Server 2008 Enterprise SP2 (92%), Microsoft Windows Server 2003 SP2 (91%), Microsoft Windows 2003 SP2 (91%), Microsoft Windows XP SP3 (90%), Microsoft Windows XP (87%), Microsoft Windows 2000 SP4 (87%), Microsoft Windows Server 2003 SP1 - SP2 (86%), Microsoft Windows XP SP2 or Windows Server 2003 (86%), Microsoft Windows XP SP2 or Windows Server 2003 SP2 (85%)
No exact OS matches for host (test conditions non-ideal).
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.82 seconds
```

* No wordlists for webdav and dirb. Start normal dirbuster. It just starts returning 500 for everything. 
* extra nmap scans for webdav. Say it's vulnerable but find nothing. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Grandpa$ locate nse | grep webdav
/usr/share/nmap/scripts/http-iis-webdav-vuln.nse
/usr/share/nmap/scripts/http-webdav-scan.nse
```

* Find some exploits

|      |                                                              |                                    |
| ---- | ------------------------------------------------------------ | ---------------------------------- |
| Good | Microsoft IIS 6.0 - WebDAV 'ScStoragePathFromUrl' Remote Buffer Overflow | exploits/windows/remote/41738.py   |
| X    | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (1)  | exploits/windows/remote/8704.txt   |
| X    | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (2)  | exploits/windows/remote/8806.pl    |
| X    | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (PHP) | exploits/windows/remote/8765.php   |
| X    | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (Patch) | exploits/windows/remote/8754.patch |
| X    | Microsoft IIS 6.0/7.5 (+ PHP) - Multiple Vulnerabilities     | exploits/windows/remote/19033.txt  |

* From this guys github it looks like the shellcode in the 41738.py is alpha_mixed

```
https://github.com/danigargu/explodingcan
```

* Exploding can worked but the command shell would just crash. 
  * [ ] Maybe just try generic command to make a shell? Tried with jsp and command, didn't work. 
* Meterpreter shell worked to get a stable callback. Gives me network service and no user.txt 

# Escalate

* Used the windows exploit suggester and the metasploit one
* ms14-058 works to escalate