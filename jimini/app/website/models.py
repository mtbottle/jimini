from django.db import models
import sendmail
from django import forms
from localflavor.us.forms import USZipCodeField, USStateField


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



class Origami(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    bullet_1 = models.CharField(max_length=255, blank=True)
    bullet_2 = models.CharField(max_length=255, blank=True)
    bullet_3 = models.CharField(max_length=255, blank=True)


    def get_pictures(self):
	    images = OrigamiImage.objects.filter(origami_id = self.id)
	    return images

    #youtube_video_id = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title
        



class OrigamiImage(models.Model):
	origami_id = models.ForeignKey(Origami)
	picture = models.ImageField(upload_to="origami/pictures/")



	
class RecipientShippingForm(forms.Form):
	recipient_name = forms.CharField(label='Recipient name', max_length=150)
	message = forms.CharField(label='Message (optional)')
	
	ship_to_name = forms.CharField(label='Ship-to name')
	ship_to_address = forms.CharField(label='Address')
	city = forms.CharField(max_length=100, label='City')
	state = USStateField()
	zip_code = USZipCodeField()
