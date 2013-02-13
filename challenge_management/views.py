from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from challenge_management.models import ChallengeForm
from challenge_management.models import Challenge
from challenge_management.models import Compiler
from challenge_management.models import Program
from user_management.models import RecentAction
from user_management.models import ActionState
from challenge_management.tasks import compile_challenge
from IntelliGame.settings import CHALLENGES_ROOT

import os



def upload_file(dir, file):
    with open(dir + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)



@login_required
def add_challenge_v(request):
    form = ChallengeForm()
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            # create directory for a challenge
            dir = CHALLENGES_ROOT + form.data["title"].replace(" ", "_") + "/"
            os.makedirs(dir)
            # upload files
            upload_file(dir, request.FILES['source_file'])
            upload_file(dir, request.FILES['description_file'])
            # gather data
            program = Program(compiler = Compiler.objects.get(id = form.data["compiler"]),
                              source_file = dir + request.FILES['source_file'].name )
            program.save()
            challenge = Challenge ( title = form.data["title"],
                                    directory = dir,
                                    short_description = form.data["short_description"],
                                    description_file = dir + request.FILES['description_file'].name,
                                    owner = request.user,
                                    bots_per_game = form.data["bots_per_game"],
                                    game_duration = form.data["game_duration"],
                                    judging_program = program)
            challenge.save()
            # queue compilation
            recent_action = RecentAction(owner = request.user,
                                         message = "Challenge validation: " + challenge.title,
                                         state = ActionState.objects.get(name = 'IN_QUEUE'))
            recent_action.save()
            compile_challenge.delay(challenge, recent_action)
            return HttpResponseRedirect('/successful/')
    return render_to_response('ChallengeManagement/add_challenge.xhtml',
                              { "form": form, "title" : "Add Challenge" },
                              context_instance = RequestContext(request));