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
from giftcard.forms import *
from decimal import Decimal


@login_required
def homepage(request):
	context = RequestContext(request)
	context_dict = {}
	user = get_object_or_404(User, id = request.user.id)
	
	if not hasattr(user,'merchant'):
		raise Http404
	else:
		merchant = user.merchant
	context_dict['code'] = "" 
	if request.method == "POST":
		code = request.POST['card[code]']  
		context_dict['code'] = code
		try:
			giftcard = GiftCard.objects.get(code = code)
			if not giftcard.valid:
				context_dict['message'] = 'Invalid Card'
			elif not giftcard.paid:
				context_dict['message'] = 'Not Paid Card'
			selfcard = giftcard.plan.giftcardplan_merchants.filter(merchant = merchant)
			if not selfcard:
                                context_dict['message'] = "Card belongs to the merchant %s" % (giftcard.plan.merchant.name)
			else:
				context_dict['giftcard'] = giftcard

			if 'card[redeem]' in request.POST:
				charge = Decimal(request.POST['card[redeem]'])
				if charge > giftcard.remainder:
					context_dict['message1'] = "The value should not exceed the giftcard's remainder %s" % (giftcard.remainder)  
				else:
					giftcard.remainder = giftcard.remainder - charge
					giftcard.save("REDEEMED", user, charge)
					#TODO create a request object to get the money from the cite!
					context_dict = {'giftcard':giftcard, 'message1':"Successfully charged! Charged Value: %s" % (charge)}
					
								
		except GiftCard.DoesNotExist:
			context_dict['message'] = "Invalid Code"

	return render_to_response('merchant/merchant_home_base.html', context_dict, context)
		
	
def gift_card_plans(request):
	context = RequestContext(request)	
	context_dict = {}
	m = request.user.merchant
	plans = GiftCardPlan.objects.filter(giftcardplan_merchants__merchant = m)
	context_dict['plans'] = plans
	return render_to_response('merchant/merchant_gift_card_plans.html', context_dict, context)


def new_fixed_gift_card_plan(request):
	context = RequestContext(request)
	context_dict = {}
	merchant = request.user.merchant
	if request.method == 'POST':
		form = GiftCardFixedPlanForm(data = request.POST)
		if form.is_valid():
			plan = form.save(commit = False)
			plan.exp_time = datetime.datetime.now() 
                        plan.save()
			relationship = MerchantGiftCardPlanRelationship(merchant = merchant, giftcardplan = plan)
			relationship.save()
			plan.name, plan.website = merchant.name, merchant.website			
					                       
                        if 'logo' in request.FILES:
                                plan.logo = request.FILES['logo']
                        plan.save()
                        return HttpResponseRedirect(reverse('merchant_gift_card_plans'))

		else:
			return HttpResponse(form.errors)
	else:
		form = GiftCardFixedPlanForm()
		context_dict['form'] = form		
        return render_to_response('merchant/merchant_new_gift_card_plan.html', context_dict, context)


def sold_gift_cards(request):
	context = RequestContext(request)
	context_dict = {}
        return render_to_response('merchant/merchant_sold_gift_cards.html', context_dict, context)

def merchant_view(request, merchant_name_url):
	context = RequestContext(request)
	merchant_name = merchant_name_url.replace('_', ' ')
	context_dict = {}
	try:
		user = User.objects.get(username = merchant_name)
		m = user.merchant
		context_dict['merchant'] = m
		plans = GiftCardPlan.objects.filter(giftcardplan_merchants__merchant = m)
		merchants = Merchant.objects.all()
		for m in merchants:
			m.url = m.user.username.replace(' ', '_')
		context_dict['merchants'] = merchants
		context_dict['giftcard_plans'] = plans
	except Merchant.DoesNotExist:
		raise Http404
	return render_to_response('merchant/merchant_view.html', context_dict, context)
			
