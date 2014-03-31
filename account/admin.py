from django.contrib import admin
from account.models import Account, PatronAccount, MerchantAccount
#from django_facebook.models import FacebookCustomUser
admin.site.register(PatronAccount)
#admin.site.register(Account)

admin.site.register(MerchantAccount)

