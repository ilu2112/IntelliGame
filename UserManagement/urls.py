from django.conf.urls import patterns, url
import UserManagement.views

urlpatterns = patterns('',
    url(r'^register[/]$', UserManagement.views.register),
    url(r'^successful[/]$', UserManagement.views.successful),
    url(r'^login[/]$', UserManagement.views.login_v),
    url(r'^logout[/]$', UserManagement.views.logout_v),
)