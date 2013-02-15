from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from task_management.models import RecentAction


@login_required
def recent_actions_v(request):
    recent_actions = RecentAction.objects.filter( owner = request.user ).order_by( "-creation_date")
    return render_to_response('TaskManagement/recent_actions.xhtml',
                              { "recent_actions": recent_actions, "title" : "Recent actions" },
                              context_instance = RequestContext(request));