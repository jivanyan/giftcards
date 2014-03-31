from django.db import models, transaction
from django.contrib.auth.models import User
from giftcard.models import GiftCardHistoryItem
from django.conf import settings
import hashlib

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
   	website 	= models.URLField(verbose_name = 'Website', blank = True)
	picture 	= models.ImageField(verbose_name = 'Picture',
					 	upload_to = 'profiles_images',
					 	blank = True)
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

	def accept_giftcard(self, ID, summa):
		try:
			hash = hashlib.sha1()
		        hID = hash.update(ID)
			g = GiftCard.objects.get(hash_id = hID)		 	

			with transaction.commit_on_success():
        	                accepted, debt, rem = g.charge(summa)
				if rem == 0 :
					comment = _("Charged Fully and Deactivated")
				else:
					comment = _("Charged %s" % summa)
               			#The next line should be replaced by the real user 
                        	#revocation corresponding to the merchant
				h = GiftCardHistoryItem(card = g, 
						comment = comment, 
						timestamp = datetime.datetime.utcnow().replace(tzinfo=utc), 
						master = self.user)
                        	h.save()
				if g.buyer.user == self.user:
					pass	#Send commission money from merchant account to giftcard site:
				else:
					pass   #request commission from site to be transferred to merchant account
		except GiftCard.DoesNotExist:
			pass
		return accepted, debt, rem				
		

	def __unicode__(self):
                return self.name
# Create your models here.
