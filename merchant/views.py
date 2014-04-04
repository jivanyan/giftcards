# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import Http404
from merchant.models import *
from giftcard.models import *

def merchant_view(request, merchant_name_url):
	context = RequestContext(request)
	merchant_name = merchant_name_url.replace('_', ' ')
	context_dict = {}
	try:
		merchant = Merchant.objects.get(name = merchant_name)
		context_dict['merchant'] = merchant
		giftcard_plans = merchant.gift_card_plans.all()
		context_dict['giftcard_plans'] = giftcard_plans
	except Merchant.DoesNotExist:
		raise Http404
	return render_to_response('merchant/merchant_base.html', context_dict, context)
			
#@login_required
#def merchant_homepage(request):
#	return HttpResponse("Hello Merchant)

