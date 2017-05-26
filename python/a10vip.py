#!/usr/bin/env python3
# Simple script to query about VIP address.
# Usage: 
# ./a10vip.py -s 192.168.1.1 -u user -q 172.16.0.1
#
# You should know before which are your partitions!
# 
# A10-Active-vMaster[1/1]>show partition
# Total Number of partitions configured: 4
# Partition Name   L3V  Index  Max. Aflex  Admin Count
# ----------------------------------------------------
# First_Partition    Yes  1      32          0
# Second_Partition  Yes  3  *   32          0
# Third_Partition  Yes  5  *   32          0
# Fourth_Partition  Yes  10 *   32          0
#
# Also you should modify 'net1', 'net2', 'net3', 'net4' to fit your needs
  

import sys
import re
import argparse

from datetime import datetime
from getpass import getpass

try:
    from netmiko import ConnectHandler
    from netaddr import IPSet

except ImportError:
    print('Please install netmiko netaddr\n')
    print('i.e. pip install netmiko netaddr\n')
    sys.exit(1)

except:
    print("Unexpected error:", sys.exc_info()[0])
    raise


def main(username, device, ipaddr):
    '''Get password and create device
    '''
    pwd = getpass('Password: ')
    dev = {
    'device_type': 'a10',
    'ip': device,
    'username': username,
    'password': pwd,
    'global_delay_factor': 3,
    'verbose': True,
    'secret': pwd,
    }

    '''Detect query, use it as a partition. Please adjust to your network. 
    '''

    net1 = IPSet(['172.29.1.0/24']) | IPSet(['172.29.2.0/24'])
    net2 = IPSet(['172.31.1.0/24'])
    net3 = IPSet(['172.29.3.0/24']) | IPSet(['172.29.4.0/24'])
    net4 = IPSet(['172.31.3.0/24'])

    '''We use ip address for partition selection
       Adjust to your needs.
    '''

    if ipaddr in net1:
        network = 'First_Partition'

    if ipaddr in net2:
        network = 'Second_partition'

    if ipaddr in net3:
        network = 'Third_Partition'

    if ipaddr in net4:
        network = 'Fourth_Partition'

    '''Connect to device
    '''

    net_connect = ConnectHandler(**dev)

    print("\nStart time: {}".format(str(datetime.now())))
    print("---------------------------------")
    print('Connected to: {}'.format(device))

    net = 'active-partition %s' % network
    net_connect.send_command_timing(net)

    '''Look for ip
    '''

    cmdip = 'show run | section %s' % (ipaddr)
    out = net_connect.send_command(cmdip)
    ports = re.findall('port\s(.*)', out)
    vip = re.findall('service-group\s(.*)', out)
    print(' ')
    print('Searching {} ports {}'.format(vip, ports))


    for m in vip:
        members = 'show slb service-group %s config | include Member' % (m)
        cmdmembers = net_connect.send_command(members)
        regex = re.findall(r'Member[0-9]:([^\t][^:]+)', cmdmembers)

        print(' ')
        print('Hosts for {} are:'.format(m))
        print(' ')
        for host in regex:
            host = host.strip()
            iphosts = 'show running-config | include %s' % (host)
            findhosts = net_connect.send_command(iphosts)
            hosts = re.findall('slb\sserver\s(.*)', findhosts)
            if hosts:
                print(hosts)

    print("---------------------------------")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store',dest='username', help='Username', required=True)
    parser.add_argument('-s', action='store',dest='device', help='Host to connect', required=False,
            default='127.0.0.1')
    parser.add_argument('-q', action='store',dest='ipaddr', help='VIP to find', required=True)
    args = parser.parse_args()
    main(args.username, args.device, args.ipaddr)