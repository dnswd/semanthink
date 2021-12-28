from django.shortcuts import render
from django.http import HttpResponse
from pymantic import sparql

server = sparql.SPARQLServer('http://169.254.0.72:9999/blazegraph/namespace/kb/sparql')

# Loading data to Blazegraph
server.update('load <https://github.com/dnswd/semanthink/raw/main/hospital-ratings-rdf-5.ttl>')

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

def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
	
def index(request):
    result = server.query(prefixes + 
		'''
			SELECT * WHERE { ?s :rating 4 }
		'''
	)
    
    res = []
    for b in result['results']['bindings']:
        res.append(b['s']['value'])
        
    context = {
		'res': res,
	}
    
    return render(request, 'index.html', context)
