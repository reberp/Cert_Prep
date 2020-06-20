$username = 'administrator'
$password = 'Welcome1!'

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword
Start-Process C:\users\alfred\1235.exe -Credential $credential
