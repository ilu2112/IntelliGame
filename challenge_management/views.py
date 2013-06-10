from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from challenge_management.forms import BotForm
from challenge_management.forms import ChallengeForm
from challenge_management.models import Bot
from challenge_management.models import Challenge
from challenge_management.models import Compiler
from challenge_management.models import Program
from task_management.models import RecentAction
from task_management.models import ActionState
from task_management.tasks import compile_challenge
from task_management.tasks import compile_bot
from task_management.tasks import enqueue_bots_battles
from IntelliGame.settings import CHALLENGES_ROOT

from celery import chain

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




@login_required
def add_bot_v(request, form = 0):
    if form == 0:
        form = BotForm()
    if request.method == 'POST':
        form = BotForm(request.POST, request.FILES)
        if form.is_valid():
            # get challenge
            challenge = Challenge.objects.get( id = form.data["target_challenge"] )
            # create directory for a bot
            directory = challenge.directory + "bots/" + form.data["name"].replace(" ", "_") + "/"
            os.makedirs(directory)
            # upload source file
            upload_file(directory, request.FILES['source_file'])
            # gather data
            program = Program(compiler = Compiler.objects.get(id = form.data["compiler"]),
                              source_file = directory + request.FILES['source_file'].name )
            program.save()
            bot = Bot( name = form.data["name"], 
                       playing_program = program,
                       directory = directory,
                       owner = request.user,
                       target_challenge = challenge)
            # delay compilation
            recent_action = RecentAction(owner = request.user,
                                         message = "Bot validation: " + bot.name
                                                    + " (for challenge: " + challenge.title + ")",
                                         state = ActionState.objects.get(name = 'IN_QUEUE'))
            recent_action.save()
            chain(compile_bot.si(bot, recent_action), enqueue_bots_battles.si(bot)).apply_async() 
            return HttpResponseRedirect('/successful/')
    return render_to_response('ChallengeManagement/add_bot.xhtml',
                              { "form": form, "title" : "Add Bot" },
                              context_instance = RequestContext(request));




def browse_challenges_v(request):
    challenges = Challenge.objects.all()
    bots_count = dict()
    for challenge in challenges:
        bots_count[challenge.id] = Bot.objects.filter(target_challenge = challenge).count()
    return render_to_response('ChallengeManagement/browse_challenges.xhtml',
                              { "challenges" : challenges, "bots_count" : bots_count,
                                "title" : "Browse challenges" },
                              context_instance = RequestContext(request));




def challenge_details_v(request, challenge_id):
    challenge = Challenge.objects.get( id = challenge_id )
    return render_to_response('ChallengeManagement/challenge_details.xhtml',
                              { "challenge" : challenge, "title" : challenge.title },
                              context_instance = RequestContext(request));




def download_challenge_desc_v(request, challenge_id):
    challenge = Challenge.objects.get( id = challenge_id )
    filename = challenge.description_file.name
    response = HttpResponse( mimetype="application/" + os.path.splitext(filename)[1][1:] )
    response['Content-Disposition'] = 'filename="{filename}"'.format(filename = filename.split('/')[-1])
    for chunk in challenge.description_file.chunks():
        response.write(chunk)
    return response




@login_required
def redirect_add_bot_v(request, challenge_id):
    form = BotForm( initial = {'target_challenge' : challenge_id})
    form.data['target_challenge'] = challenge_id
    print challenge_id
    return add_bot_v(request, form)