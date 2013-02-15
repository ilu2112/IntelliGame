import os
import subprocess
from celery import task
from subprocess import CalledProcessError

from task_management.models import ActionState




def compile_program(program):
    # prepare compilation command
    compiler = program.compiler
    source = program.source_file.path
    binary = os.path.splitext(program.source_file.path)[0]
    if (compiler.ignore_binary_extension == False):
        binary = binary + '.' + compiler.binary_extension
    command = compiler.compile_command.format(source_file = source, binary_file = binary)
    
    # compile
    subprocess.check_output(command.split(' '), stderr = subprocess.STDOUT)




@task()
def compile_challenge(challenge, recent_action):
    # recent action = "in progress"
    recent_action.state = ActionState.objects.get(name = 'IN_PROGRESS')
    recent_action.save()
        
    try:
        compile_program(challenge.judging_program)
        # subprocess.check_output(command.split(' '), stderr = subprocess.STDOUT)
        # recent action = "success"
        recent_action.state = ActionState.objects.get(name = 'SUCCESS')
        recent_action.save()
        return 0
    except CalledProcessError:
        # recent action = "error"
        recent_action.state = ActionState.objects.get(name = 'ERROR')
        recent_action.save()
        challenge.delete()

    return 1