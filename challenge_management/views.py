from django.shortcuts import render_to_response
from django.template import RequestContext
from challenge_management.models import ChallengeForm
from django.forms.models import modelformset_factory



def add_challenge_v(request):
    form = ChallengeForm()
    return render_to_response('ChallengeManagement/add_challenge.xhtml',
                              { "form": form, "title" : "Add Challenge" },
                              context_instance = RequestContext(request));