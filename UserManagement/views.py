from django.shortcuts import render_to_response
from UserManagement.models import UserForm
from django.template import RequestContext
from django.http import HttpResponseRedirect


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.create_user()
            return HttpResponseRedirect('successful/')
    return render_to_response('UserManagement/register.xhtml',
                              { "form": form, "title" : "Register" },
                              context_instance = RequestContext(request));


def successful(request):
    return render_to_response('UserManagement/successful.xhtml')
