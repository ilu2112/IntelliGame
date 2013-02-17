import shutil

from django.db import models
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
    creation_date = models.DateTimeField( auto_now_add = True )
    directory = models.CharField( max_length = 255 )
    short_description = models.TextField()
    description_file = models.FileField( upload_to = 'tmp/' )
    owner = models.ForeignKey( User )
    bots_per_game = models.IntegerField()
    game_duration = models.IntegerField( verbose_name="Game's duration [s]" )
    judging_program = models.OneToOneField( 'Program' )

    def __unicode__(self):
        return self.title

    def delete(self):
        shutil.rmtree(self.directory)
        self.judging_program.delete()




class Bot(models.Model):
    name = models.CharField( max_length = 50 )
    playing_program = models.OneToOneField( 'Program' )
    directory = models.CharField( max_length = 255 )
    creation_date = models.DateTimeField( auto_now_add = True )
    owner = models.ForeignKey( User )
    target_challenge = models.ForeignKey( Challenge )
    played_games = models.PositiveIntegerField( default = 0 )
    total_score = models.IntegerField( default = 0 )

    def __unicode__(self):
        return self.name
    
    def delete(self):
        shutil.rmtree(self.directory)
        self.playing_program.delete()