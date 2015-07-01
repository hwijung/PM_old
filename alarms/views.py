from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from alarms.forms import *
from alarms.models import *

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
	 
	entries = user.monitoringentry_set.order_by ( 'title' )
	number_of_entries = len(entries)
	settings = UserSetting.objects.get(user=user)
	
	variables = RequestContext( request, { 'username': username, 'noe': number_of_entries, 'entries': entries, 'beat': settings.beat } )
	
	return render_to_response('user_page.html', variables)
	