from django.conf.urls import patterns, include, url
from patron.views import *

urlpatterns = patterns('',
	url(r'^edit/$', edit_settings, name='edit_patron_settings'),
	url(r'^pay_gift_card/$', pay_gift_card, name = 'pay_gift_card'),
	url(r'^transactions/$', transactions, name='patron_transactions'),
	url(r'^sold-giftcards/$', sold_giftcards, name='patron_sold_giftcards'),
	url(r'^sent-giftcards/$', sent_giftcards, name='patron_sent_giftcards')
)
                                                                                                                                                                       
