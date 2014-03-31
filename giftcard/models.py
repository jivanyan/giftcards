from django.db import models
import datetime
from account.models import CurrencyField 
from django.contrib.auth.models import User
from django.utils.timezone import utc
import hashlib

def _createHash():
	"""
	This function generate 10 character long hash
	"""
    	hash = hashlib.sha1()
    	hash.update(str(time.time()))
    	return  hash.hexdigest()[:-10]

class GiftCardCategory(models.Model):
	name = models.CharField(verbose_name = 'giftcard category',
				max_length = 64,
				unique = True)
	class Meta:
		db_table = 'gift_card_categories'

	def __unicode__(self):
        	return u"%s " % (self.name)


class GiftCardPlan(models.Model):
	merchant	= models.ForeignKey('merchant.Merchant',
					related_name = 'gift_card_plans')

	value		= CurrencyField(verbose_name = 'amount',
					max_digits=8,
                                        decimal_places=2,
                                        default = 0)
	categories	= models.ManyToManyField(GiftCardCategory,
					related_name = 'all_gift_card_plans')				
					
	price		= CurrencyField(verbose_name = 'price',
					max_digits=8,
                                        decimal_places=2,
                                        default = 0)
	max_count	= models.IntegerField(verbose_name = 'allowed count', blank = True, null = True)
	description	= models.CharField(max_length = 128, blank = True)
	is_active	= models.BooleanField(verbose_name = 'is active', default = True, )
	exp_time	= models.IntegerField(verbose_name = 'valid through', default = 365)
	logo		= models.ImageField(upload_to = 'giftcards', blank = True)
	
	class Meta:
		#unique_together = ('owner', 'value', 'price')
		db_table = 'giftcard_plans'
	def __unicode__(self):
                return u"%s - %s" % (self.merchant.name, self.description)



class GiftCard(models.Model):
	hash_code      	= models.CharField(verbose_name = 'hash_code',
	                                max_length=16,
        	                        null=True,
        	                        blank=True,
        	                        db_index=True)
	code		= models.CharField(verbose_name='code',
                                        max_length=16,
                                        null=True,
                                        blank=True,
                                        db_index=True)
	plan 		= models.ForeignKey(GiftCardPlan,
					related_name = 'cards')
	buyer		= models.ForeignKey(User,
					related_name = 'buyed_cards')
	send_to		= models.EmailField(verbose_name = 'sent to')

	remainder	= CurrencyField(verbose_name = 'remainder',
					max_digits=8,
                                        decimal_places=2,
                                        default = 0)
	recipient_name  = models.CharField(max_length = 64,
					blank = True,
					null = True)
	sender_name     = models.CharField(max_length = 64,
					blank = True,
					null = True) 
	message		= models.TextField(max_length = 1024,
					blank = True,
					null = True)
	valid 		= models.BooleanField(default = True,
					editable = False)
	class Meta:
		db_table = 'giftcards'
		unique_together = ('plan', 'buyer', 'send_to', 'message')
	def __unicode__(self):
                return u"%s - %s" % (self.plan.description, self.id)
	
	def activate(self):
		#create New History Item
		self.valid = True
		self.save()
		return self

	def deactivate(self):
		#Create New History Item
		self.valid = False
		self.save()
		return self

	def charge(self, summa):
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
		self.save()
		return accepted, debt, rem
	
	def register_in_history(self, comment, master):
		h = GiftCardHistoryItem(card = self,
                                                comment = comment,
                                                timestamp = datetime.datetime.utcnow().replace(tzinfo=utc),
                                                master = master)
                h.save()

	def send_to_recipient(self):
		#TODO 
		pass

	def save(self):		
		if not self.id:
			#The hash_id should be generated according to special algorithm yet to be chosen
			#hash_id is the unique code of the gift card which is used during selling or redeeming
			hash = hashlib.sha1()
			hash.update("%s%s" % (self.buyer.username, self.plan.merchant.name ))
			self.hash_id = hash.hexdigest()			
			value = GiftCardPlan.objects.get(id = self.plan.id).value

		super(GiftCard, self).save()

class GiftCardHistoryItem(models.Model):
	card		= models.ForeignKey(GiftCard, related_name = "history items")
	comment 	= models.CharField(max_length = 128)
	timestamp	= models.DateTimeField()
	master		= models.ForeignKey(User, verbose_name = "master of change")	
	
	class Meta:
                db_table = 'giftcards_history_items'

	def __unicode__(self):
                return u"%s - %s - %s" % (self.comment, self.timestamp, self.master.username)




