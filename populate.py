import os

def populate():
	m = add_merchant(n = "Segafredo", c = 2)
	p = add_gc_plan(m, 20, 4000, 5000)	
	add_patron(u = "gexamjivanyan", p = "t")
def add_merchant(n, c):
	m = Merchant.objects.get_or_create(name = n, category = c)[0]
	return m

def add_gc_plan(m, c, p, a):
	p = GiftCardPlan.objects.get_or_create(merchant = m,
			price = p,
			value = a,
			max_count = c,
			description = "%s/%s" % (p, a))
	p[0].save()
	return p[0]

def add_patron(u, p):
	u = User.objects.get_or_create(username = u, password = p)
	u[0].save()
	a = PatronAccount(valid = True, frozen_sum = 0) 
	a.save()
	p = Patron(user = u[0], account = a)
	p.save()


if __name__ == '__main__':
	print "Starting GiftCard population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giftcards.settings')
	from patron.models import Patron
	from giftcard.models import *
	from merchant.models import *
	from account.models import *
	from django.contrib.auth.models import User

	populate()

