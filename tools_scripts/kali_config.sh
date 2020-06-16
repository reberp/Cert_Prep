#!/bin/bash

echo "source $PWD/bashrc" >> ~/.bashrc


# Things that I added to kali and should remember to install if I start over
sudo apt install seclists -y
sudo ln -n -s /usr/share/seclists /usr/share/wordlists/seclists #might not be right but I'm going to forget about this otherwise.
sudo apt install powersploit -y
sudo apt install knockd -y
wget http://pentestmonkey.net/tools/php-reverse-shell/php-reverse-shell-1.0.tar.gz
sudo gem install wpscan #might have to do this https://github.com/BBC-News/wraith/issues/526
wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip
echo "Downloaded aquatone 1.7.0, newer version?"
# I'm not going to bother diving into the github api, but should be some way to ask for latest releast.
# Alternatively, it's probably easier to just curl https://github.com/michenriksen/aquatone/releases/latest | grep <version>
sudo apt install nautilus -y

echo "Go to ur /etc/samba/smb.conf file and add the  following, client min protocol = NT1. Under the global section. Think this solves smbclient protocol errors. "

sudo gem install evil-winrm
