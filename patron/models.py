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
	
        picture         = models.ImageField(upload_to = 'profile_picture',
                                      blank = True)
	account 	= models.OneToOneField(PatronAccount, related_name = 'patron')
	class Meta:
		db_table = 'patrons'
	
	def __unicode__(self):
		return self.user.username

	def pay_for_giftcard(self, giftcard):
		"""
		Pays for the specified giftcard which is created and maybe sent already
		Should raise exception in case the giftcard is already paid or its remainder is 0
		"""
		account = self.account
		if giftcard.remainder == 0 or giftcard.paid == True:
			raise Exception("Nothing to pay for") 
			
		if giftcard.plan.price == 0:
			summa = giftcard.remainder
		else:		
			summa = giftcard.plan.price	
		print summa
		print account.balance, summa

		print account.balance - summa
		if account.balance >= summa:
			print "MUST PAY"
		with transaction.commit_on_success():
			if account.balance >= summa:
				print "Befor", account.balance
				account.balance = account.balance - summa
				print "After", account.balance
				account.save()
				giftcard.paid = True
				giftcard.save("PAID", self.user, summa)
	
		return giftcard.paid

				
	
	def debit_account(self, summa):
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
		
		if summa > 0:
			account = self.account
			balance = account.balance + summa
			account.balance = balance
			account.save()
			return account
		return summa
