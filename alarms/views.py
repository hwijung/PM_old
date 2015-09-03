from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email

from django.db import IntegrityError
from django.contrib.auth.models import User

from alarms.forms import RegistrationForm, AlarmEditForm, AlarmSaveForm
from alarms.models import Alarm, Setting, SearchWord
from common.PPparser import PPparser

import json 
import logging.config
import sys

# Get an instance of a logger
LOGGING = { 
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
logging.config.dictConfig(LOGGING)

# Main View
def home(request):
    variables = RequestContext( request )
    return render_to_response ( 'index.html', variables )

# Login View
def login_view(request):
    logout(request)
    # Initialize variables
    
    username = password = ''
    next_page = '/'
    
    if request.GET:
        next_page = request.GET['next']

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # if there were redirect page in URL..
                return HttpResponseRedirect(next_page)
        else:
            return render_to_response('login.html', {'error': True}, context_instance = RequestContext(request))

    return render_to_response('login.html', {'next': next_page}, context_instance = RequestContext(request))

# Logout
def logout_view ( request ):
    logout ( request )
    return HttpResponseRedirect ( '/' )
 
# sign up view
def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # logging.info(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            # logging.info( "" + username + password + email )
            if username:
                user = User.objects.create_superuser(username, email, password)
                # user_setting = UserSetting.objects.create(beat=True, user = user)
                # user_setting.save()
                return HttpResponseRedirect('/signup/success')
            else:
                return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    variables = RequestContext( request, {'form': form} )
    return render_to_response( 'signup.html', variables )	

# alarms view
@login_required
def alarms_view(request): 
    username = request.user.username
    user = get_object_or_404 ( User, username = username )

    # get alarms of login user
    my_alarms = Alarm.objects.filter( user = user )
    
    # Put search words into alarms
    for alarm in my_alarms:
        alarm.searchword_str = SearchWord.search_word_to_str(alarm.searchword_set.all())
        
    try:
        setting = Setting.objects.get( user = user )
    except ObjectDoesNotExist:
        setting = Setting.objects.create(user = user)

    variables = RequestContext( request, { 'username': username, 'noa': len(my_alarms), 'alarms': my_alarms, 'activated': setting.activated } )

    return render_to_response('alarms.html', variables)

# alarm create view
@login_required
def alarm_create_view(request):
    ajax = request.GET.has_key ( 'ajax' )
    variables = RequestContext( request, { 'username': request.user.username } )
    
    if request.method == 'POST':

        form = AlarmSaveForm ( request.POST )

        if form.is_valid():
            try:
                Alarm.save_with_form(request.user, form)
                return HttpResponseRedirect ( '/alarms/' )

            # duplicated Title exception
            except IntegrityError as e:
                form.site.errors = 'Duplicate title.'
                return render_to_response( 'alarm_create.html',  
                                           { 'urls': PPparser.URLS.iteritems() },
                                           RequestContext( request, { 'username': request.user.username, 'error': True, 'form': form } ))
        else:
            return render_to_response( 'alarm_create.html',  
                                       { 'urls': PPparser.URLS.iteritems() },
                                         RequestContext( request, { 'username': request.user.username, 'error': True, 'form': form } ))
    elif request.GET.has_key('url'):
        url = request.GET['url']
    else:
        form = AlarmSaveForm()

    return render_to_response('alarm_create.html', { 'urls': PPparser.URLS.iteritems() }, context_instance = variables )
    # return render_to_response( 'alarm_create.html', { 'urls': PpomppuParsor.URLS.iteritems() }, context_instance = variables )	

# alarm edit view
@login_required
def alarm_view(request, alarm_title):
    # Create Alarm from input form
    if request.method == 'POST':
        form = AlarmEditForm ( request.POST )
        if form.is_valid():
            Alarm.update(form)
            return HttpResponseRedirect ( '/alarms/' ) 
        else:
            print form.errors
    # Delete an alarm
    elif request.method == 'DELETE':
        Alarm.delete(alarm_title)
        obj = { "result": "success" }   
        return HttpResponse( json.dumps(obj) )
    # Get Request, just show the alarms           
    else:
        alarm = Alarm.objects.get(title = alarm_title)
        form = AlarmEditForm(initial= {'title': alarm.title, 
                                       'site': alarm.site,
                                       'keyword': SearchWord.search_word_to_str(alarm.searchword_set.all()) })
        
    variables = RequestContext( request, { 'username': request.user.username, 'form': form })
    return render_to_response ( 'alarm_edit.html', variables )    
    
# activate or deactivate alarm
@login_required
def alarm_activate(request):
    if request.method == 'POST':
        alarm_name = request.POST.get('alarm_name');
        on_or_off = request.POST.get('activate');
        obj = { "result": "success" }
 
        if request.user.is_authenticated():
            user = request.user
            alarm = Alarm.objects.get(title = alarm_name, user = user)
            
            if on_or_off == "ON":
                alarm.activated = True
            else:
                alarm.activated = False
                
            alarm.save()
        
            obj = { "result": "success" }
        else:
            obj = { "result": "fail" }
       
        return HttpResponse( json.dumps(obj))  
    
    
# settings view
@login_required
def settings_view(request):
    username = request.user.username
    user = get_object_or_404 ( User, username = username )
   	
    try:
        settings = Setting.objects.get( user = user )
    except ObjectDoesNotExist:
        settings = Setting.objects.create(user = user)
   	
    if request.method == 'POST':
        entry = request.POST['entry']
        if entry == "email":
            email = request.POST['email']

            # Email validation
            try:
                validate_email( email )
                user.email = email
                user.save()
                obj = { "result": "success" }
            except ValidationError:
                obj = { "result": "fail" }

            return HttpResponse( json.dumps(obj) )
        elif entry == "notification":
            method = request.POST['noti_method']
            checked = request.POST['checked']
        elif entry == "activation":
            activate = request.POST['activate']

            if activate == 'ON':
                settings.activated = 1
            else:
                settings.activated = 0
                
            settings.save()
            obj = { "result": "success" }   
            
            return HttpResponse( json.dumps(obj) )  

    variables = RequestContext( request, { 'username': username, 'email': user.email, 'setting': settings } )
    return render_to_response( 'settings.html', variables )
