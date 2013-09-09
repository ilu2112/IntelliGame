import os
import subprocess
from celery import task
from subprocess import CalledProcessError
from itertools import combinations

from task_management.models import ActionState
from challenge_management.models import Bot
from challenge_management.models import Battle
from challenge_management.models import BattleResult
from sandbox_mock import SandBox



def compile_program(program):
    # prepare compilation command
    command = program.get_compile_command()
    
    # prepare binary output file
    binary = os.path.splitext(program.source_file.path)[0]
    compiler = program.compiler
    if (compiler.ignore_binary_extension == False and compiler.binary_extension != None):
        binary = binary + '.' + compiler.binary_extension
    
    # compile
    subprocess.check_output(command.split(' '), stderr = subprocess.STDOUT)
    program.binary_file = binary
    program.save()




@task()
def compile_challenge(challenge, recent_action):
    # recent action = "in progress"
    recent_action.state = ActionState.objects.get(name = 'IN_PROGRESS')
    recent_action.save()
        
    try:
        compile_program(challenge.judging_program)
        # recent action = "success"
        recent_action.state = ActionState.objects.get(name = 'SUCCESS')
        recent_action.save()
        challenge.save()
        return 'Challenge success: ' + challenge.title
    except CalledProcessError:
        # recent action = "error"
        recent_action.state = ActionState.objects.get(name = 'ERROR')
        recent_action.save()
        challenge.delete()

    return 'Challenge error: ' + challenge.title




@task()
def compile_bot(bot, recent_action):
    # recent action = "in progress"
    recent_action.state = ActionState.objects.get(name = 'IN_PROGRESS')
    recent_action.save()
        
    try:
        compile_program(bot.playing_program)
        # recent action = "success"
        recent_action.state = ActionState.objects.get(name = 'SUCCESS')
        recent_action.save()
        bot.save()
        return 'Bot success: ' + bot.name
    except CalledProcessError:
        # recent action = "error"
        recent_action.state = ActionState.objects.get(name = 'ERROR')
        recent_action.save()
        bot.delete()

    return 'Bot error: ' + bot.name




@task()
def enqueue_bots_battles(bot):
    if Bot.objects.filter(name = bot.name, target_challenge = bot.target_challenge).exists():
        # get target challenge
        challenge = bot.target_challenge
        # gather all possible opponents
        possible_opponents = set( combinations(Bot.objects.filter(target_challenge = challenge).exclude(pk = bot.pk),
                                  challenge.bots_per_game - 1))
        # delay every possible battle
        for opponents in possible_opponents:
            bots = list(opponents)
            bots.append(bot)
            run_battle.delay(bots, challenge)




@task()
def run_battle(bots, challenge):
    # generate run commands
    judge_exec_command = challenge.judging_program.get_run_command()
    bots_exec_commands = []
    for bot in bots:
        bots_exec_commands.append(bot.playing_program.get_run_command())
    # run sandbox
    sb = SandBox(judge_exec_command, bots_exec_commands, challenge.game_duration, challenge.memory_usage)
    scores = sb.run()
    # save results
    battle = Battle(challenge = challenge)
    battle.save()
    for i in range(0, bots.__len__()):
        battle_result = BattleResult(battle = battle,
                                     bot = bots[i],
                                     comment = scores[i][1],
                                     score = scores[i][0])
        battle_result.save()




@task()
def delete_bot(bot, recent_action):
    # save new state
    recent_action.state = ActionState.objects.get(name = 'IN_PROGRESS')
    recent_action.save()
    # try to delete bot
    bot = Bot.objects.get( id = bot.id )
    if bot.locked == False:
        # delete bot
        bot.delete()
        # update state
        recent_action.state = ActionState.objects.get(name = 'SUCCESS')
        recent_action.save()
    else:
        # delay
        delete_bot.delay(bot, recent_action)




@task()
def delete_challenge(challenge, recent_action):
    # save new state
    recent_action.state = ActionState.objects.get(name = 'IN_PROGRESS')
    recent_action.save()
    # check if all bots are available to delete
    bots = Bot.objects.filter( target_challenge = challenge )
    for bot in bots:
        if bot.locked == True:
            delete_challenge.delay(challenge, recent_action)
            return
    # everything is free, I can delete this challenge
    challenge.delete()
    # update state
    recent_action.state = ActionState.objects.get(name = 'SUCCESS')
    recent_action.save()