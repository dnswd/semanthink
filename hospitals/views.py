from django.shortcuts import render
from django.http import HttpResponse
from pymantic import sparql

server = sparql.SPARQLServer('http://localhost:9999/blazegraph/namespace/kb/sparql')

# Loading data to Blazegraph
server.update('load <https://github.com/dnswd/semanthink/raw/main/hospital-ratings-rdf-5.ttl>')

prefixes = '''
	PREFIX : <http://example.org/>
	PREFIX schema: <http://schema.org/>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''

def index(request):
    states = server.query(prefixes + 
		'''
			SELECT DISTINCT ?stateName
			WHERE {
			?s :state ?state .
			?state foaf:name ?stateName .
			} ORDER BY ?stateName
		'''
	)
    
    cities = server.query(prefixes + 
		'''
			SELECT DISTINCT ?cityName
			WHERE {
			?s :city ?city .
			?city foaf:name ?cityName .
			} ORDER BY ?cityName
		'''
	)
    
    states = [state['stateName']['value'] for state in states['results']['bindings']]
    cities = [city['cityName']['value'] for city in cities['results']['bindings']]
        
    context = {
		'states': states,
  		'cities': cities,
	}
    
    return render(request, 'index.html', context)
