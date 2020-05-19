# Scan Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-19 03:45 EDT
Nmap scan report for 10.10.10.56
Host is up (0.029s latency).
Not shown: 998 closed ports
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.18 seconds

# Access
* port exploits
OpenSSHd 7.2p2 - Username Enumeration | exploits/linux/remote/40113.txt
Local privesc maybe for http

* web directories
dirbuster found nothing

* ssh brute
made small username list
Probably not going to be useful. Running in background.

* scan all ports
Nothing new

* bug.jpg
Nothing on exif

* nikto
Nothing, but I should still be using it and didn't think of it
I guess this doesn't find it either because it doesn't see the user script? 

* apache header
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Shocker$ curl -I 10.10.10.56
HTTP/1.1 200 OK
Date: Tue, 19 May 2020 08:42:57 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Fri, 22 Sep 2017 20:01:19 GMT
ETag: "89-559ccac257884"
Accept-Ranges: bytes
Content-Length: 137
Vary: Accept-Encoding
Content-Type: text/html
could use the 2.4.18 to see what ubuntu version it is based on what that package goes to on package.ubuntu.com

* shellshock
apparently the nmap scan is broken, at least against this server
adds some nonsense in that the webserver doesn't like. 

* dirbuster again, but this time with new extensions
File found: /cgi-bin/user.sh - 200
This is a hint that I should be using shellshock I guess. 

* exploit shellshock
searchsploit and see python script for shellshock


# Escalate
sudo -l
see perl
exploit 

# Lessons
add nikto to original steps
cgi-bin can have scripts like sh and pl, add to scanner extensions if I want to find those
Know what extensions to expect in certain dirs and scan for those specifically. 
nmap scripts aren't great sometimes, configuration can break things? 
