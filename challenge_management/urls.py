from django.conf.urls import patterns, url
import challenge_management.views




urlpatterns = patterns('',
    url(r'^add_challenge[/]$', challenge_management.views.add_challenge_v),
    url(r'^add_bot[/]$', challenge_management.views.add_bot_v),
    url(r'^browse_challenges[/]$', challenge_management.views.browse_challenges_v),
    url(r'^(\d+)[/]$', challenge_management.views.challenge_details_v),
    url(r'^(\d+)/download[/]$', challenge_management.views.download_challenge_desc_v),
    url(r'^(\d+)/rank[/]$', challenge_management.views.challenge_rank_v),
    url(r'^(\d+)/add_bot[/]$', challenge_management.views.redirect_add_bot_v),
    url(r'^my_bots[/]$', challenge_management.views.my_bots_v),
    url(r'^bot/(\d+)[/]$', challenge_management.views.bot_v),
    url(r'^bot/(\d+)/download[/]$', challenge_management.views.download_bots_source_v),
    url(r'^battle/(\d+)[/]$', challenge_management.views.battle_v),
    url(r'^my_challenges[/]$', challenge_management.views.my_challenges_v),
)
