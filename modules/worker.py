#!/usr/bin/python
#
#	FILENAME : worker.py
#
#	This file is used by mailWorker.py script.


import time, random, sys, os
import threading
import Queue
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate

#	Colors
HEADER = '\033[95m'
GRAY = '\033[1;30m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"

#
#	main Class
#
class Emailer(threading.Thread):
	
	def __init__ (self, ID, SSL, fromaddr, mail_server, port, user, passwd, _queue):
		self.ID 		 	 = ID
		self.SSL	 		 = SSL
		self.fromaddr 		 = fromaddr
		self.mail_server     = mail_server
		self.port 			 = port
		self.user 			 = user
		self.passwd			 = passwd
		self._queue 		 = _queue

		threading.Thread.__init__ (self)

	def send_email(self, mail, toaddr, rdelay):
		
		# make email content
		msg = MIMEMultipart()
		msg['From'] = self.fromaddr
		msg['To'] = toaddr
    	#msg["cc"]=', '.join(cc_emails)
		msg['Subject'] = mail["SUBJECT"]
		msg["Date"] = formatdate(localtime=True)
		if mail["FORMAT"] == "plain":
			html="<html><head></head><body><h3>%s</h3><p>%s</p></body></html>" % (mail["SUBJECT"], mail["CONTENT"])
		else:
			html=mail["CONTENT"]
		msg.attach( MIMEText(html, 'html') )
		text = msg.as_string()

		# set an artificial delay
		time.sleep(rdelay)
		
		# connect using settings
		try:
			if self.SSL:
				if self.port is None:
					server = smtplib.SMTP_SSL(self.mail_server)
				else:
					server = smtplib.SMTP_SSL(self.mail_server, self.port)
				server.ehlo()
			else:
				if self.port is None:
					server = smtplib.SMTP(self.mail_server)
				else:
					server = smtplib.SMTP(self.mail_server, self.port)
				server.ehlo()
				try:
					server.starttls()
				except:
					pass
				server.ehlo()
			server.login(self.user, self.passwd)
			server.ehlo()
			
			# send email and quit
			server.sendmail(self.fromaddr, toaddr, text)
			server.quit()
			print "[%s] %s%s%s send email to %s" % (self.ID, OKGREEN, self.fromaddr, ENDC, toaddr)
		except:
			self._queue.put( (toaddr, random.randint(10, 20)/1.0) )
			print "[%s] THERE WAS A %sPROBLEM%s FOR %s%s%s TO SEND MAIL TO %s" % (self.ID, FAIL, ENDC, FAIL, self.fromaddr, ENDC, toaddr)


	def run(self):
		while 1:
			# get next entry from queue 
			item = self._queue.get()
			
			# if entry is none we reached the end of queue 
			if item is None:
				break
			
			(Mail, toaddr, rdelay) = item
			# connect and send email
			self.send_email(Mail, toaddr, rdelay)
			
		self.exit()

	def exit(self):
		print "[%s] %s%s%s exited" % (self.ID, OKGREEN, self.fromaddr, ENDC)

