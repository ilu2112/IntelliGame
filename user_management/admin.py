from django.contrib import admin
from user_management.models import RecentAction
from user_management.models import ActionState
from user_management.models import RecentActionAdmin


admin.site.register(RecentAction, RecentActionAdmin)
admin.site.register(ActionState)