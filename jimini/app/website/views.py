# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import get_object_or_404, render_to_response, redirect

# import models
from models import Order, Origami, OrigamiImage, RecipientShippingForm

# import helpful libraries
import sendmail
import hashlib
import random
import os
from mws import MWS
import pprint
import check_mail
import re


MWS_ACCESS_KEY = "AKIAJXQZJU2XOOX326JQ"
MWS_SECRET_KEY = "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"
MWS_SELLER_ID = "A2OSAYU8Y178Y0"

mws = MWS(access_key=MWS_ACCESS_KEY,secret_key=MWS_SECRET_KEY,account_id=MWS_SELLER_ID,uri="/OffAmazonPayments/2013-01-01",version="2013-01-01")

app_dir = os.path.dirname(__file__) # get current directory



def gen_email_code():
	''' Generates random email code like green-frogs@jimini.co'''
	existing_codes = Order.objects.values_list('email_code', flat=True)
	noun_file = open(os.path.join(app_dir, '../../../static/noun_list.txt'),'r')
	words = [line.strip() for line in noun_file.readlines()]
	while True:
		code = random.choice(words) + "-" + random.choice(words)
		if code not in existing_codes:
			return code



def splash_page(request):
	''' This will return the splash page for index '''
	origamis = Origami.objects.all()
	return render_to_response('index.html',{'origamis': origamis},
							   context_instance=RequestContext(request))

def mail_cron(request):
	''' If user visits http://jimini.co/check_mail this function will run.
	It checks the jimini.co email inbox for UNREAD messages sent to: email-code@jimini.co.
	It then tries to find that email-code in our db. If it finds a match, it pulls the email address
	of the sender, forwards them the email we received from Amazon, Google, etc. with the digital gift
	receipt, and sends them a second email with a confirmation that we received their gift.'''

	# Connect to email server 
	server = check_mail.connect_email_server()
	
	# Check inbox for UNREAD messages sent to email-code@jimin.co
        email_list = check_mail.check_inbox(server)

	# If UNREAD 'code@jimini' emails found..
	if len(email_list) > 0:

		for msg in email_list:
			# Extract email-code from 'to' header
			jimini_code = re.search(r'([A-Za-z0-9]+)@', msg['to']).group(1)

			# TEMPORARY: fake email code for testing purposes
			jimini_code = 'smelly-socks'

			# Search for email-code in Orders table
			try:
				order = Order.objects.get(email_code=jimini_code)
			except:
				order = None

			# If order match found...
                        if order != None:
				# Update order status to 'gift received'                                                                                                                          
                                order.order_status = 'Gift Received'
				order.save()                                                                                                                       

				# TEMPORARY: Need to get sender's email address from Amazon
				order_id = order.amazonOrderReferenceId
				first_name = 'Brendan'
				email_to = 'bfortuner@gmail.com'
				
				# Grab origami details needed to generate email template
				origami = Origami.objects.get(id=order.origami_id)
				origami_price = origami.price
				origami_title = origami.title

				# Send gift received confirmation email to sender
				order.gift_received_email(first_name, email_to, origami_price, origami_title)

				# Forward Amazon, Google, etc. gift receipt email                                                                                                 
				check_mail.forward_email(msg, email_to)

        # Logout                                                                                                                                                                                     
        server.close()
        server.logout()

	# Render a blank page
	return render_to_response('blank.html', context_instance=RequestContext(request))



def choose_origami(request, origami_id=None, order_id=None):
	''' This returns the page where the user picks a design '''
	origamis = Origami.objects.all()
	return render_to_response('choose_origami.html',{'origamis':origamis, 'origami_id':origami_id, 'order_id':order_id},
								context_instance=RequestContext(request))



def choose_recipient(request, origami_id, order_id=None):
	'''This returns a form where the user picks a recipient
	and provides shipping information.'''
	origami = Origami.objects.get(id=origami_id)
	
	amazonOrderReferenceId = None
	if request.GET.has_key("session"): amazonOrderReferenceId = str(request.GET["session"])
	
	# if the user backtracked and already has an order_id...
	if order_id != None:
		order = Order.objects.get(id=order_id)
		amazonOrderReferenceId = order.amazonOrderReferenceId
		
		# if the user went back and chose a different origami, update the origami_id
		if order.origami_id != origami_id:
			order.origami_id = origami_id
			order.save()


	# if the user fills out the form and clicks "save and continue"
	if request.method == "POST":
		form = RecipientShippingForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			recipient_name = form.cleaned_data['recipient_name']
			sender_name = form.cleaned_data['sender_name']
			message = form.cleaned_data['message']
			ship_to_name = ""
			ship_to_address = ""
			city = ""
			state = ""
			zip_code = ""
			
			# If the user is submitting the form for the first time, add the data to the db
			if order_id == None:
				order = Order(amazonOrderReferenceId=amazonOrderReferenceId, origami_id=origami_id, order_status='pre-payment', email_code=gen_email_code(), 
						  recipient_name=recipient_name, sender_name=sender_name, message=message, ship_to_name=ship_to_name, 
						  ship_to_address=ship_to_address, city=city, state=state, zip_code=zip_code)
				order.save()

			# otherwise update the data in the db
			else:
				order.recipient_name = recipient_name
				order.sender_name = sender_name
				order.message = message
				order.save()

			params = {}
			params["OrderReferenceAttributes.OrderTotal.Amount"] = str(origami.price)
			params["OrderReferenceAttributes.OrderTotal.CurrencyCode"] = "USD"
			params["OrderReferenceAttributes.SellerNote"] = message
			params["OrderReferenceAttributes.SellerOrderAttributes.SellerOrderId"] = str(order.id)
			
			data = dict(Action='SetOrderReferenceDetails',
							SellerId=MWS_SELLER_ID,
							AmazonOrderReferenceId=str(amazonOrderReferenceId))
							
			data.update(params)
		
			mwsResponse = mws.make_request(data)
			
			pp = pprint.PrettyPrinter(depth=6)
			pp.pprint(mwsResponse.parsed)
			
			order.city = mwsResponse.parsed.OrderReferenceDetails.Destination.PhysicalDestination.City
			order.state = mwsResponse.parsed.OrderReferenceDetails.Destination.PhysicalDestination.StateOrRegion
			order.zip_code = mwsResponse.parsed.OrderReferenceDetails.Destination.PhysicalDestination.PostalCode
			order.save()
			

			# After submitting the form, send user to the payments page
			return HttpResponseRedirect('/payment.html/%s/%s' % (origami_id, order.id))

	# For a GET request where the user already has an order id, pre-populate the form with his previously filled-in values
	elif order_id != None:
		order = Order.objects.get(id=order_id) 
		data = {'recipient_name': order.recipient_name,
			'sender_name': order.sender_name,
			'message': order.message,
			'ship_to_name': order.ship_to_name,
			'ship_to_address': order.ship_to_address,
			'city': order.city,
			'state': order.state,
			'zip_code': order.zip_code}
		form = RecipientShippingForm(data) #A sort of bounded form - if user wants to edit!

	# User is visiting the page for the first time - show him the empty form
	else:
		form = RecipientShippingForm() # An unbound form

	return render_to_response('choose_recipient.html', {'form':form, 'origami':origami, 'order_id':order_id, 'origami_id':origami_id, 'amazonOrderReferenceId': amazonOrderReferenceId},
					  context_instance=RequestContext(request))



def payment(request, order_id, origami_id):

	'''This returns the checkout with Amazon page'''
	origami = Origami.objects.get(id=origami_id)
	order = Order.objects.get(id=order_id) 
	
	# This is just a placeholder until Thibaut adds payment api
	if request.method == "POST":

		# Redirect to confirmation page
		return HttpResponseRedirect('/confirmation.html/%s' % order.id)
	
	# Load page for normal GET request
	else:
		return render_to_response('payment.html',{'origami': origami, 'order': order},
							   context_instance=RequestContext(request))



def confirmation(request, order_id):
	'''This returns the order confirmation page with email code'''
	order = Order.objects.get(id=order_id) 
	origami = Origami.objects.get(id=order.origami_id)
	# user = User.objects.get(id=order.user_id)
	
	data = dict(Action='ConfirmOrderReference',
					SellerId=MWS_SELLER_ID,
					AmazonOrderReferenceId=str(order.amazonOrderReferenceId))
	
	mwsResponse = mws.make_request(data)
	
	data = dict(Action='GetOrderReferenceDetails',
					SellerId=MWS_SELLER_ID,
					AmazonOrderReferenceId=str(order.amazonOrderReferenceId))
	
	mwsResponse = mws.make_request(data)
	
	pp = pprint.PrettyPrinter(depth=6)
	pp.pprint(mwsResponse.parsed)
	
	'''
	Sample response from the call to MWS
	{'OrderReferenceDetails': {'AmazonOrderReferenceId': {'value': 'S01-9217317-8996004'},
                           'Buyer': {'Email': {'value': 'johndoe@jimini.co'},
                                     'Name': {'value': 'John Doe'},
                                     'value': '\n        '},
                           'CreationTimestamp': {'value': '2013-11-28T07:01:54.082Z'},
                           'Destination': {'DestinationType': {'value': 'Physical'},
                                           'PhysicalDestination': {'AddressLine1': {'value': "419 King's Road"},
                                                                   'City': {'value': 'Chelsea'},
                                                                   'CountryCode': {'value': 'GB'},
                                                                   'Name': {'value': 'Jane Doe'},
                                                                   'Phone': {'value': '800-000-0000'},
                                                                   'PostalCode': {'value': 'SW3 4ND'},
                                                                   'StateOrRegion': {'value': 'London'},
                                                                   'value': '\n          '},
                                           'value': '\n        '},
                           'ExpirationTimestamp': {'value': '2014-05-27T07:01:54.082Z'},
                           'OrderReferenceStatus': {'LastUpdateTimestamp': {'value': '2013-11-28T07:02:16.524Z'},
                                                    'State': {'value': 'Open'},
                                                    'value': '\n        '},
                           'OrderTotal': {'Amount': {'value': '10.00'},
                                          'CurrencyCode': {'value': 'USD'},
                                          'value': '\n        '},
                           'ReleaseEnvironment': {'value': 'Sandbox'},
                           'SellerOrderAttributes': {'SellerOrderId': {'value': '9'},
                                                     'value': '\n        '},
                           'value': '\n      '},
    'value': '\n    '}
    '''
	
	physicalDestination = mwsResponse.parsed.OrderReferenceDetails.Destination.PhysicalDestination
	buyer = mwsResponse.parsed.OrderReferenceDetails.Buyer
	
	order.ship_to_name = physicalDestination.Name
	address = physicalDestination.AddressLine1
	if (physicalDestination.has_key("AddressLine2")): address += physicalDestination.AddressLine2
	order.ship_to_address = address
	order.city = physicalDestination.City
	order.state = physicalDestination.StateOrRegion
	order.zip_code = physicalDestination.PostalCode
	order.save()
	
	# Change order_status to 'paid'
	order.order_status = 'paid'
	order.save()

	# Send order confirmation email
	first_name = buyer.Name
	email_to = buyer.Email

	origami_price = origami.price
	origami_title = origami.title
	
	order.confirmation_email(first_name, email_to, origami_price, origami_title)

	return render_to_response('confirmation.html',{'order':order},
							   context_instance=RequestContext(request))



def how_this_works(request):
	return render_to_response('how_it_works.html', {})



def wrap_page(request,coupon):
	origami = get_object_or_404(Origami, pk=1)
	''' This will return the wrap your gift page '''
	return render_to_response('wrap.html',{'coupon' : coupon},
							   context_instance=RequestContext(request))
				
				
							   
def handle_login(request):
	''' Source http://login.amazon.com/website '''
	
	import pycurl
	import urllib
	import json
	import StringIO
	
	b = StringIO.StringIO()
	
	if request.GET.has_key("access_token"):
		access_token = str(request.GET["access_token"])
		
		# verify that the access token belongs to us
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "https://api.amazon.com/auth/o2/tokeninfo?access_token=" + urllib.quote_plus(access_token))
		c.setopt(pycurl.SSL_VERIFYPEER, 1)
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		 
		c.perform()
		d = json.loads(b.getvalue())
		 
		if d['aud'] != 'amzn1.application-oa2-client.8b29ce13f5444fb783556d29ad0216e1' :
			# the access token does not belong to us
			raise BaseException("Invalid Token")
		 
		# exchange the access token for user profile
		b = StringIO.StringIO()
		 
		c = pycurl.Curl()
		c.setopt(pycurl.URL, "https://api.amazon.com/user/profile")
		c.setopt(pycurl.HTTPHEADER, ["Authorization: bearer " + access_token])
		c.setopt(pycurl.SSL_VERIFYPEER, 1)
		c.setopt(pycurl.WRITEFUNCTION, b.write)
		 
		c.perform()
		user = json.loads(b.getvalue())
		 
		print "%s %s %s"%(user['name'], user['email'], user['user_id'])
	
	return render_to_response('index.html',{"amazonUser": user},
							   context_instance=RequestContext(request))

def origamis(request):
	origamis = Origami.objects.all()
	''' This will return the wrap your gift page '''
	return render_to_response('origamis.html',{'origamis': origamis},
							   context_instance=RequestContext(request))

def coupon_redirect(request,coupon):
	''' This will redirect to amazon with the right coupon code '''
	return render_to_response('redirect.html',{'coupon' : coupon},
							   context_instance=RequestContext(request))
def user_page(request):
	''' This will return the page with the generated email and manage user '''
	
	email = request.REQUEST['email']

	m = hashlib.md5()

	
	# create a new order and put the requester's email in it
	new_order = Order(user_email = email)
	generated_id = str(new_order.id)

	m.update(generated_id)

	generated_email = m.hexdigest() + "@jimini.co"
	jimini_order_link = 'jimini.co/orders/' + m.hexdigest()

	# update database entry with the generated email and order link
	new_order.generated_email = generated_email
	new_order.jimini_order_link = jimini_order_link
	new_order.save()   ## TODO WEBSITE NOT TALKING

	print generated_email
	print jimini_order_link
	
	return render_to_response('user_page.html', {'generated_email' : generated_email})

