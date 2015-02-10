#!/usr/bin/python
import sys, os

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate
import datetime

import senders as S


#
#	Colors
#
HEADER = '\033[95m'
GRAY = '\033[1;30m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"

BANNER="""                                                                    
                                     lkk;                           
                                    cMMK                            
                                   'WMN.                            
                                  .NMW'                             
     .o0NMMMWXx;                  KMM:              'o0NMMMWKx,     
   'KMMXo:;;lOMMNc               OMMd             .KMM0l;,;l0MMK.   
  ,MMW:       .0Xo              oMM0             ,WMW,       :MMN.  
  NMMl                         ;MMX              NMMc         OMMo  
 'MMM.                        .WMW.             'MMMOkkkkkkkkkXMM0  
%s ,MMM                        .NMM,              ,MMMOkkkkkkkkkkkko  
 .MMM'                       KMMl               .MMM,               
  xMMK          '           xMMk                 dMMK               
   kMMXc.    'oNMK         cMM0                   dMMNc.    .;OKl   
    'kWMMMNWMMMKl.        ,MMX.                    .xNMMWNWMMMNk,   
       .,:::;'            ;cc.                        .,:::;,.      
%s"""%(GRAY,ENDC)
usage="""\nUSAGE:\n\tpython test_email.py receiver@example.com"""#%(OKGREEN,ENDC)
default={
	'email_address': 'John@gmail.com',
	'username': 'John@gmail.com',
	'password': 'John123',
	'email_provider':'gmail.com',
	'port': None,
	'SSL': True
}

def printBanner():
	os.system("clear")
	print '\n    '.join(BANNER.split('\n'))
	print """%s    %s \n    MAIL WORKER
    __________________________________________________________________%s"""%(GRAY, datetime.date.today(), ENDC)


def test_email(ID, SSL, fromaddr, mail_server, port, user, passwd, toaddr):
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	#msg["cc"] = ', '.join(cc_emails)
	msg['Subject'] = S.SUBJECT
	msg["Date"] = formatdate(localtime=True)
	if S.FORMAT == "plain":
		html="""<html><head></head><body><h3>%s</h3><p>%s</p></body></html>""" % (S.SUBJECT, S.CONTENT )
	else:
		html=S.CONTENT
	msg.attach( MIMEText(html, 'html') )
	text = msg.as_string()
	
	try:
		if SSL:
			if port is None:
				server = smtplib.SMTP_SSL(mail_server)
			else:
				server = smtplib.SMTP_SSL(mail_server, port)
			server.ehlo()
		else:
			if port is None:
				server = smtplib.SMTP(mail_server)
			else:
				server = smtplib.SMTP(mail_server, port)
			server.ehlo()
			try:
				server.starttls()
			except:
				pass
			server.ehlo()
		server.login(user, passwd)
		server.ehlo()
		server.sendmail(self.fromaddr, toaddr, text)
		server.quit()
		print "[%s] %s%s%s send email to %s" % (ID, OKGREEN, fromaddr, ENDC, toaddr)
	except:
		print """[%s] THERE WAS A %sPROBLEM%s FOR %s%s%s TO SEND MAIL TO %s""" % (ID, FAIL, ENDC, FAIL, fromaddr, ENDC, toaddr)

def main(toaddr):
	try:
		for i in xrange(len(S.email_accounts)):
			A = S.email_accounts[i]

			# stop if settings are the default ones
			if A['email_address'] == default['email_address']:
				print "%sPlease read instructions before using this tool!%s"%(FAIL,ENDC)
				print "%sYou need to setup senders.py first!%s\n\n"%(FAIL,ENDC)
				sys.exit()	
			else:
				test_email(i, A['SSL'], A['email_address'], A['email_provider'], A['port'], A['username'], A['password'], toaddr)
	
	except  KeyboardInterrupt:
		sys.exit()
	except:
		print sys.exc_info()[0];


if __name__ == "__main__":

	printBanner()
	
	if len(sys.argv)<=1:
		print "%sPlease set an email address to send our test to!%s"%(FAIL,ENDC)
		print usage
	else:
		toaddr = sys.argv[1]
		main(toaddr)
