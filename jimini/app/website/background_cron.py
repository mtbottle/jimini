from email.mime.text import message_from_string
from models import Order
from order_url_matchers import get_url
import poplib
import re

def parse_emails(pop3_domain, conn_user, password):
	''' Given a domain, user and password, parse all the emails in the domain
		and return the email objects as a list
		TODO : we should probably have the password encrypted at least '''
	pop_conn = poplib.POP3_SSL(pop3_domain)
	pop_conn.user(conn_user)
	pop_conn.pass_(password)

	# Get messages from server:
	num_messages = len(pop_conn.list()[1]

	# parse the message from emails, then remove the email from server
	messages = []
	for i in range(1, len(pop_conn.list()[1]) + 1):
		message = message_from_string('\n'.join(pop_conn.retr(i)[1]))
		messages.append(message)
		pop_conn.dele(i)
		
	pop_conn.quit()
	return messages

def generate_order_object(msg):
	''' Given a email.message object, convert it into out database object
		model type. Save the object in the database and send an email that
		gives the user the link to the printing information for the order.

		Since the user was instructed to send the email to our generated
		email, need to look at that up in the database, and send an email to
		the user with the order link info stuff. '''
		
	# check to see if msg has an order match
	order_url = order_url_matchers.get_url(msg)
	if not order_url:
		return

	# the generated email is "to"
	recipient = msg['to']
	order_obj = Order.objects.get(generated_email = recipient)
	user = order_obj.user_email
	assert(user) # make sure that we don't have a null user

	# create email and send it to user
	order_obj.send_email()

	# set the rest of the fields in the object and save it.
	# TODO: other fields? personal content?
	order_obj.parsed_order_link = order_url
	order_obj.save()
	

if __name__ == '__main__':
	''' The script-y part of the code that opens the pop3 protocol and gets
		the mail and parses it. '''
	email_messages = parse_emails('jiminico.domain.com', 'cricket@jimini.co', 'Cricket@SW2012')
	for email in email_messages:
		generate_order_object(email)