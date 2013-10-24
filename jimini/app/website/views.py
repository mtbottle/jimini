# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import get_object_or_404, render_to_response

# import models
from models import Order, Origami, OrigamiImage, RecipientShippingForm

# use a hash library to generate email
import hashlib




def splash_page(request):
	''' This will return the splash page for index '''
	origamis = Origami.objects.all()
	return render_to_response('index.html',{'origamis': origamis},
                               context_instance=RequestContext(request))

def choose_origami(request):
    ''' This returns the page where the user picks a design '''
    origamis = Origami.objects.all()
    return render_to_response('choose_origami.html',{'origamis':origamis},
                                context_instance=RequestContext(request))


def choose_recipient(request, origami_id):
	'''This returns a form where the user picks a recipient
	and provides shipping information.'''

	origami = Origami.objects.get(id=origami_id)

	if request.method == "POST":
		form = RecipientShippingForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			recipient_name = form.cleaned_data['recipient_name']
			message = form.cleaned_data['message']
			ship_to_name = form.cleaned_data['ship_to_name']
			ship_to_address = form.cleaned_data['ship_to_address']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zip_code = form.cleaned_data['zip_code']
			#generate order object with order_id
			#send use responses to db
			### order = Order(user_id='', origami_id='', recipient_name='', 
			###              message='', ship_to_name='', ship_to_address='', city='', state='', zip_code='')
			return render_to_response('payment.html', {'order':order}, context_instance=RequestContext(request))
	else:
		form = RecipientShippingForm() # An unbound form

	return render_to_response('choose_recipient.html', {'form':form,'origami':origami,},
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
    
	return render_to_response('index.html',{"user": user},
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

