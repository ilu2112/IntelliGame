'''
Basically this module uses models:
    django.contrib.auth.models.User
'''

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User
import re




def append_error(form, key, error):
    form.errors[key] = form.errors.get(key, ErrorList())
    form.errors[key].append(error)
    
    
    
    
class UserForm(forms.Form):

    username = forms.CharField(max_length = 30, required = True)
    first_name = forms.CharField(max_length = 30, required = False)
    last_name = forms.CharField(max_length = 30, required = False)
    email = forms.EmailField(required = False, label = "e-mail")
    passwd = forms.CharField(widget = forms.PasswordInput(render_value = True), label = "Password")
    r_passwd = forms.CharField(widget = forms.PasswordInput, label = "Repeat password")


    def is_valid(self):
        succ = forms.Form.is_valid(self)
        # Are passwords equal?
        if self.data["passwd"] != self.data["r_passwd"]:
            append_error(self, "passwd", "Passwords don't match.")
            succ = False
        # Is username valid?
        if not re.match("^[a-zA-Z0-9_@+.-]{1,30}$", self.data["username"]):
            append_error(self, "username", "Invalid format (only letters, digits and signs: @ - . _ +).")
            succ = False
        else:
            # Is username unique?
            if User.objects.filter(username = self.data["username"]).exists():
                append_error(self, "username", "Username '%s' is already in use." % self.data["username"])
                succ = False
        return succ


    def create_user(self):
        user = User.objects.create_user(self.data["username"], self.data["email"], self.data["passwd"])
        user.first_name = self.data["first_name"]
        user.last_name = self.data["last_name"]
        user.save()




class ChangePasswdForm(forms.Form):
    old_passwd = forms.CharField(widget = forms.PasswordInput(), label = "Old password")
    new_passwd = forms.CharField(widget = forms.PasswordInput(), label = "New password")
    r_passwd = forms.CharField(widget = forms.PasswordInput(), label = "Repeat new password")


    def is_valid(self):
        succ = forms.Form.is_valid(self)
        # Are passwords equal?
        if self.data["new_passwd"] != self.data["r_passwd"]:
            append_error(self, "new_passwd", "Passwords don't match.")
            succ = False
        return succ

    
    def check_passwd(self, user):
        if user.check_password(self.data["old_passwd"]):
            return True
        else:
            append_error(self, "old_passwd", "Wrong password.")
            return False
        
        
    def save(self, user):
        user.set_password(self.data["new_passwd"])
        user.save()    
        
        
        
        
class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 30, required = False)
    last_name = forms.CharField(max_length = 30, required = False)
    email = forms.EmailField(required = False, label = "e-mail")
    
    
    def save(self, user):
        user.first_name = self.data["first_name"]
        user.last_name = self.data["last_name"]
        user.email = self.data["email"]
        user.save()