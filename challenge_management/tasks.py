import os
import subprocess
from celery import task
from subprocess import CalledProcessError

from challenge_management.models import ChallengeForm
from user_management.models import RecentAction
from user_management.models import ActionState




@task()
def compile_challenge(challenge, recent_action):
    # recent action = "in progress"
    recent_action.state = ActionState.objects.get(name = 'IN_PROGRESS')
    recent_action.save()
    
    # prepare compilation command
    compiler = challenge.judging_program.compiler
    source = challenge.judging_program.source_file.path
    binary = os.path.splitext(challenge.judging_program.source_file.path)[0]
    if (compiler.ignore_binary_extension == False):
        binary = binary + '.' + compiler.binary_extension
    command = compiler.compile_command.format(source_file = source, binary_file = binary)
    
    # compile
    try:
        subprocess.check_output(command.split(' '), stderr = subprocess.STDOUT)
        # recent action = "success"
        recent_action.state = ActionState.objects.get(name = 'SUCCESS')
        recent_action.save()
        return 0
    except CalledProcessError as err:
        # recent action = "error"
        recent_action.state = ActionState.objects.get(name = 'ERROR')
        recent_action.save()
        challenge.delete()
        
    return 1