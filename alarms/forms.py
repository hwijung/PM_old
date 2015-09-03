import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm ( forms.Form ):
    username = forms.CharField ( label = 'Username', max_length = 30 )
    email = forms.EmailField ( label = "Email" )
    password1 = forms.CharField ( 
        label = 'Password',
        widget = forms.PasswordInput () ,
        help_text = 'Input your password.'
    )
    
    password2 = forms.CharField ( 
        label = 'Password2', 
        widget = forms.PasswordInput ()
     )
     
    def clean_username (self):
        username = self.cleaned_data['username']
        if not re.search( r'^\w+$', username ):
            raise forms.ValidationError ( 'Username can only contain alphanumeric characters and the unserscore.')
        
        try:
            User.objects.get ( username = username )
        except ObjectDoesNotExist:
            return username
            
        raise forms.ValidationError ( 'Username is already taken.' )
    
    def clean_password2 (self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            
            if password1 == password2:
                return password2
            raise forms.ValidationError ( 'Passwords do not match.' )
        
class AlarmSaveForm ( forms.Form ):
    title = forms.SlugField ( label = 'Title', widget = forms.TextInput ( attrs = { 'size': 32 }))
    site = forms.CharField ( label = 'Site', widget = forms.TextInput ( attrs = { 'size': 128 }))
    # activated = forms.BooleanField( label = 'Activated' )
    keyword = forms.CharField ( label = 'Keyword', widget = forms.TextInput ( attrs = { 'size': 32 }))
    
class AlarmEditForm ( forms.Form ):
    title = forms.SlugField ( label = 'Title', widget = forms.TextInput ( attrs = { 'size': 32 }))
    site = forms.CharField ( label = 'Site', widget = forms.TextInput ( attrs = { 'size': 128 }))
    # activated = forms.BooleanField( label = 'Activated' )
    keyword = forms.CharField ( label = 'Keyword', widget = forms.TextInput ( attrs = { 'size': 32 }))