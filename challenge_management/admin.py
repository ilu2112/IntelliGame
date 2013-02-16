from django.contrib import admin
from challenge_management.models import Compiler
from challenge_management.models import Program
from challenge_management.models import Challenge
from challenge_management.models import Bot




class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'owner')    
    list_filter = ['creation_date']




class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'target_challenge', 'owner')    
    list_filter = ('creation_date', 'target_challenge')



admin.site.register(Compiler)
admin.site.register(Program)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Bot, BotAdmin)