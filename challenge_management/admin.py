from django.contrib import admin
from challenge_management.models import Compiler
from challenge_management.models import Program
from challenge_management.models import Challenge
from challenge_management.models import Bot




class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'owner')    
    list_filter = ['creation_date']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['title', 'directory', 'owner', 'bots_per_game', 'game_duration', 'judging_program', 
                    'locked', 'to_delete',]
        else:
            return []


    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False



class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'target_challenge', 'owner')    
    list_filter = ('creation_date', 'target_challenge')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'playing_program', 'directory', 'creation_date', 'owner', 'target_challenge',
                    'locked', 'to_delete']
        else:
            return []

    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False




admin.site.register(Compiler)
admin.site.register(Program)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Bot, BotAdmin)