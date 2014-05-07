#!/usr/bin/python

import gettext
import urllib2
import pwd
import os
import re
import optparse
import sys
import socket
import time
from datetime import datetime
import output_messages
import basedefs
from ftplib import FTP
try:
    import iptools
except ImportError:
    print(
        _(output_messages.CANT_IMPORT.format(
            'iptools'
        ))
    )

_ = lambda m: gettext.dgettext(message=m, domain='port-scanner')


class Status:
    """
    Exit statuses
    """

    OK = 0
    MISSING_OPTION = 1
    KEYBOARD_INTERRUPT = 2
    CANNOT_CONNECT = 3
    RANGE_ERROR = 4
    IP_ERROR = 5
    PERMISSION_ERROR = 6


def get_args():
    """
    Command line options
    """

    parser = optparse.OptionParser(description='Reads user command line args.')
    parser.add_option('--ip',
                      dest='ip',
                      help='target ip address')
    parser.add_option('--time-interval', '-t',
                      dest='time_interval',
                      type='int',
                      default='2000',
                      help='time interval between each scan in milliseconds')
    parser.add_option('--protocol-type',
                      dest='protocol_type',
                      help='protocol type [UDP/TCP/ICMP]')
    parser.add_option('--port', '-p',
                      dest='ports',
                      help='ports [can be range : -p 22-54,'
                           'can be single port : -p 80, can be combination '
                           ': -p 80,43,23,125]')
    parser.add_option('--type',
                      dest='scan_type',
                      default='full',
                      help='scan type [full, stealth, fin, ack]')
    parser.add_option('--banner_grabber', '-b',
                      dest='banner_grabber',
                      action='store_true',
                      help='bannerGrabber status (Should work only for TCP)')
    parser.add_option('--scan',
                      dest='scan',
                      action='store_true',
                      help='scan the ip range for ICMP replies')
    parser.add_option('--ip-range',
                      dest='ip_range',
                      help='ip range. Should be used only with "--scan" option. '
                           'Example: 10.0.0.0-10.0.0.255')

    return parser.parse_args()


def print_summary(params=None,
                  map_network=False,
                  total_open_ports=None):
    """
    Prints the summary
    """

    print('\n\n')
    print(
        _(output_messages.SUMMARY)
    )
    if map_network:
        print(
            _(output_messages.TOTAL_ACTIVE_HOSTS.format(
                params['HOSTS_UP']
            ))
        )
        print(
            _(output_messages.TOTAL_DOWN_HOSTS.format(
                params['HOSTS_DOWN']
            ))
        )
        print(
            _(output_messages.TOTAL_HOSTS.format(
                params['TOTAL_HOSTS']
            ))
        )

    if total_open_ports:
        print(
            _(output_messages.TOTAL_OPEN_PORTS.format(
                total_open_ports
            ))
        )
    print(
        _(output_messages.SCANNING_STARTED.format(
            params['START_TIME']
        ))
    )
    print(
        _(output_messages.SCANNING_ENDED.format(
            params['END_TIME']
        ))
    )
    print(
        _(output_messages.SCANNING_COMPLETED.format(
            params['TOTAL']
        ))
    )


class PortScanner():
    """
    Port scanner class

    Parameters:
        dst_ip_addr - target ip address
        interval - time interval between each scan
        protocol_type - protocol type to scan
        type - scan type
        ports - ports to scan (default defined in get_args())
    """

    def __init__(self,
                 dst_ip_addr,
                 interval,
                 protocol_type,
                 type,
                 ports):

        self.dst_ip_address = dst_ip_addr
        self.interval = interval
        self.protocol_type = protocol_type.upper()
        self.ports = ports
        self.type = type

    def _grab_http(self):
        """
        Grabs the http info
        Returns:
            _service - service name
             _os - OS name
        """

        u = urllib2.urlopen('http://' + self.dst_ip_address)

        if len(u.info()['Server'].split()) == 2:
            _service, _os = u.info()['Server'].split()
            _os = _os.strip('()')
            return _service, _os

        if len(u.info()['Server'].split()) == 1:
            _service = u.info()['Server']
            return _service, None

    def _grab(self, port):
        """
        Grabs the ftp info
        Returns:
            _service - service name
            _os - OS name
        """
        s = socket.socket()
        s.connect((self.dst_ip_address, int(port)))
        _service = s.recv(basedefs.BUFSIZE)

        if basedefs.VSFTPD in _service.lower():
            _service = re.findall(basedefs.FTP_WELCOME_REGEX,
                                  _service).pop().strip('()').rstrip()
            _os = basedefs.OTHER_LINUX
        elif basedefs.OPEN_SSH in _service.lower():
            _service = _service.rstrip()
            _os = basedefs.OTHER_LINUX

        s.close()

        return _service, _os

    def port_scanner(self, with_grabber=False):
        """
        Scans the ports of the given ip address

        """

        _socket_type = None
        _socket_family = socket.AF_INET
        _ports = [self.ports]
        _total_open_ports = 0

        # Validate socket
        if self.protocol_type == 'TCP':
            _socket_type = socket.SOCK_STREAM
        if self.protocol_type == 'UDP':
            _socket_type = socket.SOCK_DGRAM

        # Validate ports
        if ',' in self.ports:
            _ports = self.ports.split(',')
        if '-' in self.ports:
            __ports = self.ports.replace('-', ',').split(',')
            if not int(__ports[0]) < int(__ports[1]):
                print(
                    _(output_messages.RANGE_ERROR.format(
                        __ports[0],
                        __ports[1]
                    ))
                )
                sys.exit(Status.RANGE_ERROR)

            _ports = range(int(__ports[0]), int(__ports[1]))
            _ports.append(int(__ports[1]))

        print(
            _(output_messages.DELIMITER)
        )
        print(
            _(output_messages.SCANNING.format(
                self.dst_ip_address
            ))
        )
        print(
            _(output_messages.DELIMITER)
        )

        # Start scan time
        _start_time = time.ctime()
        _t1 = datetime.now()

        try:
            for _port in _ports:
                _protocol = output_messages.CANT_RECOGNIZE
                if str(_port) in basedefs.ports_mapping:
                    _protocol = basedefs.ports_mapping[str(_port)].split(',')[0]

                sock = socket.socket(_socket_family, _socket_type)
                sock.settimeout(basedefs.SOCKET_TIMEOUT)
                if self.protocol_type == 'UDP':
                    try:
                        sock.sendto(output_messages.TEST_STR, (self.dst_ip_address, int(_port)))
                        recv, svr = sock.recvfrom(255)
                        print(
                            _(output_messages.OPEN_PORT.format(
                                _port,
                                _protocol
                            ))
                        )
                        _total_open_ports += 1

                    except socket.error:
                        pass
                    except socket.timeout:
                        pass

                _result = -1
                if self.protocol_type == 'TCP':
                    try:
                        _result = sock.connect_ex((self.dst_ip_address, int(_port)))
                        if _result == 0:
                            # Check if grabber is needed
                            if with_grabber:
                                if int(_port) == 80:
                                    _server, _os = self._grab_http()
                                    print(
                                        _(output_messages.OPEN_PORT_WITH_GRABBER.format(
                                            _port,
                                            _protocol,
                                            _server,
                                            _os
                                        ))
                                    )

                                    sock.close()
                                    time.sleep(self.interval * 0.001)
                                    _total_open_ports += 1
                                    continue

                                if int(_port) == 21:
                                    _server, _os = self._grab(_port)
                                    print(
                                        _(output_messages.OPEN_PORT_WITH_GRABBER.format(
                                            _port,
                                            _protocol,
                                            _server,
                                            _os
                                        ))
                                    )
                                    time.sleep(self.interval * 0.001)
                                    _total_open_ports += 1
                                    continue

                                if int(_port) == 22:
                                    _server, _os = self._grab(_port)
                                    print(
                                        _(output_messages.OPEN_PORT_WITH_GRABBER.format(
                                            _port,
                                            _protocol,
                                            _server,
                                            _os
                                        ))
                                    )
                                    time.sleep(self.interval * 0.001)
                                    _total_open_ports += 1
                                    continue
                            print(
                                _(output_messages.OPEN_PORT.format(
                                    _port,
                                    _protocol
                                ))
                            )
                            sock.close()
                            _total_open_ports += 1
                    except socket.error:
                        pass

                sock.close()
                time.sleep(self.interval * 0.001)

        except KeyboardInterrupt:
            print(
                _(output_messages.KEYBOARD_INTERRUPT)
            )
            sys.exit(Status.KEYBOARD_INTERRUPT)

        # End scan time
        _t2 = datetime.now()
        _end_time = time.ctime()
        _total = _t2 - _t1

        params = {}
        params['END_TIME'] = _end_time
        params['START_TIME'] = _start_time
        params['TOTAL'] = _total
        params['TOTAL_OPEN_PORTS'] = _total_open_ports

        print_summary(params,
                      total_open_ports=_total_open_ports)


def map_network(ip_range):
    """
    Sends ICMP packet to the ip range and maps the network

    Parameters:
        ip_range - range of ip's to scan
    """

    params = {}
    _counter_active = 0
    _counter_down = 0
    _total_hosts = 0

    _is_range_valid = re.match(basedefs.IP_RANGE_REGEX, ip_range)
    if not _is_range_valid:
        print(
            _(output_messages.IP_RANGE_NOT_VALID.format(
                ip_range
            ))
        )
        sys.exit(Status.IP_ERROR)

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                      socket.getprotobyname('icmp'))

    s.settimeout(basedefs.SOCKET_TIMEOUT)

    _start, _end = ip_range.replace(' ', '').split('-')[:]

    r = iptools.IpRange(_start, _end)

    # Start timer
    _start_time = time.ctime()
    _t1 = datetime.now()
    for _ip in r:
        try:
            s.connect((_ip, 22))
            s.send(output_messages.TEST_STR)
            buf = s.recv(basedefs.BUFSIZE)

            if output_messages.TEST_STR in buf:
                print(
                    _(output_messages.HOST_IS_UP.format(
                        _ip
                    ))
                )
                _counter_active += 1
                time.sleep(1)
        except socket.error:
            print(
                _(output_messages.HOST_IS_DOWN.format(
                    _ip
                ))
            )
            _counter_down += 1

    # End timer
    _end_time = time.ctime()
    _t2 = datetime.now()
    _total = _t2 - _t1
    _total_hosts = _counter_down + _counter_active

    params['END_TIME'] = _end_time
    params['TOTAL'] = _total
    params['TOTAL_HOSTS'] = _total_hosts
    params['HOSTS_DOWN'] = _counter_down
    params['HOSTS_UP'] = _counter_active
    params['START_TIME'] = _start_time

    print_summary(params=params,
                  map_network=True)


def _verifyUserPermissions():
    """
    Verifies that app will be executed with a root
    permissions
    """

    _username = pwd.getpwuid(os.getuid())[0]
    if os.geteuid() != 0:
        print(
            _(output_messages.ERR_EXP_INVALID_PERM.format(
                _username
            ))
        )
        sys.exit(Status.PERMISSION_ERROR)


def create_port_scanner(options):
    """
    Creates port_scanner object
    Parameters:
        options - option to create a port scanner object
    Returns port_scanner object
    """

    port_scanner = PortScanner(options.ip,
                               options.time_interval,
                               options.protocol_type,
                               options.scan_type,
                               options.ports)

    return port_scanner


def main():
    """
    Main
    """

    _verifyUserPermissions()
    (options, args) = get_args()

    if options.scan \
            and options.ip_range:
        map_network(options.ip_range)
        sys.exit(Status.OK)

    if options.ip \
        and options.protocol_type \
            and options.ports \
            and options.scan_type == 'full':

        port_scanner = create_port_scanner(options)

        if options.banner_grabber:
            port_scanner.port_scanner(with_grabber=True)
            sys.exit(Status.OK)
        port_scanner.port_scanner()
        sys.exit(Status.OK)


if __name__ == '__main__':
    main()
