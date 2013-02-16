from django.db import models
from django.contrib.auth.models import User




class ActionState(models.Model):
    name = models.CharField( max_length = 20 )

    def __unicode__(self):
        return self.name




class RecentAction(models.Model):
    owner = models.ForeignKey( User )
    creation_date = models.DateTimeField( auto_now_add = True )
    message = models.CharField( max_length = 100 )
    state = models.ForeignKey( ActionState )
    
    def __unicode__(self):
        return self.message