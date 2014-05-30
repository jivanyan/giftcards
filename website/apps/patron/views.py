from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import Http404
from apps.merchant.models import *
from apps.giftcard.models import *
from apps.account.models import *
from apps.patron.models import *

@login_required
def edit_settings(request):
	context = RequestContext(request)
	context_dict = {'settings':True}	
	if request.method == 'POST':
		user = request.user
		changed = False
		if "user[first_name]" in request.POST:
			if user.first_name != request.POST["user[first_name]"]:
				changed = True
				user.first_name = request.POST["user[first_name]"]
		if "user[last_name]" in request.POST:
			if request.POST["user[last_name]"] != "" and user.last_name != request.POST["user[last_name]"]:
				user.last_name = request.POST["user[last_name]"]
				changed = True
		if "user[email]" in request.POST:
			if request.POST["user[email]"] != "" and user.email != request.POST["user[email]"]:
				user.email = request.POST["user[email]"]
				user.username = user.email
				changed = True
		if "user[password]" in request.POST and "user[password_confirmation]" in request.POST:
			if request.POST["user[password]"] != "": 
				user.password = request.POST["user[password]"]
				user.set_password(user.password)
				changed = True
		if changed:
			user.save()
 	
			
	return render_to_response('patron/settings.html', context_dict, context)


@login_required
def transactions(request):
        context = RequestContext(request)
        context_dict = {'transactions':True}
        return render_to_response('patron/transactions.html', context_dict, context)

@login_required
def sent_giftcards(request):
        context = RequestContext(request)
        context_dict = {'sent_giftcards':True}
	giftcards = GiftCard.objects.filter(buyer = request.user).order_by('-buyed_at')
	context_dict['giftcards'] = giftcards
        return render_to_response('patron/sent_giftcards.html', context_dict, context)



@login_required
def sold_giftcards(request):
        context = RequestContext(request)
        context_dict = {'sold_giftcards':True}
	ids = GiftCardHistoryItem.objects.filter(master = request.user, comment = "SOLD").values('card')
	giftcards = GiftCard.objects.filter(id__in = ids)
	for card in giftcards:
		card.sell_price = GiftCardHistoryItem.objects.get(card = card, comment = "SOLD").amount
		card.sold_at = GiftCardHistoryItem.objects.get(card = card, comment = "SOLD").timestamp
  	import operator
	giftcards = sorted(giftcards, key=operator.attrgetter('sold_at'),reverse = True)		
	context_dict['giftcards'] = giftcards
	
        return render_to_response('patron/sold_giftcards.html', context_dict, context)

@login_required
def pay_gift_card(request):
	context = RequestContext(request)
        context_dict = {}
        if request.method == 'GET':
                code = request.GET['code']
		payment_method = request.GET['payment_method']
	
        card = get_object_or_404(GiftCard, code = code)
        user = request.user
        if not hasattr(user, 'patron') or card.buyer != user:
                raise Http404
	patron = user.patron
	if payment_method == "ACCOUNT":
		patron.pay_for_giftcard(card)
		pass
	elif payment_method == "ARCA":
		pass
	elif payment_method == "VISA/MASTERCARD":
		pass
	elif payment_method == "PAYPAL":
		pass
	return redirect("patron_sent_giftcards")

	
