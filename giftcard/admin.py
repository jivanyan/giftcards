from django.contrib import admin
from giftcard.models import *
#from django_facebook.models import FacebookCustomUser


class GiftCardPlanAdmin(admin.ModelAdmin):
	list_display = ('name', 'price','value', 'description')
	list_filter = ['name']
	search_fields = ['name']
class GiftCardAdmin(admin.ModelAdmin):
	list_display = ('plan', 'buyer', 'remainder', 'code', 'paid', 'valid')
	list_filter = ['plan', 'buyer', 'paid', 'valid']
	
class GiftCardHistoryItemAdmin(admin.ModelAdmin):
	list_display = ('card','comment', 'master', 'amount', 'timestamp')
	list_filter = ['comment', 'master', 'card']
	
class MerchantGiftCardPlanRelationshipAdmin(admin.ModelAdmin):
	list_display = ('giftcardplan', 'merchant', 'created_at')


admin.site.register(GiftCard, GiftCardAdmin)
admin.site.register(GiftCardPlan, GiftCardPlanAdmin)
admin.site.register(GiftCardCategory)
admin.site.register(GiftCardHistoryItem, GiftCardHistoryItemAdmin)
admin.site.register(MerchantGiftCardPlanRelationship, MerchantGiftCardPlanRelationshipAdmin)
