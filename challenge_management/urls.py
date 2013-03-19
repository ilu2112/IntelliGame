from django.conf.urls import patterns, url
import challenge_management.views




urlpatterns = patterns('',
    url(r'^add_challenge[/]$', challenge_management.views.add_challenge_v),
    url(r'^add_bot[/]$', challenge_management.views.add_bot_v),
    url(r'^browse_challenges[/]$', challenge_management.views.browse_challenges_v),
    url(r'^(\d+)[/]$', challenge_management.views.challenge_details_v),
    url(r'^(\d+)/download[/]$', challenge_management.views.download_challenge_desc_v),
    url(r'^(\d+)/add_bot[/]$', challenge_management.views.redirect_add_bot_v),
)
