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
#username = 'bfortuner' #'cricket@jimini.co'                                                                                                                                                          
#password = 'brendan90' #'Cricket@SW2012'                                                                                                                                                            
username = 'cricket@jimini.co'
password = 'Cricket@SW2012'

# Temporary overrides for testing                                                                                                                                                                  
#email_from = 'cricket@jimini.co'
#email_to = 'bfortuner@gmail.com'
#subject = "Your Jimini Order!"
#html = "hey man whats up"


def connect_email_server():
	''' Helper function that connects to email server '''
	#server = imaplib.IMAP4_SSL("imap.gmail.com", port = 993)
	server = imaplib.IMAP4_SSL("imap.jimini.co", port = 993)
	server.login(username, password)
	print "connected!"
	return server



def forward_email(msg, to_email):
	''' Forward gift email received from Amazon or Google'''
	print 'forwarding...'
	for part in msg.walk():
		if part.get_content_type() == 'text/html':
			body = part.get_payload(decode=True)

	sendmail.send_jimini_email('confirmation@jimini.co', to_email, 'Your Amazon Gift From Jimini', body)



def check_inbox(server):

	# Select "INBOX" mailbox
	typ, data = server.select("INBOX")
	
	# Select unread emails sent to @jimini.co
	typ, msg_ids = server.search(None,'(TO "@jimini.co" UNSEEN)')

	# Extract message_ids into new list
	message_list = msg_ids[0].split()
	print "message list: " + str(message_list)

	email_list = []
	# Loop through message id list and extract data
	for message in message_list:
		typ, msg_data = server.fetch(message, '(RFC822)')
		for response_part in msg_data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
				email_list.append(msg)

	return email_list





if __name__ == '__main__':
	server = connect_email_server()
	check_inbox(server)
	#IMAP_example_fuctions(server)
	server.close()
        server.logout()


			
#### Example Functions from IMAPlib ####

def IMAP_example_fuctions(server):

	# Shows you the name of all the mailboxes
	print "mailboxes: " + str(server.list())
	
	# Select "INBOX" mailbox
	typ, data = server.select("INBOX")
	
	print "INBOX: " + str(data)
	# Get number of messages in mailbox
	num_msgs = int(data[0])

	print "messages in INBOX: " + str(num_msgs)

	# Get list of message ids in inbox
	#typ, msg_ids = server.search(None,"TO","@jimini.co")
	typ, msg_ids = server.search(None,'(TO "@jimini.co" UNSEEN)')

	print "Message Ids: " + str(msg_ids)
	# Get list of message ids for messages with "hey" in the title
	#typ, msg_ids = server.search(None, "(SUBJECT 'hey')")

	#print "hey" + str(typ) + str(msg_ids)
	# Get list of message ids FROM "bfortuner@gmail.com" with "hey" in the SUBJECT
	#msg_ids = server.search(None, "(FROM 'bfortuner@gmail.com' SUBJECT 'hey')")
	message_list = msg_ids[0].split()
	print "message list: " + str(message_list)

	# Loop through message id list and extract data

	for message in message_list:

		# Extract HEADERS - FROM, SENT WHEN, SUBJECT, TO, etc.
		msg_data = server.fetch(message, '(BODY.PEEK[HEADER] FLAGS)')
		#print msg_data
		# Extract BODY text from email
		msg_data = server.fetch(message, '(BODY.PEEK[TEXT])')
		#print msg_data
		# Extract message FLAGS
		msg_data = server.fetch(message, '(FLAGS)')
		#print msg_data
		# Print clean display of subject, to, and from
		typ, msg_data = server.fetch(message, '(RFC822)')
		for response_part in msg_data:
			if isinstance(response_part, tuple):
				msg = email.message_from_string(response_part[1])
				print msg
				for header in [ 'subject', 'to', 'from', 'seen' ]:
					print '%-8s: %s' % (header.upper(), msg[header])
		

