# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import get_object_or_404, render_to_response

# import models
from models import Order, Origami, OrigamiImage

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

