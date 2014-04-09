from django.conf.urls import patterns, include, url
from giftcards.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', MainPageView.as_view(), name='main_page'),
    url(r'^giftcards/', include('giftcard.urls')),
    url(r'^merchant/', include('merchant.urls')),
    url(r'^account/', include('patron.urls')),
    url(r'^login/', user_login, name = 'login'),
    url(r'^signup', user_signup, name = 'signup'),
    url(r'^logout', user_logout, name = 'logout'),			
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
