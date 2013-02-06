from django.conf.urls import patterns, include, url
import IntelliGame.views

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    url(r'^user/', include('user_management.urls')),
    url(r'^challenge/', include('challenge_management.urls')),
    url(r'^$', 'IntelliGame.views.home'),
    url(r'^successful[/]$', IntelliGame.views.successful_v),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
