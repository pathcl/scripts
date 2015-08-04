#!/usr/bin/env python
# Ideally looks up for a given str on a file (bind for example)
try:

    import threading
    import paramiko
    import sys
    import getpass

except ImportError:
    print("Error: Please check threading && paramiko modules")

cmd = "grep  " + sys.argv[1] + " /etc/bind/master/db.domain.tld"
outlock = threading.Lock()
pwd = getpass.getpass('Password:')


def workon(host):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='user', password=pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write('xy\n')
        stdin.flush()
        with outlock:
            print('Buscando en {0}'.format(host))
            for line in stdout.readlines():
                print(line.rstrip())

    except paramiko.AuthenticationException:
            print('FAIL en {0}'.format(host))


def main():
    hosts = open('/home/pathcl/python/otros/dns.txt')
    threads = []
    for h in hosts:
        h = h.rstrip()
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

main()
