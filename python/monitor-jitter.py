#!/usr/bin/python2.7

try:
   import numpy
   from decimal import Decimal

except ImportError:
   raise ImportError('Please check numpy and Decimal modules')


def main():
    data = numpy.loadtxt('/path/to/somefile')
    if Decimal(data.sum()) > 1:
        print str(data.sum()) + " NOK" 
    else:
        print str(data.sum()) + " OK" 

if __name__ == "__main__":
    main()
