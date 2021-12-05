apt-get install dnscrypt-proxy
systemctl enable dnscrypt-proxy.service
sed -i 's/plugins=ifupdown,keyfile/plugins=ifupdown,keyfile\ndns=none/g' /etc/NetworkManager/NetworkManager.conf
systemctl restart NetworkManager
rm -f /etc/resolv.conf
echo "nameserver 127.0.2.1\noptions edns0 single-request-reopen\nEDNSPayloadSize 4096" > /etc/resolv.conf
systemctl restart dnscrypt-proxy.service
