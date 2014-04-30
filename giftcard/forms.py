from django import forms
import datetime
from django.forms.extras.widgets import SelectDateWidget
from giftcard.models import GiftCardPlan, GiftCardCategory
from django.contrib.auth.models import User
from multiuploader.forms import MultiuploaderField
CATEGORIES = [(s.name, s.name ) for s in GiftCardCategory.objects.all() ]
class GiftCardFixedPlanForm(forms.ModelForm):
	
        value           = forms.DecimalField(help_text = "Value", max_digits=8,
                                        decimal_places=2)

        price           = forms.DecimalField(help_text = "Price",max_digits=8,
                                        decimal_places=2)

        max_count       = forms.IntegerField(help_text = "Maximum Count", required = False)
        description     = forms.CharField(widget = forms.Textarea, help_text = "Brief Description")
        is_active       = forms.BooleanField(help_text = "Is Valid", required = False )
        exp_time        = forms.DateField(initial=datetime.date.today)
        logo            = forms.ImageField(help_text = "Select a logo", required=False)
                           


	views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
	def clean(self):
                cleaned_data = self.cleaned_data
                #rl = cleaned_data.get('url')
                #f url and not url.startswith('http://'):
                #       url = 'http://'+url
                #       cleaned_data['url'] = url
                return cleaned_data
        class Meta:
                model = GiftCardPlan
                fields = ('value','price', 'max_count','description','logo', 'is_active')


class GiftCardFloatyPlanForm(forms.ModelForm):

        value           = forms.DecimalField(help_text = "Minimum Value", max_digits=8,
                                        decimal_places=2)

        max_count       = forms.IntegerField(help_text = "Maximum Count")
        description     = forms.CharField(widget = forms.Textarea, help_text = "Brief Description")
        is_active       = forms.BooleanField(help_text = "Is Valid", required = False )
        exp_time        = forms.DateField(help_text = "Valid through", initial=datetime.date.today)
        logo            = forms.ImageField(help_text = "Select a logo", required=False)
        #uploadedFiles   = MultiuploaderField(required=False)
                           


        views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
        def clean(self):
                cleaned_data = self.cleaned_data
                #rl = cleaned_data.get('url')
                #f url and not url.startswith('http://'):
                #       url = 'http://'+url
                #       cleaned_data['url'] = url
                return cleaned_data
        class Meta: 
                model = GiftCardPlan
                fields = ('value','max_count','description','logo', 'is_active')


class GiftCardOrderForm(forms.ModelForm):
        send_to         = forms.EmailField(help_text = 'Recipient email address')
	sender_name 	= forms.CharField(help_text = 'Sender name')
        recipient_name  = forms.CharField(help_text = 'Recipient Name')
                                        
        message         = forms.CharField(widget = forms.Textarea, help_text = 'Gift Wish')
	remainder	= forms.DecimalField(help_text = "Value", max_digits=8,
	                                        decimal_places=2)
	class Meta:
		model = GiftCardPlan
 			


