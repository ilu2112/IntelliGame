from django.conf.urls import patterns, url
import UserManagement.views

urlpatterns = patterns('',
    url(r'^register[/]$', UserManagement.views.register_v),
    url(r'^successful[/]$', UserManagement.views.successful_v),
    url(r'^login[/]$', UserManagement.views.login_v),
    url(r'^logout[/]$', UserManagement.views.logout_v),
    url(r'^show_profile[/]$', UserManagement.views.show_profile_v),
    url(r'^change_passwd[/]$', UserManagement.views.change_passwd_v),
    url(r'^edit_profile[/]$', UserManagement.views.edit_profile_v),
)