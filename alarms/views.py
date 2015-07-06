from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.db import IntegrityError

from alarms.forms import *
from alarms.models import *

from common.PPparser import PPparser

import json 
import logging, logging.config
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
			return render_to_response('login.html', {'error': True}, 
									context_instance = RequestContext(request))
			
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
	
	# activated or not
	try:
		setting = Setting.objects.get( user = user )
	except ObjectDoesNotExist:
		setting = Setting.objects.create(user = user)
	
	variables = RequestContext( request, { 'username': username, 'noa': len(my_alarms), 'alarms': my_alarms, 'activated': setting.activated } )
	
	return render_to_response('alarms.html', variables)

# alarm craete view
@login_required
def alarms_create_view(request):
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
				return render_to_response( 'alarm_create.html',  
										   { 'urls': PPparser.URLS.iteritems() },
										   RequestContext( request, { 'username': request.user.username, 'error': True } ))

	elif request.GET.has_key('url'):
		url = request.GET['url']
	else:
		form = AlarmSaveForm()
	
	return render_to_response('alarm_create.html', { 'urls': PPparser.URLS.iteritems() }, context_instance = variables )
	# return render_to_response( 'alarm_create.html', { 'urls': PpomppuParsor.URLS.iteritems() }, context_instance = variables )	

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
   			
   			# Update Notification
   	
   	variables = RequestContext( request, { 'username': username, 'email': user.email, 'setting': settings } )
   	return render_to_response( 'settings.html', variables ) 	
	