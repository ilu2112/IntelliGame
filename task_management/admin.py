from django.contrib import admin
from task_management.models import RecentAction
from task_management.models import ActionState
from task_management.models import RecentActionAdmin




admin.site.register(RecentAction, RecentActionAdmin)
admin.site.register(ActionState)