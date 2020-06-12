# Enumerate

## Scan

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Granny$ scan 10.10.10.15
==================================
Found ports: 80
==================================
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-11 18:11 EDT
Nmap scan report for 10.10.10.15
Host is up (0.069s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
| http-methods: 
|_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND PROPPATCH SEARCH MKCOL LOCK UNLOCK PUT
|_http-server-header: Microsoft-IIS/6.0
|_http-title: Under Construction
| http-webdav-scan: 
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   WebDAV type: Unknown
|   Server Date: Thu, 11 Jun 2020 22:15:55 GMT
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK
|_  Server Type: Microsoft-IIS/6.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.67 seconds
```

* OS scan shows 2003 SP1/2 probably. 

## Explore Services

* plenty of exploits for 6.0
* Web page is nothing. 
* Dirbuster finds _private. Dirbust on that directory finds nothing. 

# Access

| Stat | Name                                                         | Loc                                |
| ---- | ------------------------------------------------------------ | ---------------------------------- |
|      | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (1)  | exploits/windows/remote/8704.txt   |
|      | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (2)  | exploits/windows/remote/8806.pl    |
|      | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (PHP) | exploits/windows/remote/8765.php   |
|      | Microsoft IIS 6.0 - WebDAV Remote Authentication Bypass (Patch) | exploits/windows/remote/8754.patch |
|      | Microsoft IIS 6.0/7.5 (+ PHP) - Multiple Vulnerabilities     | exploits/windows/remote/19033.txt  |

* 8806 can show me directories? Only has _private that dirbuster already found. The put doesn't add the file anywhere?
* 8704 assumes I know the path of a protected file. Dirbust doesn't find anything. Tried some defaults and I just get bad request response. 

```
$> path
HTTP/1.1 207 Multi-Status
Connection: close
Date: Thu, 11 Jun 2020 22:38:35 GMT
Server: Microsoft-IIS/6.0
MicrosoftOfficeWebServer: 5.0_Pub
X-Powered-By: ASP.NET
Content-Type: text/xml
Transfer-Encoding: chunked

2fe
<?xml version="1.0"?><a:multistatus xmlns:b="urn:uuid:c2f41010-65b3-11d1-a29f-00aa00c14882/" xmlns:c="xml:" xmlns:a="DAV:"><a:response><a:href>http://10.10.10.15/_private/</a:href><a:propstat><a:status>HTTP/1.1 200 OK</a:status><a:prop><a:getcontentlength b:dt="int">0</a:getcontentlength><a:creationdate b:dt="dateTime.tz">2017-04-12T14:17:19.421Z</a:creationdate><a:displayname>_private</a:displayname><a:getetag>"fe60b27e97b3d21:358"</a:getetag><a:getlastmodified b:dt="dateTime.rfc1123">Wed, 12 Apr 2017 14:17:19 GMT</a:getlastmodified><a:resourcetype><a:collection/></a:resourcetype><a:supportedlock/><a:ishidden b:dt="boolean">0</a:ishidden><a:iscollection b:dt="boolean">1</a:iscollection><a:getcontenttype/></a:prop></a:propstat></a:response></a:multistatus>
0

```

* Found some other interesting directories by listing files. But starting 8806 with that private dir shows nothing in the directory. I guess the _private is all hidden files normally? Maybe has a default file? Frontpage seems to have the same _vti things referenced, so is there a default file type? 
* Found a cve pl file to exploit a buffer overflow that didn't work, even though: 
* MSF scstorage path exploit works. 
* [ ] Ok, so how without MSF? https://exp1o1t9r.com/2020/01/28/hackthebox-granny-writeup/
  * Not sure how he knew to use asp format? 
* [ ] Apparently the python buffer overflow 41738 works too? Want to test but the box won't reset =/
  * https://github.com/g0rx/iis6-exploit-2017-CVE-2017-7269/blob/master/iis6%20reverse%20shell

# Escalate

* Gives me a shell as nt authority\network service

* Grabbed sysinfo and ran the exploit suggester script and on MSF. The MSF ones didn't work with access denied errors. Might need to get the Lakis access before being able to use them? 

* ms14-070 should work. Having issues. ms14_058_track_popup_menu should have also worked. 

  * Apparently I needed to migrate to a different process.

  ```
  meterpreter > ps
  
  Process List
  ============
  
   PID   PPID  Name               Arch  Session  User                          Path
   ---   ----  ----               ----  -------  ----                          ----          	1724  396   alg.exe                                                         
   1816  584   wmiprvse.exe       x86   0        NT AUTHORITY\NETWORK SERVICE  C:\WINDOWS\system32\wbem\wmiprvse.exe
   1916  396   dllhost.exe                                                     
   2060  3588  rundll32.exe       x86   0                                      C:\WINDOWS\system32\rundll32.exe
   2432  584   wmiprvse.exe                                                    
   2580  348   logon.scr                                                       
   3588  1472  w3wp.exe           x86   0        NT AUTHORITY\NETWORK SERVICE  c:\windows\system32\inetsrv\w3wp.exe
   3676  584   davcdata.exe       x86   0        NT AUTHORITY\NETWORK SERVICE  C:\WINDOWS\system32\inetsrv\davcdata.exe
  
  meterpreter > migrate 2060
  [-] Process already running at PID 2060
  meterpreter > migrate 1472
  [*] Migrating from 2060 to 1472...
  [-] Error running command migrate: Rex::RuntimeError Cannot migrate into this process (insufficient privileges)
  meterpreter > migrate 1816
  [*] Migrating from 2060 to 1816...
  [*] Migration completed successfully.
  meterpreter > 
  
  ```

  

* That gives me access to user and root flags. 

# Lessons

* Added davtest to tool list for webdav scanning. 
* Can't run an exploit that you think should work. Try migrating to a different process first. 

