from django.contrib import admin
from challenge_management.models import Compiler
from challenge_management.models import Program
from challenge_management.models import Challenge




class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'owner')    
    list_filter = ['creation_date']




admin.site.register(Compiler)
admin.site.register(Program)
admin.site.register(Challenge, ChallengeAdmin)