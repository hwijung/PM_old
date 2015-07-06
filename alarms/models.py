from django.db import models
from django.contrib.auth.models import User

class Alarm(models.Model):
    user = models.ForeignKey( User )
    
    title = models.CharField( max_length = 32 )
    site = models.CharField( max_length = 512 )
    
    activated = models.BooleanField( default = True )
    
    @staticmethod
    def save_with_form(user, form):
        # title
        title = form.cleaned_data['title']
        
        # extract url from tagged url in parser
        url_with_tag =  form.cleaned_data['site']
        site = url_with_tag[url_with_tag.find("http"):]
 
        # Create or get Entry
        alarm, created = Alarm.objects.get_or_create( user = user, 
                                                      title = title,
                                                      site = site )
        
        # Save entry to database
        alarm.save()
        
        # Create or get Keyword
        search_words = form.cleaned_data['keyword'].split(',')
        
        for word in search_words:
            keyword, created = SearchWord.objects.get_or_create(search_word = word)
            keyword.alarms.add(alarm)
    
        return alarm
    
    def __str__ (self):
        return '%s, %s, %s' % ( self.user.username, self.title, self.site)
    
    class Admin:
        pass 
        
class SearchWord(models.Model):
    search_word = models.CharField( max_length = 64, unique = True )
    alarms = models.ManyToManyField( Alarm )
    
    def __str__(self):
        return self.word
    
class Site(models.Model):
    site = models.URLField()
    def __str__(self):
        return self.url
    
    class Admin:
        pass
    
class Setting(models.Model):
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