from django.shortcuts import render
from django.http import HttpResponse
from .utils import *

index_context = dict()

def index(request):
	states = get_states()
	cities = get_cities()
	types = get_types()
	ownerships = get_ownerships()
	ratings = get_ratings()
	emergencies = get_emergency_services()
		
	index_context['states'] = states
	index_context['cities'] = cities
	index_context['types'] = types
	index_context['ownerships'] = ownerships
	index_context['ratings'] = ratings
	index_context['emergencies'] = emergencies
	
	return render(request, 'index.html', index_context)

def filters(request):  
	state = request.GET.get('state', '')
	city = request.GET.get('city', '')
	tipe = request.GET.get('type', '')
	ownership = request.GET.get('ownership', '')
	rating = request.GET.get('rating', '')
	emergency = request.GET.get('emergency', '')
	ehr = request.GET.get('ehr', '')
 
	return render(request, 'index.html', index_context)
