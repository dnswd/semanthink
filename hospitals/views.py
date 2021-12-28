from django.shortcuts import render
from django.http import HttpResponse
from .utils import *

index_context = dict()

def index(request):
	states = get_states()
	cities = get_cities()
	tipes = get_tipes()
	ownerships = get_ownerships()
	ratings = get_ratings()
	emergencies = get_emergency()
		
	index_context['states'] = states
	index_context['cities'] = cities
	index_context['tipes'] = tipes
	index_context['ownerships'] = ownerships
	index_context['ratings'] = ratings
	index_context['emergencies'] = emergencies
	
	return render(request, 'index.html', index_context)

def filters(request):  
	state = request.GET.get('state', '')
	city = request.GET.get('city', '')
	tipe = request.GET.get('tipe', '')
	ownership = request.GET.get('ownership', '')
	rating = request.GET.get('rating', '')
	emergency = request.GET.get('emergency', '')
	ehr = request.GET.get('ehr', '')
	
	filters = []
	if state:
		filters.extend(get_rs_by_state(state))
	if city:
		filters.extend(get_rs_by_city(city))
	if tipe:
		filters.extend(get_rs_by_tipe(tipe))
	if ownership:
		filters.extend(get_rs_by_ownership(ownership))
	if rating:
		filters.extend(get_rs_by_rating(rating))
	if emergency:
		filters.extend(get_rs_by_emergency(emergency))
	if ehr:
		filters.extend(get_rs_by_ehr(ehr))
	
	index_context['filters'] = filters
  
	return render(request, 'index.html', index_context)
