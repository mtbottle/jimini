from email.mime.text import MIMEText

import smtplib, imaplib
import email
from subprocess import Popen, PIPE
from jinja2 import Environment, FileSystemLoader
import sys, os
import re
import sendmail

app_dir = os.path.dirname(__file__) # get current directory 

''' Need help here - import existing Django models '''
#sys.path.append("/Users/bfortuner/workplace/jimini/jimini/jimini")
#os.environ["DJANGO_SETTINGS_MODULE"] = settings
#from models import Order, Origami, OrigamiImage, RecipientShippingForm


# Load Jinja email templates
template_dir = os.path.join(app_dir, '../../../templates/email_templates')
loader = FileSystemLoader(template_dir)
env = Environment(loader=loader)


# Temporary login info for personal gmail account
username = 'bfortuner' #'cricket@jimini.co'
password = 'brendan90' #'Cricket@SW2012'


# Temporary overrides for testing
email_from = 'bfortuner@gmail.com'
email_to = 'bfortuner@gmail.com'
subject = "Your Jimini Order!"



def connect_email_server():
	''' Helper function that connects to email server '''
	server = imaplib.IMAP4_SSL("imap.gmail.com", port = 993)
	server.login(username, password)
	print "connected!"
	return server



def forward_email(msg, to_email):
	''' Forward gift email received from Amazon or Google'''
	for part in msg.walk():
		if part.get_content_type() == 'text/html':
			body = part.get_payload(decode=True)

	sendmail.send_jimini_email('confirmation@jimini.co', to_email, 'Your Amazon Gift From Jimini', body)


			
def check_inbox(server):
	''' Check inbox for new Jimini orders '''

	# Select "INBOX" mailbox
	typ, data = server.select("INBOX")

	# Search for emails [from/to] [@jimini.co] domain name
	email_list = []
	msg_ids = server.search(None, "(FROM '@jimini.co' UNSEEN)")
	message_list = msg_ids[1][0].split()
	for message in message_list:
		typ, msg_data = server.fetch(message, '(RFC822)')
		for response_part in msg_data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
       				email_list.append(msg)
	return email_list



######  Need help connecting to models.py to finalize this function  ######	

def extract_order_code(email_list):
	'''Extract order codes from list of emails'''
	# Check is list is empty
	print 'searching for message'
	if len(email_list) > 0:
		for msg in email_list:
			msg['to'] == 'smelly-socks@jimini.com'
			email_code = re.search(r'<([A-Za-z0-9-]+)@', msg['to']).group(1)

			order = Order.objects.get(order_code=email_code)
			print order
			print 'found message'

			# check if code is in DB
			if order != None:
				# Update order status to 'gift received'
				# order.order_status = 'paid'
				# order.save()
				
				# Send gift received email! 
				first_name = 'Brendan'
				email_to = 'bfortuner@gmail.com'
				# order.gift_received_email(first_name, email_to)
				sendmail.send_jimini_email('confirmation@jimini.co', email_to, 'Jimini received your digital gift', 'hey there %s for order %s' % (email_code, order))
				
				# Forward Amazon Gift Email
				forward_email(msg, email_to)

			else:
				print 'order is None'

 	# Logout
	server.close()
	server.logout()




if __name__ == '__main__':
	server = connect_email_server()
	extract_order_code(check_inbox(server))





#### Example Functions from IMAPlib ####

def IMAP_example_fuctions():
	# Open the connection
	server = connect_email_server()
	print "connected!"

	# Shows you the name of all the mailboxes
	# print server.list()
	
	# Select "INBOX" mailbox
	typ, data = server.select("INBOX")

	# Get number of messages in mailbox
	# num_msgs = int(data[0])


	# Get list of message ids in inbox
	# typ, msg_ids = server.search(None,"ALL")

	# Get list of message ids for messages with "hey" in the title
	#typ, msg_ids = server.search(None, "(SUBJECT 'hey')")

	# Get list of message ids FROM "bfortuner@gmail.com" with "hey" in the SUBJECT
	#msg_ids = server.search(None, "(FROM 'bfortuner@gmail.com' SUBJECT 'hey')")
	#message_list = msg_ids[1][0].split()
	#print message_list

	# Loop through message id list and extract data
	'''
	for message in message_list:

		# Extract HEADERS - FROM, SENT WHEN, SUBJECT, TO, etc.
		# msg_data = server.fetch(message, '(BODY.PEEK[HEADER] FLAGS)')

		# Extract BODY text from email
		#msg_data = server.fetch(message, '(BODY.PEEK[TEXT])')
		
		# Extract message FLAGS
		#msg_data = server.fetch(message, '(FLAGS)')

		# Print clean display of subject, to, and from
		typ, msg_data = server.fetch(message, '(RFC822)')
		for response_part in msg_data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
				for header in [ 'subject', 'to', 'from' ]:
					print '%-8s: %s' % (header.upper(), msg[header])
					'''


