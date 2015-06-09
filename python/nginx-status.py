#!/usr/bin/python
import urllib2
import sys
import getopt
import re


def Usage():
    print "Usage: nginx-status.py -h 127.0.0.1 -p 80 -a [active|accepted|waiting]"
    sys.exit(2)


def main():
    if len(sys.argv) < 6:
        Usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:a:")
        Dict = dict(opts)
    except getopt.GetoptError:
        Usage()
    # Base url for nginx status module
    Nginx_url = "http://" + Dict['-h'] + ":" + Dict['-p'] + "/status"
    # Create an object using urllib2 to ask for our url
    Nginx_req = urllib2.Request(Nginx_url)
    # Then we read what's inside
    Nginx_res = urllib2.urlopen(Nginx_req)
    # This is a regular expression which enables parses our nginx status
    status = re.findall(r'\d{1,8}', Nginx_res.read())
    # Given Dict we handle parameters 'active', 'accepted', 'handled'
    if (Dict['-a'] == "active"):
        print status[0]
    elif (Dict['-a'] == "accepted"):
        print status[1]
    elif (Dict['-a'] == "waiting"):
        print status[6]
    else:
        print "unknown!!"
        sys.exit(1)

if __name__ == '__main__':
    main()
