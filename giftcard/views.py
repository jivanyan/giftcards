# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from giftcard.models import *
from merchant.models import *
from django.contrib.auth.models import User

c = GiftCardCategory.objects.all()
g = GiftCardPlan.objects.all()
m = Merchant.objects.all()
for merchant in m:
                merchant.url = merchant.name.replace(' ','_')



def giftcards(request):
	context = RequestContext(request)
	
	context_dict = {'categories' : c,
			'giftcards' : g,
			'merchants' : m}
	if request.user.is_authenticated():
		print "User ID:{0}".format(request.user.id)
		user = User.objects.get(id = request.user.id)
		if hasattr(user, 'patron'):
			patron = user.patron
			account = patron.account
			context_dict['account'] = True
			context_dict['balance'] = account.balance
	return render_to_response("giftcard/giftcards_base.html", context_dict, context)

def sell_giftcard(request):
        context = RequestContext(request)
	context_dict = {'categories' : c,
                        'giftcards' : g,
                        'merchants' : m}
        
        return render_to_response("giftcard/giftcards_base.html", context_dict, context)
                                                                                    
