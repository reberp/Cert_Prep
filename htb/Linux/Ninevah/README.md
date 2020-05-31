# Enumeration

# Scan

* scanning all ports, found 80/443. Scan those ports 

```
80/tcp  open  http     Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=nineveh.htb/organizationName=HackTheBox Ltd/stateOrProvinceName=Athens/countryName=GR
| Not valid before: 2017-07-01T15:03:30
|_Not valid after:  2018-07-01T15:03:30
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
```

# Services

## Known Exploits

* for apache - no

## Enumerate

* 80 just has a default text with nothing, 443 just has default picture with nothing

### Nikto

* 80

  ```
  + /info.php: Output from the phpinfo() function was found.
  + OSVDB-3233: /info.php: PHP is installed, and a test script which runs phpinfo() was found. This gives a lot of system information.
  + OSVDB-3233: /icons/README: Apache default file found.
  + OSVDB-5292: /info.php?file=http://cirt.net/rfiinc.txt?: RFI from RSnake's list (http://ha.ckers.org/weird/rfi-locations.dat) or from http://osvdb.org/
  ```

  * Info page shows zend engine v3.0.0 running - found nothing. 

  * OSVBD-5292: Tried to include a php script I had locally, nothing happened. 

* 443 - nothing interesting. 

### Dirbuster

* 80

  * /info.php
  * /department/
    * login page. Gives username enumeration. Sqlmap returns nothing. 
    * brute forcing username and admin:pw with hydra. 
    * dirbuster only finds files that redirects to login

* 443

  * /db/ - phpliteadmin v1.9, default pw on 'admin' doesn't work. 
  * [x] brute force if stuck
  
  ```
  [ ] PHPLiteAdmin 1.9.3 - Remote PHP Code Injection  exploits/php/webapps/24044.txt
  [X] phpLiteAdmin - 'table' SQL Injection            exploits/php/webapps/38228.txt
  [X] phpLiteAdmin 1.9.6 - Multiple Vulnerabilities   exploits/php/webapps/39714.txt
  ```
  
  * /secure_notes/ - just a picture, running dibuster on it. found nothing. 

# Access

* 24044 is post-auth
* used 38228 - sqlmap says not vulnerable from sqlmap -u "https://10.10.10.43/db/index.php?action=row_view&table=users" searchsploit says for all 1.8 and 1.9, but on their page it just says 1.9.3, so maybe I need the 1.9.6.
* exploits/php/webapps/39714.txt
  * bunch of html injections to try. Doesn't seem to work? 
* Tried hydra on phpliteadmin page -> found Password123

```
hydra -l "admin" -P /usr/share/wordlists/rockyou.txt 10.10.10.43 https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect"
```

* Can log in and do the 1.9.3 thing. 
* Tried some of the 1.9.6 things with url encoding the input and didn't seem to work still.  
* The table injection doesn't seem to work. 

## 24044.txt

* followed the 1.9.3 exploit to make a table and it says that the db is in /var/tmp/ - how do I go to that? 
* Tried renaming which maybe works but says that it doesn't in one spot and then does in another? The dB seems to disappear but I can't go to that url still? 
* Fine - reading writeup. Apparently my hydra brute force on 80 wasn't working because I was too vague on the failure phrase. Logging in gives the LFI that I need to navigate to the /var/tmp/hack.php db. 
* Could have also just named it h.p instead of hack.php and then the length restriction passes. No idea why /ninevehNotes.txt../ works though, like that folder shouldn't really exist? 
* Not sure how to get dowdotpwn to work 

# Escalation

* Have www-data
* apparently I'm supposed to be looking for strings in images -.- 
* See the strings and then remake the key. 
* I can see that there's ssh ports listening, so there must be something stopping it. Privesc scripts would see knockd. 
* get the user, would see the crontab going, or just notice the files and overwrite the file to get root



# Lessons

Apparently having the phpinfo and a LFI is enough to get RCE: https://alamot.github.io/nineveh_writeup/#getting-shell-without-using-phpliteadmin







