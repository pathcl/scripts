#!/usr/bin/python
import time
import smtplib

sender = 'otrs@u.uchile.cl'
receivers = ['luis.sanmartin@u.uchile.cl']
now = time.strftime("%c")
message = """From: OTRS <otrs@u.uchile.cl>
To: Luis San Martin <luis.sanmartin@u.uchile.cl>
Subject: Alerta procesos OTRS

ALRT ALRT ALRT ALRT.
"""

try:
   smtpObj = smtplib.SMTP('mtaprod.uchile.cl:25')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
   print ("Current time %s"  % now )
except Exception:
   print "Error: unable to send email"
