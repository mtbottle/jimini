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



def choose_origami(request, origami_id=None, order_id=None):
    ''' This returns the page where the user picks a design '''
    origamis = Origami.objects.all()
    return render_to_response('choose_origami.html',{'origamis':origamis, 'origami_id':origami_id, 'order_id':order_id},
                                context_instance=RequestContext(request))



def choose_recipient(request, origami_id, order_id=None):
	'''This returns a form where the user picks a recipient
	and provides shipping information.'''
	origami = Origami.objects.get(id=origami_id)
	
	# if the user backtracked and already has an order_id...
	if order_id != None:
		order = Order.objects.get(id=order_id)
		
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
			ship_to_name = form.cleaned_data['ship_to_name']
			ship_to_address = form.cleaned_data['ship_to_address']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zip_code = str(form.cleaned_data['zip_code'])
			
			# If the user is submitting the form for the first time, add the data to the db
			if order_id == None:
				order = Order(origami_id=origami_id, order_status='pre-payment', email_code=gen_email_code(), 
					      recipient_name=recipient_name, sender_name=sender_name, message=message, ship_to_name=ship_to_name, 
					      ship_to_address=ship_to_address, city=city, state=state, zip_code=zip_code)
				order.save()

			# otherwise update the data in the db
			else:
				order.recipient_name = recipient_name
				order.sender_name = sender_name
				order.message = message
				order.ship_to_name = ship_to_name
				order.ship_to_address = ship_to_address
				order.city = city
				order.state = state
				order.zip_code = zip_code
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

	return render_to_response('choose_recipient.html', {'form':form,'origami':origami,'order_id':order_id, 'origami_id':origami_id},
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
		return render_to_response('payment.html',{'origami' : origami, 'order':order},
                               context_instance=RequestContext(request))



def confirmation(request, order_id):
	'''This returns the order confirmation page with email code'''
	order = Order.objects.get(id=order_id) 
	origami = Origami.objects.get(id=order.origami_id)
	# user = User.objects.get(id=order.user_id)
	
	# Change order_status to 'paid'
	order.order_status = 'paid'
	order.save()

	# Send order confirmation email
	first_name = 'Brendan' #user.first_name
	email_to = 'bfortuner@gmail.com' #user.email

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

