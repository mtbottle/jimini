# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response


def splash_page(request):
	''' This will return the splash page for index '''
	return HttpResponse("This will be the splash page")