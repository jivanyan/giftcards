# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from giftcard.models import *
from merchant.models import *
def giftcards(request):
	context = RequestContext(request)
	c = GiftCardCategory.objects.all()
	g = GiftCardPlan.objects.all()
	m = Merchant.objects.all()
	for merchant in m:
		merchant.url = merchant.name.replace(' ','_')	
	context_dict = {'categories' : c,
			'giftcards' : g,
			'merchants' : m
			}
	return render_to_response("giftcard/giftcards_base.html", context_dict, context)

def sell_giftcard(request):
        context = RequestContext(request)
        context_dict = {}
        return render_to_response("giftcard/giftcards_base.html", context_dict, context)
                                                                                    
