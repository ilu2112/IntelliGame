from django.conf.urls import patterns, url
import user_management.views
import task_management.views


urlpatterns = patterns('',
    url(r'^register[/]$', user_management.views.register_v),
    url(r'^login[/]$', user_management.views.login_v),
    url(r'^logout[/]$', user_management.views.logout_v),
    url(r'^show_profile[/]$', user_management.views.show_profile_v),
    url(r'^change_passwd[/]$', user_management.views.change_passwd_v),
    url(r'^edit_profile[/]$', user_management.views.edit_profile_v),
    
    url(r'recent_actions[/]$', task_management.views.recent_actions_v)
)
