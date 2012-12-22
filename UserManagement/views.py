from django.shortcuts import render_to_response

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from UserManagement.models import UserForm
from UserManagement.models import ChangePasswdForm
from UserManagement.models import EditProfileForm
from UserManagement.models import append_error



def register_v(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.create_user()
            return HttpResponseRedirect('../successful/')
    return render_to_response('UserManagement/register.xhtml',
                              { "form": form, "title" : "Register" },
                              context_instance = RequestContext(request));



def successful_v(request):
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



@login_required
def logout_v(request):
    logout(request)
    return HttpResponseRedirect('../successful/')



@login_required
def show_profile_v(request):
    return render_to_response('UserManagement/show_profile.xhtml',
                              { "title" : "Profile details" },
                              context_instance = RequestContext(request));



@login_required
def change_passwd_v(request):
    form = ChangePasswdForm()
    if request.method == 'POST':
        form = ChangePasswdForm(request.POST)
        if form.is_valid() and form.check_passwd(request.user):
            form.save(request.user)
            return HttpResponseRedirect('../successful/')
    return render_to_response('UserManagement/change_passwd.xhtml',
                              { "form": form, "title" : "Change password" },
                              context_instance = RequestContext(request));



@login_required
def edit_profile_v(request):
    form = EditProfileForm(initial = {'first_name' : request.user.first_name,
                                     'last_name' : request.user.last_name,
                                     'email' : request.user.email})
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('../successful/')
    return render_to_response('UserManagement/edit_profile.xhtml',
                              { "form": form, "title" : "Edit profile" },
                              context_instance = RequestContext(request));
