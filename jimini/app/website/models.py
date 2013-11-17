from django.db import models
import sendmail
from django import forms
from localflavor.us.forms import USZipCodeField, USStateField
from jinja2 import Environment, FileSystemLoader
import os

# Set up email templates directory
app_dir = os.path.dirname(__file__) # get current directory                                                                                                                       
template_dir = os.path.join(app_dir, '../../../templates/email_templates')
loader = FileSystemLoader(template_dir)
env = Environment(loader=loader)



# This is the old order model which we're not using (but may take elements from later)
class OLD_Order(models.Model):
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



class Origami(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bullet_1 = models.CharField(max_length=255, blank=True)
    bullet_2 = models.CharField(max_length=255, blank=True)
    bullet_3 = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add = True)

    def get_pictures(self):
	    images = OrigamiImage.objects.filter(origami_id = self.id)
	    return images

    #youtube_video_id = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title
        



class OrigamiImage(models.Model):
	origami_id = models.ForeignKey(Origami)
	picture = models.ImageField(upload_to="origami/pictures/")



# This is the form model for the "choose_recipient" page	
class RecipientShippingForm(forms.Form):
	recipient_name = forms.CharField(label='Recipient name', max_length=150)
	sender_name = forms.CharField(label='Sender name', max_length=150, required=False)
	message = forms.CharField(widget=forms.Textarea(attrs={'cols':40,'rows':5}), label='Message (optional)', required=False)
	
	ship_to_name = forms.CharField(label='Ship-to name')
	ship_to_address = forms.CharField(label='Address')
	city = forms.CharField(max_length=100, label='City')
	state = USStateField()
	zip_code = USZipCodeField()
	

# This is the order model which takes an origami entries from the RecipientShipping form 
class Order(models.Model):
	user_id = 1
	amazonOrderReferenceId = models.CharField(max_length=100)
	order_date = models.DateTimeField(auto_now_add = True)
	order_status = models.CharField(max_length=100)
	email_code = models.CharField(max_length=100)

	origami_id = models.PositiveIntegerField()

	recipient_name = models.CharField(max_length=150)
	sender_name = models.CharField(max_length=150, blank=True)
	message = models.TextField(blank=True, max_length=500)
	
	ship_to_name = models.CharField(max_length=150)
	ship_to_address = models.CharField(max_length=200)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=20)


	def confirmation_email(self, first_name, email_to, origami_price, origami_title):
		template = env.get_template('order_confirm.html')
		html = template.render(first_name=first_name, email_code=self.email_code, origami_price=origami_price, origami_title=origami_title)
		email_from = 'confirmation@jimini.co'
		subject = "Your Jimini Order!"

		sendmail.send_jimini_email(email_from, email_to, subject, html)


	def gift_received_email(self, first_name, email_to):
		template = env.get_template('digital_gift_received.html')
		html = template.render(first_name=first_name)
		email_from = 'confirmation@jimini.co'
		subject = "We Received Your Digital Gift!"

		sendmail.send_jimini_email(email_from, email_to, subject, html)


	def origami_shipped_email(self):
		template = env.get_template('origami_shipped.html')
		html = template.render(first_name=first_name)
		email_from = 'confirmation@jimini.co'
		subject = "Your Jimini Order Has Shipped!"

		sendmail.send_jimini_email(email_from, email_to, subject, html)

