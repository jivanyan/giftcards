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
from account.models import *
from patron.models import *

@login_required
def edit_settings(request):
	context = RequestContext(request)
	context_dict = {'settings':True}	
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
		
	context_dict['giftcards'] = giftcards
	
        return render_to_response('patron/sold_giftcards.html', context_dict, context)


