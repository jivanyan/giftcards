from django.conf.urls import patterns, include, url
from views import *
import multiuploader
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', MainPageView.as_view(), name='main_page'),
    url(r'^giftcards/', include('apps.giftcard.urls')),
    url(r'^merchant/', include('apps.merchant.urls')),
    url(r'^account/', include('apps.patron.urls')),
    url(r'^upload/', include('multiuploader.urls')),
    url(r'^login/', user_login, name = 'login'),
    url(r'^signup', user_signup, name = 'signup'),
    url(r'^logout', user_logout, name = 'logout'),			
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )


