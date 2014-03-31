import time
import logging

from django.conf import settings
from django.core.mail import send_mail as core_send_mail
from giftcard import models
try:
    # Django 1.2
    from django.core.mail import get_connection
except ImportError:
    # ImportError: cannot import name get_connection
    from django.core.mail import SMTPConnection
    get_connection = lambda backend=None, fail_silently=False, **kwds: SMTPConnection(fail_silently=fail_silently)

def send_giftcard_to_recipient(giftcard):
	pass
