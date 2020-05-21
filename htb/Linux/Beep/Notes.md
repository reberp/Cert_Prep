# Scan/Enumerate
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
| ssh-hostkey: 
|   1024 ad:ee:5a:bb:69:37:fb:27:af:b8:30:72:a0:f9:6f:53 (DSA)
|_  2048 bc:c6:73:59:13:a1:8a:4b:55:07:50:f6:65:1d:6d:0d (RSA)
25/tcp    open  smtp       Postfix smtpd
|_smtp-commands: beep.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, 
80/tcp    open  http       Apache httpd 2.2.3
|_http-server-header: Apache/2.2.3 (CentOS)
|_http-title: Did not follow redirect to https://10.10.10.7/
|_https-redirect: ERROR: Script execution failed (use -d to debug)
110/tcp   open  pop3       Cyrus pop3d 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_pop3-capabilities: RESP-CODES UIDL LOGIN-DELAY(0) APOP TOP IMPLEMENTATION(Cyrus POP3 server v2) USER AUTH-RESP-CODE STLS EXPIRE(NEVER) PIPELINING
111/tcp   open  rpcbind    2 (RPC #100000)
143/tcp   open  imap       Cyrus imapd 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
|_imap-capabilities: NAMESPACE IMAP4rev1 LISTEXT X-NETSCAPE ACL OK IDLE STARTTLS SORT LIST-SUBSCRIBED Completed URLAUTHA0001 ATOMIC CONDSTORE ANNOTATEMORE NO RENAME QUOTA LITERAL+ ID UNSELECT THREAD=ORDEREDSUBJECT MULTIAPPEND SORT=MODSEQ BINARY THREAD=REFERENCES CHILDREN MAILBOX-REFERRALS UIDPLUS IMAP4 RIGHTS=kxte CATENATE                                                                                              
443/tcp   open  ssl/https?                                                                                                                                                                                       
|_ssl-date: 2020-05-21T11:25:32+00:00; +3m28s from scanner time.                                                                                                                                                 
993/tcp   open  ssl/imap   Cyrus imapd                                                                                                                                                                           
|_imap-capabilities: CAPABILITY                                                                                                                                                                                  
995/tcp   open  pop3       Cyrus pop3d                                                                                                                                                                           
3306/tcp  open  mysql      MySQL (unauthorized)                                                                                                                                                                  
4445/tcp  open  upnotifyp?                                                                                                                                                                                       
10000/tcp open  http       MiniServ 1.570 (Webmin httpd)                                                                                                                                                         
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).                                                                                                                                         
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).                                                                                                              
TCP/IP fingerprint:

* Search for known vulns
openssh - no
postfix - unk, maybe shellshock if 4.2.X-4.2.48, didn't work
apache - no
pop3d - no
rpc - unk
imapd - no
https - elastic - maybe
	[_/] Elastix 2.2.0 - 'graph.php' Local File Inclusion | exploits/php/webapps/37637.pl
		not successful	
		just kidding, it is, but I'm dumb and should have just copied the thing from the perl script and see that it works. 
	[X] Elastix 2.x - Blind SQL Injection                | exploits/php/webapps/36305.txt
		seems to just freeze the server?
	[X] Elastix < 2.5 - PHP Code Injection               | exploits/php/webapps/38091.php
mysql - unk but can't seem to connect to it. 
upnotifyp - unk
miniserv - maybe:
	[X] Webmin 1.5 - Brute Force / Command Execution   | exploits/multiple/remote/746.pl
		seems to expect http
	[X] Webmin 1.5 - Web Brute Force (CGI)             | exploits/multiple/remote/745.pl
		not helpful probably
* page contents
80 directs to elastix login page on 443
10000 has webmin login



# Access
* Default logins for pages?
	webmin - no
	elastix - no, tried these: https://www.elastix.org/community/threads/default-passwords-not-password.8416/
* Test exploits above
what is elastix version? Response doesn't have it? 
rpcinfo shows portmapper and status ports? Worth anything?
upnotifyp shows nothing online 
Found /mail/ directory and /admin/
	no default logins for either
	roundcube might have some exploits, but not sure what version, only RCE requires file create on host. 
sqlmap on webmin doesn't give anything. 
        on elastix doesn't give anything.
dirbuster
	found /mail/ with roundcube. No default login and no results in searchsploit
	found /pipermail/ empty dir 
	/admin/ with another login prompt, no default login 
	eventually would have found vtigercrm when I let it run and with a bigger/different list? 
Read that file and see what it has the admin password to log into the /admin/ in ARI_ADMIN_PASSWORD and others
Same login gets into the index also 
now what, upload a file? Maybe I can upload a module? 
	tried to make a custom module with a php command in the installer. Said that it executed but I never got a callback. Not sure why. 
Can log into the vtiger page on extras tab of / 
vtiger exploit
	[_/] vTiger CRM 5.1.0 - Local File Inclusion | exploits/php/webapps/18770.txt
		The listed link doesn't work, nvm, tried it later and it worked again -_- 
 
	
# Escalate
No need

# Alternatives:
could have found the /vtigercrm and used that to get a local file with config for the password with different LFI exploit 

# Lessons:
Didn't check the password on SSH until reading writeup. Need to know what passwords I've tried on what and then make sure I try reasonable things when I find new passwords and write it down.  
