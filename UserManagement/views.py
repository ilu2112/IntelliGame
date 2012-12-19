from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from UserManagement.models import UserForm




def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.create_user()
            return HttpResponseRedirect('../successful/')
    return render_to_response('UserManagement/register.xhtml',
                              { "form": form, "title" : "Register" },
                              context_instance = RequestContext(request));



def successful(request):
    return render_to_response('base.xhtml',
                              {"title" : "Success"},
                              context_instance = RequestContext(request));



def login_v(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['passwd']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../successful/')
            else:
                return render_login_v(request, "Account disabled.")
        else:
            return render_login_v(request, "Invalid username and/or password.")
    return render_login_v(request, None)



def render_login_v(request, error_msg):
    return render_to_response('UserManagement/login.xhtml',
                              { "title" : "Log in", "error_msg" : error_msg },
                              context_instance = RequestContext(request));



def logout_v(request):
    logout(request)
    return HttpResponseRedirect('../successful/')



@login_required
def show_profile(request):
    return render_to_response('UserManagement/profile.xhtml',
                              { "title" : "Profile details" },
                              context_instance = RequestContext(request));
