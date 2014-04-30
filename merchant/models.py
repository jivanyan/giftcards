from django.db import models, transaction
from django.contrib.auth.models import User
from giftcard.models import GiftCardHistoryItem
from account.models import CurrencyField
from django.conf import settings
import hashlib


def merchant_image(instance, filename):
    return '/'.join(['merchants', instance.user.username, filename])


class Merchant(models.Model):
	class MerchantCategory:
		RESTAURANT = 1
	        SHOP = 2
	        SPA = 3
	        SALON = 4
	        OTHER = 99
	Category_Types = (
        	(MerchantCategory.RESTAURANT, 'Restaurant'),
        	(MerchantCategory.SHOP, 'Shop'),
        	(MerchantCategory.RESTAURANT,'SPA Centre'),
        	(MerchantCategory.SALON,'Salon'),
        	(MerchantCategory.OTHER,'Other'),
	)

	user            = models.OneToOneField(User, related_name='merchant')

	name    	= models.CharField(verbose_name = 'Name',
					   max_length = 250,
					   db_index = True,
					   unique = True)
	category	= models.IntegerField(verbose_name = 'Category',
					      choices = Category_Types,
					      default = MerchantCategory.OTHER)
	commission 	= models.PositiveSmallIntegerField(verbose_name = 'Commission Fee Percent',
					      default = settings.GIFT_CARD_COMMISION_PERCENT)
   	website 	= models.URLField(verbose_name = 'Website', blank = True)
	picture 	= models.ImageField(verbose_name = 'Picture',
					 	upload_to = merchant_image,
					 	blank = True)
	phone    	= models.CharField(verbose_name='Phone Number',
                                  		max_length=128,
                                  		null=True,
                                  		blank=True)
	lat          = models.FloatField(verbose_name='Latitude',
                                   null=True,
                                   blank=True)
	lng          = models.FloatField(verbose_name='Longitude',
                                   null=True,
                                   blank=True)

	class Meta:
		db_table = 'merchants'

	def give_present(self, gc_plan, e_mail, summa, message, name):
		try:
			plan = self.gift_card_plans.get(id = gc_plan)
		except	GiftCardPlan.DoesNotExist:
			pass	
		gc = GiftCard(plan = gc_plan,
			buyer = self.user,
			send_to = e_mail,
			message = message,
			name = name)
		if gc_plan.price != 0:
			summa = gc_plan.price		
		gc.price = summa
		gc.amount = summa		
		
		with transaction.commit_on_success():		
			gc.save()		
			commission = (gc.price * settings.GIFT_CARD_COMMISION_PERCENT) / 100
			
		#reserve money from merchant account to giftcard site account

	def __unicode__(self):
                return self.name

class Transaction(models.Model):
	merchant 	= models.ForeignKey(Merchant, related_name = 'Transactions')
	timestamp	= models.DateTimeField(verbose_name = 'timestamp', auto_now_add = True)
	comment 	= models.TextField(verbose_name = 'Comment', max_length = 512)
	purchase_id	= models.CharField(verbose_name = 'Purchase ID', max_length = 32,blank = True, default = '')
	amount		= CurrencyField(verbose_name = 'Price', max_digits = 10, decimal_places=2, default = 0)
	giftcard_code 	= models.CharField(verbose_name = 'Giftcard code', max_length=12)
	
	def __unicode__(self):
                return self.name
		






