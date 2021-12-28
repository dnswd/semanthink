from django.shortcuts import render
from django.http import HttpResponse
from .utils import *


server = sparql.SPARQLServer('http://169.254.0.72:9999/blazegraph/namespace/kb/sparql')

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

prefixes = '''
	PREFIX : <http://example.org/>
	PREFIX schema: <http://schema.org/>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''
def infographics(request):
	#TODO: data tidak auto load

	# Queries
	hospital_count_query = server.query(prefixes +
	'''
		SELECT (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
		}
	'''
	)
	er_count_query = server.query(prefixes +
	'''
		SELECT (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :hasEmergencyServices ?hasEr .
			FILTER(?hasEr="Yes"^^xsd:string)
		}
	'''
	)
	patient_experience_query = server.query(prefixes +
	'''
		SELECT ?patientRating (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :patientExperience ?patientRating .
		} GROUP BY ?patientRating
	'''
	)
	hospital_overall_rating_query = server.query(prefixes +
	'''
		SELECT ?rating (COUNT(?hospital) as ?hospitalCount)
		WHERE {
			?hospital a <http://dbpedia.org/resource/Hospital> .
			?hospital :rating ?rating .
		} GROUP BY ?rating
	'''
	)

	# Extract data from queries
	hospital_count = int(hospital_count_query['results']['bindings'][0]['hospitalCount']['value'])
	er_count = int(er_count_query['results']['bindings'][0]['hospitalCount']['value'])
	patient_experience = patient_experience_query['results']['bindings']
	ratings = hospital_overall_rating_query['results']['bindings']

	experience_label = [i['patientRating']['value'] for i in patient_experience]
	experience_count = [i['hospitalCount']['value'] for i in patient_experience]
	
	ratings_label = [i['rating']['value'] for i in ratings]
	ratings_count = [i['hospitalCount']['value'] for i in ratings]\
	
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
