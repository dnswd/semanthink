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

def rs_res(res):
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

def get_tipes():
	GET_TYPES = '''
				SELECT DISTINCT ?tipe
				WHERE {
					?rs :type ?tipe .
				} ORDER BY ?tipe
			'''
	tipes = query(GET_TYPES)
	return [tipe['tipe']['value'] for tipe in tipes['results']['bindings']]

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

def get_emergency():
	GET_EMERGENCIES = '''
				SELECT DISTINCT ?emergency
				WHERE {
					?rs :hasEmergencyServices ?emergency .
				} ORDER BY DESC(?emergency)
			'''
	emergency = query(GET_EMERGENCIES)
	return [emergency['emergency']['value'] for emergency in emergency['results']['bindings']]

def get_rs_by_state(state):
	GET_STATE = '''
				SELECT ?rs
				WHERE {
					?rs :state ?state .
					?state foaf:name "%s" .
				} ORDER BY ?rs
			''' % state
	return rs_res(query(GET_STATE))

def get_rs_by_city(city):
	GET_CITY = '''
				SELECT ?rs
				WHERE {
					?rs :city ?city .
					?city foaf:name "%s" .
				} ORDER BY ?rs
			''' % city
	return rs_res(query(GET_CITY))

def get_rs_by_tipe(tipe):
	GET_TYPE = '''
				SELECT ?rs
				WHERE {
					?rs :type "%s" .
				} ORDER BY ?rs
			''' % tipe
	return rs_res(query(GET_TYPE))

def get_rs_by_ownership(ownership):
	GET_OWNERSHIP = '''
				SELECT ?rs
				WHERE {
					?rs :ownership "%s" .
				} ORDER BY ?rs
			''' % ownership
	return rs_res(query(GET_OWNERSHIP))

def get_rs_by_rating(rating):
	GET_RATING = '''
				SELECT ?rs
				WHERE {
					?rs :rating "%s" .
				} ORDER BY ?rs
			''' % rating
	return rs_res(query(GET_RATING))

def get_rs_by_emergency(emergency):
	GET_EMERGENCY = '''
				SELECT ?rs
				WHERE {
					?rs :hasEmergencyServices "%s" .
				} ORDER BY ?rs
			''' % emergency
	return rs_res(query(GET_EMERGENCY))

def get_rs_by_ehr(ehr):
	GET_EHR = '''
				SELECT ?rs
				WHERE {
					?rs :meetsMeaningfulUseOfEHRs "Y" .
				} ORDER BY ?rs
			'''
	return rs_res(query(GET_EHR))
