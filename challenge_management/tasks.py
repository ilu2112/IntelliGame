from celery import task
from challenge_management.models import ChallengeForm



@task()
def compile_challenge(challenge):
    # recent action = "in queue"
    # recent action = "in progress"
    # recent action = "success"
    # recent action = "error"
    return challenge.title