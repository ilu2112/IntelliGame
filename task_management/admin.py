from django.contrib import admin
from task_management.models import RecentAction




class RecentActionAdmin(admin.ModelAdmin):
    list_display = ('message', 'state', 'creation_date', 'owner')    
    list_filter = ['creation_date']




admin.site.register(RecentAction, RecentActionAdmin)
