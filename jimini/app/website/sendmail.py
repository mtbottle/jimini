from email.mime.text import MIMEText
import smtplib, imaplib
import email
from subprocess import Popen, PIPE
from jinja2 import Environment, FileSystemLoader
import os

app_dir = os.path.dirname(__file__) # get current directory 

template_dir = os.path.join(app_dir, '../../../templates/email_templates')
loader = FileSystemLoader(template_dir)
env = Environment(loader=loader)

username = 'bfortuner' #'cricket@jimini.co'
password = 'brendan90' #'Cricket@SW2012'
template = env.get_template('order_confirm.html')
html = template.render()
email_from = 'bfortuner@gmail.com'
email_to = 'bfortuner@gmail.com'
subject = "Your Jimini Order!"



def send_jimini_email(email_from, email_to, subject, html):
	''' Primary email sending function that takes in pre-generated HTML, sender and recipient, and subject'''
	msg = MIMEText(html, 'html')
	msg["From"] = email_from
	msg["To"] = email_to
	msg["Subject"] = subject


 	server = smtplib.SMTP("smtp.gmail.com", 587)
        #server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(email_from, email_to, msg.as_string())
        #print "sent email to %s" % toaddrs
        server.quit()	


	# open process to start sending email via sendmail
	# p = Popen(['/usr/sbin/sendmail', '-t'], stdin=PIPE)
	# p.communicate(msg.as_string())





def connect_email_server():
	''' Helper function that connects to email server '''
	server = imaplib.IMAP4_SSL("imap.gmail.com", port = 993)
	server.login(username, password)
	return server



def show_inbox():

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
	typ, msg_ids = server.search(None, "(SUBJECT 'hey')")

	# Get list of message ids FROM "bfortuner@gmail.com" with "hey" in the SUBJECT
	msg_ids = server.search(None, "(FROM 'bfortuner@gmail.com' SUBJECT 'hey')")
	message_list = msg_ids[1][0].split()
	print message_list


	# Loop through message id list and extract data
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



		


	# Logout
	server.close()
	server.logout()



if __name__ == '__main__':
	show_inbox()
#send_jimini_email(email_from, email_to, subject, html)

