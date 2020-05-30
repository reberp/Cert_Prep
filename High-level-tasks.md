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

## Enumerate Machine

### Linux

* [ ] Search dirs: /opt/, /usr/local
* [ ] cat /etc/crontab
* [ ] sudo -l
* [ ] netstat -lp
* [ ] Enumeration tool

### Win

* [ ] Enumeration tool

