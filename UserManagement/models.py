'''
Basically this module uses models:
    django.contrib.auth.models.User
'''

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User
import re


class UserForm(forms.Form):

    username = forms.CharField(max_length = 30, required = True)
    first_name = forms.CharField(max_length = 30, required = False)
    last_name = forms.CharField(max_length = 30, required = False)
    email = forms.EmailField(required = False, label = "e-mail")
    passwd = forms.CharField(widget = forms.PasswordInput(render_value = True), label = "Password")
    r_passwd = forms.CharField(widget = forms.PasswordInput, label="Repeat password")


    def is_valid(self):
        succ = forms.Form.is_valid(self)
        # Are passwords equal?
        if self.data["passwd"] != self.data["r_passwd"]:
            self.append_error("passwd", "Passwords don't match")
            succ = False
        # Is username valid?
        if not re.match("^[a-zA-Z0-9_@+.-]{1,30}$", self.data["username"]):
            self.append_error("username", "Invalid format (only letters, digits and signs: @ - . _ +)")
            succ = False
        else:
            # Is username unique?
            if User.objects.filter(username = self.data["username"]).exists():
                self.append_error("username", "Username '%s' is already in use" % self.data["username"])
                succ = False
        return succ


    def append_error(self, key, error):
        self.errors[key] = self.errors.get(key, ErrorList())
        self.errors[key].append(error)


    def create_user(self):
        user = User.objects.create_user(self.data["username"], self.data["email"], self.data["passwd"])
        user.first_name = self.data["first_name"]
        user.last_name = self.data["last_name"]
        user.save()
