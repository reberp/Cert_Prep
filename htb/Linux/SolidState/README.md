### Solidstate - 10.10.10.51

# Enumerate

## Scan

```
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.4p1 Debian 10+deb9u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 77:00:84:f5:78:b9:c7:d3:54:cf:71:2e:0d:52:6d:8b (RSA)
|   256 78:b8:3a:f6:60:19:06:91:f5:53:92:1d:3f:48:ed:53 (ECDSA)
|_  256 e4:45:e9:ed:07:4d:73:69:43:5a:12:70:9d:c4:af:76 (ED25519)
25/tcp  open  smtp    JAMES smtpd 2.3.2
|_smtp-commands: solidstate Hello nmap.scanme.org (10.10.14.11 [10.10.14.11]), 
80/tcp  open  http    Apache httpd 2.4.25 ((Debian))
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Home - Solid State Security
110/tcp open  pop3    JAMES pop3d 2.3.2
119/tcp open  nntp    JAMES nntpd (posting ok)
```

* [x] all ports necessary?  

New scan for all ports finds 4555, the thing that the 35513 looks for.

## Exploits?

* [ ] 22 - probably not

* [ ] 25 - probably not

* [ ] 80 - maybe

  | Stat  | Name                                                         | File                            |
  | ----- | ------------------------------------------------------------ | ------------------------------- |
  | later | Apache 2.4.17 < 2.4.38 - 'apache2ctl graceful' 'logrotate' Local Privilege Escalation | exploits/linux/local/46676.php  |
  | Fail? | Apache < 2.2.34 / < 2.4.27 - OPTIONS Memory Leak             | exploits/linux/webapps/42745.py |

* [ ] 110 - no? Not sure what the JAMES stuff is

* [ ] 119 - no

Searching for just JAMES finds a few things? 

| Stat | Name                                                 | File                           |
| ---- | ---------------------------------------------------- | ------------------------------ |
|      | Apache James Server 2.3.2 - Remote Command Execution | exploits/linux/remote/35513.py |

## Dirb

* readme.txt file - Mentions combining from Pixelarity
* services.html

## Nikto

Done. Nothing interesting. 

# Access

See that I can connect on 4555 with root/root from the python script

Connect and list users

```
user: james
user: ../../../../../../../../etc/bash_completion.d
user: thomas
user: john
user: mindy
user: mailadmin
```

I tried to set the password for everyone but I can't ssh. Can I log in to nntp? No 

I can log into the 110 pop3d. No shell, maybe fix the script for that user? 

Ok, logged in as mindy and found an email, even though never got reverse shell:

```
Trying 10.10.10.51...
Connected to 10.10.10.51.
Escape character is '^]'.
+OK solidstate POP3 server (JAMES POP3 Server 2.3.2) ready 
USER mindy
+OK
PASS root
+OK Welcome mindy
STAT
+OK 2 1945
RETR 2
+OK Message follows
Return-Path: <mailadmin@localhost>
Message-ID: <16744123.2.1503422270399.JavaMail.root@solidstate>
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Delivered-To: mindy@localhost
Received: from 192.168.11.142 ([192.168.11.142])
          by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 581
          for <mindy@localhost>;
          Tue, 22 Aug 2017 13:17:28 -0400 (EDT)
Date: Tue, 22 Aug 2017 13:17:28 -0400 (EDT)
From: mailadmin@localhost
Subject: Your Access
Dear Mindy,
Here are your ssh credentials to access the system. Remember to reset your password after your first login. 
Your access is restricted at the moment, feel free to ask your supervisor to add any commands you need to your path. 
username: mindy
pass: $EXPORTED_PASSWORD
Respectfully,
James
```

well uh... logging in as mindy gives me a bunch of garbage, but the command ran and I got my shell...

# Escalate

no sudo -l, nothing interesting in crontab

downloaded and ran linpeas

* something listening on 631? What's IPP? Doesn't matter I guess

Read a writeup to see a reference to /opt

Overwrite the script to give a new shell (I guess it's cron'd even though nothing was listed)



# Lessons

* From https://reboare.github.io/hackthebox/solidstate.html: always check the `/opt` and `/usr/local` directories for any interesting custom packages or scripts
* From same: https://speakerdeck.com/knaps/escape-from-shellcatraz-breaking-out-of-restricted-unix-shells

# Tags

telnet

restricted shell



