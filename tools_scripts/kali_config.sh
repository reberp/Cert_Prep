#!/bin/bash

echo "source /home/pat/Desktop/Cert_Prep/tools_scripts/bashrc" >> ~/.bashrc

# Things that I added to kali and should remember to install if I start over
sudo apt install seclists -y
sudo ln -n -s /usr/share/seclists /usr/share/wordlists/seclists #might not be right but I'm going to forget about this otherwise. 
sudo apt install powersploit -y 
sudo apt install knockd -y
wget http://pentestmonkey.net/tools/php-reverse-shell/php-reverse-shell-1.0.tar.gz
sudo gem install wpscan #might have to do this https://github.com/BBC-News/wraith/issues/526
