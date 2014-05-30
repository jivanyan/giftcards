from django.core.mail import send_mail
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.conf import settings

def send_new_created_giftcard_notification(giftcard):
	"""
        This function sends an notificatin mail to manager about new baught giftcard 
        """
	template = get_template('email_templates/new_giftcard_notification.html')
	send_to = settings.NEW_GIFTCARD_NOTIFICATION_RECEIVER_EMAIL
	context = Context({'user': user, 'other_info': info})
	content = template.render(context)
	subject = "GiftCard %s" % (giftcard.code)
	msg = EmailMessage(subject, content, "nvercard@nvercard.am", to=[send_to,])
	msg.send()
	
def send_email_for_new_created_giftcard_plan(giftcard_plan):
	"""
	This function sends an acklowdgement mail to manager that new giftcardplan has been created
	"""
	pass


def send_email_for_new_payment_request(payment_request):
        """
        This function sends an acklowdgement mail to manager that new giftcardplan has been created
        """
        pass

def send_giftcard_by_email(giftcard):
	"""
	This function sends a gift-style designed mail to the giftcard's recipient, which includes 
	the giftcard value, expiration time and etc..
	"""
	template = get_template('email_templates/giftcard.html')
	text_content = "GiftCard %s" % (giftcard.code)
        send_to = giftcard.send_to
        context = Context({'user':giftcard.buyer})
        content = template.render(context)
        subject = "GiftCard %s" % (giftcard.code)
        msg = EmailMultiAlternatives(subject, text_content,  "nvercard@nvercard.am", to=[send_to,])
	msg.attach_alternative(content, "text/html")
        msg.send()

























