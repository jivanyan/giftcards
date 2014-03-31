from django.contrib import admin
from giftcard.models import *
#from django_facebook.models import FacebookCustomUser
admin.site.register(GiftCard)
admin.site.register(GiftCardPlan)
admin.site.register(GiftCardCategory)
