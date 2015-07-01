"""PM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import os.path

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from alarms.views import *

static = os.path.join (
    os.path.dirname( __file__ ), 'static' )

urlpatterns = [ 
	# Administration
    url(r'^admin/', include(admin.site.urls)),

    # Alarm Management 
    url(r'^$', home),

    # Session Management
    url(r'^login/$', login_view),
    url(r'^logout/$', logout_view),
    url(r'^signup/$', signup_view),
    url(r'^signup/success/$', TemplateView.as_view(
            template_name='signup_success.html'),
              name="home" ), 
    
    # Settings 

    # Media/Static
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': static }),

]
