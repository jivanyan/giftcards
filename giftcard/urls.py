from django.conf.urls import patterns, url
from giftcard import views 

urlpatterns = patterns('',
	url(r'^$', views.giftcards, name='giftcards'),
	#url(r'^buy/(?P<giftcard_id>\w+)/$', views.buy_giftcard, name = 'buy_giftcard'),
	url(r'^sell/$', views.sell_giftcard, name = 'sell_giftcard'),
	)

