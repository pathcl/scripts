#!/usr/bin/python
import urllib2
import sys
import getopt
import re


def Usage():
    print "Usage: nginx-status.py -h 127.0.0.1 -p 80 -a [active|accepted|requests]"
    sys.exit(2)


def main():
    if len(sys.argv) < 6:
        Usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:a:")
        Dict = dict(opts)
    except getopt.GetoptError:
        Usage()
    Nginx_url = "http://" + Dict['-h'] + ":" + Dict['-p'] + "/status"
    Nginx_req = urllib2.Request(Nginx_url)
    Nginx_res = urllib2.urlopen(Nginx_req)
    Output_key = re.findall(r'\d{1,8}', Nginx_res.read())
    if (Dict['-a'] == "active"):
        print Output_key[0]
    elif (Dict['-a'] == "accepted"):
        print Output_key[1]
    elif (Dict['-a'] == "handled"):
        print Output_key[2]
    elif (Dict['-a'] == "requests"):
        requests = float(Output_key[3]) / float(Output_key[2])
        print round(requests)
    else:
        print "unknown!!"
        sys.exit(1)

if __name__ == '__main__':
    main()
