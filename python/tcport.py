#!/usr/bin/env python
# Measures response time on a given TCP PORT
# example: ./tcport.py google.cl 80
#

import sys, socket, time

host = sys.argv[1]
port = sys.argv[2]

try:
    measure = socket.getaddrinfo(host, port, socket.AF_UNSPEC, 
                                 socket.SOCK_STREAM)
except socket.gaierror:
    print "getaddrinfo() error:", sys.exc_info()[1]
    sys.exit(1)

for (family, socktype, proto, canon, sockaddr) in measure:
    addr, port = sockaddr[0:2]
    try:
        t1 = time.time()
        s = socket.socket(family, socktype)
        s.connect(sockaddr)
        t2 = time.time()
        s.close()
    except socket.error:
        print "ERROR: %s -> %s" % (sockaddr[0], sys.exc_info()[1])
        pass
    else:
        print "%-40s %8.5f ms" % (sockaddr[0], (t2-t1)*1000.0)
