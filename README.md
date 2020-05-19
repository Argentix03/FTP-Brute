# FTP-Brute
Multi-threaded FTP Bruteforce Cracker
=
Simple Python implementation of an FTP Bruteforce attack using ftplib.
I made this tool to practice multithreading in python.

## Install
$ git clone https://github.com/Argentix03/FTP-Brute.git


Usage example:
```
$ python3 ftp-cracker-cli.py --target 10.10.10.10 --port 21 --user ftpuser --passlist /usr/share/wordlists/rockyou.txt --threads 100 --clean
```
The above exmaple will do 50/sec connections (with the default 2 second timeout) to 10.10.10.10:21 with user ftpuser and a 
different password from /usr/share/wordlists/rockyou.txt each connection. Output only if succeeded.

## Arguments

| Command	            | Description             |
----------------------|-------------------------|
|-t, --target \<target> | IPv4 Address of FTP server.      |
|-p, --port	\<port> | Port number to connect on.  |
|-u, --user \<username> | Username to try with.|
|-P, --passlist \<password file> | Password file delimited by newlines|
|-T, --threads \<number of threads> | The number of threads to run with. each thread has a timeout of 2 seconds.|
|--timeout <seconds> | Set the timeout in seconds for each connection.|
|--clean | Only output success and ignore fails. Recommended!|
