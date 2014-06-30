#!/usr/bin/python
import time
import smtplib

sender = 'user@domain.tld'
receivers = ['luis.sanmartin@unix.cl']
now = time.strftime("%c")
message = """From: OTRS <user@domain.tld>
To: Luis San Martin <luis.sanmartin@unix.cl>
Subject: ALRT ALRT

ALRT ALRT ALRT ALRT.
"""

try:
   smtpObj = smtplib.SMTP('localhost.localdomain:25')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
   print ("Current time %s"  % now )
except Exception:
   print "Error: unable to send email"
