Super slow box, didn't actually bother working through it once my scans kept returning different results. Just read a writeup. 
# Enumerate

## Scan

* all ports taking too long, default scan shows 

```
PORT      STATE    SERVICE
79/tcp    open     finger
111/tcp   open     rpcbind
544/tcp   filtered kshell
3580/tcp  filtered nati-svrloc
4125/tcp  filtered rww
9500/tcp  filtered ismserver
12000/tcp filtered cce4x
```

* scan service

```
PORT    STATE SERVICE VERSION
79/tcp  open  finger  Sun Solaris fingerd
|_finger: No one logged on\x0D
111/tcp open  rpcbind
Service Info: OS: Solaris; CPE: cpe:/o:sun:sunos
```

## Services

* no exploits for those 
* couldn't figure out how to use it to get anything? 
* finger-user-enum script and the username file from ippsec video to get the users sunny and sammy. 
* Also missed the 22022 port because I didn't scan everything. Got max-retries change from ippsec and find it. 
* Alternatively, apparently a script scan on 79 would find sunny at least. Not sure why it didn't the first time? Shitty box I guess. 

# Access

Box is so slow I'm not gonna bother, just noting some writeup steps. 

* hydra

```
hydra -f -l sunny -P /usr/share/wordlists/rockyou.txt 10.10.10.76 -s 22022 ssh
```

# Escalate

* find and crack backup file
* switch to sammy
* see wget -> post shadow and root.txt files to self. See gtfobins



