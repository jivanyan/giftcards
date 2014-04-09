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

def sent_giftcards(request):
        context = RequestContext(request)
        context_dict = {'sent_giftcards':True}
        return render_to_response('patron/sent_giftcards.html', context_dict, context)
def sold_giftcards(request):
        context = RequestContext(request)
        context_dict = {'sold_giftcards':True}
        return render_to_response('patron/sent_giftcards.html', context_dict, context)


