from django.db import models
from django.contrib.auth.models import User

class Alarms(models.Model):
    user = models.ForeignKey( User )
    
    title = models.CharField( max_length = 32, unique = True )
    site = models.CharField( max_length = 512 )
    
    activated = models.BooleanField( default = True )
    
    def __str__ (self):
        return '%s, %s, %s' % ( self.user.username, self.title, self.site)
    
    class Admin:
        pass
        
class SearchWords(models.Model):
    search_word = models.CharField( max_length = 64, unique = True )
    alarms = models.ManyToManyField( Alarms )
    
    def __str__(self):
        return self.word
    
class Sites(models.Model):
    site = models.URLField()
    def __str__(self):
        return self.url
    
    class Admin:
        pass
    
class Settings(models.Model):
    # if alarm is turn on or off
    activated = models.IntegerField(default = 1)
    
    # Other notification options
    noti_email = models.BooleanField(default=True)
    noti_SMS = models.BooleanField(default=False)
    noti_push = models.BooleanField(default=False)   
    
    user = models.ForeignKey ( User )
    class Admin:
        pass
    
'''
class Notifications(models.Model):
    datetime = models.DateTimeField()
    noti_method = models.CharField( max_length = 8 )
    site = models.CharField( max_length = 32 )
    url = models.URLField()
    search_word = models.CharField( max_length = 64)    
    user = models.ForeignKey( User )
    class Admin:
        pass        
'''        