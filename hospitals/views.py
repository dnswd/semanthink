from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound
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

def infographics(request):

	# Make query calls from utils.py, and extract them
	hospital_count = get_hospital_count()
	er_count = get_er_count()

	experience_label = get_patient_experiences_and_count()['experienceLabel']
	experience_count = get_patient_experiences_and_count()['experienceCount']
	
	ratings_label = get_hospital_overall_rating_and_count()['ratingsLabel']
	ratings_count = get_hospital_overall_rating_and_count()['ratingsCount']
	
	# Package Data
	context = {
		"hospitalWithNoEr" : hospital_count - er_count,
		"hospitalWithEr" : er_count,
		"experienceLabel" : experience_label,
		"experienceCount" : experience_count,
		"ratingsLabel" : ratings_label,
		"ratingsCount" : ratings_count,
	}

	# Return to render
	return render(request, 'infographics.html', context)

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


def kb(request: HttpRequest) -> HttpResponse:
    query_param = request.GET
    hospital = query_param.get('hospital', None)

    if not hospital:
        return HttpResponseNotFound("hospital query is required")

    predicate_obj = get_rs_info(hospital)

    if not len(predicate_obj):
        return HttpResponseNotFound("hospital invalid")

    ctx = {
        'd': predicate_obj[0],
        'n': 'No information'
    }

    return render(request, 'hospital_kb.html', context=ctx)

