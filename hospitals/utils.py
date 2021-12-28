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

def query(q):
	return server.query(prefixes + q)

def results(res):
	return [r['rs']['value'] for r in res['results']['bindings']]

def get_states():
	GET_STATES = '''
				SELECT DISTINCT ?stateName
				WHERE {
					?s :state ?state .
					?state foaf:name ?stateName .
				} ORDER BY ?stateName
			'''
	states = query(GET_STATES)
	return [state['stateName']['value'] for state in states['results']['bindings']]
  
def get_cities():
	GET_CITIES = '''
				SELECT DISTINCT ?cityName
				WHERE {
					?s :city ?city .
					?city foaf:name ?cityName .
				} ORDER BY ?cityName
			'''
	cities = query(GET_CITIES)
	return [city['cityName']['value'] for city in cities['results']['bindings']]

def get_types():
	GET_TYPES = '''
				SELECT DISTINCT ?type
				WHERE {
					?rs :type ?type .
				} ORDER BY ?type
			'''
	types = query(GET_TYPES)
	return [type['type']['value'] for type in types['results']['bindings']]

def get_ownerships():
	GET_OWNERSHIPS = '''
				SELECT DISTINCT ?ownership
				WHERE {
					?rs :ownership ?ownership .
				} ORDER BY ?ownership
			'''
	ownerships = query(GET_OWNERSHIPS)
	return [ownership['ownership']['value'] for ownership in ownerships['results']['bindings']]

def get_ratings():
	GET_RATINGS = '''
				SELECT DISTINCT ?rating
				WHERE {
					?rs :rating ?rating .
				} ORDER BY DESC(?rating)
			'''
	ratings = query(GET_RATINGS)
	return [rating['rating']['value'] for rating in ratings['results']['bindings']]

def get_emergency_services():
	GET_EMERGENCIES = '''
				SELECT DISTINCT ?emergency
				WHERE {
					?rs :hasEmergencyServices ?emergency .
				} ORDER BY DESC(?emergency)
			'''
	emergency_services = query(GET_EMERGENCIES)
	return [emergency['emergency']['value'] for emergency in emergency_services['results']['bindings']]