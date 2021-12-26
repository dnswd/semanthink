from django.shortcuts import render
from django.http import HttpResponse
from pymantic import sparql

server = sparql.SPARQLServer('http://192.168.100.5:9999/blazegraph/namespace/kb/sparql')

# Loading data to Blazegraph
server.update('load <https://github.com/dnswd/semanthink/raw/main/hospital-ratings-rdf-5.ttl>')

prefixes = '''
	PREFIX : <http://example.org/>
	PREFIX schema: <http://schema.org/>
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''

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
