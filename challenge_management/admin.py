from django.contrib import admin
from challenge_management.models import Compiler
from challenge_management.models import Program
from challenge_management.models import Challenge
from challenge_management.models import ChallengeAdmin


admin.site.register(Compiler)
admin.site.register(Program)
admin.site.register(Challenge, ChallengeAdmin)