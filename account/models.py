from django.db import models
from decimal import Decimal
#from patron.models import Patron
#from merchant.models import Merchant
from django.contrib.auth.models import User 


class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        try:
           return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
           return None

class Account(models.Model):
	valid 		= models.BooleanField()
	frozen		= models.BooleanField()
	balance		= CurrencyField(max_digits = 10, decimal_places=2, default = 0) 
	#credit		= CurrencyField(max_digits=8, decimal_places=2)
	class Meta:
		abstract = True
	def __unicode__(self):
                return u"%s" % (self.id)


class PatronAccount(Account):
	#patron 		= models.OneToOneField(Patron, related_name = 'Account')
	class Meta:
		db_table = 'patron_accounts'
	def __unicode__(self):
		return u"%s" % (self.patron.user.first_name + self.patron.user.last_name)


class MerchantAccount(Account):
	merchant 		= models.OneToOneField('merchant.Merchant', related_name = 'Account')
	account_holder_name     = models.CharField(max_length = 32)
        routing_number 		= models.CharField(max_length = 16)
	account_number		= models.CharField(max_length = 16)
        class Meta:
                db_table = 'merchant_accounts'
        

