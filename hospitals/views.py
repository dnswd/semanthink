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
	rs = request.GET.get('rs', '')
	state = request.GET.get('state', '')
	city = request.GET.get('city', '')
	tipe = request.GET.get('tipe', '')
	ownership = request.GET.get('ownership', '')
	rating = request.GET.get('rating', '')
	emergency = request.GET.get('emergency', '')
	ehr = request.GET.get('ehr', '')

	if rs:
		try:
			results = get_rs(rs)
			index_context['q'] = '[Hospital Name] ' + rs
		except:
			results = None
	if state:
		results = get_rs_by_state(state)
		index_context['q'] = '[State] ' + state
	if city:
		results = get_rs_by_city(city)
		index_context['q'] = '[City] ' + city
	if tipe:
		results = get_rs_by_tipe(tipe)
		index_context['q'] = '[Type] ' + tipe
	if ownership:
		results = get_rs_by_ownership(ownership)
		index_context['q'] = '[Ownership] ' + ownership
	if rating:
		results = get_rs_by_rating(rating)
		index_context['q'] = '[Rating] ' + rating
	if emergency:
		results = get_rs_by_emergency(emergency)
		index_context['q'] = '[Emergency] ' + emergency
	if ehr:
		results = get_rs_by_ehr(ehr)
		index_context['q'] = '[EHR] ' + 'Yes'
	
	index_context['results'] = results
  
	return render(request, 'index.html', index_context)
