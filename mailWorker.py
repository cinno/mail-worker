#!/usr/bin/python
import time, random, sys, os
import threading
import Queue
import datetime
import optparse

sys.path.insert(0,'modules')
import senders as S
import worker as E
FILENAME = "receivers.txt"



#	Colors
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

default={
	'email_address': 'John@gmail.com',
	'username': 'John@gmail.com',
	'password': 'John123',
	'email_provider':'gmail.com',
	'port': None,
	'SSL': True
}
Mail={
	"SUBJECT" : ".", 
	"FORMAT"  : "plain",
	"CONTENT" : ""
}

# setup command line arguments
parser = optparse.OptionParser()
parser.add_option('-e', '--email', dest='content', help='Content of email')
parser.add_option('-f', '--file', dest='filename', help='List of email addresses')
parser.add_option('-s', '--subject', dest='subject', help='Subject of email')
parser.add_option('-F', '--format', dest='form', help='Format of email: "plain" or "html"')

#
#	print banner
#
def printBanner():
	os.system("clear")
	print '\n    '.join(BANNER.split('\n'))
	print """%s    %s \n    MAIL WORKER
    __________________________________________________________________%s"""%(GRAY, datetime.date.today(), ENDC)

#
#	main
#
def main():
	print "\nPlease be patient, this is gonna take a while!"
	
	# fill queue with email addresses from the given file
	queue = Queue.Queue(0)
	for email in open(FILENAME, "r").readlines():
		if "@" in email:
			queue.put( ( Mail ,email.strip(), random.randint(10, 20)/1.0) )

	# use accounts from settings
	# and make a worker for each account 
	for i in xrange(len(S.email_accounts)): 
		A = S.email_accounts[i]
		
		# stop if settings are the default ones
		if A['email_address'] == default['email_address']:
			print "\n\n\t%sPlease read instructions before using this tool!%s\n\n"%(FAIL,ENDC)
			sys.exit()
			
		else:
			E.Emailer(i, A['SSL'], A['email_address'], A['email_provider'], A['port'], A['username'], A['password'], queue).start()
			# add an empty entry for each worker
			# to exit when there is no more 
			#entries in the queue.
			queue.put( None )
			print "[%s] %s%s%s is ready" % (i, OKGREEN, A['email_address'], ENDC)



#
#	command line arguements
#
def set_argvs():
	global FILENAME
	(opts, args) = parser.parse_args()
	
	# important arguments
	if opts.content != None:
		CONTENT = opts.content
	else:
		print "\n%s-e or --email IS MISSING!%s\ntype -h or --help to list possible arguements\n"%(FAIL, ENDC)
		sys.exit()

	if opts.filename != None:
		FILENAME = opts.filename
		if os.path.exists(FILENAME)==False:
			print "\n%sThe file you specified couldn't be found!%s\nPlease specify a correct one\n"%(FAIL, ENDC)
			sys.exit()
	else:
		if os.path.exists(os.getcwd()+"/"+FILENAME)==False:
			print "\n%sThe default \"receivers.txt\" file couldn't be found!%s\nPlease specify a one usinf -f or --file\n"%(FAIL, ENDC)
			sys.exit()

	# secondary arguements
	if opts.form != None:
		Mail['FORMAT']=opts.form
	if opts.subject != None:
		Mail['SUBJECT']=opts.subject
		
	


if __name__ == "__main__":
	printBanner()
	set_argvs()
	main()

