import shutil
import os

from django.db import models
from django.contrib.auth.models import User




class Compiler(models.Model):
    name = models.CharField(max_length = 50, 
                            blank = False)
    compile_command = models.CharField(max_length = 100, 
                                       blank = False,
                                       help_text = """Please use {source_file}, {binary_file}, {directory} tags. <br />
                                                      Example 1: g++ {directory}/{source_file} -o {directory}/{binary_file}<br />
                                                      Example 2: javac {directory}/{source_file}""")
    run_command = models.CharField(max_length = 100, 
                                   blank = False,
                                   help_text = """Please use {binary_file} and {directory} tags. <br />
                                                  Example 1: {directory}/{binary_file} (for plain binary files}<br />
                                                  Example 2: java -cp {directory}/ {binary_file}""")
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

    def get_compile_command(self):
        source = os.path.split(self.source_file.path)[1]
        binary = os.path.splitext(source)[0]
        dir = os.path.dirname(self.source_file.path)
        if (self.compiler.ignore_binary_extension == False and self.compiler.binary_extension != None):
            binary = binary + '.' + self.compiler.binary_extension
        command = self.compiler.compile_command.format(source_file = source, binary_file = binary, directory = dir)
        return command

    def get_run_command(self):
        dir = os.path.dirname(self.binary_file.path)
        binary = self.binary_file.path.split("/")[-1]
        command = self.compiler.run_command.format(binary_file = binary, directory = dir)
        return command




class Challenge(models.Model):
    title = models.CharField( max_length = 50, unique = True )
    creation_date = models.DateTimeField( auto_now_add = True )
    directory = models.CharField( max_length = 255 )
    short_description = models.TextField()
    description_file = models.FileField( upload_to = 'tmp/' )
    owner = models.ForeignKey( User )
    bots_per_game = models.PositiveIntegerField()
    game_duration = models.PositiveIntegerField( verbose_name="Game's duration [s]" )
    memory_usage = models.PositiveIntegerField( verbose_name="Memory per bot [Mb]" )
    judging_program = models.OneToOneField( 'Program' )
    locked = models.BooleanField( default = False )
    to_delete = models.BooleanField( default = False )
    
    def __unicode__(self):
        return self.title

    def delete(self):
        # delete bots
        bots = Bot.objects.filter( target_challenge = self )
        for bot in bots:
            bot.delete()
        shutil.rmtree(self.directory)
        self.judging_program.delete()




class Bot(models.Model):
    name = models.CharField( max_length = 50 )
    playing_program = models.OneToOneField( 'Program' )
    directory = models.CharField( max_length = 255 )
    creation_date = models.DateTimeField( auto_now_add = True )
    owner = models.ForeignKey( User )
    target_challenge = models.ForeignKey( Challenge )
    locked = models.BooleanField( default = False )
    to_delete = models.BooleanField( default = False )

    def __unicode__(self):
        return self.name
    
    def delete(self):
        # delete all battles
        own_battle_results = BattleResult.objects.filter( bot = self ).all()
        for own_b_r in own_battle_results:
            battle = own_b_r.battle
            BattleResult.objects.filter( battle = battle ).all().delete()
            battle.delete()
        # delete directory
        shutil.rmtree(self.directory)
        self.playing_program.delete()




class Battle(models.Model):
    challenge = models.ForeignKey( Challenge )
    creation_date = models.DateTimeField( auto_now_add = True )




class BattleResult(models.Model):
    battle = models.ForeignKey( Battle )
    bot = models.ForeignKey( Bot )
    comment = models.CharField( max_length = 128 )
    score = models.IntegerField()