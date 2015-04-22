#!/usr/bin/python
import time, smtplib

sender = 'user@domain.tld'
receivers = ['someMail@domain.tld']
now = time.strftime("%c")
message = """From: SomeSender <user@domain.tld>
To: Luis San Martin <luis.sanmartin@domain.tld>
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
