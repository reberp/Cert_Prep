#!/bin/bash
git clone https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite
git clone https://github.com/SecureAuthCorp/impacket
git clone https://github.com/swisskyrepo/PayloadsAllTheThings
git clone https://github.com/sleventyeleven/linuxprivchecker
git clone https://github.com/pentestmonkey/unix-privesc-check
git clone https://github.com/rebootuser/LinEnum
git clone https://github.com/mattiareggiani/WinEnum
git clone https://github.com/samratashok/nishang
git clone https://github.com/FortyNorthSecurity/EyeWitness.git
git clone https://github.com/kavishgr/xmlrpc-bruteforcer
git clone https://github.com/DominicBreuker/pspy.git
wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32 > pspy/pspy32
wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64 > pspy/pspy64
echo "Check if pspy32 and 64 and most current version (downloaded v1.2.0)"
