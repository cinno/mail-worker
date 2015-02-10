#!/usr/bin/python
#
#	FILENAME : senders.py
#
#	This file is used by mailWorker.py script.
#
#
#############################################
#											#
#		 EMAIL ACCOUNT CONFIGURATION		#
#											#
#############################################
#
#
#   email_accounts = [
#		{
#			'email_address': 'John@gmail.com',
#			'username': 'John@gmail.com',
#			'password': 'John123',
#			'email_provider':'gmail.com',
#			'port': None,
#			'SSL': True
#		},
#		{
#			'email_address': 'John@openmailbox.com',
#			'username': 'John@openmailbox.com',
#			'password': 'John123',
#			'email_provider':'openmailbox.org',
#			'port': 587,
#			'SSL': False
#		},
#		{
#			'email_address': '...',
#			...
#		}
#	]
#
#
#	1. Fill Variables:
#		email_address  -> your email address
#		username       -> the username you use to login, John@gmail.com or John - try both if not sure
#		password       -> your password
#		email_provider -> if you use gmail it would be gmail.com 
#		port           -> Don't need in most cases. If you don't know what is this use None
#		SSL	           -> If your email Provider supports it consider to set it to True. If you don't 
#			              know try first True otherwise False.
#
#	2. Your Email provider should allow you to connect using SMTP Protocol.
#		You can find it by serching your webmail's settings or search over the Internet
#
#	3. Don't forget you can add as many accounts as you like. Just keep the same form
#
#############################################################################################################

email_accounts = [
	{
		'email_address': 'example@example.com',
		'username': 'example@example.com',
		'password': '123456',
		'email_provider':'example.com',
		'port': None,
		'SSL': True,
	}
]
