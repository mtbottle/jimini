# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response


def splash_page(request):
	''' This will return the splash page for index '''
	return render_to_response('index.html',{},
                               context_instance=RequestContext(request))

def how_this_works(request):
	return render_to_response('how_it_works.html', {})

def wrap_page(request,coupon):
	''' This will return the wrap your gift page '''
	return render_to_response('wrap.html',{'coupon' : coupon},
                               context_instance=RequestContext(request))

def coupon_redirect(request,coupon):
	''' This will redirect to amazon with the right coupon code '''
	return render_to_response('redirect.html',{'coupon' : coupon},
                               context_instance=RequestContext(request))
