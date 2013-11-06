from email.mime.text import MIMEText
import smtplib, imaplib
import email
from subprocess import Popen, PIPE
from jinja2 import Environment, FileSystemLoader
import os
import re

app_dir = os.path.dirname(__file__) # get current directory 


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



def send_jimini_email(email_from, email_to, subject, html):
	''' Primary email sending function that takes in pre-generated 
	    HTML, sender, recipient, and subject'''

	# Generate email header
	msg = MIMEText(html, 'html')
	msg["From"] = email_from
	msg["To"] = email_to
	msg["Subject"] = subject

	
	# Connect to server
 	server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(email_from, email_to, msg.as_string())

	# Exit server
        server.quit()	


if __name__ == '__main__':
	pass
#send_jimini_email(email_from, email_to, subject, html)

