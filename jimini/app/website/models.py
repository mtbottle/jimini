from django.db import models

# Create your models here.
class Order(model.Model):
	''' Contains info for order '''
	user_email = models.CharField(max_length=100)
	generated_email = models.CharField(max_length=100)
	order_email_content = models.TextField()
	parsed_order_link = models.TextField()
	parsed_personal_content = models.TextField()
	gemini_website_url = models.CharField()
