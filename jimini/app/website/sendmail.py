from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def send_jemini_email(email_from, recipient, subject, content):
	msg = MIMEText(content)
	msg["From"] = email_from
	msg["To"] = recipient
	msg["Subject"] = subject

	# open process to start sending email via sendmail
	p = Popen(['/usr/sbin/sendmail', '-t'], stdin=PIPE)
	p.communicate(msg.as_string())

if __name__ == '__main__':
	send_jemini_email('jimini.origami@gmail.com', \
		'mtsyne@gmail.com', \
		'Your Jimini Order', \
		'This is the content')