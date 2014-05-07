#!/usr/bin/python

SOCKET_TIMEOUT = 2
BUFSIZE = 1500
_REGEX = '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
IP_RANGE_REGEX = '^{0}-{1}$'.format(
    _REGEX,
    _REGEX
)
FTP_WELCOME_REGEX = '\(.*\)'
OTHER_LINUX = 'Other: Linux'
OPEN_SSH = 'openssh'
VSFTPD = 'vsftpd'
ports_mapping = {
    '80': 'http, tcp',
    '443': 'https, tcp',
    '22': 'ssh, tcp',
    '21': 'ftp, udp'
}
