from django.conf.urls import patterns, url
import challenge_management.views




urlpatterns = patterns('',
    url(r'^add_challenge[/]$', challenge_management.views.add_challenge_v),
    url(r'^add_bot[/]$', challenge_management.views.add_bot_v),
)
