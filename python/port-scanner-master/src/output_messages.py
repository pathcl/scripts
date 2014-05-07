#!/usr/bin/python

"""
Output messages for the program
"""

# Text colors
RED = '\033[0;31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
NO_COLOR = '\033[0m'

CANNOT_CONNECT = RED + 'ERROR:' + NO_COLOR \
    + 'Could not connect to server "{0}" on protocol "{1}" port "{2}"'
MISSING_OPTION = RED + 'ERROR:' + NO_COLOR + ' Missing option "{}"'
KEYBOARD_INTERRUPT = 'You pressed Ctrl+C'
SCANNING = 'Please wait, scanning remote ip "{0}"'
OPEN_PORT = 'Port "{0}": \t' + GREEN + 'Open' + NO_COLOR + ' [{1}]'
OPEN_PORT_WITH_GRABBER = OPEN_PORT + '\t' + 'Service name: {2}\t' + 'OS: {3}'
RANGE_ERROR = RED + 'ERROR:' + NO_COLOR \
                    + ' in "--ip" First argument "{0}" ' \
                      'cannot be lower then second "{1}"'
SCANNING_COMPLETED = 'Scan Completed in: {0}'
CANT_RECOGNIZE = RED + 'CANT RECOGNIZE PROTOCOL' + NO_COLOR
SCANNING_STARTED = 'Scanning started at : {0}'
SCANNING_ENDED = 'Scanning ended at : {0}'
SUMMARY = YELLOW + 'SUMMARY:' + NO_COLOR
DELIMITER = '-' * 60
HOST_IS_UP = '"{0}"\t' + 'Status: ' + GREEN + 'UP' + NO_COLOR
HOST_IS_DOWN = '"{0}"\t ' + 'Status: ' + RED + 'DOWN' + NO_COLOR
TEST_STR = '--TEST LINE--'
CANT_IMPORT = 'Sorry, cannot import {0} module. ' \
              'Please install it and run once again'
IP_NOT_VALID = '{0} is not a valid ip address'
IP_RANGE_NOT_VALID = '{0} is not a valid ip range'
ERR_EXP_INVALID_PERM = 'Error: insufficient permissions for user {}, ' \
                       'you must run with user root.'
TOTAL_OPEN_PORTS = 'Total open ports: {0}'
TOTAL_HOSTS = 'Total hosts: {0}'
TOTAL_ACTIVE_HOSTS = 'Total active hosts: {0}'
TOTAL_DOWN_HOSTS = 'Total down hosts: {0}'
