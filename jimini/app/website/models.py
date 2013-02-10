from django.db import models
import sendmail

# Create your models here.
class Order(models.Model):
	''' Contains info for order '''
	user_email = models.CharField(max_length=100)
	generated_email = models.CharField(max_length=100)
	order_email_content = models.TextField()
	parsed_order_link = models.TextField()
	parsed_personal_content = models.TextField()
	jimini_order_link = models.CharField(max_length=100)

	def send_email(self):
		''' Function that takes the order object and sends an email with the
			content of the order. This is tightly coupled with the model, so
			that's why the function is here! '''
		from_address = 'cricket@jimini.co'
		to_address = user_email
		subject = 'Your Origami is ready to print!'
		body = 'Find your origami here: ' + jimini_order_link
		
		sendmail.send_jemini_email(fromMail, userMail, subject , body)