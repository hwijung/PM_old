from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
def main(request):
	variables = RequestContext( request )
	return render_to_response ( 'index.html', variables )