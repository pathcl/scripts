#!/usr/bin/env python

import threading, paramiko

cmd = "someCommand"
outlock = threading.Lock()

def workon(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='someUser', password='somePass')
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write('xy\n')
        stdin.flush()
        with outlock:
            print "Connecting to %s " % host
            print stdout.readlines()

    except paramiko.AuthenticationException:
            print "FAIL " + host

def main():
    threads = []
    for h in open('hosts.txt'):
        h = h.rstrip()
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
