from django.db import models, transaction
from django.contrib.auth.models import User
from giftcard.models import GiftCardHistoryItem
from account.models import CurrencyField
from django.conf import settings
from giftcard.models import GiftCard	
import hashlib, math
from decimal import Decimal


def merchant_image(instance, filename):
    return '/'.join(['merchants', instance.user.username, filename])

def image_path(instance, filename):
    return '/'.join(['merchants', instance.merchant.user.username, 'pictures',  filename])


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
	
	#images 		= models.ManyToManyField(Image, related_name = 'merchant_images', blank = True)
	phone    	= models.CharField(verbose_name='Phone Number',
                                  		max_length=128,
                                  		null=True,
                                  		blank=True)
	email		= models.EmailField(blank = True, null = True)
	lat          	= models.FloatField(verbose_name='Latitude',
                                   null=True,
                                   blank=True)
	lng          	= models.FloatField(verbose_name='Longitude',
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
			
		#reserve money from merchant account to giftcard site accoun
	
	def register_transaction(self, giftcard, charge, comment = '', id = ''):
		transaction = Transaction(merchant = self, comment = comment, purchase_item_id = id, amount = charge, giftcard= giftcard)
		transaction.save()
		#TODO	SEND E_MAIL TO MERCHANT ADMIN
		return transaction

	def __unicode__(self):
                return self.name


class Image(models.Model):
        id              = models.CharField(primary_key = True, max_length=255)
        merchant        = models.ForeignKey(Merchant, related_name = 'images')
        image           = models.FileField(upload_to = image_path, max_length=255)
        upload_date     = models.DateTimeField(auto_now_add = True)




class Transaction(models.Model):
	merchant 		= models.ForeignKey(Merchant, related_name = 'transactions')
	timestamp		= models.DateTimeField(verbose_name = 'Timestamp', auto_now_add = True)
	comment 		= models.TextField(verbose_name = 'Comment', max_length = 512,default = '')
	purchase_item_id	= models.CharField(verbose_name = 'Purchase ID', max_length = 32,blank = True, default = '')
	amount			= CurrencyField(verbose_name = 'Price', max_digits = 10, decimal_places=2, default = 0)
	giftcard 		= models.ForeignKey(GiftCard, related_name = 'giftcard_transactions')
	class Meta:
		db_table = 'merchant_transactions'
	def create_payment_request(self):
		giftcardplan = self.giftcard.plan
		price  = giftcardplan.price
		value  = giftcardplan.value
		if price == value or price == 0:
			request_amount = self.amount
		elif price != 0 and price != value:
			percent = Decimal(giftcardplan.price / Decimal(giftcardplan.value))
			request_amount = Decimal(math.floor(percent * Decimal(self.amount)))
		request_amount = math.floor((1 - (self.merchant.commission / Decimal(100))) * request_amount)
		request = MerchantPaymentRequest(transaction = self, satisfied = False, amount = request_amount)
		request.save()
		#TODO SEND MAIL TO NVERCARD manager
		return request
	def __unicode__(self):
                return u'%s:ID(%s)' % (self.merchant.name, self.id)
		
class MerchantPaymentRequest(models.Model):
	#EACH PAYMENT REQUEST SHOULD BE BOUND WITH ONE TRANSACTION
	transaction 	= models.OneToOneField(Transaction, related_name = 'Payment Request')
	satisfied	= models.BooleanField(verbose_name = 'Fulfilled', default = False)
	amount 		= CurrencyField(verbose_name = 'Requested amount', max_digits = 10, decimal_places = 2, default = 0)
	fulfilled_at	= models.DateTimeField(verbose_name = 'Fulfilled at', blank = True, null = True)
	
	class Meta:
		db_table = 'merchant_payment_requests'
	def __unicode__(self):
		return u'%s' % (self.transaction.merchant.name)





