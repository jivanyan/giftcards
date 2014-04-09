from django.views.generic.base import TemplateView
from giftcard.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from patron.models import *


class MainPageView(TemplateView):
	template_name = "main_page.html"
	def get_context_data(self, **kwargs):
		context = super(MainPageView, **kwargs)
		return context


def user_login(request):
	context = RequestContext(request)
	next_link = ""
	if request.GET:
		next_link = request.GET['next']
	if request.method == 'POST':
		next_link = request.POST['login_next']
		username = request.POST['login']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if next_link == "":
					return HttpResponseRedirect('/giftcards/')
				else:
					return HttpResponseRedirect(next_link)
			else:
				return render_to_response('login.html',{'message':"Your account is disabled"}, context)
		else:
			return render_to_response('login.html',{'message':"Invalid login details are supplied"}, context)
	else:
		return render_to_response('login.html',{'next':next_link},context)
			


def user_signup(request):
	context = RequestContext(request)
	registered = False
	user = User(username = '')
	next_link = ""
	if request.GET:
		next_link = request.GET['next']	
	
	if request.method == 'POST':
		next_link = request.POST['signup_next']
		user.first_name = request.POST['user[full_name]']
		user.last_name = request.POST['user[sur_name]']
		user.username = request.POST['user[email]']
		user.email = request.POST['user[email]']
		user.password = request.POST['user[password]']
		user.set_password(user.password)
		user.save()
		patron = Patron(user = user)
		account = PatronAccount(balance = 0, frozen_sum = 0, frozen = False, valid = True )
		account.save()
		patron.account = account
		patron.save()
		user = authenticate(username = request.POST['user[email]'], password = request.POST['user[password]'])
                if user is not None:
                        if user.is_active:
                                login(request, user)

		print "{0}-{1}-{2}-{3}-{4}".format(request.POST['user[full_name]'],request.POST['user[email]'],request.POST['user[password]'],patron.id,account.id)
		if next_link == "":
			return HttpResponseRedirect('/giftcards')
		else:
			return HttpResponseRedirect(next_link)
	
	else:
		return render_to_response('login.html', {'next':next_link}, context)		
	return 
	

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/giftcards/')



