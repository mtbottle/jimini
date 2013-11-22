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
#username = 'bfortuner' #'cricket@jimini.co'
#password = 'brendan90' #'Cricket@SW2012'
username = 'cricket@jimini.co'
password = 'Cricket@SW2012'

# Temporary overrides for testing
#email_from = 'cricket@jimini.co'
#email_to = 'bfortuner@gmail.com'
#subject = "Your Jimini Order!"
#html = "hey man whats up"


def send_jimini_email(from_email, to_email, subject, html):
	''' Primary email sending function that takes in pre-generated 
	    HTML, sender, recipient, and subject'''

	# Generate email header
	msg = MIMEText(html, 'html')
	msg["From"] = from_email
	msg["To"] = to_email
	msg["Subject"] = subject

	
	# Connect to server
 	# server = smtplib.SMTP("smtp.gmail.com", 587)
        server = smtplib.SMTP("smtp.jimini.co", 587)
	server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_email, msg.as_string())

	# Exit server
        server.quit()	


if __name__ == '__main__':
	send_jimini_email('bfortuner@gmail.com', 'cricket@jimini.co', 'hey there hot dog', 'sup')

