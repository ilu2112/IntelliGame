from django.conf.urls import patterns, include, url
# import UserManagement.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/', include('UserManagement.urls')),
    url(r'^$', 'IntelliGame.views.home'),
    # url(r'^user/register$', UserManagement.views.register)
    # Examples:
    # url(r'^$', 'IntelliGame.views.home', name='home'),
    # url(r'^IntelliGame/', include('IntelliGame.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
