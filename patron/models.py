from django.db import models, transaction
from django.contrib.auth.models import User
from account.models import PatronAccount
from django.utils.timezone import utc
from django.utils.translation import ugettext as _	
from django.conf import settings
from giftcard.models import *
#from email_manager.engine import *
#except ImportError:
#	print "Can not import engine"

import datetime
import decimal

#from transaction.models import Transaction

############################
# In case tracking of SQL commands needed, this code should be added to shell
# import logging
# l = logging.getLogger('django.db.backends')
# l.setLevel(logging.DEBUG)
# l.addHandler(logging.StreamHandler())
###############################

# TODO TODO TODO TODO TODO
# 1. New CHECK_ACCOUNT_VALIDITY function which can be called in buy_giftcard and sell_giftcard functions.
#
#

class Patron(models.Model):
        user            = models.OneToOneField(User, related_name='patron')

        picture         = models.ImageField(upload_to = 'profile_pictures',
                                      blank = True)
	account 	= models.OneToOneField(PatronAccount, related_name = 'patron')
	class Meta:
		db_table = 'patrons'
	
	def __unicode__(self):
		return self.user.username

	
	def buy_giftcard(self, gcplan_id, recipient_email, message, value):
		"""
		Buys a giftcard of the given type and sends to the recipient. Must do active checks
		of account validness and balance availability. A transaction object should be created
		"""
		gc_plan = GiftCardPlan.objects.get(id = gcplan_id)
		card = GiftCard(plan = gc_plan,
				buyer = self.user,
				send_to = recipient_email, 
				#buyed_at = datetime.datetime.utcnow().replace(tzinfo=utc),
				message = message)

		if gc_plan.value != 0:
			card.remainder = gc_plan.value
			price = gc_plan.price
		else:
			price, card.remainder = value, value
		
		# TODO
		# check transaction validity: 
		#	1. If the gift card plan is 0, the user entered price does not exceed his balance or
		#   The user is allowed to pay later and the balance - price does not exceed the allowed limit
		#	2. 
		with transaction.commit_on_success():
			self.change_balance( decimal.Decimal(-price))
			card.activate()
			card.send_to_recipient()
			card.save()
			card.register_in_history(comment = _("Created"), master = self.user)				
		return u"%s" % (card.id) 
		
	#@transaction.atomic
	def sell_giftcard(self, gift_card_id):
		"""
		Sells the owned giftcard back to the service site at the price defined by 
		settings.GIFT_CARD_SELL_BACK_RETURN_PERCENT
		"""
		try:
			card = Giftcard.objects.get(hash_id = gift_card_id)
           	except GiftCard.DoesNotExist:
        		print "No Such giftcard"
			#raise Http404 			
		cashback = decimal.Decimal((card.price * settings.GIFT_CARD_SELL_BACK_RETURN_PERCENT) / 100)
		with transaction.commit_on_success():
			self.change_balance(cashback)
			card.deactivate()
			card.register_in_history(comment = _("Created"), master = self.user)
				
	
	def change_account_balance(self, summa):
		"""
		Charges the account balance by the given summa. Should raise also signals
		to activate the frozen giftcards
		"""
		# TODO
		#	a. the summa should be casted to decimal
		# 	b. check transaction validity: 
                #       	1. If the gift card plan is 0, the user entered price does not exceed his balance or
                #          	The user is allowed to pay later and the balance - price does not exceed the allowed limit
                #       	2. 
		#	c. register transaction
		account = self.account
		balance = account.balance + summa
		account.balance = balance
		account.save()
		return account
