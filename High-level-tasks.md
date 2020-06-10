# Enumerate

## Scan

* [ ] nmap -p- \<HOST\> --max-retries 5
  * [ ] For open ports: nmap -sC -sV -o nmap_scan.txt -O -p \<PORTS\> \<HOST\>  
  * [ ] Taking too long? lower max-retries toward 0 

## Enumerate Services

* [ ] web:
  * [ ] dirb/dirbuster/gobuster (with .php/txt/js/sh/pl)
  * [ ] nikto
  * [ ] Stuck?: 
    * [ ] dotdotpwn
    * [ ] Eyewitness? Haven't tried yet
  * [ ] Form:
    * [ ] sqlmap 
    * [ ] payloadsallthethings
* [ ] Stuck?:
  * [ ] hydra on any login
* [ ] grab tool rec from excel for service (e.x. smbclient for smb)

## Find Exploits

* [ ] searchsploit for open ports/services
* [ ] web search for exploits or default logins for open ports/services

# Access

Just do it

# Escalate

* [ ] Meterpreter: post/multi/recon/local_exploit_suggester

## Enumerate Machine

### Linux

* [ ] Search dirs: /opt/, /usr/local
* [ ] cat /etc/crontab, may be repeating functionality elsewhere still. 
* [ ] sudo -l, can I run anything as root?
* [ ] netstat -lp, find localhost listeners
* [ ] find /bin -perm -4000 or find / -xdev -user root \( -perm -4000 -o -perm -2000 \)
  * [ ] gtfobins for any standard and unexpected binaries
  * [ ] test any non-standard scripts/binaries. L/Strace as necessary. 
* [ ] Enumeration tool

### Win

* [ ] Enumeration tool
* [ ] systeminfo -> windows-exploit-suggester
