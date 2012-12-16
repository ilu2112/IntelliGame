from django.conf.urls import patterns, url
import UserManagement.views

urlpatterns = patterns('',
    url(r'^register[/]$', UserManagement.views.register),
    url(r'^register/successful[/]$', UserManagement.views.successful),
)