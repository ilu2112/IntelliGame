from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.models import User



class Compiler(models.Model):
    name = models.CharField(max_length = 50, 
                            blank = False)
    compile_command = models.CharField(max_length = 100, 
                                       blank = False,
                                       help_text = """Please use {source_file} and %{binary_file} tags (second one if needed). <br />
                                                      Example 1: g++ {source_file} -o {binary_file} <br />
                                                      Example 2: javac {source_file}""")
    run_command = models.CharField(max_length = 100, 
                                   blank = False,
                                   help_text = """Please use {binary_file} tag.<br />
                                                  Example 1: ./{binary_file} <br />
                                                  Example 2: java {binary_file} """)
    binary_extension = models.CharField(max_length = 10, 
                                        blank = True,
                                        help_text = """ Example 1: class for java compiler <br />
                                                        Example 2: pyc for python compiler <br />
                                                        Example 3: leave blank for c++ compiler""")
    ignore_binary_extension = models.BooleanField(help_text = """Enable this when run command ignores binary file's extension. <br />
                                                                 Example: java Main, NOT java Main.class.""")
    
    def __unicode__(self):
        return self.name



class Program(models.Model):
    source_file = models.FileField( upload_to = 'tmp/' )
    binary_file = models.FileField( upload_to = 'tmp/', blank = True )
    compiler = models.ForeignKey( 'Compiler' )
    
    def __unicode__(self):
        return self.source_file.name
    
    
    

class Challenge(models.Model):
    title = models.CharField( max_length = 50, unique = True )
    creation_date = models.DateField( auto_now_add = True )
    directory = models.CharField( max_length = 70 )
    short_description = models.TextField()
    description_file = models.FileField( upload_to = 'tmp/' )
    owner = models.ForeignKey( User )
    bots_per_game = models.IntegerField()
    game_duration = models.IntegerField()
    judging_program = models.OneToOneField( 'Program' )
    
    def __unicode__(self):
        return self.title




class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date', 'owner')    
    list_filter = ['creation_date']




class ChallengeForm(ModelForm):
    source_file = forms.FileField()
    compiler = forms.ModelChoiceField( queryset = Compiler.objects.all() )
    
    class Meta:
        model = Challenge
        exclude = ['judging_program', 'owner', 'directory', 'creation_date']