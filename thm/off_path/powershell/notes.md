# Basic commands

Verb-Noun pairs like Get-Command
Get-Help [-examples], -h for powershell
Wild cards allowed: Get-Command <Verb>-*
pipe to pass output from one to another
	Get-Command | Get-Member -Membertype Method
grep and cat
	cat: type file
	grep: sls "string" <file/stdin>
Create new object with select-object
	get-children | select-object -property mode, name
filter with where-object
	Verb-Noun | Where-Object -Property PropertyName -operator Value
	Verb-Noun | Where-Object {$_.PropertyName -operator Value}
Sort with sort-object
	Verb-Noun | Sort-Object -property propertyname
Search for file
	get-childitem -path C:\ -Recurse -ErrorAction silentlycontinue -include <filename>
	| to get-content to read it
pipe output to measure to count
get-filehash -algorithm * to get hashes
test-path to see if folder exists

# Enumeration
get users
	net user for AD and local
	get-localuser for local
	get-localuser -sid <> - for matching to sid
	wmic useraccount where name="duck" get sid - to reverse
	wmic useraccount get name for also inactive accounts
	net user <> - for details
network
	get-netipaddress - for ip info
	get-nettcpconnection - for netstat kindof
get-patches
	wmic qfe list
	get-hotfix
search for file contents: get-childitem -path C:\ -recurse -erroraction silentlycontinue | sls "THING"

# Scripting

