from django.views.generic.base import TemplateView
from giftcard.models import *

class MainPageView(TemplateView):
	template_name = "main_page.html"
	def get_context_data(self, **kwargs):
		context = super(MainPageView, **kwargs)
		return context
