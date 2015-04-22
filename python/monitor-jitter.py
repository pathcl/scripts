#!/usr/bin/python2.7

try:
   import numpy
   from decimal import Decimal

except ImportError:
   raise ImportError('Please check numpy and Decimal modules')


def main():
    data = numpy.loadtxt('ultimo.txt')
    if Decimal(data.sum()) > 1:
        return "Jitter Lag!"
    else:
        return "Ok"


if __name__ == '__main__':
   print main()
