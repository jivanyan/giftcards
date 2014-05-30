from django.contrib import admin
from apps.merchant.models import *
class MerchantPaymentRequestAdmin(admin.ModelAdmin):
        list_display = ('transaction', 'amount', 'satisfied','fulfilled_at')
        list_filter = ['satisfied', 'fulfilled_at']
        
class TransactionAdmin(admin.ModelAdmin):
	list_display = ('merchant', 'id', 'amount', 'giftcard', 'timestamp')
	list_filter = ['timestamp']

#from django_facebook.models import FacebookCustomUser
admin.site.register(Merchant)
admin.site.register(Image)	
admin.site.register(MerchantPaymentRequest, MerchantPaymentRequestAdmin)
admin.site.register(Transaction, TransactionAdmin)
