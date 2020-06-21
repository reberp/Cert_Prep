# Enumerate

## Scan

* [ ] scan <ip> #see bashrc

## Enumerate Services

* [ ] web:
  * [ ] dirbust <ip> #see bashrc
  * [ ] nikto
  * [ ] Stuck?: 
    * [ ] dotdotpwn
    * [ ] Eyewitness? Haven't tried yet
  * [ ] Form:
    * [ ] sqlmap 
    * [ ] payloadsallthethings #or other injection cheatsheets
* [ ] Stuck?:
  * [ ] hydra on any login
* [ ] grab tool rec from excel for service (e.x. smbclient for smb)

## Find Exploits

* [ ] web search for exploits or default logins for open ports/services
* [ ] searchsploit for open ports/services
  * [ ] compiled or pre-made? https://github.com/offensive-security/exploitdb-bin-sploits
  * [ ] some precompiled sorted by MS-XXX: https://github.com/SecWiki/windows-kernel-exploits
  * [ ] web search for exploits to find scripts

# Access

Just do it

# Escalate

* [ ] Meterpreter: post/multi/recon/local_exploit_suggester

## Persist

* [ ] Get another shell if it's hard to re-create or a service might crash. 

## Enumerate Machine

### Linux

* [ ] Search dirs: /opt/, /usr/local
* [ ] cat /etc/crontab, may be repeating functionality elsewhere still. 
  * [ ] pspy to try and see additional recurring processes 
* [ ] sudo -l, can I run anything as root?
* [ ] netstat -lp, find localhost listeners
* [ ] find /bin -perm -4000 or find / -xdev -user root \( -perm -4000 -o -perm -2000 \)
  * [ ] gtfobins for any standard and unexpected binaries
  * [ ] test any non-standard scripts/binaries. L/Strace as necessary. 
* [ ] Enumeration tool
* [ ] pspy - anything usual showing up? 

### Win

* [ ] Enumeration tool (winpeas, Seatbelt, JAWS, etc.)
* [ ] systeminfo -> windows-exploit-suggester
* [ ] PowerUp
* [ ] Check Program files and x86, anything unusual installed? 
