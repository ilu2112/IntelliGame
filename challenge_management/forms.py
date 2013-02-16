from django import forms
from django.forms import ModelForm

from challenge_management.models import Compiler
from challenge_management.models import Challenge




class ChallengeForm(ModelForm):
    source_file = forms.FileField()
    compiler = forms.ModelChoiceField( queryset = Compiler.objects.all() )
    
    class Meta:
        model = Challenge
        exclude = ['judging_program', 'owner', 'directory', 'creation_date']