from django.db import models , transaction
import datetime, time
from account.models import CurrencyField 
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.core.mail import send_mail
import hashlib

def giftcardplan_logo_path(instance, filename):

	if hasattr(instance, 'merchants'):
		if instance.merchants.count() <= 1:
			merchant = instance.merchants.all()[0]
			s =  '/'.join(['merchants', merchant.user.username, "{0}".format(instance.id), filename])
	else:
		s = '/'.join(['groupgiftcards', instance.name, filename])
	return s


class GiftCardCategory(models.Model):
	name = models.CharField(verbose_name = 'Giftcard Category',
				max_length = 64,
				unique = True)
	class Meta:
		db_table = 'giftcard_categories'

	def __unicode__(self):
        	return u"%s " % (self.name)




class GiftCardPlan(models.Model):
	merchants        = models.ManyToManyField('merchant.Merchant',
                                        related_name = 'all_gift_card_plans',
					blank = True,
					through = 'MerchantGiftCardPlanRelationship')
        categories      = models.ManyToManyField(GiftCardCategory,
                                        related_name = 'gift_card_plans',
                                        blank = True)
	name 		= models.CharField(verbose_name = 'Name', max_length = 128, blank = True, default = '')	
	website		= models.URLField(verbose_name = 'Website', blank = True)
	value		= CurrencyField(verbose_name = 'Value', max_digits = 10,
						 decimal_places=2, default = 0)
	price		= CurrencyField(verbose_name = 'Price', max_digits = 10, 
                                                 decimal_places=2, default = 0)

	created_date	= models.DateTimeField(verbose_name = 'Date Created', auto_now_add=True,
			                         null=True, blank=True)
	
	description	= models.TextField(max_length = 2048, blank = True)
	is_active	= models.BooleanField(verbose_name = 'is active', default = True)
	exp_time	= models.DateTimeField(verbose_name = 'valid through', blank = True)
	logo		= models.ImageField(upload_to = giftcardplan_logo_path, blank = True)
 	views 		= models.IntegerField(default = 0)		
	sold		= models.IntegerField(default = 0)
	class Meta:
		db_table = 'giftcard_plans'	
	def __unicode__(self):
                return "%s - %s" % (self.name, self.id)

class GiftCard(models.Model):
	hash_code      	= models.CharField(verbose_name = 'Hash Code',
	                                max_length=16,
        	                        db_index=True)
	code		= models.CharField(verbose_name='Code',
                                        max_length=12,
					db_index = True,
					unique = True)
	plan 		= models.ForeignKey('GiftCardPlan', related_name = 'giftcards')
	buyed_at 	= models.DateTimeField(verbose_name = 'Date Created',auto_now_add=True,
                                                 null=True, blank=True )
	buyer		= models.ForeignKey(User,related_name = 'buyed_cards')
	send_to		= models.EmailField(verbose_name = 'Send To')

	remainder	= CurrencyField(verbose_name = 'Remainder',
					max_digits = 10, 
					decimal_places=2,
					default = 0)

	recipient_name 	= models.CharField(verbose_name = 'Recipient Name', max_length = 64,
					blank = True,
					null = True)
	recipient_phone = models.CharField(verbose_name='Phone Number',
                                        max_length=128,
                                        null=True,
                                        blank=True)

	sender_name 	= models.CharField(verbose_name = 'Sender Name', max_length = 64,
					blank = True,
					null = True)
	message		= models.TextField(verbose_name = 'Message', max_length = 1024,
					blank = True,
					null = True)
	valid 		= models.BooleanField(verbose_name = 'Is Valid', default = True, editable = False)
	paid		= models.BooleanField(verbose_name = 'Paid', default = False,
					blank = True)
	class Meta:
		db_table = 'giftcards'

	def __unicode__(self):
                return u"%s" % ( self.code)
	
	def activate(self, comment, master, money):
		
		with transaction.commit_on_success():
			self.valid = True
			self.save(comment, master, money)
					
		return self

	def deactivate(self, comment, master, money):
		
		with transaction.commit_on_success():
                        self.valid = False
                        self.save(comment, master, money )
                                       

		return self

	def redeem(self, summa, master):
		#create a history item with comment "Charged summa"
		#decrease the reminder
		rem = self.remainder
		if summa <= rem:
			rem = rem - summa 
			accepted = True
			debt = 0
		else:  
			rem = 0
			debt = summa - rem
			accepted = False
		self.remainder = rem
		self.save("REDEEMED", master, summa)
		return accepted, debt, rem
	
	def register_history_item(self, comment, master, money):
		h = GiftCardHistoryItem(card = self,
                                                comment = comment,
                                                timestamp = datetime.datetime.utcnow().replace(tzinfo=utc),
                                                master = master,
						amount = money)
	
                h.save()
	
	def generate_code(self):
		hash = hashlib.md5()
		hash.update("%s%s%s%s%s%s" % (self.buyed_at, self.plan.id, self.buyer.username, self.send_to, str(time.time()), self.message ) )
		self.code = hash.hexdigest()[:12]
		hash = hashlib.sha1()
		hash.update("%s" % (self.code) )
		self.hash_code = hash.hexdigest()
		
	def send_to_recipient(self):
		send_mail('New Giftcard', self.message, 'NVERCARD@nvercard.com',
		    [self.send_to], fail_silently=False)
		

	def save(self, comment = None, master = None, amount = None ):		
		if not self.id:
			super(GiftCard, self).save()
			self.register_history_item("CREATED", self.buyer, self.remainder)
		else:
			super(GiftCard, self).save()
			self.register_history_item(comment, master, amount)
		
class MerchantGiftCardPlanRelationship(models.Model):
	merchant 	= models.ForeignKey('merchant.Merchant', related_name = 'merchant_giftcardplans')
	giftcardplan 	= models.ForeignKey(GiftCardPlan, related_name = 'giftcardplan_merchants')
	created_at	= models.DateTimeField(verbose_name = 'Created at', auto_now_add=True,
                                                 null=True, blank=True )
	class Meta:
		db_table = 'merchant_giftcardplan_relationship'
	def __unicode__(self):
		return u"%s/%s" % (self.giftcardplan.name, self.merchant.name)

class GiftCardHistoryItem(models.Model):
	card		= models.ForeignKey(GiftCard, related_name = "history items")
	comment 	= models.CharField(verbose_name = 'Comment', max_length = 128)
	timestamp	= models.DateTimeField(verbose_name = 'Timestamp',auto_now_add=True,
                                                 null=True, blank=True )
	master		= models.ForeignKey(User, verbose_name = "Change Master")	
	amount		= CurrencyField(verbose_name = 'Transaction Amount', max_digits = 10, 
                                                 decimal_places=2, default = 0)
	class Meta:
                db_table = 'giftcard_history_items'
	def __unicode__(self):
                return u"%s - %s - %s" % (self.comment, self.timestamp, self.master.username)



