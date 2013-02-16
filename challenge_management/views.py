from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from challenge_management.forms import ChallengeForm
from challenge_management.models import Challenge
from challenge_management.models import Compiler
from challenge_management.models import Program
from task_management.models import RecentAction
from task_management.models import ActionState
from task_management.tasks import compile_challenge
from IntelliGame.settings import CHALLENGES_ROOT

import os




def upload_file(directory, file_to_upload):
    with open(directory + file_to_upload.name, 'wb+') as destination:
        for chunk in file_to_upload.chunks():
            destination.write(chunk)




@login_required
def add_challenge_v(request):
    form = ChallengeForm()
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            # create directory for a challenge
            directory = CHALLENGES_ROOT + form.data["title"].replace(" ", "_") + "/"
            os.makedirs(directory)
            # upload files
            upload_file(directory, request.FILES['source_file'])
            upload_file(directory, request.FILES['description_file'])
            # gather data
            program = Program(compiler = Compiler.objects.get(id = form.data["compiler"]),
                              source_file = directory + request.FILES['source_file'].name )
            program.save()
            challenge = Challenge ( title = form.data["title"],
                                    directory = directory,
                                    short_description = form.data["short_description"],
                                    description_file = directory + request.FILES['description_file'].name,
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