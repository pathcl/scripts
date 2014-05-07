port-scanner
============

Examples:
---------

**Map the network:**

`$ sudo python port-scanner.py --scan --ip-range 10.0.0.1-10.0.0.254`

**Scan ip with banner grabber:**

`$ sudo python port-scanner.py --ip 10.0.0.1 -p 80,22 --protocol-type TCP -b`

**Scan ip without banner grabber:**

`$ sudo python port-scanner.py --ip 10.0.0.1 -p 80,22 --protocol-type TCP`

**Scan with a port range:**

`$ sudo python port-scanner.py --ip 10.0.0.1 -p 1-1024 --protocol-type TCP`
