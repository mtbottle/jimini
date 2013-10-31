from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from jinja2 import Environment, FileSystemLoader
import os

app_dir = os.path.dirname(__file__) # get current directory 

template_dir = os.path.join(app_dir, '../../../templates/email_templates')
loader = FileSystemLoader(template_dir)
env = Environment(loader=loader)


template = env.get_template('order_confirm.html')
html = template.render()
email_from = 'confirmation@jimini.co'
email_to = 'bfortuner@gmail.com'
subject = "Your Jimini Order!"

def send_jimini_email(email_from, email_to, subject, html):
	msg = MIMEText(html, 'html')
	msg["From"] = email_from
	msg["To"] = email_to
	msg["Subject"] = subject

	# open process to start sending email via sendmail
	p = Popen(['/usr/sbin/sendmail', '-t'], stdin=PIPE)
	p.communicate(msg.as_string())


'''
if __name__ == '__main__':
	send_jimini_email(email_from, email_to, subject, html)
'''
