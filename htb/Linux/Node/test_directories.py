#!/usr/bin/env python3

import requests
import hashlib
import threading

def run_threads(name):
	filepath = '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'
	#filepath = './directory-list-2.3-medium.txt'
	with open(filepath) as fp:
		for line in fp:
			line.strip('\n')
			url = 'http://10.10.10.58:3000/'+line
			url = url.strip('\n')
			url+=str(".html")
			x = requests.get(url)
			#print("Checking: "+url)
			if ('30f2cc86275a96b522f9818576ec65cf' != hashlib.md5(x.text.encode('utf-8')).hexdigest()):
				print(line)

# Was thinking of making it threaded, probably not worth any effort. 
run_threads(1)

