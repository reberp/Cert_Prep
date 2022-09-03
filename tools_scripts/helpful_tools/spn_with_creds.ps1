$domainobj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = ($domainobj.pdcRoleOwner).name
$searchString = "LDAP://"
$searchString += $PDC + "/"

$DistinguishedName = "DC=$($domainObj.Name.Replace('.', ',DC='))"
#$SearchString += "CN=domain Computers,CN=Users,"+$DistinguishedName
$SearchString += $DistinguishedName
$Searcher = New-Object System.DirectoryServices.DirectorySearcher([ADSI]$SearchString)
$objDomain = New-Object System.DirectoryServices.DirectoryEntry($SearchString, "DOMAIN\USERNAME", "PASSWORD")
$Searcher.SearchRoot = $objDomain

$Searcher.filter="serviceprincipalname=*"

$Result = $Searcher.FindAll()

Foreach($obj in $Result)
{
write-host("--------------------------")
    Foreach($prop in $obj.Properties)
    {
        $prop
    }
}


