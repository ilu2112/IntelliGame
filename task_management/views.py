from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from task_management.models import RecentAction




@login_required
def my_actions_v(request):
    recent_actions = RecentAction.objects.filter( owner = request.user ).order_by( "-creation_date")
    page = request.GET.get('page')
    paginator = Paginator(recent_actions, 25)
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)
    return render_to_response('TaskManagement/my_actions.xhtml',
                              { "recent_actions": actions, "title" : "My actions" },
                              context_instance = RequestContext(request));




def recent_actions_v(request):
    recent_actions = RecentAction.objects.all().order_by( "-creation_date")
    page = request.GET.get('page')
    paginator = Paginator(recent_actions, 25)
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)
    return render_to_response('TaskManagement/recent_actions.xhtml',
                              { "recent_actions": actions, "title" : "Recent actions" },
                              context_instance = RequestContext(request));