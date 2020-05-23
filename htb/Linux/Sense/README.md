

# Enumerate 

## Scan

```bash
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Sense$ sudo nmap -sC -sV -O 10.10.10.60 -o nmap_scan.txt
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-23 07:07 EDT
Nmap scan report for 10.10.10.60
Host is up (0.027s latency).
Not shown: 998 filtered ports
PORT    STATE SERVICE    VERSION
80/tcp  open  http       lighttpd 1.4.35
|_http-server-header: lighttpd/1.4.35
|_http-title: Did not follow redirect to https://10.10.10.60/
|_https-redirect: ERROR: Script execution failed (use -d to debug)
443/tcp open  ssl/https?
|_ssl-date: TLS randomness does not represent time
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: specialized|general purpose
Running (JUST GUESSING): Comau embedded (92%), FreeBSD 8.X (85%), OpenBSD 4.X (85%)
OS CPE: cpe:/o:freebsd:freebsd:8.1 cpe:/o:openbsd:openbsd:4.3
Aggressive OS guesses: Comau C4G robot control unit (92%), FreeBSD 8.1 (85%), OpenBSD 4.3 (85%), OpenBSD 4.0 (85%)
No exact OS matches for host (test conditions non-ideal).

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 130.96 seconds
```

## Exploits for those:

* [ ] 80 - no

* [ ] 443 (pfsense) - unk version. Deleted the various CSS/CSRF vulns listed

| Status      | Name                                                         | Loc                            |
| ----------- | ------------------------------------------------------------ | ------------------------------ |
| no, privesc | pfSense 2.1 build 20130911-1816 - Directory Traversal        | exploits/php/webapps/31263.t   |
| Tried =/    | pfSense 2.2.5 - Directory Traversal                          | exploits/php/webapps/39038.txt |
| post auth   | pfSense 2.3.1_1 - Command Execution                          | exploits/php/webapps/43128.txt |
| req U/P     | pfSense < 2.1.4 - 'status_rrd_graph_img.php' Command Injection | exploits/php/webapps/43560.py  |
| post auth   | pfSense Community Edition 2.2.6 - Multiple Vulnerabilities   | exploits/php/webapps/39709.txt |

* [ ] OS - unk

## Explore websites

* Nikto
  * [x] Didn't find anything helpful 
* Dirb
  * 80 redirects to 443
  * pfsense webpage - unk version 
    * Didn't seem like much
  * Didn't find much with the medium list - maybe try a more tailored IOT list? 
  * /tree/ has some silverstripe tree control thing - no exploits

```bash
Dir found: / - 200
File found: /index.php - 200
File found: /themes/pfsense_ng/javascript/niftyjsCode.js - 200
File found: /csrf/csrf-magic.js - 200
File found: /javascript/jquery.js - 200
File found: /edit.php - 200
Fil1.xmle found: /exec.php - 200
File found: /graph.php - 200
Dir found: /favicon.ico/ - 200
File found: /help.php - 200
Dir found: /index.html/ - 200
Dir found: /index.php/ - 200
File found: /license.php - 200
Dir found: /installer/ - 302
File found: /pkg.php - 200
File found: /stats.php - 200
File found: /status.php - 200
File found: /system.php - 200
Dir found: /tree/ - 200
File found: /wizard.php - 200
File found: /xmlrpc.php - 200
Dir found: /xmlrpc.php/ - 200
File found: /tree/tree.js - 200
```



# Access

* PFSense not using admin-pfsense/password/admin
* SQLMAP took some time to get to even maybe work but says no. Also tried some SQLi checks and nothing worked. 
* So I can send post requests to xmlrpc.php
  * https://nitesculucian.github.io/2019/07/01/exploiting-the-xmlrpc-php-on-all-wordpress-versions/
  * use burp to send with repeater
  * [ ] try with python later

```
POST /xmlrpc.php HTTP/1.1
Host: 10.10.10.60
Content-Length: 131

<?xml version="1.0" encoding="utf-8"?> 
<methodCall> 
<methodName>system.listMethods</methodName> 
<params></params> 
</methodCall>
```

```
POST /xmlrpc.php HTTP/1.1
Host: 10.10.10.60
Content-Length: 236

<?xml version="1.0" encoding="utf-8"?> 
<methodCall> 
<methodName>pfsense.exec_shell</methodName> 
<params>
<param><value><string>admin</string></value></param>
<param><value><string>ls</string></value></param>
</params> 
</methodCall>
```

Get authentication failed when trying to call exec_shell or exec_php. No luck. 

Well shit, looked at a writeup that showed that there's a file called system-users.txt. Just realized I should all .txt to things I use dirb to search for. I'm always trying something way too hard -.- 

Find changelog.txt and system-users.txt

```
# Security Changelog 

### Issue
There was a failure in updating the firewall. Manual patching is therefore required

### Mitigated
2 of 3 vulnerabilities have been patched.

### Timeline
The remaining patches will be installed during the next maintenance window
```

```
####Support ticket###

Please create the following user


username: Rohit
password: company defaults
```

Login to web page with rohit:pfsense

Use the graph.php exploit to get a shell. 

* Good example of custom: https://github.com/Alamot/code-snippets/blob/master/hacking/HTB/Sense/autopwn_sense.py

# Escalate

The exploit already gives root

# Lessons

Add .txt to directory search tools. 