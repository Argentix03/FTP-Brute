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
## Arguments

| Command	            | Description             |
----------------------|-------------------------|
|-t, --target \<target> | IPv4 Address of FTP server.      |
|-p, --port	\<port> | Port number to connect on.  |
|-u, --user \<username> | Username to try with.|
|-P, --passlist \<password file> | Password file delimited by newlines|
|-T, --threads \<number of threads> | the number of threads to run with. each thread has a timeout of 2 seconds.|
|--clean | only output success and ignore fails. Recommended!|
