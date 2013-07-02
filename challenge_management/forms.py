from django import forms
from django.forms import ModelForm

from IntelliGame.settings import CHALLENGES_ROOT
from IntelliGame.utils import upload_file
from challenge_management.models import Bot
from challenge_management.models import Compiler
from challenge_management.models import Challenge
from user_management.forms import append_error

import os




class ChallengeForm(ModelForm):
    source_file = forms.FileField()
    compiler = forms.ModelChoiceField( queryset = Compiler.objects.all() )

    class Meta:
        model = Challenge
        exclude = ['judging_program', 'owner', 'directory', 'creation_date', 'locked', 'to_delete']

    def is_valid(self):
        succ = forms.ModelForm.is_valid(self)
        if self.data["title"] != "":
            directory = CHALLENGES_ROOT + self.data["title"].replace(" ", "_") + "/"
            if os.path.exists(directory):
                succ = False
                append_error(self, 'title', 'Challenge with this Title already exists.') 
        return succ




class BotForm(ModelForm):
    source_file = forms.FileField()
    compiler = forms.ModelChoiceField( queryset = Compiler.objects.all() )

    class Meta:
        model = Bot
        exclude = ['playing_program', 'owner', 'creation_date', 'directory', 'locked', 'to_delete']

    def is_valid(self):
        succ = forms.ModelForm.is_valid(self)
        if self.data["name"] != "" and self.data["target_challenge"] != "":
            challenge = Challenge.objects.get( id = self.data["target_challenge"] )
            directory = challenge.directory + "bots/" + self.data["name"].replace(" ", "_") + "/"
            if os.path.exists(directory):
                succ = False
                append_error(self, 'name', 'Bot with this Name already exists.') 
        return succ




class EditChallengeForm(forms.Form):
    short_description = forms.CharField( widget = forms.Textarea, required = False)
    description_file = forms.FileField( required = False )
    
    def save(self, request, challenge):
        challenge.short_description = self.data["short_description"]
        if request.FILES.has_key("description_file"):
            os.remove(challenge.description_file.name)
            upload_file(challenge.directory, request.FILES["description_file"])
            challenge.description_file = challenge.directory + request.FILES['description_file'].name
        challenge.save()