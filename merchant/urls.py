from django.conf.urls import patterns, url
from merchant import views 

urlpatterns = patterns('',
	url(r'^home/$', views.homepage, name = 'merchant_home'),
	url(r'^home/gift-card-plans/$', views.gift_card_plans, name = 'merchant_gift_card_plans'),
	url(r'^home/new-giftcard-plan/$', views.new_fixed_gift_card_plan, name = 'merchant_new_fixed_gift_card_plan'),
	url(r'^home/sold-gift-cards/$', views.sold_gift_cards, name = 'merchant_sold_gift_cards'),
	url(r'(?P<merchant_name_url>\w+)/$', views.merchant_view, name='merchant_view'),
	#url(r'^buy/(?P<giftcard_id>\w+)/$', views.buy_giftcard, name = 'buy_giftcard'),
	#url(r'^sell/$', views.sell_giftcard, name = 'sell_giftcard'),
	)

