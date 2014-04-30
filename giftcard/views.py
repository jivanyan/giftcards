# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from giftcard.models import *
from giftcard.forms import *
from merchant.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.conf import settings
from decimal import Decimal  
import math
def giftcards(request):
	context = RequestContext(request)
	c = GiftCardCategory.objects.all()
	g = GiftCardPlan.objects.all()
	m = Merchant.objects.all()
	for merchant in m:
                merchant.url = merchant.user.username.replace(' ','_')


	context_dict = {'categories' : c,
			'giftcards' : g,
			'merchants' : m}
	if request.user.is_authenticated():
		user = User.objects.get(id = request.user.id)
		if hasattr(user, 'patron'):
			patron = user.patron
			account = patron.account
			context_dict['account'] = True
			context_dict['balance'] = account.balance
	giftcard_plans = GiftCardPlan.objects.all()
	context_dict['plans'] = giftcard_plans

	return render_to_response("giftcard/giftcards_base.html", context_dict, context)


def gift_card_view(request,plan_id):
	context = RequestContext(request)
	context_dict = {}
	try:
		giftcardplan = GiftCardPlan.objects.get(id = plan_id)
		merchants = giftcardplan.merchants
		if merchants.count() == 1:			
			m = merchants.all()[0]
			context_dict['merchant']=m
			context_dict['merchant_other_plans'] = GiftCardPlan.objects.filter(giftcardplan_merchants__merchant = m).exclude(id = plan_id) 
		else:
			context_dict['merchants'] = merchants
		related_plans = related_gift_card_plans(giftcardplan)
		
		context_dict['giftcardplan'] = giftcardplan
		context_dict['related_plans'] = related_plans
		
	except GiftCardPlan.DoesNotExist:
		raise Http404
	
	return render_to_response("giftcard/gift_card_view.html", context_dict, context)
	
@login_required
def buy_gift_card(request, plan_id):
	context = RequestContext(request)
	user = request.user
	if not hasattr(user, 'patron'):
		return render_to_response('login.html',{'message':"Please Log In by Patron Account"}, context)	

	context_dict = {}
	giftcardplan = get_object_or_404(GiftCardPlan, id = plan_id)
	merchants = giftcardplan.merchants
        context_dict['merchants'] = merchants
        context_dict['plan_id'] = plan_id
	
	if request.method == "POST":
		giftcard = GiftCard()
		giftcard.message = request.POST["gift[message]"]
		giftcard.send_to = request.POST["gift[send_to]"]
		
		if giftcardplan.price == 0:
			if "gift[amount]" in request.POST:
				giftcard.remainder = Decimal(request.POST["gift[amount]"])
			else:
				raise Exception("There is no gift[amount] field in the post request. Something wrong!")
		else:
			giftcard.remainder = giftcardplan.value

		giftcard.plan = giftcardplan
		giftcard.buyer = user
		giftcard.generate_code()
		if giftcard.send_to:
			pass
			#giftcard.send_to_recipient()
		giftcard.save()
		user.patron.pay_for_giftcard(giftcard)

		return HttpResponseRedirect(reverse('patron_sent_giftcards'))

	else:	
		if giftcardplan.price != 0:
			context_dict['fixed'] = giftcardplan.price
			context_dict['plan'] = giftcardplan

        return render_to_response("giftcard/buy_gift_card.html", context_dict, context)

	


@login_required
def sell_giftcard(request):
        context = RequestContext(request)
	context_dict = {}        
	
	if not hasattr(request.user, 'patron'):
                return render_to_response('login.html',{'message':"Please Log In by Patron Account"}, context)

	if request.method == "POST":
		c = request.POST["card[code]"]
		patron = request.user.patron
		giftcard = get_object_or_404(GiftCard, code = c)
		
		if not giftcard.paid:
			error = "Gift Card is not paid!!!"
                        context_dict['error'] = error
		elif giftcard.valid:
			cashback = (cash_back_return_amount(giftcard) * cash_back_return_percent(giftcard))
			with transaction.commit_on_success():
				giftcard.deactivate("SOLD", request.user, cashback)			
				patron.debit_account(cashback) 	
			
			return HttpResponseRedirect(reverse('patron_sold_giftcards'))
		else:
			error = "Gift Card is not valid!!!"
			context_dict['error'] = error
	
	
        return render_to_response("giftcard/sell_giftcards.html", context_dict, context)
                                                                                    




def cash_back_return_percent(giftcard):
	"""
	This function returns the cashback percent for the given giftcard. 
	The returned value should depends on the expiration time of the giftcard , can also depends on the remainder
	Now we simply return the constant value specified in settings
	"""	
	c =  settings.GIFT_CARD_SELL_BACK_RETURN_PERCENT / Decimal(100)
	return c 

def cash_back_return_amount(giftcard):
        """
        This function returns the giftcard remainder which is subject to return back at selling. 
        The returned value should depends on the expiration time of the giftcard , can also dpends on the remainder
        Now we simply return the constant value specified in settings
        """
	plan = giftcard.plan
	if plan.price == 0 or plan.price == plan.value:
		c =  Decimal(giftcard.remainder)
	else:
		c = Decimal(math.floor(Decimal(giftcard.remainder) * Decimal(plan.price / Decimal(plan.value))))
	return c



def related_gift_card_plans(plan):
        return GiftCardPlan.objects.all()

def filter_gift_card_plans(query):
        return GiftCardPlan.objects.filter(giftcardplan_merchants__merchant__name__startswith = query)



def search_gift_card_plans(request):
        context = RequestContext(request)
        plans = []
        query = ''
        if request.method == 'GET':
                query = request.GET['query']
        plans = filter_gift_card_plans(query)
        return render_to_response('giftcard/giftcards_list_as_a_table.html',{'plans':plans}, context)


