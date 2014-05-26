from django.conf.urls import patterns, url
from giftcard import views 

urlpatterns = patterns('',
	url(r'^$', views.giftcards, name='giftcards'),
	url(r'^search/$', views.search_gift_card_plans, name = 'search_gift_card_plans'),
	url(r'^(?P<plan_id>\d+)$', views.gift_card_plan_view, name = 'gift_card_plan_view'),
	url(r'^(?P<plan_id>\d+)/buy/$', views.buy_gift_card, name = 'buy_gift_card'),
	url(r'^gift_card_history_view/$', views.gift_card_history_view, name = 'gift_card_history_view'),
	url(r'^pay_gift_card_view/$', views.pay_gift_card_view, name = 'pay_gift_card_view'),
	url(r'^sell/$', views.sell_giftcard, name = 'sell_giftcard'),
)

