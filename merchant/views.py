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
		code = code.strip()
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
					transaction = merchant.register_transaction(giftcard, charge)
					request = transaction.create_payment_request()
					context_dict = {'code': code, 'message':"Successfully charged! Charged Value: %s" % (charge)}
					
								
		except GiftCard.DoesNotExist:
			context_dict['message'] = "Invalid Code"

	return render_to_response('merchant/merchant_home_base.html', context_dict, context)
		
@login_required
def delete_gift_card_plan(request):
	"""this function was intended to delete the gift card plan by the merchant. However we have implemented the deactivation/activation 
	functionality but the function name and URL has remaind unchanged/delete-gift-card-plan/
	"""	
        context = RequestContext(request)
        context_dict = {}
	user = request.user
        if not hasattr(user,'merchant'):
                raise Http404
        else:
                m = user.merchant
	if request.method == 'GET':
                planid = request.GET['id']

	plan = GiftCardPlan.objects.get(id = planid)
	if plan.is_active:
		plan.is_active = False
		plan.save()
	else:
		plan.is_active = True
		#TODO check the expiration data before activating
                plan.save()

		return HttpResponse(planid)
	return HttpResponse(0) 
        


@login_required	
def gift_card_plans(request):
	context = RequestContext(request)	
	context_dict = {}
	m = request.user.merchant
	plans = GiftCardPlan.objects.filter(giftcardplan_merchants__merchant = m)
	context_dict['plans'] = plans
	return render_to_response('merchant/merchant_gift_card_plans.html', context_dict, context)

@login_required
def new_fixed_gift_card_plan(request):
	context = RequestContext(request)
	context_dict = {}
	merchant = request.user.merchant
	if request.method == 'POST':
		
		plan = GiftCardPlan(price = Decimal(request.POST['price']),
						value = Decimal(request.POST['value']),
						description = request.POST['description'],
						exp_time = request.POST['exp_date'])
		plan.exp_time = datetime.datetime.now() 
                plan.save()
		relationship = MerchantGiftCardPlanRelationship(merchant = merchant, giftcardplan = plan)
		relationship.save()
		plan.name, plan.website = merchant.name, merchant.website			
				                       
                if 'Logo' in request.FILES:
                        plan.logo = request.FILES['Logo']
                plan.save()
                return HttpResponseRedirect(reverse('merchant_gift_card_plans'))
	else:		
        	return render_to_response('merchant/merchant_new_gift_card_plan.html', context_dict, context)

@login_required
def settings(request):
	context = RequestContext(request)
        context_dict = {}
        user = get_object_or_404(User, id = request.user.id)
	changed, userchanged = False, False
        if not hasattr(user,'merchant'):
                raise Http404
	merchant = user.merchant
	context_dict['merchant'] = merchant
	if request.method == "POST":
		if "merchant[name]" in request.POST:
                        if merchant.name != request.POST["merchant[name]"]:
                                changed = True
                                merchant.name = request.POST["merchant[name]"]
		if "merchant[email]" in request.POST:
                        if merchant.user.email != request.POST["merchant[email]"]:
                                changed = True
				userchanged = True
                                merchant.user.email = request.POST["merchant[email]"]
	if userchanged:
		user.save()
	if changed:
		merchant.save()

	print "SETTINGS MERCHANT"
	return render_to_response('merchant/merchant_settings.html', context_dict, context)




@login_required
def transactions(request):
	context = RequestContext(request)
        context_dict = {}
        user = get_object_or_404(User, id = request.user.id)

        if not hasattr(user,'merchant'):
                raise Http404

        merchant = user.merchant
	begindate = datetime.datetime.today()-datetime.timedelta(days = 7)
        enddate  = datetime.datetime.today()
                
	if request.method == "POST":
		if 'begindate' in request.POST and request.POST['begindate'] != '':
			begindate = request.POST['begindate']
		
		if 'enddate' in request.POST and request.POST['enddate'] != '':
			enddate = request.POST['enddate']
			
	print begindate, enddate
	
	from django.utils.dateformat import DateFormat
	
	transactions = merchant.transactions.filter(timestamp__lte = enddate, timestamp__gte = begindate)
 
	context_dict['transactions'] = transactions
	context_dict['begindate'] = begindate
	context_dict['enddate'] = enddate
	return render_to_response('merchant/merchant_transactions.html', context_dict, context)
		




def sold_gift_cards(request):
	context = RequestContext(request)
	context_dict = {}
        return render_to_response('merchant/merchant_sold_gift_cards.html', context_dict, context)

def merchant_view(request, merchant_name_url):
	context = RequestContext(request)
	merchant_name = merchant_name_url.replace('_', ' ')
	context_dict = {}
	print ">>>>>",merchant_name_url,  merchant_name
	try:
		user = get_object_or_404(User, username = merchant_name)
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
			
