from django.conf.urls import patterns, url
from merchant import views 

urlpatterns = patterns('',
	url(r'(?P<merchant_name_url>\w+)/$', views.merchant_view, name='merchant_view'),
	#url(r'^buy/(?P<giftcard_id>\w+)/$', views.buy_giftcard, name = 'buy_giftcard'),
	#url(r'^sell/$', views.sell_giftcard, name = 'sell_giftcard'),
	)

