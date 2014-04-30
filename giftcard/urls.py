from django.conf.urls import patterns, url
from giftcard import views 

urlpatterns = patterns('',
	url(r'^$', views.giftcards, name='giftcards'),
	url(r'^search/$', views.search_gift_card_plans, name = 'search_gift_card_plans'),
	url(r'^(?P<plan_id>\d+)$', views.gift_card_view, name = 'gift_card_view'),
	url(r'^(?P<plan_id>\d+)/buy/$', views.buy_gift_card, name = 'buy_gift_card'),
	url(r'^sell/$', views.sell_giftcard, name = 'sell_giftcard'),
)

